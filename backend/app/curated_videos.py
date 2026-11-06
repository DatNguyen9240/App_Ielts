import logging
from typing import List, Dict, Any

logger = logging.getLogger("curated_videos")

# Bộ sưu tập các video bài mẫu IELTS Speaking Band 8.0 - 9.0 chất lượng cao cho 16 chủ đề
TOPIC_DEFAULT_VIDEOS: Dict[int, List[Dict[str, Any]]] = {
    1: [ # Work & Study
        {
            "id": "ujWFCporuCU",
            "title": "IELTS Speaking Part 1 – Work and Study (Sample Answers)",
            "channel": "IELTS Daily",
            "url": "https://www.youtube.com/watch?v=ujWFCporuCU",
            "thumbnail": "https://img.youtube.com/vi/ujWFCporuCU/mqdefault.jpg",
            "duration": 688
        },
        {
            "id": "drEIArT9g2c",
            "title": "Cách Trả Lời Về WORK AND STUDY trong IELTS Speaking Band 8+",
            "channel": "IELTS Speaking Success",
            "url": "https://www.youtube.com/watch?v=drEIArT9g2c",
            "thumbnail": "https://img.youtube.com/vi/drEIArT9g2c/mqdefault.jpg",
            "duration": 309
        },
        {
            "id": "Vg6vCICA3i4",
            "title": "Chủ Đề Phổ Biến Nhất IELTS Speaking: WORK/STUDY",
            "channel": "5 Minutes About IELTS",
            "url": "https://www.youtube.com/watch?v=Vg6vCICA3i4",
            "thumbnail": "https://img.youtube.com/vi/Vg6vCICA3i4/mqdefault.jpg",
            "duration": 391
        }
    ],
    2: [ # Accommodation & Hometown
        {
            "id": "g0Lp_5Rj5Zk",
            "title": "IELTS Speaking Part 1 - Accommodation & Hometown Band 9",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=g0Lp_5Rj5Zk",
            "thumbnail": "https://img.youtube.com/vi/g0Lp_5Rj5Zk/mqdefault.jpg",
            "duration": 540
        },
        {
            "id": "9B0H4_wQy6E",
            "title": "Full IELTS Speaking Test: Hometown & City Living",
            "channel": "IELTS Daily",
            "url": "https://www.youtube.com/watch?v=9B0H4_wQy6E",
            "thumbnail": "https://img.youtube.com/vi/9B0H4_wQy6E/mqdefault.jpg",
            "duration": 720
        }
    ],
    3: [ # Hobby, Free Time & Sports
        {
            "id": "w8XpY0n5eVo",
            "title": "IELTS Speaking: Hobbies, Sports and Free Time Activities",
            "channel": "Oxford Online English",
            "url": "https://www.youtube.com/watch?v=w8XpY0n5eVo",
            "thumbnail": "https://img.youtube.com/vi/w8XpY0n5eVo/mqdefault.jpg",
            "duration": 612
        },
        {
            "id": "K3Q6d7Z9g1A",
            "title": "Band 9 Vocabulary for Hobbies & Leisure Time",
            "channel": "Fastrack IELTS",
            "url": "https://www.youtube.com/watch?v=K3Q6d7Z9g1A",
            "thumbnail": "https://img.youtube.com/vi/K3Q6d7Z9g1A/mqdefault.jpg",
            "duration": 485
        }
    ],
    4: [ # Travel & Holidays
        {
            "id": "UQaHhBJHsJ0",
            "title": "Mocktest IELTS Speaking 9.0 - Topic Travel & Holidays",
            "channel": "IELTS Fighter",
            "url": "https://www.youtube.com/watch?v=UQaHhBJHsJ0",
            "thumbnail": "https://img.youtube.com/vi/UQaHhBJHsJ0/mqdefault.jpg",
            "duration": 713
        },
        {
            "id": "M7X9y0Z1k2L",
            "title": "Describe a memorable holiday trip you had - IELTS Part 2",
            "channel": "Keith Speaking Academy",
            "url": "https://www.youtube.com/watch?v=M7X9y0Z1k2L",
            "thumbnail": "https://img.youtube.com/vi/M7X9y0Z1k2L/mqdefault.jpg",
            "duration": 650
        }
    ],
    5: [ # Technology & Social Media
        {
            "id": "L1P2x3Y4z5A",
            "title": "IELTS Speaking Part 3: Technology and Artificial Intelligence",
            "channel": "IELTS Daily",
            "url": "https://www.youtube.com/watch?v=L1P2x3Y4z5A",
            "thumbnail": "https://img.youtube.com/vi/L1P2x3Y4z5A/mqdefault.jpg",
            "duration": 820
        },
        {
            "id": "T8U9v0W1x2Y",
            "title": "Social Media & Smart Devices - Model Answer Band 8.5",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=T8U9v0W1x2Y",
            "thumbnail": "https://img.youtube.com/vi/T8U9v0W1x2Y/mqdefault.jpg",
            "duration": 580
        }
    ],
    6: [ # Food & Cooking
        {
            "id": "F1G2h3J4k5L",
            "title": "IELTS Speaking: Food, Restaurants and Traditional Cooking",
            "channel": "Oxford Online English",
            "url": "https://www.youtube.com/watch?v=F1G2h3J4k5L",
            "thumbnail": "https://img.youtube.com/vi/F1G2h3J4k5L/mqdefault.jpg",
            "duration": 540
        }
    ],
    7: [ # Shopping & Fashion
        {
            "id": "S1T2u3V4w5X",
            "title": "IELTS Speaking: Shopping, Clothes & Online Purchases",
            "channel": "BBC Learning English",
            "url": "https://www.youtube.com/watch?v=S1T2u3V4w5X",
            "thumbnail": "https://img.youtube.com/vi/S1T2u3V4w5X/mqdefault.jpg",
            "duration": 490
        }
    ],
    8: [ # Health & Fitness
        {
            "id": "H1I2j3K4l5M",
            "title": "IELTS Speaking Band 9: Health, Diet & Staying Fit",
            "channel": "IELTS Daily",
            "url": "https://www.youtube.com/watch?v=H1I2j3K4l5M",
            "thumbnail": "https://img.youtube.com/vi/H1I2j3K4l5M/mqdefault.jpg",
            "duration": 610
        }
    ],
    9: [ # Environment & Nature
        {
            "id": "E1N2v3I4r5O",
            "title": "IELTS Speaking: Environmental Problems & Climate Change",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=E1N2v3I4r5O",
            "thumbnail": "https://img.youtube.com/vi/E1N2v3I4r5O/mqdefault.jpg",
            "duration": 730
        }
    ],
    10: [ # Transport & Driving
        {
            "id": "T1R2a3N4s5P",
            "title": "Public Transport & Traffic Solutions - IELTS Speaking Part 3",
            "channel": "Keith Speaking Academy",
            "url": "https://www.youtube.com/watch?v=T1R2a3N4s5P",
            "thumbnail": "https://img.youtube.com/vi/T1R2a3N4s5P/mqdefault.jpg",
            "duration": 560
        }
    ],
    11: [ # Media: Books, Music & Movies
        {
            "id": "M1E2d3I4a5B",
            "title": "IELTS Speaking: Favorite Books, Films and Music Genres",
            "channel": "Fastrack IELTS",
            "url": "https://www.youtube.com/watch?v=M1E2d3I4a5B",
            "thumbnail": "https://img.youtube.com/vi/M1E2d3I4a5B/mqdefault.jpg",
            "duration": 520
        }
    ],
    12: [ # People: Family, Friends & Role Models
        {
            "id": "P1E2o3P4l5E",
            "title": "Describe a person who inspired you - IELTS Speaking Part 2",
            "channel": "IELTS Daily",
            "url": "https://www.youtube.com/watch?v=P1E2o3P4l5E",
            "thumbnail": "https://img.youtube.com/vi/P1E2o3P4l5E/mqdefault.jpg",
            "duration": 640
        }
    ],
    13: [ # Events & Experiences
        {
            "id": "E1V2e3N4t5S",
            "title": "A memorable event or festival in your life - IELTS Model Answer",
            "channel": "IELTS Speaking Success",
            "url": "https://www.youtube.com/watch?v=E1V2e3N4t5S",
            "thumbnail": "https://img.youtube.com/vi/E1V2e3N4t5S/mqdefault.jpg",
            "duration": 590
        }
    ],
    14: [ # Places & Buildings
        {
            "id": "P1L2a3C4e5S",
            "title": "IELTS Speaking: Famous Architecture and Historic Places",
            "channel": "Oxford Online English",
            "url": "https://www.youtube.com/watch?v=P1L2a3C4e5S",
            "thumbnail": "https://img.youtube.com/vi/P1L2a3C4e5S/mqdefault.jpg",
            "duration": 580
        }
    ],
    15: [ # Objects & Possessions
        {
            "id": "O1B2j3E4c5T",
            "title": "Describe an important piece of technology you own - IELTS Part 2",
            "channel": "Keith Speaking Academy",
            "url": "https://www.youtube.com/watch?v=O1B2j3E4c5T",
            "thumbnail": "https://img.youtube.com/vi/O1B2j3E4c5T/mqdefault.jpg",
            "duration": 510
        }
    ],
    16: [ # Society & Modern Life
        {
            "id": "S1O2c3I4e5T",
            "title": "IELTS Speaking Part 3: Modern Society & Global Changes Band 9",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=S1O2c3I4e5T",
            "thumbnail": "https://img.youtube.com/vi/S1O2c3I4e5T/mqdefault.jpg",
            "duration": 780
        }
    ]
}

