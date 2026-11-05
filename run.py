import os
import sys
import uvicorn

# Đảm bảo đường dẫn import đúng module
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURRENT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"

    print("=" * 65)
    print("  SMART VIDEO VOCABULARY & FLASHCARD APP (FastAPI + Whisper)")
    print("=" * 65)
    print(f"🚀 Đang khởi động server tại: http://{host}:{port}")
    print(f"📚 Swagger API Docs: http://{host}:{port}/docs")
    print("💡 Mẹo: Chạy 'python seed_demo_data.py' để nạp sẵn dữ liệu mẫu nếu chưa có video.")
    print("=" * 65)

    uvicorn.run(
        "backend.app.main:app",
        host=host,
        port=port,
        reload=not bool(os.environ.get("PORT"))
    )

