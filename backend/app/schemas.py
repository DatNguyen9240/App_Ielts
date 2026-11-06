from datetime import datetime
from typing import List, Optional, Any, Union
from pydantic import BaseModel

# === VIDEO SCHEMAS ===
class VideoBase(BaseModel):
    title: str
    topic: Optional[str] = "1. Work & Study (Công việc và Học tập)"

class VideoFromUrlRequest(BaseModel):
    url: str
    title: Optional[str] = None
    topic: Optional[str] = None
    model_name: Optional[str] = "base"

class VideoResponse(VideoBase):
    id: int
    filename: str
    filepath: str
    duration: float
    created_at: datetime
    topic: Optional[str] = "1. Work & Study (Công việc và Học tập)"
    description: Optional[str] = None
    source_url: Optional[str] = None

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


# === DESCRIPTION VOCABULARY SCHEMAS ===
class ScanDescriptionRequest(BaseModel):
    description_text: Optional[str] = None
    source_url: Optional[str] = None

class OnlineYoutubeScanRequest(BaseModel):
    youtube_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    custom_description: Optional[str] = None

class DescriptionMatchedVocabItem(BaseModel):
    word: str
    raw_entry: Optional[str] = None
    definition_in_desc: Optional[str] = None
    vietnamese_meaning: str
    vietnamese_suggestions: List[str] = []
    context_sentence: str
    sentence_start_time: float
    sentence_end_time: float
    word_start_time: float
    word_end_time: float
    occurrences_count: int = 1

class ScanDescriptionResponse(BaseModel):
    video_id: Union[int, str]
    video_title: str
    description: str
    total_found: int
    matched_vocab: List[DescriptionMatchedVocabItem]


# === YOUTUBE ONLINE SEARCH & IMPORT SCHEMAS ===
class YoutubeWordSearchRequest(BaseModel):
    youtube_id: str
    query: str

class YoutubeOnlineImportRequest(BaseModel):
    url_or_id: str
    title: Optional[str] = None
    topic: Optional[str] = None

# === TOPIC VOCABULARY SCHEMAS ===
class TopicVocabSaveRequest(BaseModel):
    word: str
    meaning: str
    context_sentence: str
    topic_id: Optional[int] = None

class SetApiKeyRequest(BaseModel):
    api_key: str

class GenerateAiVocabRequest(BaseModel):
    topic_id: int
    api_key: Optional[str] = None

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

