import os
import shutil
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from . import models, schemas, crud, whisper_service, downloader, translation_service, topics, curated_videos, description_service

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("main_app")

# Khởi tạo bảng trong cơ sở dữ liệu SQLite
Base.metadata.create_all(bind=engine)

# Khởi tạo FastAPI App
app = FastAPI(
    title="Smart Video Vocabulary & Flashcard API",
    description="Backend API phục vụ tra cứu từ vựng video qua Whisper và quản lý Flashcard tương tác",
    version="1.0.0"
)

# Cấu hình CORS để frontend có thể gọi API mà không bị chặn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thiết lập thư mục lưu trữ file
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BACKEND_DIR, "uploads")
FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_DIR), "frontend")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

# Mount thư mục upload làm static files (FastAPI StaticFiles hỗ trợ sẵn HTTP 206 Partial Content để tua video)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# ==================== TOPICS ENDPOINT ====================

@app.get("/api/topics")
def get_all_topics():
    """Lấy danh sách 16 chủ đề IELTS chuẩn có đánh số để hiển thị tabs"""
    return topics.IELTS_TOPICS


@app.get("/api/topics/{topic_id}/videos")
def get_videos_for_topic(topic_id: int):
    """
    Tìm kiếm và gợi ý danh sách video IELTS thực tế theo chủ đề để người dùng tự do xem và học.
    Gồm các video chọn lọc sẵn + tìm kiếm YouTube.
    """
    topic_item = next((t for t in topics.IELTS_TOPICS if t["id"] == topic_id), None)
    if not topic_item:
        raise HTTPException(status_code=404, detail="Không tìm thấy chủ đề này")

    # 1. Tìm kiếm video thực tế trực tiếp từ YouTube
    online_videos = curated_videos.search_topic_videos_online(topic_item["short_title"], max_results=4)

    # 2. Video chọn lọc sẵn (đảm bảo luôn có bài học chất lượng cao ngay cả khi offline)
    default_videos = curated_videos.TOPIC_DEFAULT_VIDEOS.get(topic_id, [])

    seen_ids = set()
    combined = []
    # Ưu tiên kết quả online mới nhất, kết hợp danh sách tuyển chọn không trùng lặp
    for v in (online_videos or []) + (default_videos or []):
        if v.get("id") and v["id"] not in seen_ids:
            seen_ids.add(v["id"])
            combined.append(v)

    return {
        "topic_id": topic_id,
        "topic_title": topic_item["title"],
        "videos": combined
    }


# ==================== VIDEO ENDPOINTS ====================