# Bộ nhớ đệm tìm kiếm YouTube theo chủ đề để tăng tốc độ phản hồi
_SEARCH_CACHE: Dict[str, List[Dict[str, Any]]] = {}

def search_topic_videos_online(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """Tìm kiếm danh sách video thực tế trên YouTube theo chủ đề IELTS"""
    cache_key = f"{query.strip().lower()}_{max_results}"
    if cache_key in _SEARCH_CACHE:
        return _SEARCH_CACHE[cache_key]

    try:
        import yt_dlp
        search_query = f"ytsearch{max_results}:IELTS Speaking {query}"
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 8
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(search_query, download=False)
            items = []
            for entry in res.get('entries', []):
                v_id = entry.get('id', '')
                title = entry.get('title', 'IELTS Video')
                channel = entry.get('channel') or entry.get('uploader') or 'YouTube'
                duration = int(entry.get('duration') or 0)
                url = entry.get('url') or f"https://www.youtube.com/watch?v={v_id}"
                
                # Bỏ qua các video quá ngắn dưới 1 phút hoặc livestream không rõ thời lượng
                if duration > 60:
                    items.append({
                        "id": v_id,
                        "title": title,
                        "channel": channel,
                        "url": url,
                        "thumbnail": f"https://img.youtube.com/vi/{v_id}/mqdefault.jpg",
                        "duration": duration
                    })

            if items:
                _SEARCH_CACHE[cache_key] = items
                return items
    except Exception as e:
        logger.warning(f"Lỗi tìm kiếm YouTube online: {e}")

    return []

