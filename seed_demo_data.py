"""
Tệp khởi tạo dữ liệu mẫu (Mock Demo Data)
Giúp người dùng có thể trải nghiệm ngay giao diện tìm kiếm và Flashcard 
ngay cả khi chưa tải lên video lớn hoặc chưa cài xong Whisper.
"""
import os
import sys

# Thêm thư mục backend vào sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from app.database import engine, Base, SessionLocal
from app import models

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Kiểm tra nếu đã có dữ liệu
    if db.query(models.Video).first():
        print("Cơ sở dữ liệu đã có dữ liệu, bỏ qua bước khởi tạo mẫu.")
        db.close()
        return

    print("Đang nạp dữ liệu mẫu cho ứng dụng...")

    # 1. Tạo Video mẫu
    sample_video = models.Video(
        title="IELTS Speaking Sample - Environmental Challenges",
        filename="sample_ielts.mp4",
        filepath="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4", # Video demo công khai
        duration=180.0
    )
    db.add(sample_video)
    db.flush()

    # 2. Tạo các đoạn câu (Segments) & Từ vựng (Words with timestamps)
    sample_transcripts = [
        {
            "text": "Climate change poses an unprecedented threat to biodiversity across the globe.",
            "start": 5.2,
            "end": 10.8,
            "words": [
                {"word": "climate", "display": "Climate", "start": 5.2, "end": 5.8},
                {"word": "change", "display": "change", "start": 5.9, "end": 6.3},
                {"word": "poses", "display": "poses", "start": 6.4, "end": 6.8},
                {"word": "an", "display": "an", "start": 6.9, "end": 7.0},
                {"word": "unprecedented", "display": "unprecedented", "start": 7.1, "end": 8.0},
                {"word": "threat", "display": "threat", "start": 8.1, "end": 8.6},
                {"word": "to", "display": "to", "start": 8.7, "end": 8.8},
                {"word": "biodiversity", "display": "biodiversity", "start": 8.9, "end": 9.8},
                {"word": "across", "display": "across", "start": 9.9, "end": 10.2},
                {"word": "the", "display": "the", "start": 10.3, "end": 10.4},
                {"word": "globe", "display": "globe", "start": 10.5, "end": 10.8},
            ]
        },
        {
            "text": "Governments must implement sustainable policies to curb harmful carbon emissions.",
            "start": 14.5,
            "end": 21.0,
            "words": [
                {"word": "governments", "display": "Governments", "start": 14.5, "end": 15.2},
                {"word": "must", "display": "must", "start": 15.3, "end": 15.6},
                {"word": "implement", "display": "implement", "start": 15.7, "end": 16.3},
                {"word": "sustainable", "display": "sustainable", "start": 16.4, "end": 17.2},
                {"word": "policies", "display": "policies", "start": 17.3, "end": 17.9},
                {"word": "to", "display": "to", "start": 18.0, "end": 18.2},
                {"word": "curb", "display": "curb", "start": 18.3, "end": 18.8},
                {"word": "harmful", "display": "harmful", "start": 18.9, "end": 19.4},
                {"word": "carbon", "display": "carbon", "start": 19.5, "end": 20.1},
                {"word": "emissions", "display": "emissions", "start": 20.2, "end": 21.0},
            ]
        },
        {
            "text": "Individual actions, though seemingly trivial, collectively yield substantial impact.",
            "start": 25.0,
            "end": 31.5,
            "words": [
                {"word": "individual", "display": "Individual", "start": 25.0, "end": 25.7},
                {"word": "actions", "display": "actions", "start": 25.8, "end": 26.3},
                {"word": "though", "display": "though", "start": 26.4, "end": 26.7},
                {"word": "seemingly", "display": "seemingly", "start": 26.8, "end": 27.4},
                {"word": "trivial", "display": "trivial", "start": 27.5, "end": 28.1},
                {"word": "collectively", "display": "collectively", "start": 28.2, "end": 29.1},
                {"word": "yield", "display": "yield", "start": 29.2, "end": 29.6},
                {"word": "substantial", "display": "substantial", "start": 29.7, "end": 30.6},
                {"word": "impact", "display": "impact", "start": 30.7, "end": 31.5},
            ]
        }
    ]

    import json
    for item in sample_transcripts:
        seg = models.TranscriptSegment(
            video_id=sample_video.id,
            text=item["text"],
            start_time=item["start"],
            end_time=item["end"],
            words_json=json.dumps(item["words"])
        )
        db.add(seg)
        db.flush()

        for w in item["words"]:
            db_w = models.TranscriptWord(
                video_id=sample_video.id,
                segment_id=seg.id,
                word=w["word"],
                display_word=w["display"],
                start_time=w["start"],
                end_time=w["end"]
            )
            db.add(db_w)

    # 3. Tạo một số Flashcards mẫu
    sample_cards = [
        models.Flashcard(
            word="unprecedented",
            meaning="Chưa từng có tiền lệ, chưa từng xảy ra trong quá khứ",
            context_sentence="Climate change poses an unprecedented threat to biodiversity across the globe.",
            video_id=sample_video.id,
            start_time=7.1,
            end_time=8.0,
            status="learning"
        ),
        models.Flashcard(
            word="sustainable",
            meaning="Bền vững, có thể duy trì lâu dài mà không gây hại môi trường",
            context_sentence="Governments must implement sustainable policies to curb harmful carbon emissions.",
            video_id=sample_video.id,
            start_time=16.4,
            end_time=17.2,
            status="mastered"
        ),
        models.Flashcard(
            word="substantial",
            meaning="Đáng kể, quan trọng, có giá trị hoặc kích thước lớn",
            context_sentence="Individual actions, though seemingly trivial, collectively yield substantial impact.",
            video_id=sample_video.id,
            start_time=29.7,
            end_time=30.6,
            status="learning"
        )
    ]
    for c in sample_cards:
        db.add(c)

    db.commit()
    db.close()
    print("Nạp dữ liệu mẫu thành công!")

if __name__ == "__main__":
    seed()

