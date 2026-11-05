import os
import sys
import shutil
import re
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("whisper_service")

def ensure_ffmpeg_in_path():
    """Đảm bảo ffmpeg luôn có sẵn trong PATH của tiến trình để Whisper không bị lỗi [WinError 2]"""
    if shutil.which("ffmpeg"):
        return

    # 1. Kiểm tra trong thư mục Scripts của python/venv
    venv_dir = os.path.dirname(sys.executable)
    candidate_exe = os.path.join(venv_dir, "ffmpeg.exe")
    if os.path.exists(candidate_exe):
        os.environ["PATH"] = venv_dir + os.pathsep + os.environ.get("PATH", "")
        logger.info(f"Đã bổ sung FFmpeg từ venv vào PATH: {venv_dir}")
        return

    # 2. Tự động kiểm tra và cấu hình từ imageio_ffmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        alias_path = os.path.join(ffmpeg_dir, "ffmpeg.exe")
        if not os.path.exists(alias_path):
            shutil.copyfile(ffmpeg_path, alias_path)
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        logger.info(f"Đã kích hoạt FFmpeg từ imageio_ffmpeg vào PATH: {ffmpeg_dir}")
    except Exception as e:
        logger.warning(f"Chưa thể tự động nạp FFmpeg: {e}")

# Kích hoạt ffmpeg ngay khi nạp module
ensure_ffmpeg_in_path()

# Cache model whisper toàn cục để tránh load lại nhiều lần gây tốn RAM/VRAM
_whisper_model = None

def get_whisper_model(model_name: str = "base"):
    """Tải và cache mô hình Whisper (mặc định 'base' phù hợp cân bằng tốc độ/chính xác)"""
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            logger.info(f"Đang nạp mô hình OpenAI Whisper '{model_name}'...")
            _whisper_model = whisper.load_model(model_name)
            logger.info("Nạp mô hình Whisper thành công.")
        except Exception as e:
            logger.error(f"Lỗi khi nạp OpenAI Whisper: {e}")
            raise e
    return _whisper_model


def clean_word(word: str) -> str:
    """Chuẩn hóa từ: loại bỏ khoảng trắng thừa và dấu câu, chuyển về chữ thường để phục vụ tìm kiếm"""
    cleaned = re.sub(r"[^\w\s]", "", word).strip().lower()
    return cleaned


def transcribe_video_with_word_timestamps(video_path: str, model_name: str = "base") -> Dict[str, Any]:
    """
    Trích xuất âm thanh từ video và nhận diện giọng nói kèm Word-level Timestamps bằng OpenAI Whisper.
    
    Tham số:
        video_path: Đường dẫn tuyệt đối tới file video (.mp4)
        model_name: Phiên bản model ('tiny', 'base', 'small', 'medium')
        
    Trả về:
        Dictionary chứa danh sách các đoạn câu (segments) và danh sách chi tiết các từ (words) kèm mốc thời gian.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Không tìm thấy file video tại: {video_path}")

    model = get_whisper_model(model_name)

    logger.info(f"Bắt đầu transcribe video: {video_path} (word_timestamps=True)...")
    
    # word_timestamps=True kích hoạt cơ chế cross-attention alignment trích xuất timestamp chi tiết từng từ
    result = model.transcribe(
        video_path,
        word_timestamps=True,
        fp16=False, # Đặt False để chạy mượt trên cả CPU và GPU
        language="en" # Ưu tiên tiếng Anh cho app học IELTS / Tiếng Anh
    )

    parsed_segments: List[Dict[str, Any]] = []
    all_words: List[Dict[str, Any]] = []
    
    total_duration = 0.0

    for seg in result.get("segments", []):
        seg_start = float(seg.get("start", 0.0))
        seg_end = float(seg.get("end", 0.0))
        seg_text = seg.get("text", "").strip()

        if seg_end > total_duration:
            total_duration = seg_end

        # Trích xuất danh sách word-level timestamps của đoạn này
        seg_words = []
        raw_words = seg.get("words", [])
        
        for w in raw_words:
            w_text = w.get("word", "").strip()
            w_clean = clean_word(w_text)
            w_start = float(w.get("start", seg_start))
            w_end = float(w.get("end", seg_end))

            if w_clean:
                word_info = {
                    "word": w_clean,
                    "display_word": w_text,
                    "start_time": round(w_start, 3),
                    "end_time": round(w_end, 3)
                }
                seg_words.append(word_info)
                all_words.append(word_info)

        parsed_segments.append({
            "text": seg_text,
            "start_time": round(seg_start, 3),
            "end_time": round(seg_end, 3),
            "words": seg_words,
            "words_json": json.dumps(seg_words, ensure_ascii=False)
        })

    logger.info(f"Hoàn thành transcribe: {len(parsed_segments)} đoạn câu, {len(all_words)} từ vựng.")

    return {
        "duration": round(total_duration, 2),
        "segments": parsed_segments,
        "total_words_count": len(all_words)
    }

