"""
Dịch vụ tự động sinh từ vựng IELTS Speaking Band 8.0+ bằng Google Gemini AI.
Tự động sinh từ vựng, phiên âm IPA, nghĩa tiếng Việt, câu hỏi Speaking và câu ngữ cảnh chuẩn.
Hỗ trợ lưu cấu hình API key và tích hợp cơ sở dữ liệu.
"""

import os
import json
import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from . import models, topics

logger = logging.getLogger("ai_vocab_service")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "ai_config.json")
ENV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")


def get_gemini_api_key() -> str:
    """Lấy Gemini API Key từ biến môi trường, file ai_config.json hoặc .env"""
    # 1. Biến môi trường
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key and key.strip():
        return key.strip()

    # 2. File ai_config.json
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                val = data.get("gemini_api_key", "").strip()
                if val:
                    return val
        except Exception as e:
            logger.warning(f"Không thể đọc {CONFIG_PATH}: {e}")

    # 3. File .env
    if os.path.exists(ENV_PATH):
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
                    if line.startswith("GOOGLE_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass

    return ""


def save_gemini_api_key(api_key: str) -> bool:
    """Lưu Gemini API Key vào ai_config.json để sử dụng lâu dài"""
    clean_key = (api_key or "").strip()
    
    # Tự động trích xuất mã API Key nếu người dùng vô tình dán lẫn văn bản hướng dẫn
    import re
    match = re.search(r'(AIzaSy[A-Za-z0-9_-]{33}|AQ\.[A-Za-z0-9_\-\.]{30,80})', clean_key)
    if match:
        clean_key = match.group(0)
    elif " " in clean_key or "\n" in clean_key or len(clean_key) < 20:
        raise ValueError("API Key không hợp lệ. Vui lòng vào aistudio.google.com/app/apikey và bấm nút 'Copy key' thực tế.")

    try:
        data = {}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        data["gemini_api_key"] = clean_key
        data["updated_at"] = datetime.utcnow().isoformat()

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.environ["GEMINI_API_KEY"] = clean_key
        return True
    except Exception as e:
        logger.error(f"Lỗi khi lưu API key: {e}")
        return False


def call_gemini_api(prompt: str, api_key: str) -> List[Dict[str, Any]]:
    """Gửi yêu cầu tới Gemini API với cấu hình JSON output"""
    # Sử dụng các model Gemini thế hệ mới nhất hỗ trợ v1beta generateContent
    models_to_try = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-pro"]
    last_error = None

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                result_json = resp.json()
                candidates = result_json.get("candidates", [])
                if candidates:
                    text_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    if text_content:
                        parsed = json.loads(text_content)
                        if isinstance(parsed, list):
                            return parsed
                        elif isinstance(parsed, dict) and "vocabularies" in parsed:
                            return parsed["vocabularies"]
            else:
                err_detail = resp.text
                logger.warning(f"Gemini model {model_name} trả về lỗi HTTP {resp.status_code}: {err_detail[:200]}")
                try:
                    err_json = resp.json().get("error", {})
                    msg = err_json.get("message", "")
                    if "api key not valid" in msg.lower():
                        raise RuntimeError(
                            "API Key không hợp lệ (HTTP 400). Bạn đã dán nhầm chữ hướng dẫn thay vì mã key thực tế. "
                            "Hãy vào aistudio.google.com/app/apikey, bấm nút 'Copy key' bên cạnh tên key và dán lại!"
                        )
                    if "free tier is not available" in msg.lower() or "billing" in msg.lower():
                        raise RuntimeError(
                            "API Key này thuộc Google Cloud Project chưa bật Free Tier (HTTP 403). "
                            "Khắc phục 100% miễn phí: Vào aistudio.google.com/apikey bằng Gmail cá nhân, "
                            "bấm 'Create API key' và chọn 'Create API key in new project' để tạo key Free!"
                        )
                    last_error = f"HTTP {resp.status_code}: {msg}" if msg else f"HTTP {resp.status_code}"
                except RuntimeError:
                    raise
                except Exception:
                    last_error = f"HTTP {resp.status_code}: {err_detail[:120]}"
        except RuntimeError:
            raise
        except Exception as e:
            logger.warning(f"Lỗi kết nối Gemini model {model_name}: {e}")
            last_error = str(e)

    raise RuntimeError(f"Không thể kết nối Gemini API ({last_error}). Vui lòng kiểm tra lại API Key hoặc mạng Internet.")


def generate_topic_vocabularies_with_ai(
    topic_id: int, 
    topic_title: str, 
    existing_words: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Dùng Gemini AI sinh 8 từ vựng học thuật & collocations Band 8.0+ cho chủ đề.
    Mỗi từ có phiên âm IPA, nghĩa tiếng Việt, câu hỏi Speaking và câu ngữ cảnh thực tế.
    """
    key = api_key or get_gemini_api_key()
    if not key:
        raise ValueError("Chưa cấu hình Google Gemini API Key. Vui lòng nhập API Key để tạo từ vựng tự động bằng AI.")

    existing_clause = ""
    if existing_words and len(existing_words) > 0:
        words_preview = ", ".join(f"'{w}'" for w in existing_words[:30])
        existing_clause = f"Do NOT duplicate any of these existing words: {words_preview}."

    prompt = f"""
You are an expert Cambridge IELTS Examiner & Senior Speaking Coach (Band 9.0).
Generate exactly 8 NEW, sophisticated, high-scoring vocabulary items, collocations, or idiomatic expressions for IELTS Speaking topic:
"{topic_title}" (Topic ID: {topic_id}).

{existing_clause}

Requirements:
1. Target Level: Band 8.0 - 9.0 (natural collocations, C1/C2 adjectives, phrasal verbs, idiomatic expressions that native speakers actually use in IELTS Speaking).
2. For EACH item, provide:
   - "word": The English word, phrase, collocation, or idiom (e.g. "lucrative", "climb the career ladder").
   - "phonetic": Accurate IPA phonetic transcription with stress marks (e.g. "/ˈluːkrətɪv/").
   - "part_of_speech": "adjective" | "noun" | "verb" | "idiom" | "collocation".
   - "meaning": Concise, accurate Vietnamese translation and explanation of how to use it naturally.
   - "context_sentence": An authentic, realistic Band 9 IELTS Speaking response sentence demonstrating exact context usage in an interview (Part 1, 2, or 3).
   - "speaking_question": A common IELTS Speaking question where this vocabulary item fits perfectly.
   - "collocations": An array of 2-3 common collocations or related phrases (in English).

Return ONLY a JSON array of 8 objects matching this exact structure:
[
  {{
    "word": "...",
    "phonetic": "...",
    "part_of_speech": "...",
    "meaning": "...",
    "context_sentence": "...",
    "speaking_question": "...",
    "collocations": ["...", "..."]
  }}
]
"""

    items = call_gemini_api(prompt, key)
    cleaned_items = []
    for raw in items:
        w = raw.get("word", "").strip()
        if not w:
            continue
        cleaned_items.append({
            "word": w,
            "phonetic": raw.get("phonetic", "").strip(),
            "part_of_speech": raw.get("part_of_speech", "collocation").strip(),
            "meaning": raw.get("meaning", "").strip(),
            "context_sentence": raw.get("context_sentence", "").strip(),
            "speaking_question": raw.get("speaking_question", "").strip(),
            "collocations": raw.get("collocations", []) if isinstance(raw.get("collocations"), list) else []
        })

    return cleaned_items


def get_topic_vocabularies(db: Session, topic_id: int) -> List[Dict[str, Any]]:
    """
    Lấy danh sách từ vựng của chủ đề được tạo tự động bởi AI từ Database.
    Nếu chưa có, trả về danh sách rỗng để người dùng bấm AI sinh từ vựng.
    """
    records = db.query(models.TopicVocabulary).filter(models.TopicVocabulary.topic_id == topic_id).all()
    results = []
    for r in records:
        colls = []
        if r.collocations_json:
            try:
                colls = json.loads(r.collocations_json)
            except Exception:
                colls = []
        results.append({
            "id": r.id,
            "word": r.word,
            "phonetic": r.phonetic or "",
            "part_of_speech": r.part_of_speech or "word",
            "meaning": r.meaning,
            "context_sentence": r.context_sentence,
            "speaking_question": r.speaking_question or "",
            "collocations": colls,
            "source": r.source or "ai"
        })
    return results


# Bí danh tương thích
get_or_seed_topic_vocabularies = get_topic_vocabularies


def add_ai_generated_vocabularies_to_db(
    db: Session, 
    topic_id: int, 
    new_items: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Lưu các từ vựng AI vừa sinh vào Database để sử dụng lâu dài"""
    saved_items = []
    for item in new_items:
        word_clean = item["word"].strip()
        # Kiểm tra xem từ này đã có trong chủ đề chưa
        existing = db.query(models.TopicVocabulary).filter(
            models.TopicVocabulary.topic_id == topic_id,
            models.TopicVocabulary.word == word_clean
        ).first()

        if existing:
            continue

        colls_str = json.dumps(item.get("collocations", []), ensure_ascii=False)
        tv = models.TopicVocabulary(
            topic_id=topic_id,
            word=word_clean,
            phonetic=item.get("phonetic", ""),
            part_of_speech=item.get("part_of_speech", "word"),
            meaning=item.get("meaning", ""),
            context_sentence=item.get("context_sentence", ""),
            speaking_question=item.get("speaking_question", ""),
            collocations_json=colls_str,
            source="ai"
        )
        db.add(tv)
        db.flush()
        saved_items.append({
            "id": tv.id,
            **item,
            "source": "ai"
        })

    db.commit()
    return saved_items

