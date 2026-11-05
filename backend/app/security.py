import os
import re
import socket
import ipaddress
import urllib.parse
import logging
from typing import Tuple

logger = logging.getLogger("security")

# Giới hạn an toàn hệ thống
MAX_VIDEO_DURATION_SECONDS = 1800  # Tối đa 30 phút cho 1 video
MAX_FILE_SIZE_BYTES = 150 * 1024 * 1024  # Tối đa 150 MB

# Danh sách các domain video uy tín được tin cậy
TRUSTED_VIDEO_DOMAINS = {
    "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be",
    "tiktok.com", "www.tiktok.com", "vt.tiktok.com", "vm.tiktok.com",
    "facebook.com", "www.facebook.com", "fb.watch", "web.facebook.com",
    "instagram.com", "www.instagram.com",
    "vimeo.com", "player.vimeo.com",
    "ted.com", "www.ted.com",
    "dailymotion.com", "www.dailymotion.com",
    "drive.google.com", "dropbox.com", "www.dropbox.com"
}

# Các đuôi file video trực tiếp được phép
SAFE_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mkv", ".mov"}


def is_ip_private_or_restricted(ip_str: str) -> bool:
    """Kiểm tra IP có phải là IP nội bộ, loopback hoặc IP metadata đám mây không (Chặn SSRF)"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private or
            ip.is_loopback or
            ip.is_reserved or
            ip.is_link_local or
            ip.is_multicast or
            ip == ipaddress.ip_address("0.0.0.0")
        )
    except ValueError:
        return True


def validate_url_safety(url: str) -> Tuple[bool, str]:
    """
    Kiểm tra toàn diện tính an toàn của URL trước khi server tải về.
    Phòng chống:
      1. Tấn công SSRF (Server-Side Request Forgery vào localhost, 127.0.0.1, 169.254.169.254)
      2. Giao thức nguy hiểm (file://, gopher://, dict://, ftp://)
      3. Link rác hoặc domain tấn công nội bộ
    
    Trả về:
      (is_safe: bool, message: str)
    """
    if not url or not isinstance(url, str):
        return False, "Đường link không hợp lệ."

    url = url.strip()

    # 1. Kiểm tra Scheme (Chỉ cho phép http hoặc https)
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False, "Không thể phân tích cú pháp đường link."

    if parsed.scheme not in ("http", "https"):
        return False, f"Giao thức '{parsed.scheme}://' không được hỗ trợ vì lý do bảo mật. Chỉ chấp nhận http:// hoặc https://"

    hostname = parsed.hostname
    if not hostname:
        return False, "Đường link không chứa tên miền hợp lệ."

    # 2. Chặn các tên miền cục bộ rõ ràng
    lowered_host = hostname.lower()
    if lowered_host in ("localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal"):
        return False, "Cảnh báo bảo mật: Không được phép truy cập địa chỉ nội bộ (SSRF Blocked)."

    # 3. Phân giải DNS và kiểm tra IP (Chống DNS Rebinding & SSRF)
    try:
        addr_info = socket.getaddrinfo(hostname, None)
        for item in addr_info:
            ip_resolved = item[4][0]
            if is_ip_private_or_restricted(ip_resolved):
                return False, f"Cảnh báo bảo mật: Tên miền phân giải về địa chỉ IP nội bộ bị cấm ({ip_resolved})."
    except socket.gaierror:
        return False, f"Không thể phân giải tên miền '{hostname}'. Vui lòng kiểm tra lại đường link."
    except Exception as e:
        return False, f"Lỗi kiểm tra bảo mật: {str(e)}"

    # 4. Kiểm tra loại link: Domain video uy tín HOẶC link file video trực tiếp an toàn
    is_trusted = False
    for trusted in TRUSTED_VIDEO_DOMAINS:
        if lowered_host == trusted or lowered_host.endswith("." + trusted):
            is_trusted = True
            break

    if not is_trusted:
        # Nếu không nằm trong danh sách uy tín, bắt buộc phải là link trực tiếp tới file video
        path_lower = parsed.path.lower()
        has_safe_ext = any(path_lower.endswith(ext) for ext in SAFE_VIDEO_EXTENSIONS)
        if not has_safe_ext:
            return False, (
                f"Đường link từ '{hostname}' không nằm trong danh sách nền tảng video được hỗ trợ "
                f"(YouTube, TikTok, Facebook, Vimeo...) và không có đuôi file video an toàn (.mp4, .webm, .mov)."
            )

    return True, "URL an toàn."


def verify_file_is_genuine_video(filepath: str) -> Tuple[bool, str]:
    """
    Kiểm tra Magic Bytes (chữ ký nhị phân đầu file) sau khi tải về
    để đảm bảo đây thực sự là file video, không phải virus .exe, script độc hại hay file giả mạo.
    """
    if not os.path.exists(filepath):
        return False, "File không tồn tại."

    try:
        with open(filepath, "rb") as f:
            header = f.read(32)

        if len(header) < 12:
            return False, "File quá nhỏ hoặc bị hỏng."

        # Kiểm tra MP4/MOV: byte 4 đến 8 thường chứa 'ftyp'
        if b"ftyp" in header[4:12]:
            return True, "Định dạng MP4/MOV hợp lệ."

        # Kiểm tra WebM / Matroska: Bắt đầu bằng 0x1A 0x45 0xDF 0xA3
        if header.startswith(b"\x1a\x45\xdf\xa3"):
            return True, "Định dạng WebM/MKV hợp lệ."

        # Kiểm tra AVI (RIFF ... AVI)
        if header.startswith(b"RIFF") and b"AVI" in header[8:12]:
            return True, "Định dạng AVI hợp lệ."

        return False, "Cảnh báo bảo mật: File tải về không phải là định dạng video hợp lệ (Magic Bytes không khớp)."
    except Exception as e:
        return False, f"Không thể kiểm tra định dạng file: {str(e)}"
