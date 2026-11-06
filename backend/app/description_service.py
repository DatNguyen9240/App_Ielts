import re
import logging
from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import Session
from sqlalchemy import or_

from . import models, schemas, crud, translation_service, downloader

logger = logging.getLogger("description_service")

# Danh sách từ dừng (Stopwords) tiếng Anh và thuật ngữ rác YouTube cần loại bỏ
COMMON_STOPWORDS: Set[str] = {
    # Pronouns & determiners
    "the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her", "its", "our", "their",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "us", "them", "who", "whom", "whose", "which", "what",
    # Prepositions & conjunctions
    "in", "on", "at", "to", "for", "with", "from", "by", "about", "into", "through", "during", "before", "after",
    "above", "below", "between", "under", "since", "without", "and", "but", "or", "so", "yet", "because", "although", "while",
    # Auxiliary verbs & common verbs
    "is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could",
    "will", "would", "shall", "should", "may", "might", "must", "get", "got", "go", "goes", "went", "come", "make", "made",
    "say", "said", "know", "see", "think", "take", "look", "use", "find", "tell", "ask", "seem", "feel", "try", "leave", "call",
    # Adverbs & qualifiers
    "not", "no", "very", "too", "also", "just", "only", "now", "then", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "than", "much", "many", "well", "even",
    # YouTube boilerplate & metadata words
    "http", "https", "www", "com", "net", "org", "bit", "ly", "youtube", "video", "channel", "subscribe", "subscriber",
    "like", "share", "comment", "playlist", "watch", "link", "click", "below", "description", "lesson", "free", "pdf",
    "download", "join", "member", "instagram", "facebook", "twitter", "telegram", "tiktok", "email", "contact",
    "ielts", "speaking", "band", "test", "part", "exam", "score", "sample", "answer", "answers", "questions", "tips"
}


def clean_word(text: str) -> str:
    """Loại bỏ ký tự đặc biệt ở đầu/cuối từ"""
    return re.sub(r'^[^\w]+|[^\w]+$', '', text).strip()


