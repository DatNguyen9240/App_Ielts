import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Đường dẫn lưu trữ SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "vocab_app.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Kết nối SQLite với chế độ check_same_thread=False để hỗ trợ đa luồng trong FastAPI
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency injection cung cấp database session cho mỗi request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

