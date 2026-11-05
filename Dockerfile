# Sử dụng image Python 3.11 chính thức
FROM python:3.11-slim

# Thiết lập biến môi trường không tạo file .pyc và xuất log trực tiếp
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt FFmpeg và các công cụ hệ thống cần thiết cho Whisper & yt-dlp
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements trước để tận dụng Docker cache layer
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . /app

# Đảm bảo thư mục lưu trữ video tồn tại
RUN mkdir -p /app/backend/uploads

# Railway cung cấp cổng qua biến môi trường $PORT
ENV PORT=8000
EXPOSE 8000

# Khởi chạy server FastAPI phục vụ cả API và giao diện Frontend
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