def extract_candidate_vocab_from_text(description_text: str) -> List[Dict[str, Any]]:
    """
    Trích xuất các ứng viên từ vựng từ nội dung mô tả (Description) của YouTube.
    Bao gồm:
    1. Các dòng có định dạng danh sách bài học (1. Word: definition, - Word - meaning, • Word...)
    2. Các dòng có mốc thời gian kèm từ (01:24 - Word)
    3. Các từ/cụm từ tiếng Anh nổi bật trong văn bản
    """
    if not description_text:
        return []

    candidates: List[Dict[str, Any]] = []
    seen_words: Set[str] = set()

    lines = description_text.splitlines()

    # BƯỚC 1: TRÍCH XUẤT CÓ CẤU TRÚC (Ưu tiên cao nhất)
    for raw_line in lines:
        line = raw_line.strip()
        if not line or len(line) < 3:
            continue

        # Bỏ qua các dòng chỉ chứa URL hoặc mạng xã hội
        if re.search(r'https?://|www\.|@|subscribe|facebook|instagram|telegram', line, re.IGNORECASE):
            continue

        matched_word = None
        definition = None

        # Pattern 1: Dòng đánh số hoặc gạch đầu dòng kèm định nghĩa
        # ví dụ: "1. Sedentary lifestyle: a way of life..." hoặc "- Commute (v) - travel to work"
        m1 = re.match(r'^(?:\d+[\.\)]|\-|\*|•|👉|🔹|▪️)\s*([A-Za-z\s\-\']{2,45})(?:[\:\–\—\(\]](.*))?$', line)
        if m1:
            matched_word = m1.group(1).strip()
            if m1.group(2):
                definition = m1.group(2).strip()

        # Pattern 2: Dòng mốc thời gian (Timestamps)
        # ví dụ: "03:15 - Pristine environment" hoặc "02:40 Invigorate"
        if not matched_word:
            m2 = re.match(r'^\d{1,2}:\d{2}(?::\d{2})?(?:\s*[\-–—:])?\s*([A-Za-z\s\-\']{2,45})(?:[\:\–\—\(\]](.*))?$', line)
            if m2:
                matched_word = m2.group(1).strip()
                if m2.group(2):
                    definition = m2.group(2).strip()

        # Pattern 3: Dòng từ vựng dạng "Word: Definition"
        if not matched_word:
            m3 = re.match(r'^([A-Za-z\s\-\']{2,35})\s*[:–—]\s*(.+)$', line)
            if m3:
                matched_word = m3.group(1).strip()
                definition = m3.group(2).strip()

        if matched_word:
            cw = clean_word(matched_word)
            lowered = cw.lower()
            if (len(cw) >= 3 and 
                lowered not in COMMON_STOPWORDS and 
                lowered not in seen_words and 
                not re.match(r'^\d+$', cw)):
                seen_words.add(lowered)
                candidates.append({
                    "word": cw,
                    "definition_in_desc": definition,
                    "is_structured": True
                })

    # BƯỚC 2: TRÍCH XUẤT CÁC TỪ TRONG NGOẶC KÉP HOẶC IN ĐẬM
    quoted_matches = re.findall(r'["“\']([A-Za-z\s\-\']{3,35})["”\']|\*\*([A-Za-z\s\-\']{3,35})\*\*', description_text)
    for q1, q2 in quoted_matches:
        raw = q1 or q2
        cw = clean_word(raw)
        lowered = cw.lower()
        if (len(cw) >= 3 and 
            lowered not in COMMON_STOPWORDS and 
            lowered not in seen_words and 
            not re.match(r'^\d+$', cw)):
            seen_words.add(lowered)
            candidates.append({
                "word": cw,
                "definition_in_desc": None,
                "is_structured": True
            })

    # BƯỚC 3: TRÍCH XUẤT CÁC TỪ VỰNG TIẾNG ANH ĐƠN LẺ & CỤM TỪ TIỀM NĂNG (Collocations)
    # Tách các từ riêng lẻ trong văn bản mô tả
    raw_tokens = re.findall(r'\b[A-Za-z]{4,25}\b', description_text)
    for token in raw_tokens:
        lowered = token.lower()
        if lowered not in COMMON_STOPWORDS and lowered not in seen_words:
            seen_words.add(lowered)
            candidates.append({
                "word": token,
                "definition_in_desc": None,
                "is_structured": False
            })

    return candidates


