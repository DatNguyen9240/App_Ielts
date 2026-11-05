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
from . import models, schemas, crud, whisper_service, downloader, translation_service

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


# ==================== VIDEO ENDPOINTS ====================

@app.post("/api/videos/upload", response_model=schemas.VideoResponse)
async def upload_video(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    model_name: Optional[str] = Form("base"),
    db: Session = Depends(get_db)
):
    """
    Tải lên video .mp4, chạy OpenAI Whisper để lấy Word-level Timestamps và lưu vào SQLite.
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

    # 3. Lưu dữ liệu đã xử lý vào Database
    video_record = crud.create_video_with_transcripts(
        db=db,
        title=video_title,
        filename=safe_filename,
        filepath=f"/uploads/{safe_filename}",
        duration=whisper_data["duration"],
        segments_data=whisper_data["segments"]
    )

    logger.info(f"Video {video_record.id} đã được lưu thành công với {len(whisper_data['segments'])} câu.")
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
        downloaded_filepath, detected_title, _ = downloader.download_video_from_url(
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

    # 3. Lưu vào Database
    video_record = crud.create_video_with_transcripts(
        db=db,
        title=video_title,
        filename=filename,
        filepath=f"/uploads/{filename}",
        duration=whisper_data["duration"],
        segments_data=whisper_data["segments"]
    )

    logger.info(f"Video từ URL đã xử lý hoàn tất (ID: {video_record.id}, Tiêu đề: {video_title})")
    return video_record



@app.get("/api/videos", response_model=List[schemas.VideoResponse])
def get_all_videos(db: Session = Depends(get_db)):
    """Lấy danh sách các video đã tải lên"""
    return crud.get_videos(db)


@app.get("/api/videos/{video_id}")
def get_video_detail(video_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết video kèm danh sách các câu phụ đề"""
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
        "filename": video.filename,
        "filepath": video.filepath,
        "duration": video.duration,
        "created_at": video.created_at,
        "segments": segments
    }


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

