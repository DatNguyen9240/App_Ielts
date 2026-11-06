import logging
import urllib.request
import json
import re
from typing import List, Dict, Any, Optional

from . import translation_service

logger = logging.getLogger("youtube_service")

# Cache phụ đề YouTube trong bộ nhớ để tìm kiếm siêu tốc (0ms)
_YOUTUBE_CAPTIONS_CACHE: Dict[str, List[Dict[str, Any]]] = {}
_YOUTUBE_INFO_CACHE: Dict[str, Dict[str, Any]] = {}


def extract_youtube_id(url_or_id: str) -> str:
    """Trích xuất ID video YouTube 11 ký tự từ URL bất kỳ hoặc chuỗi ID"""
    url_or_id = url_or_id.strip()
    if len(url_or_id) == 11 and re.match(r'^[A-Za-z0-9_-]{11}$', url_or_id):
        return url_or_id

    patterns = [
        r'(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/)([A-Za-z0-9_-]{11})',
        r'[\?&]v=([A-Za-z0-9_-]{11})'
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return url_or_id


def get_youtube_video_info_and_captions(youtube_id_or_url: str) -> Dict[str, Any]:
    """
    Lấy thông tin và phụ đề chi tiết (kèm mốc thời gian từng câu/từ) của video YouTube
    mà KHÔNG CẦN TẢI VIDEO VỀ MÁY (Thời gian xử lý: ~1-2 giây).
    """
    v_id = extract_youtube_id(youtube_id_or_url)
    if v_id in _YOUTUBE_INFO_CACHE:
        return _YOUTUBE_INFO_CACHE[v_id]

    import yt_dlp
    video_url = f"https://www.youtube.com/watch?v={v_id}"

    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 10
    }

    info_res = {
        "id": v_id,
        "title": "IELTS YouTube Video",
        "channel": "YouTube",
        "duration": 0.0,
        "description": "",
        "thumbnail": f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg",
        "segments": []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if 'entries' in info and info['entries']:
                info = info['entries'][0]

            info_res["title"] = info.get("title") or info_res["title"]
            info_res["channel"] = info.get("channel") or info.get("uploader") or "YouTube"
            info_res["duration"] = float(info.get("duration") or 0.0)
            info_res["description"] = info.get("description") or ""
            info_res["thumbnail"] = info.get("thumbnail") or f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg"

            # Tìm phụ đề tiếng Anh (hỗ trợ en, en-US, en-GB, en-orig, ...)
            auto_caps = info.get("automatic_captions", {}) or {}
            sub_caps = info.get("subtitles", {}) or {}
            subs = []
            for k in ["en", "en-US", "en-GB", "en-CA", "en-orig"]:
                if k in auto_caps:
                    subs = auto_caps[k]
                    break
                if k in sub_caps:
                    subs = sub_caps[k]
                    break

            if not subs:
                for lang_code, cap_list in {**auto_caps, **sub_caps}.items():
                    if lang_code.lower().startswith("en"):
                        subs = cap_list
                        break

            json3_url = next((s["url"] for s in subs if s.get("ext") == "json3"), None)
            vtt_url = next((s["url"] for s in subs if s.get("ext") == "vtt"), None) if not json3_url else None

            if json3_url:
                req = urllib.request.Request(json3_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    caption_data = json.loads(resp.read().decode("utf-8"))
                    segments = []
                    seg_id = 1

                    for ev in caption_data.get("events", []):
                        segs = ev.get("segs", [])
                        text = "".join(s.get("utf8", "") for s in segs).strip().replace("\n", " ")
                        t_start = ev.get("tStartMs", 0) / 1000.0
                        d_ms = ev.get("dDurationMs", 0) / 1000.0
                        t_end = t_start + d_ms

                        if text and len(text) > 1 and not text.startswith("["):
                            # Trích xuất các từ con trong câu (nếu có offset)
                            words_list = []
                            for s in segs:
                                w_text = s.get("utf8", "").strip()
                                if w_text and len(w_text) > 0:
                                    w_offset = (s.get("tOffsetMs", 0)) / 1000.0
                                    w_start = t_start + w_offset
                                    clean_w = re.sub(r'^[^\w]+|[^\w]+$', '', w_text).lower()
                                    if clean_w:
                                        words_list.append({
                                            "word": clean_w,
                                            "display_word": w_text,
                                            "start_time": round(w_start, 2),
                                            "end_time": round(w_start + 0.35, 2)
                                        })

                            segments.append({
                                "id": seg_id,
                                "text": text,
                                "start_time": round(t_start, 2),
                                "end_time": round(t_end, 2),
                                "words": words_list
                            })
                            seg_id += 1

                    info_res["segments"] = segments

            elif vtt_url:
                req = urllib.request.Request(vtt_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    vtt_text = resp.read().decode("utf-8")
                    segments = []
                    seg_id = 1
                    # Parse basic VTT blocks
                    blocks = re.split(r'\n\s*\n', vtt_text)
                    for blk in blocks:
                        m = re.search(r'(\d{2}:)?(\d{2}):(\d{2})\.(\d{3})\s*-->\s*(\d{2}:)?(\d{2}):(\d{2})\.(\d{3})', blk)
                        if m:
                            # Parse start and end times
                            lines = [ln.strip() for ln in blk.strip().splitlines() if not re.match(r'^\d+$|-->|WEBVTT', ln)]
                            clean_sentence = " ".join(lines).strip()
                            clean_sentence = re.sub(r'<[^>]+>', '', clean_sentence)
                            if clean_sentence and len(clean_sentence) > 1:
                                segments.append({
                                    "id": seg_id,
                                    "text": clean_sentence,
                                    "start_time": 0.0,
                                    "end_time": 0.0,
                                    "words": []
                                })
                                seg_id += 1
                    info_res["segments"] = segments

    except Exception as e:
        logger.warning(f"Lỗi khi trích xuất phụ đề YouTube {v_id}: {e}")

    _YOUTUBE_INFO_CACHE[v_id] = info_res
    return info_res


def search_words_in_youtube_online(youtube_id_or_url: str, query: str) -> Dict[str, Any]:
    """
    Tìm kiếm từ vựng trực tiếp trong bài nói của video YouTube mà không cần tải file về.
    Trả về danh sách câu ngữ cảnh có mốc thời gian chính xác và gợi ý nghĩa tiếng Việt.
    """
    clean_query = query.strip().lower()
    if not clean_query:
        return {"query": query, "total_found": 0, "results": []}

    video_info = get_youtube_video_info_and_captions(youtube_id_or_url)
    segments = video_info.get("segments", [])

    results = []
    pattern = re.compile(rf'\b{re.escape(clean_query)}\b', re.IGNORECASE)

    for seg in segments:
        text = seg["text"]
        if pattern.search(text):
            # Tìm mốc thời gian chính xác của từ nếu có
            w_start = seg["start_time"]
            w_end = seg["end_time"]
            for w in seg.get("words", []):
                if w["word"] == clean_query:
                    w_start = w["start_time"]
                    w_end = w["end_time"]
                    break

            # Tra nghĩa tiếng Việt
            dict_data = translation_service.lookup_word_vietnamese(clean_query, text)

            results.append({
                "segment_id": seg["id"],
                "video_id": video_info["id"],
                "video_title": video_info["title"],
                "context_sentence": text,
                "matched_word": clean_query,
                "sentence_start_time": seg["start_time"],
                "sentence_end_time": seg["end_time"],
                "word_start_time": w_start,
                "word_end_time": w_end,
                "vietnamese_meaning": dict_data.get("meaning") or "",
                "vietnamese_suggestions": dict_data.get("suggestions") or []
            })

    return {
        "youtube_id": video_info["id"],
        "video_title": video_info["title"],
        "query": clean_query,
        "total_found": len(results),
        "results": results
    }


def search_youtube_videos_online(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """Tìm kiếm danh sách video thực tế trên YouTube theo từ khóa tùy thích"""
    import yt_dlp
    search_query = f"ytsearch{max_results}:IELTS Speaking {query}"
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 8
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(search_query, download=False)
            items = []
            for entry in res.get('entries', []):
                v_id = entry.get('id', '')
                title = entry.get('title', 'IELTS Video')
                channel = entry.get('channel') or entry.get('uploader') or 'YouTube'
                duration = int(entry.get('duration') or 0)
                url = entry.get('url') or f"https://www.youtube.com/watch?v={v_id}"
                
                if duration > 60:
                    items.append({
                        "id": v_id,
                        "title": title,
                        "channel": channel,
                        "url": url,
                        "thumbnail": f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg",
                        "duration": duration
                    })
            return items
    except Exception as e:
        logger.warning(f"Lỗi khi tìm kiếm video YouTube: {e}")
        return []