def match_description_vocab_with_video(
    db: Session, 
    video_id: int, 
    description_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Dò tìm các từ vựng xuất hiện trong Description xem có câu nào trong video sử dụng từ đó không.
    Trả về danh sách câu ngữ cảnh, mốc thời gian phát âm chính xác và gợi ý nghĩa tiếng Việt.
    """
    video = crud.get_video_by_id(db, video_id)
    if not video:
        raise ValueError("Không tìm thấy video này trong cơ sở dữ liệu")

    # 1. Xác định nội dung Description
    final_desc = ""
    if description_text and description_text.strip():
        final_desc = description_text.strip()
        # Lưu lại vào database nếu trước đó video chưa có description
        if not video.description or video.description != final_desc:
            crud.update_video_description(db, video_id, final_desc)
    elif video.description and video.description.strip():
        final_desc = video.description.strip()
    elif video.source_url and video.source_url.strip():
        # Thử lấy trực tiếp từ YouTube nếu có source_url
        logger.info(f"Đang tự động lấy Description từ YouTube cho video {video_id}...")
        fetched_desc = downloader.fetch_video_description_from_url(video.source_url)
        if fetched_desc:
            final_desc = fetched_desc
            crud.update_video_description(db, video_id, final_desc)

    if not final_desc:
        return {
            "video_id": video.id,
            "video_title": video.title,
            "description": "",
            "total_found": 0,
            "matched_vocab": []
        }

    # 2. Lấy toàn bộ câu (segments) và từ vựng (words) của video từ SQLite
    segments = db.query(models.TranscriptSegment).filter(
        models.TranscriptSegment.video_id == video.id
    ).order_by(models.TranscriptSegment.start_time).all()

    if not segments:
        return {
            "video_id": video.id,
            "video_title": video.title,
            "description": final_desc,
            "total_found": 0,
            "matched_vocab": []
        }

    # Tạo từ điển câu để tra cứu nhanh
    segments_by_id = {s.id: s for s in segments}

    # 3. Trích xuất danh sách ứng viên từ Description
    candidates = extract_candidate_vocab_from_text(final_desc)
    structured_count = sum(1 for c in candidates if c.get("is_structured"))

    # NẾU DESCRIPTION KHÔNG CÓ TỪ VỰNG CÓ CẤU TRÚC: Tự động lấy bình luận được ghim từ YouTube
    if structured_count == 0 and video.source_url:
        try:
            from . import youtube_service
            comments_res = youtube_service.fetch_youtube_pinned_or_top_comments(video.source_url)
            pinned_text = comments_res.get("combined_text") or comments_res.get("pinned_comment")
            if pinned_text:
                logger.info(f"Description không có từ vựng, tự động bổ sung Bình luận ghim cho video {video.id}")
                final_desc = (final_desc + "\n\n📌 [BÌNH LUẬN ĐƯỢC GHIM TỪ TÁC GIẢ]:\n" + pinned_text).strip()
                candidates = extract_candidate_vocab_from_text(final_desc)
        except Exception as e_comm:
            logger.warning(f"Không thể lấy bình luận ghim: {e_comm}")

    matched_results: List[schemas.DescriptionMatchedVocabItem] = []
    processed_words_lower: Set[str] = set()

    for item in candidates:
        cand_word = item["word"]
        cand_lower = cand_word.lower()

        if cand_lower in processed_words_lower:
            continue

        # Tìm kiếm trong cơ sở dữ liệu:
        # Trường hợp 1: Từ đơn -> Tìm qua TranscriptWord để có mốc thời gian chính xác của từ
        matched_segment = None
        w_start = 0.0
        w_end = 0.0
        occurrences = 0

        if " " not in cand_word:
            # Tra cứu qua bảng TranscriptWord
            words_in_db = db.query(models.TranscriptWord).filter(
                models.TranscriptWord.video_id == video.id,
                models.TranscriptWord.word == cand_lower
            ).all()

            if words_in_db:
                occurrences = len(words_in_db)
                first_w = words_in_db[0]
                w_start = first_w.start_time
                w_end = first_w.end_time
                matched_segment = segments_by_id.get(first_w.segment_id)

        # Trường hợp 2: Cụm từ (Collocation/Idiom) hoặc từ không có trong TranscriptWord
        if not matched_segment:
            # Quét regex nguyên từ trong các câu segments
            pattern = re.compile(rf'\b{re.escape(cand_word)}\b', re.IGNORECASE)
            for seg in segments:
                if pattern.search(seg.text):
                    occurrences += 1
                    if not matched_segment:
                        matched_segment = seg
                        w_start = seg.start_time
                        w_end = seg.end_time

        # Nếu tìm thấy câu trong video sử dụng từ vựng này
        if matched_segment:
            processed_words_lower.add(cand_lower)

            # Tra cứu gợi ý nghĩa tiếng Việt
            dict_data = translation_service.lookup_word_vietnamese(
                word=cand_word, 
                context_sentence=matched_segment.text
            )
            vn_meaning = dict_data.get("meaning") or ""
            vn_suggestions = dict_data.get("suggestions") or []

            matched_results.append(
                schemas.DescriptionMatchedVocabItem(
                    word=cand_word,
                    raw_entry=item.get("word"),
                    definition_in_desc=item.get("definition_in_desc"),
                    vietnamese_meaning=vn_meaning,
                    vietnamese_suggestions=vn_suggestions,
                    context_sentence=matched_segment.text,
                    sentence_start_time=matched_segment.start_time,
                    sentence_end_time=matched_segment.end_time,
                    word_start_time=w_start,
                    word_end_time=w_end,
                    occurrences_count=occurrences
                )
            )

    # Ưu tiên các từ vựng có cấu trúc từ description lên trước, sắp xếp theo thời gian xuất hiện trong video
    matched_results.sort(key=lambda x: x.sentence_start_time)

    logger.info(f"Đã quét Description video {video.id}: tìm thấy {len(matched_results)} từ vựng xuất hiện trong video")

    return {
        "video_id": video.id,
        "video_title": video.title,
        "description": final_desc,
        "total_found": len(matched_results),
        "matched_vocab": matched_results
    }


# Bộ nhớ đệm quét từ vựng online cho video YouTube trên các tab chủ đề
_ONLINE_VOCAB_CACHE: Dict[str, Dict[str, Any]] = {}

def scan_youtube_online_vocab(
    youtube_id: str,
    url: Optional[str] = None,
    title: Optional[str] = None,
    custom_description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Trích xuất từ vựng trong Description và dò câu ngữ cảnh thực tế của video YouTube trực tuyến (Topic Videos)
    qua phụ đề / captions của YouTube hoặc mô tả video mà không cần tải file về máy.
    """
    cache_key = f"{youtube_id}_{hash(custom_description) if custom_description else 'default'}"
    if cache_key in _ONLINE_VOCAB_CACHE:
        return _ONLINE_VOCAB_CACHE[cache_key]

    from . import youtube_service

    video_url = url or f"https://www.youtube.com/watch?v={youtube_id}"
    video_info = youtube_service.get_youtube_video_info_and_captions(youtube_id or video_url)
    video_title = title or video_info.get("title") or "IELTS Video"
    description = custom_description or video_info.get("description", "")
    segments = video_info.get("segments", [])

    # 2. Bóc tách từ vựng từ Description
    candidates = extract_candidate_vocab_from_text(description)
    structured_count = sum(1 for c in candidates if c.get("is_structured"))

    # NẾU DESCRIPTION KHÔNG CÓ TỪ VỰNG: Tự động lấy bình luận ghim của video
    if structured_count == 0:
        try:
            comments_res = youtube_service.fetch_youtube_pinned_or_top_comments(youtube_id)
            pinned_text = comments_res.get("combined_text") or comments_res.get("pinned_comment")
            if pinned_text:
                logger.info(f"Description online {youtube_id} không có từ vựng, tự động bổ sung Bình luận ghim")
                description = (description + "\n\n📌 [BÌNH LUẬN ĐƯỢC GHIM TỪ TÁC GIẢ]:\n" + pinned_text).strip()
                candidates = extract_candidate_vocab_from_text(description)
        except Exception as e_comm:
            logger.warning(f"Không thể lấy bình luận ghim cho {youtube_id}: {e_comm}")

    matched_results: List[Dict[str, Any]] = []
    processed_words_lower: Set[str] = set()

    for item in candidates:
        cand_word = item["word"]
        cand_lower = cand_word.lower()

        if cand_lower in processed_words_lower:
            continue

        matched_segment = None
        occurrences = 0

        # Nếu có phụ đề thì dò trong phụ đề video
        if segments:
            pattern = re.compile(rf'\b{re.escape(cand_word)}\b', re.IGNORECASE)
            for seg in segments:
                if pattern.search(seg['text']):
                    occurrences += 1
                    if not matched_segment:
                        matched_segment = seg

        # Dù có phụ đề hay không, nếu là từ có cấu trúc bài học trong description thì vẫn lấy
        if matched_segment or item.get("is_structured"):
            processed_words_lower.add(cand_lower)
            ctx = matched_segment['text'] if matched_segment else f"Từ vựng trọng tâm trong bài: {cand_word}"
            s_time = matched_segment['start_time'] if matched_segment else 0.0
            e_time = matched_segment['end_time'] if matched_segment else 0.0

            dict_data = translation_service.lookup_word_vietnamese(word=cand_word, context_sentence=ctx)
            vn_meaning = dict_data.get("meaning") or ""
            vn_suggestions = dict_data.get("suggestions") or []

            matched_results.append({
                "word": cand_word,
                "raw_entry": item.get("word"),
                "definition_in_desc": item.get("definition_in_desc"),
                "vietnamese_meaning": vn_meaning,
                "vietnamese_suggestions": vn_suggestions,
                "context_sentence": ctx,
                "sentence_start_time": s_time,
                "sentence_end_time": e_time,
                "word_start_time": s_time,
                "word_end_time": e_time,
                "occurrences_count": max(1, occurrences)
            })

    matched_results.sort(key=lambda x: x["sentence_start_time"])

    result = {
        "video_id": youtube_id,
        "video_title": video_title,
        "description": description,
        "total_found": len(matched_results),
        "matched_vocab": matched_results
    }
    _ONLINE_VOCAB_CACHE[cache_key] = result
    return result

