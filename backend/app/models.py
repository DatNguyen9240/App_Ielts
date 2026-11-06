from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=True, default="1. Work & Study (Công việc và Học tập)")
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    duration = Column(Float, default=0.0)
    description = Column(Text, nullable=True)  # Nội dung mô tả video từ YouTube hoặc người dùng nhập
    source_url = Column(String(500), nullable=True)  # Link gốc video (nếu có)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Quan hệ với các bảng khác
    segments = relationship("TranscriptSegment", back_populates="video", cascade="all, delete-orphan")
    words = relationship("TranscriptWord", back_populates="video", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="video", cascade="all, delete-orphan")


class TranscriptSegment(Base):
    """Bảng lưu trữ từng câu / đoạn hội thoại trong video"""
    __tablename__ = "transcript_segments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)  # Nội dung câu hoàn chỉnh
    start_time = Column(Float, nullable=False)  # Thời gian bắt đầu (giây)
    end_time = Column(Float, nullable=False)    # Thời gian kết thúc (giây)
    words_json = Column(Text, nullable=True)    # Dữ liệu JSON chi tiết từng từ kèm timestamp

    video = relationship("Video", back_populates="segments")
    words = relationship("TranscriptWord", back_populates="segment", cascade="all, delete-orphan")


class TranscriptWord(Base):
    """Bảng lập chỉ mục (index) chi tiết đến từng từ để tra cứu siêu tốc"""
    __tablename__ = "transcript_words"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False, index=True)
    segment_id = Column(Integer, ForeignKey("transcript_segments.id", ondelete="CASCADE"), nullable=False, index=True)
    word = Column(String(100), nullable=False, index=True)       # Từ vựng đã chuẩn hóa (chữ thường, bỏ dấu câu)
    display_word = Column(String(100), nullable=False)           # Từ nguyên bản để hiển thị
    start_time = Column(Float, nullable=False)                   # Mốc bắt đầu phát âm từ (giây)
    end_time = Column(Float, nullable=False)                     # Mốc kết thúc phát âm từ (giây)

    video = relationship("Video", back_populates="words")
    segment = relationship("TranscriptSegment", back_populates="words")

# Index tổng hợp giúp tìm kiếm từ theo video cực nhanh
Index("idx_word_search", TranscriptWord.word, TranscriptWord.video_id)


class Flashcard(Base):
    """Bảng lưu trữ Flashcard học từ vựng kèm ngữ cảnh video"""
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, index=True)
    meaning = Column(Text, nullable=False)                        # Định nghĩa / nghĩa tiếng Việt
    context_sentence = Column(Text, nullable=False)               # Câu trích dẫn ngữ cảnh từ video
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(Float, nullable=False)                    # Mốc thời gian để tua video đúng đoạn này
    end_time = Column(Float, nullable=False)
    status = Column(String(50), default="learning")               # Trạng thái: learning, mastered
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="flashcards")


class TopicVocabulary(Base):
    """Bảng lưu trữ từ vựng chuẩn & từ vựng AI sinh theo 16 chủ đề IELTS"""
    __tablename__ = "topic_vocabularies"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, index=True, nullable=False)
    word = Column(String(150), index=True, nullable=False)
    phonetic = Column(String(100), nullable=True)
    part_of_speech = Column(String(50), nullable=True)
    meaning = Column(Text, nullable=False)
    context_sentence = Column(Text, nullable=False)
    speaking_question = Column(Text, nullable=True)
    collocations_json = Column(Text, nullable=True)  # Chuỗi JSON danh sách collocations
    source = Column(String(50), default="curated")   # "curated" hoặc "ai"
    created_at = Column(DateTime, default=datetime.utcnow)


