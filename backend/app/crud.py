import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from . import models, schemas

# ==================== VIDEO & TRANSCRIPT CRUD ====================

def create_video_with_transcripts(
    db: Session, 
    title: str, 
    filename: str, 
    filepath: str, 
    duration: float, 
    segments_data: List[dict],
    topic: Optional[str] = None,
    description: Optional[str] = None,
    source_url: Optional[str] = None
) -> models.Video:
    """Lưu video cùng toàn bộ câu (segments) và mốc từ vựng (words) vào SQLite theo quan hệ quan hệ 1-N"""
    # 1. Tạo bản ghi Video
    db_video = models.Video(
        title=title,
        topic=topic or "1. Work & Study (Công việc và Học tập)",
        filename=filename,
        filepath=filepath,
        duration=duration,
        description=description,
        source_url=source_url
    )
    db.add(db_video)
    db.flush()  # Sinh id cho db_video

    # 2. Tạo bản ghi các câu và từ vựng tương ứng
    for seg in segments_data:
        db_seg = models.TranscriptSegment(
            video_id=db_video.id,
            text=seg["text"],
            start_time=seg["start_time"],
            end_time=seg["end_time"],
            words_json=seg.get("words_json", "[]")
        )
        db.add(db_seg)
        db.flush()  # Sinh id cho db_seg

        # Lưu danh sách từ vựng chi tiết
        for w in seg.get("words", []):
            db_word = models.TranscriptWord(
                video_id=db_video.id,
                segment_id=db_seg.id,
                word=w["word"],
                display_word=w["display_word"],
                start_time=w["start_time"],
                end_time=w["end_time"]
            )
            db.add(db_word)

    db.commit()
    db.refresh(db_video)
    return db_video


def get_videos(db: Session, topic: Optional[str] = None) -> List[models.Video]:
    """Lấy danh sách video, có thể lọc theo chủ đề (topic)"""
    query = db.query(models.Video)
    if topic and isinstance(topic, str) and topic.strip() and topic.lower() != "all":
        query = query.filter(models.Video.topic == topic.strip())
    return query.order_by(desc(models.Video.created_at)).all()


def get_video_by_id(db: Session, video_id: int) -> Optional[models.Video]:
    """Lấy thông tin chi tiết một video"""
    return db.query(models.Video).filter(models.Video.id == video_id).first()


def update_video_description(db: Session, video_id: int, description: str, source_url: Optional[str] = None) -> Optional[models.Video]:
    """Cập nhật nội dung mô tả cho video"""
    video = get_video_by_id(db, video_id)
    if not video:
        return None
    video.description = description
    if source_url:
        video.source_url = source_url
    db.commit()
    db.refresh(video)
    return video


# ==================== VOCABULARY SEARCH ====================

