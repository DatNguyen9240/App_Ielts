"""
Danh sách 16 Chủ đề IELTS Speaking & Vocabulary chuẩn.
Hỗ trợ đánh số, phân loại video và tìm kiếm liên quan theo từ khóa.
"""

IELTS_TOPICS = [
    {
        "id": 1,
        "title": "1. Work & Study (Công việc và Học tập)",
        "short_title": "Work & Study",
        "keywords": ["work", "study", "job", "career", "university", "college", "school", "colleague", "student", "teacher", "learn", "major", "profession", "boss", "office", "homework", "exam"]
    },
    {
        "id": 2,
        "title": "2. Accommodation & Hometown (Chỗ ở và Quê hương)",
        "short_title": "Accommodation & Hometown",
        "keywords": ["home", "house", "apartment", "flat", "hometown", "neighborhood", "city", "countryside", "village", "room", "living", "rent", "suburb"]
    },
    {
        "id": 3,
        "title": "3. Hobby, Free Time & Sports (Sở thích, thời gian rảnh và Thể thao)",
        "short_title": "Hobby & Sports",
        "keywords": ["hobby", "leisure", "free time", "sport", "game", "football", "swim", "play", "relax", "exercise", "weekend", "activity", "interest"]
    },
    {
        "id": 4,
        "title": "4. Travel & Holidays (Du lịch và Kỳ nghỉ)",
        "short_title": "Travel & Holidays",
        "keywords": ["travel", "holiday", "vacation", "trip", "tourist", "tourism", "destination", "hotel", "flight", "journey", "explore", "culture", "sightseeing"]
    },
    {
        "id": 5,
        "title": "5. Technology & Social Media (Công nghệ và Mạng xã hội)",
        "short_title": "Technology & Social Media",
        "keywords": ["technology", "computer", "phone", "smartphone", "social media", "internet", "app", "ai", "artificial intelligence", "online", "digital", "network", "device", "software"]
    },
    {
        "id": 6,
        "title": "6. Food & Cooking (Đồ ăn và Nấu nướng)",
        "short_title": "Food & Cooking",
        "keywords": ["food", "cook", "restaurant", "meal", "diet", "dish", "cuisine", "taste", "delicious", "healthy", "dinner", "breakfast", "lunch", "eating"]
    },
    {
        "id": 7,
        "title": "7. Shopping & Fashion (Mua sắm và Thời trang)",
        "short_title": "Shopping & Fashion",
        "keywords": ["shopping", "clothes", "fashion", "style", "store", "mall", "market", "buy", "purchase", "brand", "outfit", "wear", "discount", "price"]
    },
    {
        "id": 8,
        "title": "8. Health & Fitness (Sức khỏe và Thể hình)",
        "short_title": "Health & Fitness",
        "keywords": ["health", "fitness", "healthy", "exercise", "gym", "workout", "doctor", "hospital", "illness", "disease", "mental health", "diet", "lifestyle", "sleep"]
    },
    {
        "id": 9,
        "title": "9. Environment & Nature (Môi trường và Thiên nhiên)",
        "short_title": "Environment & Nature",
        "keywords": ["environment", "nature", "climate", "climate change", "pollution", "green", "sustainable", "wildlife", "animal", "plant", "forest", "planet", "carbon", "recycle"]
    },
    {
        "id": 10,
        "title": "10. Transport & Driving (Phương tiện đi lại)",
        "short_title": "Transport & Driving",
        "keywords": ["transport", "traffic", "car", "bus", "train", "drive", "driving", "bicycle", "bike", "vehicle", "metro", "subway", "commute", "road"]
    },
    {
        "id": 11,
        "title": "11. Media: Books, Music & Movies (Sách, Âm nhạc và Phim ảnh)",
        "short_title": "Media, Books & Music",
        "keywords": ["book", "music", "movie", "film", "song", "read", "reading", "cinema", "artist", "author", "watch", "entertainment", "actor", "genre"]
    },
    {
        "id": 12,
        "title": "12. People: Family, Friends & Role Models (Con người: Gia đình, bạn bè, người truyền cảm hứng)",
        "short_title": "People & Family",
        "keywords": ["family", "friend", "people", "parent", "mother", "father", "child", "children", "role model", "relationship", "personality", "admire", "mentor"]
    },
    {
        "id": 13,
        "title": "13. Events & Experiences (Sự kiện và Trải nghiệm đáng nhớ)",
        "short_title": "Events & Experiences",
        "keywords": ["event", "experience", "memory", "celebration", "ceremony", "party", "festival", "challenge", "milestone", "memorable", "special occasion"]
    },
    {
        "id": 14,
        "title": "14. Places & Buildings (Địa điểm và Công trình: Bảo tàng, công viên, cửa hàng...)",
        "short_title": "Places & Buildings",
        "keywords": ["place", "building", "museum", "park", "architecture", "library", "monument", "historic", "structure", "city center", "tower"]
    },
    {
        "id": 15,
        "title": "15. Objects & Possessions (Đồ vật: Món quà yêu thích, thiết bị điện tử, đồ dùng cũ...)",
        "short_title": "Objects & Possessions",
        "keywords": ["object", "item", "gift", "possession", "gadget", "equipment", "keepsake", "valuable", "tool", "belonging", "watch", "camera"]
    },
    {
        "id": 16,
        "title": "16. Society & Modern Life (Xã hội và Cuộc sống hiện đại)",
        "short_title": "Society & Modern Life",
        "keywords": ["society", "modern", "life", "community", "culture", "tradition", "globalization", "population", "issue", "government", "future", "development", "generation"]
    }
]

def auto_detect_topic(text: str) -> str:
    """Tự động phân tích từ khóa trong tiêu đề/nội dung để gợi ý chủ đề phù hợp nhất"""
    lowered = text.lower()
    best_topic = IELTS_TOPICS[0]["title"]
    max_score = 0

    for item in IELTS_TOPICS:
        score = sum(1 for kw in item["keywords"] if kw in lowered)
        if score > max_score:
            max_score = score
            best_topic = item["title"]

    return best_topic

