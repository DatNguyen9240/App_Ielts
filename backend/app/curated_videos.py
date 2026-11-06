import logging
from typing import List, Dict, Any

logger = logging.getLogger("curated_videos")

# Bộ sưu tập các video bài mẫu IELTS Speaking Band 8.0 - 9.0 chất lượng cao đã kiểm duyệt cho 16 chủ đề
TOPIC_DEFAULT_VIDEOS: Dict[int, List[Dict[str, Any]]] = {
    1: [
        {
            "id": "drEIArT9g2c",
            "title": "IELTS Speaking Part 1 | Cách Nói Về WORK AND STUDY trong IELTS Speaking",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=drEIArT9g2c",
            "thumbnail": "https://img.youtube.com/vi/drEIArT9g2c/mqdefault.jpg",
            "duration": 309
        },
        {
            "id": "ujWFCporuCU",
            "title": "IELTS Speaking Part 1 – Work and Study | Study Focus",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=ujWFCporuCU",
            "thumbnail": "https://img.youtube.com/vi/ujWFCporuCU/mqdefault.jpg",
            "duration": 688
        },
        {
            "id": "-88HUSOzs5Y",
            "title": "IELTS Speaking Part 1 – Work and Study | Work Focus",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=-88HUSOzs5Y",
            "thumbnail": "https://img.youtube.com/vi/-88HUSOzs5Y/mqdefault.jpg",
            "duration": 744
        },
    ],
    2: [
        {
            "id": "BmH722JfWVU",
            "title": "IELTS Speaking Topic - Home and Accommodation",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=BmH722JfWVU",
            "thumbnail": "https://img.youtube.com/vi/BmH722JfWVU/mqdefault.jpg",
            "duration": 1146
        },
        {
            "id": "rETE_GoIwXw",
            "title": "IELTS Speaking Part 1 SAMPLE ANSWERS | Hometown",
            "channel": "Fastrack IELTS",
            "url": "https://www.youtube.com/watch?v=rETE_GoIwXw",
            "thumbnail": "https://img.youtube.com/vi/rETE_GoIwXw/mqdefault.jpg",
            "duration": 752
        },
        {
            "id": "row-gEm1S80",
            "title": "How to Talk About Your Hometown in IELTS Speaking",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=row-gEm1S80",
            "thumbnail": "https://img.youtube.com/vi/row-gEm1S80/mqdefault.jpg",
            "duration": 1201
        },
    ],
    3: [
        {
            "id": "08gLWFYZQuc",
            "title": "IELTS Speaking Part 1: Habits - Hobbies, Free time, Sport, Reading | Sample Answers + Tips",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=08gLWFYZQuc",
            "thumbnail": "https://img.youtube.com/vi/08gLWFYZQuc/mqdefault.jpg",
            "duration": 584
        },
        {
            "id": "0fNJKMtupnU",
            "title": "IELTS Speaking Part 1 | Cách Nói Về Hobbies (Sở Thích) trong IELTS Speaking",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=0fNJKMtupnU",
            "thumbnail": "https://img.youtube.com/vi/0fNJKMtupnU/mqdefault.jpg",
            "duration": 314
        },
        {
            "id": "hoyhPZDp3dE",
            "title": "Nói về thời gian rảnh rỗi của bạn và sở thích bằng tiếng Anh",
            "channel": "Oxford Online English",
            "url": "https://www.youtube.com/watch?v=hoyhPZDp3dE",
            "thumbnail": "https://img.youtube.com/vi/hoyhPZDp3dE/mqdefault.jpg",
            "duration": 550
        },
    ],
    4: [
        {
            "id": "qy7BKkJz-1Y",
            "title": "IELTS English Podcast - Speaking Topic: Travel and Holidays",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=qy7BKkJz-1Y",
            "thumbnail": "https://img.youtube.com/vi/qy7BKkJz-1Y/mqdefault.jpg",
            "duration": 609
        },
        {
            "id": "Arq9QlXwta0",
            "title": "IELTS Speaking Vocabulary: HOLIDAYS",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=Arq9QlXwta0",
            "thumbnail": "https://img.youtube.com/vi/Arq9QlXwta0/mqdefault.jpg",
            "duration": 2152
        },
        {
            "id": "nRB2zrl4fPo",
            "title": "IELTS Speaking 🗣️ Part 1 | Travel and Holidays | Real Practice with Band 8 Sample",
            "channel": "Mr. English Guide",
            "url": "https://www.youtube.com/watch?v=nRB2zrl4fPo",
            "thumbnail": "https://img.youtube.com/vi/nRB2zrl4fPo/mqdefault.jpg",
            "duration": 217
        },
    ],
    5: [
        {
            "id": "ieFuu3afNCg",
            "title": "IELTS English Podcast - Speaking Topic: Social Media",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=ieFuu3afNCg",
            "thumbnail": "https://img.youtube.com/vi/ieFuu3afNCg/mqdefault.jpg",
            "duration": 745
        },
        {
            "id": "VBx-CatWQDw",
            "title": "IELTS Speaking Band 7: Technology | Sample Answers with Advanced Vocabulary",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=VBx-CatWQDw",
            "thumbnail": "https://img.youtube.com/vi/VBx-CatWQDw/mqdefault.jpg",
            "duration": 508
        },
        {
            "id": "LNvLVXVTOpc",
            "title": "IELTS English Podcast - Speaking Topic: Technology",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=LNvLVXVTOpc",
            "thumbnail": "https://img.youtube.com/vi/LNvLVXVTOpc/mqdefault.jpg",
            "duration": 626
        },
    ],
    6: [
        {
            "id": "UUs1Fp7-D-M",
            "title": "IELTS Speaking part 1: Food & Cooking | Band 7+ Sample Answers with Advanced Vocabulary",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=UUs1Fp7-D-M",
            "thumbnail": "https://img.youtube.com/vi/UUs1Fp7-D-M/mqdefault.jpg",
            "duration": 287
        },
        {
            "id": "uah_ReNfx5E",
            "title": "IELTS Speaking Part 2&3: Food and Cooking | Band 7+ Sample Answers with Advanced Vocabulary",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=uah_ReNfx5E",
            "thumbnail": "https://img.youtube.com/vi/uah_ReNfx5E/mqdefault.jpg",
            "duration": 420
        },
        {
            "id": "IvESDq8Aayc",
            "title": "IELTS Speaking Part 1 – Food",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=IvESDq8Aayc",
            "thumbnail": "https://img.youtube.com/vi/IvESDq8Aayc/mqdefault.jpg",
            "duration": 702
        },
    ],
    7: [
        {
            "id": "l99SKOUZ4n0",
            "title": "Free English Class! Topic: Shopping! 🏪🛒🛍️ (Lesson Only)",
            "channel": "Learn English with Bob the Canadian",
            "url": "https://www.youtube.com/watch?v=l99SKOUZ4n0",
            "thumbnail": "https://img.youtube.com/vi/l99SKOUZ4n0/mqdefault.jpg",
            "duration": 1599
        },
        {
            "id": "lUbkq5chA2M",
            "title": "IELTS English Podcast - Speaking Topic: Shopping",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=lUbkq5chA2M",
            "thumbnail": "https://img.youtube.com/vi/lUbkq5chA2M/mqdefault.jpg",
            "duration": 650
        },
        {
            "id": "BVy6dbgCCM0",
            "title": "IELTS Speaking: Fashion & Clothing 👕 | Describe Your Style Naturally with Emma & Ben",
            "channel": "Easy learn English ",
            "url": "https://www.youtube.com/watch?v=BVy6dbgCCM0",
            "thumbnail": "https://img.youtube.com/vi/BVy6dbgCCM0/mqdefault.jpg",
            "duration": 496
        },
    ],
    8: [
        {
            "id": "9kQHy8kjCn4",
            "title": "IELTS Speaking Practice 2025: Health & Fitness 💪 | Band 9 Answers, Vocabulary & Natural Phrases",
            "channel": "Easy learn English ",
            "url": "https://www.youtube.com/watch?v=9kQHy8kjCn4",
            "thumbnail": "https://img.youtube.com/vi/9kQHy8kjCn4/mqdefault.jpg",
            "duration": 597
        },
        {
            "id": "EH140c_2nF8",
            "title": "Hướng dẫn trả lời Topic Health - IELTS Speaking Part 1",
            "channel": "ZIM Academy",
            "url": "https://www.youtube.com/watch?v=EH140c_2nF8",
            "thumbnail": "https://img.youtube.com/vi/EH140c_2nF8/mqdefault.jpg",
            "duration": 349
        },
        {
            "id": "eT74Md1tA90",
            "title": "TALKING ABOUT THE TOPIC \"HEALTH\" | Super Good IELTS Speaking Tips | 5 Minutes about IELTS",
            "channel": "andy ở canada",
            "url": "https://www.youtube.com/watch?v=eT74Md1tA90",
            "thumbnail": "https://img.youtube.com/vi/eT74Md1tA90/mqdefault.jpg",
            "duration": 434
        },
    ],
    9: [
        {
            "id": "0vB7lrTQKJ8",
            "title": "IELTS English Podcast - Speaking Topic: Environment",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=0vB7lrTQKJ8",
            "thumbnail": "https://img.youtube.com/vi/0vB7lrTQKJ8/mqdefault.jpg",
            "duration": 682
        },
        {
            "id": "3qeV5IdsWxg",
            "title": "IELTS Speaking Band 7: Environment & Climate | Sample Answers with Advanced Vocabulary",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=3qeV5IdsWxg",
            "thumbnail": "https://img.youtube.com/vi/3qeV5IdsWxg/mqdefault.jpg",
            "duration": 603
        },
        {
            "id": "i4OkQROglnE",
            "title": "IELTS Speaking Practice 2025: Environment & Conservation 🌿 | Band 9 Sample Answers + Vocabulary",
            "channel": "Easy learn English ",
            "url": "https://www.youtube.com/watch?v=i4OkQROglnE",
            "thumbnail": "https://img.youtube.com/vi/i4OkQROglnE/mqdefault.jpg",
            "duration": 663
        },
    ],
    10: [
        {
            "id": "YL_xB7v-97M",
            "title": "IELTS English Podcast - Speaking Topic: Transportation",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=YL_xB7v-97M",
            "thumbnail": "https://img.youtube.com/vi/YL_xB7v-97M/mqdefault.jpg",
            "duration": 654
        },
        {
            "id": "NSEcVOOny0o",
            "title": "IELTS Speaking Free Lesson: Topic TRANSPORTATION",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=NSEcVOOny0o",
            "thumbnail": "https://img.youtube.com/vi/NSEcVOOny0o/mqdefault.jpg",
            "duration": 5841
        },
        {
            "id": "5WGDTOm3xRk",
            "title": "How to Talk About Transport and Driving in English - Spoken English Lesson",
            "channel": "Oxford Online English",
            "url": "https://www.youtube.com/watch?v=5WGDTOm3xRk",
            "thumbnail": "https://img.youtube.com/vi/5WGDTOm3xRk/mqdefault.jpg",
            "duration": 1090
        },
    ],
    11: [
        {
            "id": "B6uoH5GD_x4",
            "title": "IELTS Speaking: Books & TV 📚🎬 | Talk About Reading & Watching Naturally with Emma & Ben",
            "channel": "Easy learn English ",
            "url": "https://www.youtube.com/watch?v=B6uoH5GD_x4",
            "thumbnail": "https://img.youtube.com/vi/B6uoH5GD_x4/mqdefault.jpg",
            "duration": 530
        },
        {
            "id": "k4715CJ0Ii8",
            "title": "IELTS Speaking Test- Perfect Band 9 [+ Free Speaking PDF]",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=k4715CJ0Ii8",
            "thumbnail": "https://img.youtube.com/vi/k4715CJ0Ii8/mqdefault.jpg",
            "duration": 1045
        },
        {
            "id": "GyGSfjNPGP0",
            "title": "IELTS Speaking Practice – Topic: Books | Band 9 Sample Answers & Vocabulary",
            "channel": "English Speakology",
            "url": "https://www.youtube.com/watch?v=GyGSfjNPGP0",
            "thumbnail": "https://img.youtube.com/vi/GyGSfjNPGP0/mqdefault.jpg",
            "duration": 630
        },
    ],
    12: [
        {
            "id": "7DQidAxMPWQ",
            "title": "IELTS Speaking Part 1– Family",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=7DQidAxMPWQ",
            "thumbnail": "https://img.youtube.com/vi/7DQidAxMPWQ/mqdefault.jpg",
            "duration": 651
        },
        {
            "id": "ns0Y70C-jbg",
            "title": "30 Phrases to Talk about your Family",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=ns0Y70C-jbg",
            "thumbnail": "https://img.youtube.com/vi/ns0Y70C-jbg/mqdefault.jpg",
            "duration": 1562
        },
        {
            "id": "MxNP-i4sQP8",
            "title": "IELTS Speaking Part 1  | FAMILY | Sample answers and vocabulary",
            "channel": "Fastrack IELTS",
            "url": "https://www.youtube.com/watch?v=MxNP-i4sQP8",
            "thumbnail": "https://img.youtube.com/vi/MxNP-i4sQP8/mqdefault.jpg",
            "duration": 492
        },
    ],
    13: [
        {
            "id": "YODIiPkVKAc",
            "title": "IELTS Speaking Band 7+ Practice Test | IELTS with Charles",
            "channel": "IELTS with Charles",
            "url": "https://www.youtube.com/watch?v=YODIiPkVKAc",
            "thumbnail": "https://img.youtube.com/vi/YODIiPkVKAc/mqdefault.jpg",
            "duration": 783
        },
        {
            "id": "PbkZeCyQNNo",
            "title": "IELTS Speaking: Describe an Important Event in Your Life | Band 9 Sample Answers & Vocabulary",
            "channel": "Easy learn English ",
            "url": "https://www.youtube.com/watch?v=PbkZeCyQNNo",
            "thumbnail": "https://img.youtube.com/vi/PbkZeCyQNNo/mqdefault.jpg",
            "duration": 569
        },
        {
            "id": "RuvVc3Mdgvg",
            "title": "IELTS Speaking Tips You MUST Know Before Your Test",
            "channel": "IELTS Advantage",
            "url": "https://www.youtube.com/watch?v=RuvVc3Mdgvg",
            "thumbnail": "https://img.youtube.com/vi/RuvVc3Mdgvg/mqdefault.jpg",
            "duration": 684
        },
    ],
    14: [
        {
            "id": "x9aCR1oDJs4",
            "title": "IELTS Speaking Part 2: Band 9 TEMPLATES - #3 PLACES",
            "channel": "English Speaking Success",
            "url": "https://www.youtube.com/watch?v=x9aCR1oDJs4",
            "thumbnail": "https://img.youtube.com/vi/x9aCR1oDJs4/mqdefault.jpg",
            "duration": 927
        },
        {
            "id": "wZ_c6SLbv6A",
            "title": "IELTS English Podcast - Speaking Topic: Buildings",
            "channel": "IELTS Plus",
            "url": "https://www.youtube.com/watch?v=wZ_c6SLbv6A",
            "thumbnail": "https://img.youtube.com/vi/wZ_c6SLbv6A/mqdefault.jpg",
            "duration": 629
        },
        {
            "id": "c7xHisq5DqU",
            "title": "IELTS Speaking Part 3  – Tall Buildings and Urban Development",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=c7xHisq5DqU",
            "thumbnail": "https://img.youtube.com/vi/c7xHisq5DqU/mqdefault.jpg",
            "duration": 653
        },
    ],
    15: [
        {
            "id": "2yNOmp-WTlE",
            "title": "IELTS Speaking Part 1 - Hướng dẫn chủ đề: Keeping old things | Smartcom English",
            "channel": "Smartcom English",
            "url": "https://www.youtube.com/watch?v=2yNOmp-WTlE",
            "thumbnail": "https://img.youtube.com/vi/2yNOmp-WTlE/mqdefault.jpg",
            "duration": 119
        },
        {
            "id": "yLEQvpvG0Is",
            "title": "Easy English _ IELTS speaking part 1: Collecting things _ with mindmap and vocabulary quiz",
            "channel": "Easy English",
            "url": "https://www.youtube.com/watch?v=yLEQvpvG0Is",
            "thumbnail": "https://img.youtube.com/vi/yLEQvpvG0Is/mqdefault.jpg",
            "duration": 174
        },
        {
            "id": "Ih1X8kolVwA",
            "title": "IELTS Speaking Part 1 – Collecting things",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=Ih1X8kolVwA",
            "thumbnail": "https://img.youtube.com/vi/Ih1X8kolVwA/mqdefault.jpg",
            "duration": 652
        },
    ],
    16: [
        {
            "id": "-Q6PuAVEEKo",
            "title": "IELTS Speaking: Technology and Modern Life",
            "channel": "Bright Sun",
            "url": "https://www.youtube.com/watch?v=-Q6PuAVEEKo",
            "thumbnail": "https://img.youtube.com/vi/-Q6PuAVEEKo/mqdefault.jpg",
            "duration": 236
        },
        {
            "id": "HLdC8njalLE",
            "title": "Work-Life Balance in Modern Life | IELTS Speaking & Real-Life English",
            "channel": "English Talks Podcast",
            "url": "https://www.youtube.com/watch?v=HLdC8njalLE",
            "thumbnail": "https://img.youtube.com/vi/HLdC8njalLE/mqdefault.jpg",
            "duration": 302
        },
        {
            "id": "F0vmwkdYLOA",
            "title": "IELTS Speaking Part 3 – The Impact of Technology on Society",
            "channel": "Tracy Wang",
            "url": "https://www.youtube.com/watch?v=F0vmwkdYLOA",
            "thumbnail": "https://img.youtube.com/vi/F0vmwkdYLOA/mqdefault.jpg",
            "duration": 796
        },
    ],
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
                        "thumbnail": entry.get("thumbnail") or f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg",
                        "duration": duration
                    })

            if items:
                _SEARCH_CACHE[cache_key] = items
                return items
    except Exception as e:
        logger.warning(f"Lỗi tìm kiếm YouTube online: {e}")

    return []