def search_vocabulary(db: Session, query_str: str, video_id: Optional[int] = None) -> List[schemas.SearchResultItem]:
    """
    Tìm kiếm từ vựng trong video:
    - Tìm kiếm cả trong danh sách từ vựng chi tiết (TranscriptWord) và câu ngữ cảnh (TranscriptSegment).
    - Trả về câu chứa từ, mốc thời gian của câu và mốc thời gian chính xác của từ cần tìm.
    """
    clean_query = query_str.strip().lower()
    if not clean_query:
        return []

    # Truy vấn bảng TranscriptWord kết hợp Segment và Video
    query = (
        db.query(
            models.TranscriptWord,
            models.TranscriptSegment,
            models.Video
        )
        .join(models.TranscriptSegment, models.TranscriptWord.segment_id == models.TranscriptSegment.id)
        .join(models.Video, models.TranscriptWord.video_id == models.Video.id)
        .filter(models.TranscriptWord.word.like(f"%{clean_query}%"))
    )

    if video_id:
        query = query.filter(models.TranscriptWord.video_id == video_id)

    results = query.order_by(models.TranscriptWord.start_time.asc()).limit(50).all()

    items: List[schemas.SearchResultItem] = []
    seen_matches = set() # Tránh trùng lặp mốc thời gian quá gần nhau

    for word_obj, seg_obj, vid_obj in results:
        dedup_key = (seg_obj.id, round(word_obj.start_time, 1))
        if dedup_key in seen_matches:
            continue
        seen_matches.add(dedup_key)

        items.append(
            schemas.SearchResultItem(
                segment_id=seg_obj.id,
                video_id=vid_obj.id,
                video_title=vid_obj.title,
                video_filename=vid_obj.filename,
                context_sentence=seg_obj.text,
                matched_word=word_obj.display_word,
                word_start_time=word_obj.start_time,
                word_end_time=word_obj.end_time,
                sentence_start_time=seg_obj.start_time,
                sentence_end_time=seg_obj.end_time
            )
        )

    # Nếu tìm kiếm theo từ đơn lẻ không thấy, tìm kiếm chuỗi trong toàn bộ câu Segment
    if not items:
        seg_query = (
            db.query(models.TranscriptSegment, models.Video)
            .join(models.Video, models.TranscriptSegment.video_id == models.Video.id)
            .filter(models.TranscriptSegment.text.ilike(f"%{clean_query}%"))
        )
        if video_id:
            seg_query = seg_query.filter(models.TranscriptSegment.video_id == video_id)
        
        seg_results = seg_query.limit(30).all()
        for seg_obj, vid_obj in seg_results:
            items.append(
                schemas.SearchResultItem(
                    segment_id=seg_obj.id,
                    video_id=vid_obj.id,
                    video_title=vid_obj.title,
                    video_filename=vid_obj.filename,
                    context_sentence=seg_obj.text,
                    matched_word=query_str,
                    word_start_time=seg_obj.start_time,
                    word_end_time=seg_obj.end_time,
                    sentence_start_time=seg_obj.start_time,
                    sentence_end_time=seg_obj.end_time
                )
            )

    return items


# ==================== FLASHCARD CRUD ====================

def create_flashcard(db: Session, flashcard_in: schemas.FlashcardCreate) -> models.Flashcard:
    """Thêm một từ vựng mới vào danh sách Flashcard kèm ngữ cảnh video"""
    db_flashcard = models.Flashcard(
        word=flashcard_in.word.strip(),
        meaning=flashcard_in.meaning.strip(),
        context_sentence=flashcard_in.context_sentence.strip(),
        video_id=flashcard_in.video_id,
        start_time=flashcard_in.start_time,
        end_time=flashcard_in.end_time,
        status="learning"
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard


def get_flashcards(db: Session) -> List[schemas.FlashcardResponse]:
    """Lấy danh sách tất cả Flashcard kèm thông tin video để phục vụ ôn tập"""
    results = (
        db.query(models.Flashcard, models.Video)
        .join(models.Video, models.Flashcard.video_id == models.Video.id)
        .order_by(desc(models.Flashcard.created_at))
        .all()
    )
    
    flashcard_list = []
    for fc, vid in results:
        flashcard_list.append(
            schemas.FlashcardResponse(
                id=fc.id,
                word=fc.word,
                meaning=fc.meaning,
                context_sentence=fc.context_sentence,
                video_id=fc.video_id,
                video_title=vid.title,
                video_filename=vid.filename,
                start_time=fc.start_time,
                end_time=fc.end_time,
                status=fc.status,
                created_at=fc.created_at
            )
        )
    return flashcard_list


def update_flashcard(db: Session, flashcard_id: int, update_data: schemas.FlashcardUpdate) -> Optional[models.Flashcard]:
    """Cập nhật định nghĩa hoặc trạng thái (learning / mastered) của Flashcard"""
    fc = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if not fc:
        return None
    if update_data.meaning is not None:
        fc.meaning = update_data.meaning.strip()
    if update_data.status is not None:
        fc.status = update_data.status
    db.commit()
    db.refresh(fc)
    return fc


def delete_flashcard(db: Session, flashcard_id: int) -> bool:
    """Xóa một thẻ Flashcard"""
    fc = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if not fc:
        return False
    db.delete(fc)
    db.commit()
    return True

