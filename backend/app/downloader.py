import os
import sys
import shutil
import subprocess
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger("downloader")

def get_ffmpeg_binary_path() -> str:
    """Trả về đường dẫn tới ffmpeg để yt-dlp và hậu xử lý sử dụng"""
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    
    venv_dir = os.path.dirname(sys.executable)
    ffmpeg_exe = os.path.join(venv_dir, "ffmpeg.exe")
    if os.path.exists(ffmpeg_exe):
        return ffmpeg_exe
        
    return ""


def apply_faststart(filepath: str) -> str:
    """
    Di chuyển chỉ mục 'moov atom' lên đầu file MP4 (FastStart).
    Giúp trình duyệt web có thể phát ngay lập tức (Zero-latency) mà không cần phải chờ 
    tải toàn bộ file hoặc tải metadata từ cuối file.
    """
    ffmpeg_exe = get_ffmpeg_binary_path()
    if not ffmpeg_exe or not os.path.exists(filepath):
        return filepath

    temp_file = filepath + ".fast.mp4"
    try:
        # -c copy giữ nguyên chất lượng gốc, chỉ tái cấu trúc header (mất < 1 giây)
        cmd = [
            ffmpeg_exe, "-y", "-loglevel", "error",
            "-i", filepath,
            "-c", "copy",
            "-movflags", "+faststart",
            temp_file
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0 and os.path.exists(temp_file):
            os.replace(temp_file, filepath)
            logger.info(f"Đã tối ưu hóa FastStart thành công cho: {filepath}")
    except Exception as e:
        logger.warning(f"Lỗi khi áp dụng FastStart: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    return filepath


def download_video_from_url(url: str, output_dir: str) -> Tuple[str, str, float]:
    """
    Tải video từ đường link (YouTube, TikTok, Facebook, Google Drive, hoặc link trực tiếp .mp4).
    Ưu tiên chuẩn H.264 720p - 1080p có phần cứng tăng tốc và tự động gắn FastStart để web phát tức thì.
    """
    import yt_dlp

    os.makedirs(output_dir, exist_ok=True)
    ffmpeg_path = get_ffmpeg_binary_path()

    # Cấu hình tối ưu tốc độ phát web:
    # 1. Giới hạn độ phân giải tối đa 720p/1080p (tránh kéo 4K AV1 cực nặng làm trình duyệt bị đơ)
    # 2. Ưu tiên H.264 (avc1) + AAC vì 100% thiết bị đều hỗ trợ Hardware Acceleration
    ydl_opts: Dict[str, Any] = {
        'format': (
            'bestvideo[height<=720][vcodec^=avc1]+bestaudio[ext=m4a]/'
            'bestvideo[height<=720]+bestaudio[ext=m4a]/'
            'best[height<=720]/'
            'bestvideo[height<=1080][vcodec^=avc1]+bestaudio[ext=m4a]/'
            'bestvideo[height<=1080]+bestaudio/'
            'best'
        ),
        'outtmpl': os.path.join(output_dir, '%(id)s_%(title).50s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': True,
    }

    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    logger.info(f"Đang bắt đầu tải video từ URL: {url}...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        
        if 'entries' in info:
            info = info['entries'][0]

        video_title = info.get('title', 'Video từ Link')
        duration = float(info.get('duration', 0.0) or 0.0)
        
        downloaded_file = ydl.prepare_filename(info)
        base_name, _ = os.path.splitext(downloaded_file)
        mp4_file = f"{base_name}.mp4"
        final_file = mp4_file if os.path.exists(mp4_file) else downloaded_file

        if not os.path.exists(final_file):
            raise FileNotFoundError(f"Không tìm thấy file sau khi tải: {final_file}")

        # Tối ưu hóa FastStart ngay sau khi tải
        final_file = apply_faststart(final_file)

        logger.info(f"Tải và tối ưu hóa video thành công: {final_file} ({duration}s)")
        return final_file, video_title, duration
