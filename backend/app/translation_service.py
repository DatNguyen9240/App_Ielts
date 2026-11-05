import urllib.request
import urllib.parse
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("translation_service")

# Bộ từ điển offline dự phòng cho các từ IELTS phổ biến trong trường hợp mất kết nối mạng
OFFLINE_FALLBACK = {
    "unprecedented": ["chưa từng có tiền lệ", "chưa từng xảy ra"],
    "sustainable": ["bền vững", "có thể duy trì lâu dài"],
    "substantial": ["đáng kể", "quan trọng", "lớn lao"],
    "eloquent": ["có tài hùng biện", "lưu loát", "hùng hồn"],
    "biodiversity": ["đa dạng sinh học"],
    "mitigate": ["giảm nhẹ", "làm dịu bớt"],
    "implement": ["thực thi", "triển khai", "áp dụng"],
    "crucial": ["quan trọng", "cốt yếu", "mang tính quyết định"],
    "significant": ["có ý nghĩa", "đáng kể"],
    "perspective": ["góc nhìn", "quan điểm"],
    "environment": ["môi trường"],
    "challenge": ["thách thức", "khó khăn"],
    "opportunity": ["cơ hội", "dịp may"],
    "consequence": ["hậu quả", "kết quả"],
}


def lookup_word_vietnamese(word: str, context_sentence: Optional[str] = None) -> Dict[str, Any]:
    """
    Tra cứu định nghĩa và gợi ý nghĩa tiếng Việt cho từ vựng và câu ngữ cảnh.
    Sử dụng dịch tự động kèm trích xuất danh sách các từ đồng nghĩa (synonyms).
    """
    clean_word = word.strip().lower()
    result = {
        "word": word,
        "primary_meaning": "",
        "suggestions": [],
        "sentence_translation": ""
    }

    if not clean_word:
        return result

    # 1. Tra cứu nghĩa từ vựng
    try:
        encoded_word = urllib.parse.quote(clean_word)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&dt=bd&dt=at&q={encoded_word}"
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        
        with urllib.request.urlopen(req, timeout=3.5) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            # Trích xuất nghĩa chính
            if data and data[0] and data[0][0] and data[0][0][0]:
                result["primary_meaning"] = data[0][0][0].strip()
                result["suggestions"].append(result["primary_meaning"])

            # Trích xuất các gợi ý thay thế / từ đồng nghĩa
            if len(data) > 5 and data[5]:
                try:
                    for group in data[5]:
                        if len(group) > 2 and group[2]:
                            for item in group[2]:
                                candidate = item[0].strip()
                                if candidate and candidate not in result["suggestions"]:
                                    result["suggestions"].append(candidate)
                except Exception as e:
                    logger.debug(f"Không thể parse danh sách từ đồng nghĩa: {e}")

    except Exception as e:
        logger.warning(f"Lỗi khi tra từ trực tuyến '{clean_word}': {e}. Đang dùng từ điển dự phòng.")
        if clean_word in OFFLINE_FALLBACK:
            fallback_list = OFFLINE_FALLBACK[clean_word]
            result["primary_meaning"] = fallback_list[0]
            result["suggestions"] = fallback_list

    # 2. Dịch cả câu ngữ cảnh (nếu có truyền vào)
    if context_sentence and context_sentence.strip():
        try:
            encoded_sentence = urllib.parse.quote(context_sentence.strip())
            sentence_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q={encoded_sentence}"
            req_sent = urllib.request.Request(
                sentence_url, 
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req_sent, timeout=3.5) as s_response:
                s_data = json.loads(s_response.read().decode("utf-8"))
                if s_data and s_data[0]:
                    full_translated = "".join([part[0] for part in s_data[0] if part and part[0]]).strip()
                    result["sentence_translation"] = full_translated
        except Exception as e:
            logger.debug(f"Không thể dịch câu ngữ cảnh: {e}")

    # Đảm bảo danh sách gợi ý tối đa 5 từ và không trùng lặp
    clean_suggestions = []
    for s in result["suggestions"]:
        s_lower = s.lower()
        if s and s_lower not in [x.lower() for x in clean_suggestions]:
            clean_suggestions.append(s)

    result["suggestions"] = clean_suggestions[:5]
    if not result["primary_meaning"] and clean_suggestions:
        result["primary_meaning"] = clean_suggestions[0]

    return result