@app.post("/api/videos/upload", response_model=schemas.VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    topic: Optional[str] = Form(None),
    model_name: Optional[str] = Form("base"),
    db: Session = Depends(get_db)
):
    """
    Tải lên video .mp4, chạy OpenAI Whisper để lấy Word-level Timestamps và lưu vào SQLite kèm chủ đề.
    """
    if not file.filename.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ các định dạng video (.mp4, .mov, .mkv, .webm)")

    video_title = title if title and title.strip() else file.filename
    # Tạo tên file an toàn
    safe_filename = f"{os.urandom(6).hex()}_{file.filename.replace(' ', '_')}"
    saved_filepath = os.path.join(UPLOAD_DIR, safe_filename)

    # 1. Lưu file video vào đĩa cứng
    logger.info(f"Đang lưu file video: {saved_filepath}...")
    with open(saved_filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Tối ưu hóa FastStart (đưa moov atom lên đầu để web phát ngay không bị delay)
    saved_filepath = downloader.apply_faststart(saved_filepath)

    # 2. Xử lý Whisper trích xuất văn bản & Word-level timestamps
    try:
        logger.info(f"Đang xử lý Whisper cho file {safe_filename}...")
        whisper_data = whisper_service.transcribe_video_with_word_timestamps(
            saved_filepath, 
            model_name=model_name
        )
    except Exception as e:
        logger.error(f"Lỗi khi transcribe Whisper: {str(e)}")
        # Xóa file nếu lỗi xử lý
        if os.path.exists(saved_filepath):
            os.remove(saved_filepath)
        raise HTTPException(status_code=500, detail=f"Không thể xử lý Whisper: {str(e)}")

    # Xác định chủ đề (người dùng chọn hoặc tự động nhận diện theo từ khóa)
    assigned_topic = topic.strip() if topic and topic.strip() else topics.auto_detect_topic(video_title)

    # 3. Lưu dữ liệu đã xử lý vào Database
    video_record = crud.create_video_with_transcripts(
        db=db,
        title=video_title,
        filename=safe_filename,
        filepath=f"/uploads/{safe_filename}",
        duration=whisper_data["duration"],
        segments_data=whisper_data["segments"],
        topic=assigned_topic
    )

    logger.info(f"Video {video_record.id} đã được lưu thành công với chủ đề '{assigned_topic}'.")
    return video_record


@app.post("/api/videos/from-url", response_model=schemas.VideoResponse)
async def process_video_from_url(
    req: schemas.VideoFromUrlRequest,
    db: Session = Depends(get_db)
):
    """
    Tự động tải video từ đường link (YouTube, TikTok, Facebook, MP4 trực tiếp...) và trích xuất Whisper.
    """
    url = req.url.strip()
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL không hợp lệ. Vui lòng nhập link bắt đầu bằng http:// hoặc https://")

    # 1. Tải video qua yt-dlp (Kèm kiểm duyệt an ninh đa tầng)
    try:
        logger.info(f"Đang tải video từ đường link: {url}...")
        downloaded_filepath, detected_title, _, detected_desc = downloader.download_video_from_url(
            url=url, 
            output_dir=UPLOAD_DIR
        )
    except ValueError as ve:
        # Lỗi phát hiện link độc hại, vi phạm an ninh SSRF hoặc file giả mạo
        logger.warning(f"Từ chối link vi phạm an ninh: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Lỗi khi tải video từ URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Không thể tải video từ link này: {str(e)}")

    video_title = req.title.strip() if req.title and req.title.strip() else detected_title
    filename = os.path.basename(downloaded_filepath)

    # 2. Xử lý Whisper trích xuất từ vựng & timestamps
    try:
        logger.info(f"Đang xử lý Whisper cho video vừa tải: {filename}...")
        whisper_data = whisper_service.transcribe_video_with_word_timestamps(
            downloaded_filepath,
            model_name=req.model_name or "base"
        )
    except Exception as e:
        logger.error(f"Lỗi khi xử lý Whisper: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Không thể xử lý Whisper: {str(e)}")

    # Xác định chủ đề (người dùng chọn hoặc tự động nhận diện theo từ khóa)
    assigned_topic = req.topic.strip() if req.topic and req.topic.strip() else topics.auto_detect_topic(video_title)

    # 3. Lưu vào Database
    video_record = crud.create_video_with_transcripts(
        db=db,
        title=video_title,
        filename=filename,
        filepath=f"/uploads/{filename}",
        duration=whisper_data["duration"],
        segments_data=whisper_data["segments"],
        topic=assigned_topic,
        description=detected_desc,
        source_url=url
    )

    logger.info(f"Video từ URL đã xử lý hoàn tất (ID: {video_record.id}, Tiêu đề: {video_title}, Chủ đề: {assigned_topic})")
    return video_record



@app.get("/api/videos", response_model=List[schemas.VideoResponse])
def get_all_videos(
    topic: Optional[str] = Query(None, description="Lọc theo chủ đề cụ thể"),
    db: Session = Depends(get_db)
):
    """Lấy danh sách các video đã tải lên (có thể lọc theo chủ đề)"""
    return crud.get_videos(db, topic=topic)


@app.get("/api/videos/{video_id}")
def get_video_detail(video_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết video kèm danh sách các câu phụ đề và mô tả"""
    video = crud.get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Không tìm thấy video")
    
    segments = [
        {
            "id": s.id,
            "text": s.text,
            "start_time": s.start_time,
            "end_time": s.end_time
        }
        for s in video.segments
    ]
    return {
        "id": video.id,
        "title": video.title,
        "topic": video.topic or "1. Work & Study (Công việc và Học tập)",
        "filename": video.filename,
        "filepath": video.filepath,
        "duration": video.duration,
        "description": video.description or "",
        "source_url": video.source_url or "",
        "created_at": video.created_at,
        "segments": segments
    }


# ==================== DESCRIPTION VOCABULARY SCANNING ====================

@app.get("/api/videos/{video_id}/description")
def get_video_description(video_id: int, db: Session = Depends(get_db)):
    """Lấy nội dung mô tả (description) của video, nếu rỗng thì thử lấy từ YouTube nếu có source_url"""
    video = crud.get_video_by_id(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Không tìm thấy video")
    
    desc = video.description or ""
    if not desc and video.source_url:
        desc = downloader.fetch_video_description_from_url(video.source_url)
        if desc:
            crud.update_video_description(db, video_id, desc)

    return {
        "video_id": video.id,
        "title": video.title,
        "description": desc,
        "source_url": video.source_url or ""
    }


@app.post("/api/videos/{video_id}/description/scan", response_model=schemas.ScanDescriptionResponse)
def scan_video_description_vocab(
    video_id: int,
    req: Optional[schemas.ScanDescriptionRequest] = None,
    db: Session = Depends(get_db)
):
    """
    Trích xuất từ vựng trong Description và dò tìm câu nói thực tế trong video sử dụng từ vựng đó.
    Trả về danh sách câu phát âm, mốc thời gian tua và gợi ý nghĩa tiếng Việt.
    """
    try:
        custom_desc = req.description_text if req else None
        source_url = req.source_url if req else None
        
        # Nếu có source_url truyền vào mà video chưa có, cập nhật source_url
        if source_url:
            video = crud.get_video_by_id(db, video_id)
            if video and not video.source_url:
                video.source_url = source_url
                db.commit()

        result = description_service.match_description_vocab_with_video(
            db=db,
            video_id=video_id,
            description_text=custom_desc
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Lỗi khi quét từ vựng description: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể quét từ vựng description: {str(e)}")


@app.post("/api/youtube/scan-description", response_model=schemas.ScanDescriptionResponse)
def scan_online_youtube_description_vocab(req: schemas.OnlineYoutubeScanRequest):
    """
    Trích xuất từ vựng từ Description của video YouTube trên các Tab chủ đề IELTS
    và dò tìm câu nói thực tế trong video qua phụ đề YouTube mà không cần tải video về máy.
    """
    try:
        res = description_service.scan_youtube_online_vocab(
            youtube_id=req.youtube_id,
            url=req.url,
            title=req.title,
            custom_description=req.custom_description
        )
        return res
    except Exception as e:
        logger.error(f"Lỗi khi quét từ vựng YouTube online: {e}")
        raise HTTPException(status_code=500, detail=f"Không thể quét từ vựng video YouTube: {str(e)}")


# ==================== VOCABULARY SEARCH ENDPOINTS ====================

@app.get("/api/search", response_model=List[schemas.SearchResultItem])
def search_words(
    q: str = Query(..., description="Từ vựng cần tìm kiếm"),
    video_id: Optional[int] = Query(None, description="Lọc theo ID video cụ thể (nếu có)"),
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm từ vựng trong video:
    Trả về danh sách câu chứa từ vựng, mốc thời gian bắt đầu câu và mốc thời gian chính xác của từ.
    """
    return crud.search_vocabulary(db, query_str=q, video_id=video_id)


# ==================== DICTIONARY & MEANING SUGGESTIONS ====================

@app.get("/api/dictionary/lookup")
def lookup_dictionary(
    word: str = Query(..., description="Từ tiếng Anh cần tra nghĩa"),
    context: Optional[str] = Query(None, description="Câu ngữ cảnh trong video")
):
    """
    Tự động tra cứu và gợi ý nghĩa tiếng Việt cho từ vựng và câu ngữ cảnh.
    """
    return translation_service.lookup_word_vietnamese(word=word, context_sentence=context)


# ==================== FLASHCARD ENDPOINTS ====================

@app.post("/api/flashcards", response_model=schemas.FlashcardResponse)
def create_flashcard(card: schemas.FlashcardCreate, db: Session = Depends(get_db)):
    """Thêm một từ vựng vào bộ thẻ Flashcard kèm theo mốc video"""
    new_card = crud.create_flashcard(db, card)
    video = crud.get_video_by_id(db, new_card.video_id)
    return schemas.FlashcardResponse(
        id=new_card.id,
        word=new_card.word,
        meaning=new_card.meaning,
        context_sentence=new_card.context_sentence,
        video_id=new_card.video_id,
        video_title=video.title if video else "Unknown Video",
        video_filename=video.filename if video else "",
        start_time=new_card.start_time,
        end_time=new_card.end_time,
        status=new_card.status,
        created_at=new_card.created_at
    )


@app.get("/api/flashcards", response_model=List[schemas.FlashcardResponse])
def get_all_flashcards(db: Session = Depends(get_db)):
    """Lấy toàn bộ Flashcards hiện có để ôn tập"""
    return crud.get_flashcards(db)


@app.patch("/api/flashcards/{card_id}")
def update_flashcard(card_id: int, update_data: schemas.FlashcardUpdate, db: Session = Depends(get_db)):
    """Cập nhật nghĩa hoặc trạng thái của thẻ Flashcard"""
    updated = crud.update_flashcard(db, card_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy Flashcard")
    return {"message": "Cập nhật thành công", "card_id": card_id}


@app.delete("/api/flashcards/{card_id}")
def delete_flashcard(card_id: int, db: Session = Depends(get_db)):
    """Xóa một thẻ Flashcard"""
    success = crud.delete_flashcard(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy Flashcard")
    return {"message": "Đã xóa Flashcard thành công"}


# Mount thư mục frontend làm static files cho giao diện web
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

