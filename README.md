# 🎬 Smart Video Vocabulary & Flashcard App

Ứng dụng web thông minh giúp học từ vựng tiếng Anh qua ngữ cảnh video thực tế. Hệ thống tích hợp **OpenAI Whisper** trích xuất văn bản kèm **mốc thời gian chi tiết đến từng từ (word-level timestamps)**, hỗ trợ tìm kiếm từ vựng và tự động tua video đến đúng thời điểm phát âm, kết hợp ôn tập bằng bộ thẻ **Flashcard 3D lật tương tác**.

---

## 🏗️ Kiến trúc Hệ thống (System Architecture)

```
+-----------------------------------------------------------------------------------+
|                                 FRONTEND SPA                                      |
|  - HTML5 Video Player (Tua currentTime chính xác)                                 |
|  - Tab 1: Tra cứu từ vựng theo video (Highlight từ, Seek mốc phát âm)             |
|  - Tab 2: 3D Flip Flashcard Deck (Ngữ cảnh video + Nút replay clip gốc)           |
+------------------------------------------+----------------------------------------+
                                           | HTTP Requests / JSON (REST APIs)
                                           v
+-----------------------------------------------------------------------------------+
|                             BACKEND (FastAPI Python)                              |
|  - Video Processing Pipeline (Upload -> Whisper word_timestamps=True -> Save DB)  |
|  - Search Engine (Full-text query kết hợp Word & Segment Indexing)                |
|  - Static Files Mount (/uploads/ với HTTP 206 Partial Content phục vụ Tua Video)   |
|  - Flashcard CRUD APIs                                                            |
+---------------------+-------------------------------------+-----------------------+
                      |                                     |
                      v                                     v
+-------------------------------+         +-----------------------------------------+
|     OpenAI Whisper Model      |         |             SQLite Database             |
|  (Audio to Word Timestamps)   |         |  - videos                               |
|  - segments: [start, end, text]         |  - transcript_segments                  |
|  - words: [start, end, word]  |         |  - transcript_words (Indexed)           |
+-------------------------------+         |  - flashcards                           |
                                          +-----------------------------------------+
```

---

## 📁 Cấu trúc Thư mục Dự án

```text
IELTS App/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py         # Kết nối SQLite & SQLAlchemy Engine
│   │   ├── models.py           # Thiết kế bảng CSDL (Video, Segment, Word, Flashcard)
│   │   ├── schemas.py          # Pydantic schemas xác thực dữ liệu vào/ra
│   │   ├── crud.py             # Truy vấn CSDL, Full-text Search từ vựng & Flashcards
│   │   ├── whisper_service.py  # Trích xuất Whisper với word_timestamps=True
│   │   └── main.py             # FastAPI App, REST APIs & Static Files Mounting
│   ├── uploads/                # Thư mục lưu trữ file video (.mp4)
│   ├── vocab_app.db            # Cơ sở dữ liệu SQLite (Tự động sinh khi chạy)
│   └── requirements.txt        # Các thư viện Python cần thiết
├── frontend/
│   ├── index.html              # Giao diện chính (2 Tabs: Tra cứu & Flashcard)
│   ├── css/
│   │   └── style.css           # Hiệu ứng 3D Flip Card & styling
│   └── js/
│       └── app.js              # Logic xử lý giao diện, tua video, Flashcard Deck
├── seed_demo_data.py           # Script nạp dữ liệu mẫu để trải nghiệm nhanh
├── run.py                      # Script khởi chạy ứng dụng 1 dòng lệnh
└── README.md
```

---

## 🛠️ Hướng dẫn Cài đặt & Triển khai trên Máy Cá nhân

### Yêu cầu tiên quyết:
- **Python**: Phiên bản 3.9 đến 3.12.
- **FFmpeg**: Cần thiết cho `openai-whisper` để giải mã âm thanh từ video.
  - *Windows*: Tải từ [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) hoặc cài bằng `winget install Gyan.FFmpeg` hoặc `choco install ffmpeg`.
  - *macOS*: `brew install ffmpeg`
  - *Ubuntu/Debian*: `sudo apt update && sudo apt install ffmpeg`

### Bước 1: Mở Terminal và điều hướng vào thư mục dự án
```bash
cd "d:/Dat/IELTS App"
```

### Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)
```bash
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt các thư viện phụ thuộc
```bash
pip install -r backend/requirements.txt
```

> **Lưu ý với PyTorch:** Nếu máy bạn có card đồ họa NVIDIA CUDA, bạn có thể cài bản PyTorch hỗ trợ GPU để Whisper chạy siêu tốc theo hướng dẫn tại [pytorch.org](https://pytorch.org/). Mặc định CPU vẫn chạy rất tốt với mô hình `base` hoặc `tiny`.

### Bước 4 (Tùy chọn): Nạp sẵn dữ liệu mẫu để thử nghiệm ngay
Nếu bạn chưa có sẵn video bài thi IELTS hoặc muốn xem ngay cách ứng dụng hoạt động:
```bash
python seed_demo_data.py
```

### Bước 5: Khởi động ứng dụng
```bash
python run.py
```
- Mở trình duyệt truy cập: **`http://127.0.0.1:8000`**
- Truy cập tài liệu API tự động (Swagger UI): **`http://127.0.0.1:8000/docs`**

---

## 💡 Hướng dẫn Sử dụng Chi tiết

### 1. Tab 1: Tra cứu Từ vựng trong Video
1. Bấm nút **"Tải video mới"**. Bạn có 2 lựa chọn:
   - **Dán Link Video (Khuyên dùng):** Dán link bất kỳ từ **YouTube**, **TikTok**, **Facebook**, hoặc link file `.mp4` trực tiếp. Hệ thống sẽ tự động tải về và chạy Whisper.
   - **Tải file từ máy tính:** Chọn file `.mp4` có sẵn trên máy của bạn.
2. Tại ô **"Tra cứu từ vựng"**, gõ từ tiếng Anh bạn muốn tìm (ví dụ: `climate`, `sustainable`, `unprecedented`...).
3. Bấm nút **"Phát đoạn này"**: Video sẽ ngay lập tức nhảy (`video.currentTime`) đến khoảnh khắc nhân vật phát âm từ đó.
4. Bấm nút **"+ Flashcard"**: Hộp thoại xuất hiện cho phép bạn nhập nghĩa tiếng Việt và lưu ngay vào bộ thẻ cá nhân.

### 2. Tab 2: Ôn tập Flashcard thông minh
1. Chuyển sang tab **"Ôn tập Flashcard"** (hoặc xem số lượng thẻ trên badge).
2. Thẻ hiển thị **Mặt trước** gồm từ vựng + câu ví dụ trong video (từ được highlight).
3. Nhấp vào thẻ hoặc bấm phím **Space** để lật sang **Mặt sau** xem nghĩa tiếng Việt.
4. Bấm nút **"Xem lại đoạn video gốc"**: Một popup phát đúng phân đoạn ngữ cảnh trong video sẽ hiện lên, giúp bạn ôn lại cách phát âm, ngữ điệu và biểu cảm thực tế!
5. Bấm **"Đánh dấu đã thuộc"** để theo dõi tiến độ ghi nhớ.

