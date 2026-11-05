from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# === VIDEO SCHEMAS ===
class VideoBase(BaseModel):
    title: str

class VideoFromUrlRequest(BaseModel):
    url: str
    title: Optional[str] = None
    model_name: Optional[str] = "base"

class VideoResponse(VideoBase):
    id: int
    filename: str
    filepath: str
    duration: float
    created_at: datetime

    class Config:
        from_attributes = True


# === WORD & SEGMENT SCHEMAS ===
class WordDetail(BaseModel):
    word: str
    display_word: str
    start_time: float
    end_time: float

class SegmentResponse(BaseModel):
    id: int
    video_id: int
    text: str
    start_time: float
    end_time: float
    words: Optional[List[WordDetail]] = []

    class Config:
        from_attributes = True


# === SEARCH RESULT SCHEMAS ===
class SearchResultItem(BaseModel):
    segment_id: int
    video_id: int
    video_title: str
    video_filename: str
    context_sentence: str
    matched_word: str
    word_start_time: float
    word_end_time: float
    sentence_start_time: float
    sentence_end_time: float


# === FLASHCARD SCHEMAS ===
class FlashcardCreate(BaseModel):
    word: str
    meaning: str
    context_sentence: str
    video_id: int
    start_time: float
    end_time: float

class FlashcardUpdate(BaseModel):
    meaning: Optional[str] = None
    status: Optional[str] = None

class FlashcardResponse(BaseModel):
    id: int
    word: str
    meaning: str
    context_sentence: str
    video_id: int
    video_title: Optional[str] = None
    video_filename: Optional[str] = None
    start_time: float
    end_time: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

