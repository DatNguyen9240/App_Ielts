"""
Dữ liệu bộ từ vựng IELTS Speaking Band 7.5 - 9.0 cho 16 chủ đề chuẩn.
Mỗi từ vựng được xây dựng với phát âm IPA, loại từ, giải nghĩa tiếng Việt,
câu hỏi Speaking gợi ý và ĐẶC BIỆT là CÂU NGỮ CẢNH THỰC TẾ (Context Sentence) tự nhiên.
"""

from typing import List, Dict, Any, Optional

TOPIC_VOCABULARIES: Dict[int, List[Dict[str, Any]]] = {
    # ==================== CHỦ ĐỀ 1: WORK & STUDY ====================
    1: [
        {
            "word": "lucrative",
            "phonetic": "/ˈluːkrətɪv/",
            "part_of_speech": "adjective",
            "meaning": "Mang lại nhiều lợi nhuận, thu nhập rất cao",
            "context_sentence": "Many university graduates aspire to land a lucrative job in the fintech sector to achieve financial independence early.",
            "speaking_question": "What kind of job do you want to do in the future?",
            "collocations": ["lucrative job", "lucrative career", "lucrative market"]
        },
        {
            "word": "heavy workload",
            "phonetic": "/ˈhevi ˈwɜːkləʊd/",
            "part_of_speech": "collocation",
            "meaning": "Khối lượng công việc nặng nề, áp lực lớn",
            "context_sentence": "Despite the heavy workload and tight deadlines, I find my current position deeply rewarding because I learn something new every day.",
            "speaking_question": "Do you find your study or work stressful?",
            "collocations": ["cope with a heavy workload", "struggle with a heavy workload"]
        },
        {
            "word": "climb the career ladder",
            "phonetic": "/klaɪm ðə kəˈrɪə ˈlædə/",
            "part_of_speech": "idiom",
            "meaning": "Thăng tiến từng bước trên con đường sự nghiệp",
            "context_sentence": "She has been working tirelessly for the past five years to climb the career ladder and secure a senior managerial position.",
            "speaking_question": "Do you plan to stay in your current job for a long time?",
            "collocations": ["ambition to climb the career ladder"]
        },
        {
            "word": "hands-on experience",
            "phonetic": "/hændz ɒn ɪkˈspɪəriəns/",
            "part_of_speech": "collocation",
            "meaning": "Kinh nghiệm thực hành, trải nghiệm thực tế",
            "context_sentence": "My university emphasizes practical internships, which gave me invaluable hands-on experience before entering the competitive job market.",
            "speaking_question": "What is the most useful thing you learned from your university?",
            "collocations": ["gain hands-on experience", "invaluable hands-on experience"]
        },
        {
            "word": "burn the midnight oil",
            "phonetic": "/bɜːn ðə ˈmɪdnaɪt ɔɪl/",
            "part_of_speech": "idiom",
            "meaning": "Thức khuya miệt mài học tập hoặc làm việc",
            "context_sentence": "During the final exam period, my classmates and I frequently burned the midnight oil at the university library.",
            "speaking_question": "Do you prefer to study in the morning or at night?",
            "collocations": ["have to burn the midnight oil"]
        },
        {
            "word": "hectic schedule",
            "phonetic": "/ˈhektɪk ˈʃedjuːl/",
            "part_of_speech": "collocation",
            "meaning": "Lịch trình dày đặc, vô cùng bận rộn",
            "context_sentence": "Balancing a hectic study schedule with extracurricular activities taught me how to manage my time effectively.",
            "speaking_question": "How do you organize your study routine?",
            "collocations": ["a hectic daily schedule", "juggle a hectic schedule"]
        },
        {
            "word": "career prospects",
            "phonetic": "/kəˈrɪə ˈprɒspekts/",
            "part_of_speech": "collocation",
            "meaning": "Triển vọng và cơ hội phát triển nghề nghiệp",
            "context_sentence": "I decided to major in Artificial Intelligence because the career prospects in this sector are exceptionally promising.",
            "speaking_question": "Why did you choose your current major?",
            "collocations": ["promising career prospects", "bright career prospects"]
        },
        {
            "word": "job satisfaction",
            "phonetic": "/dʒɒb ˌsætɪsˈfækʃn/",
            "part_of_speech": "collocation",
            "meaning": "Sự thỏa mãn và hài lòng trong công việc",
            "context_sentence": "For me, personal job satisfaction is far more essential than just earning a high salary in an uninspiring environment.",
            "speaking_question": "What is more important to you: salary or passion?",
            "collocations": ["derive great job satisfaction", "high job satisfaction"]
        }
    ],

    # ==================== CHỦ ĐỀ 2: ACCOMMODATION & HOMETOWN ====================
    2: [
        {
            "word": "quaint",
            "phonetic": "/kweɪnt/",
            "part_of_speech": "adjective",
            "meaning": "Cổ kính, duyên dáng và thanh bình",
            "context_sentence": "My hometown is a quaint coastal town surrounded by lush mountains, where life moves at a peaceful pace.",
            "speaking_question": "Can you describe your hometown?",
            "collocations": ["quaint village", "quaint little town", "quaint streets"]
        },
        {
            "word": "hustle and bustle",
            "phonetic": "/ˈhʌsl ænd ˈbʌsl/",
            "part_of_speech": "idiom",
            "meaning": "Sự nhộn nhịp, hối hả của đô thị",
            "context_sentence": "Although I enjoy the hustle and bustle of city life, I often return to my hometown on weekends to recharge my batteries.",
            "speaking_question": "Do you prefer living in a city or the countryside?",
            "collocations": ["get away from the hustle and bustle"]
        },
        {
            "word": "amenities",
            "phonetic": "/əˈmiːnətiz/",
            "part_of_speech": "noun (plural)",
            "meaning": "Các tiện ích sinh hoạt (công viên, siêu thị, trường học...)",
            "context_sentence": "My apartment is situated in a vibrant neighborhood with convenient access to modern amenities like supermarkets and fitness centers.",
            "speaking_question": "What do you like about your current living area?",
            "collocations": ["modern amenities", "local amenities", "basic amenities"]
        },
        {
            "word": "cosy",
            "phonetic": "/ˈkəʊzi/",
            "part_of_speech": "adjective",
            "meaning": "Ấm cúng, thoải mái, dễ chịu",
            "context_sentence": "Even though my studio apartment is relatively small, I decorated it with warm lights and indoor plants to create a cosy atmosphere.",
            "speaking_question": "What does your room look like?",
            "collocations": ["cosy atmosphere", "cosy room", "feel cosy and relaxed"]
        },
        {
            "word": "sprawling metropolis",
            "phonetic": "/ˈsprɔːlɪŋ məˈtrɒpəlɪs/",
            "part_of_speech": "collocation",
            "meaning": "Đại đô thị rộng lớn, phát triển sầm uất",
            "context_sentence": "Hanoi is a sprawling metropolis where centuries-old historical pagodas stand side by side with modern skyscrapers.",
            "speaking_question": "Has your hometown changed a lot recently?",
            "collocations": ["transform into a sprawling metropolis"]
        },
        {
            "word": "sense of community",
            "phonetic": "/sens əv kəˈmjuːnəti/",
            "part_of_speech": "collocation",
            "meaning": "Tinh thần gắn kết tình làng nghĩa xóm",
            "context_sentence": "What I cherish most about my neighborhood is the strong sense of community, where neighbors always look out for one another.",
            "speaking_question": "How well do you get along with your neighbors?",
            "collocations": ["strong sense of community", "foster a sense of community"]
        },
        {
            "word": "within walking distance",
            "phonetic": "/wɪðˈɪn ˈwɔːkɪŋ ˈdɪstəns/",
            "part_of_speech": "idiom",
            "meaning": "Ở rất gần, chỉ cách vài bước chân đi bộ",
            "context_sentence": "One huge perk of my current accommodation is that the metro station and grocery stores are within walking distance.",
            "speaking_question": "Is public transport convenient where you live?",
            "collocations": ["located within walking distance of"]
        },
        {
            "word": "peace and tranquility",
            "phonetic": "/piːs ænd træŋˈkwɪləti/",
            "part_of_speech": "collocation",
            "meaning": "Sự thanh bình và tĩnh lặng tuyệt đối",
            "context_sentence": "Whenever I feel overwhelmed by urban noise, I visit my grandparents' countryside cottage to enjoy the peace and tranquility.",
            "speaking_question": "Where do you go when you want to relax?",
            "collocations": ["soak up the peace and tranquility"]
        }
    ],

    # ==================== CHỦ ĐỀ 3: HOBBY, FREE TIME & SPORTS ====================
    3: [
        {
            "word": "unwind",
            "phonetic": "/ʌnˈwaɪnd/",
            "part_of_speech": "verb",
            "meaning": "Thư giãn, xả hơi sau những giờ làm việc căng thẳng",
            "context_sentence": "Listening to acoustic melodies or strumming my guitar is my favorite way to unwind after an exhausting day at work.",
            "speaking_question": "What do you usually do in your free time?",
            "collocations": ["unwind after work", "unwind with music", "a great way to unwind"]
        },
        {
            "word": "sedentary lifestyle",
            "phonetic": "/ˈsedntri ˈlaɪfstaɪl/",
            "part_of_speech": "collocation",
            "meaning": "Lối sống ít vận động, ngồi nhiều một chỗ",
            "context_sentence": "Playing badminton with friends on weekends helps office workers combat the detrimental effects of a sedentary lifestyle.",
            "speaking_question": "Why is playing sports important nowadays?",
            "collocations": ["lead a sedentary lifestyle", "counteract a sedentary lifestyle"]
        },
        {
            "word": "blow off steam",
            "phonetic": "/bləʊ ɒf stiːm/",
            "part_of_speech": "idiom",
            "meaning": "Giải tỏa ức chế, xả hết bực dọc hoặc áp lực",
            "context_sentence": "Hitting the gym three times a week is not just for physical fitness; it is also a fantastic outlet for me to blow off steam.",
            "speaking_question": "What do you do when you feel stressed?",
            "collocations": ["need to blow off steam", "an effective way to blow off steam"]
        },
        {
            "word": "avid reader",
            "phonetic": "/ˈævɪd ˈriːdə/",
            "part_of_speech": "collocation",
            "meaning": "Người đam mê đọc sách",
            "context_sentence": "I consider myself an avid reader because diving into a thought-provoking novel allows me to broaden my horizon effortlessly.",
            "speaking_question": "Do you enjoy reading books?",
            "collocations": ["be an avid reader of fiction"]
        },
        {
            "word": "recharge one's batteries",
            "phonetic": "/riːˈtʃɑːdʒ wʌnz ˈbætəriz/",
            "part_of_speech": "idiom",
            "meaning": "Nạp lại năng lượng tinh thần và thể chất",
            "context_sentence": "Spending a quiet Sunday morning hiking in nature allows me to fully recharge my batteries for the demanding week ahead.",
            "speaking_question": "How do you spend your typical Sunday?",
            "collocations": ["take time to recharge your batteries"]
        },
        {
            "word": "keep in shape",
            "phonetic": "/kiːp ɪn ʃeɪp/",
            "part_of_speech": "idiom",
            "meaning": "Giữ gìn vóc dáng thon gọn và thể lực khỏe mạnh",
            "context_sentence": "I took up swimming last summer because it provides a full-body workout that helps me keep in shape without stressing my joints.",
            "speaking_question": "What sports do you play to stay healthy?",
            "collocations": ["exercise regularly to keep in shape"]
        },
        {
            "word": "passion for",
            "phonetic": "/ˈpæʃn fɔː/",
            "part_of_speech": "collocation",
            "meaning": "Niềm đam mê sâu sắc đối với điều gì",
            "context_sentence": "Ever since my early childhood, I have nurtured an immense passion for landscape photography and visual storytelling.",
            "speaking_question": "How did you start your favorite hobby?",
            "collocations": ["develop a passion for", "pursue a lifelong passion for"]
        },
        {
            "word": "leisure pursuit",
            "phonetic": "/ˈleʒə pəˈsjuːt/",
            "part_of_speech": "collocation",
            "meaning": "Hoạt động giải trí, thú vui lúc rảnh rỗi",
            "context_sentence": "Urban gardening has emerged as an increasingly popular leisure pursuit among youngsters seeking tranquility.",
            "speaking_question": "What popular hobbies do young people have in your country?",
            "collocations": ["outdoor leisure pursuit", "relaxing leisure pursuit"]
        }
    ],

    # ==================== CHỦ ĐỀ 4: TRAVEL & HOLIDAYS ====================
    4: [
        {
            "word": "breathtaking",
            "phonetic": "/ˈbreθteɪkɪŋ/",
            "part_of_speech": "adjective",
            "meaning": "Đẹp ngoạn mục, choáng ngợp đến nghẹt thở",
            "context_sentence": "Standing on top of the mountain peak at dawn, I was treated to a breathtaking panorama of rolling clouds and green valleys.",
            "speaking_question": "Can you describe a beautiful place you have visited?",
            "collocations": ["breathtaking view", "breathtaking scenery", "breathtaking landscape"]
        },
        {
            "word": "off the beaten track",
            "phonetic": "/ɒf ðə ˈbiːtn træk/",
            "part_of_speech": "idiom",
            "meaning": "Nơi hoang sơ, hẻo lánh, ít người biết đến",
            "context_sentence": "Instead of crowded tourist hotspots, I much prefer backpacking to off the beaten track destinations to experience authentic local life.",
            "speaking_question": "Do you prefer popular tourist spots or quiet places?",
            "collocations": ["travel off the beaten track", "places off the beaten track"]
        },
        {
            "word": "wanderlust",
            "phonetic": "/ˈwɒndəlʌst/",
            "part_of_speech": "noun",
            "meaning": "Niềm khao khát xê dịch, đam mê khám phá thế giới",
            "context_sentence": "Ever since I embarked on my first solo trip across Southeast Asia, I have had an insatiable sense of wanderlust.",
            "speaking_question": "Do you like traveling abroad?",
            "collocations": ["fueled by wanderlust", "satisfy one's wanderlust"]
        },
        {
            "word": "immerse oneself in",
            "phonetic": "/ɪˈmɜːs wʌnˈself ɪn/",
            "part_of_speech": "collocation",
            "meaning": "Đắm mình, hòa mình trọn vẹn vào một nền văn hóa",
            "context_sentence": "Traveling to a foreign country gives you an unmatched opportunity to immerse yourself in exotic customs and sample local delicacies.",
            "speaking_question": "What do you enjoy most when traveling?",
            "collocations": ["immerse oneself in local culture", "immerse oneself in the atmosphere"]
        },
        {
            "word": "hospitality",
            "phonetic": "/ˌhɒspɪˈtæləti/",
            "part_of_speech": "noun",
            "meaning": "Lòng hiếu khách, sự đón tiếp nồng hậu",
            "context_sentence": "We were deeply moved by the incredible hospitality of the islanders, who treated us like members of their own family.",
            "speaking_question": "What was the most memorable part of your last holiday?",
            "collocations": ["warm hospitality", "generous hospitality", "famous for their hospitality"]
        },
        {
            "word": "picturesque",
            "phonetic": "/ˌpɪktʃəˈresk/",
            "part_of_speech": "adjective",
            "meaning": "Đẹp như tranh vẽ, thơ mộng",
            "context_sentence": "Hoi An ancient town is famous for its picturesque alleys adorned with hundreds of glowing handmade silk lanterns.",
            "speaking_question": "Which tourist city in your country would you recommend?",
            "collocations": ["picturesque town", "picturesque coastal village"]
        },
        {
            "word": "broaden one's horizons",
            "phonetic": "/ˈbrɔːdn wʌnz həˈraɪznz/",
            "part_of_speech": "idiom",
            "meaning": "Mở rộng tầm mắt và hiểu biết về thế giới",
            "context_sentence": "Stepping out of your comfort zone and visiting foreign cultures truly broadens your horizons and dispels narrow prejudices.",
            "speaking_question": "Why do many people love traveling?",
            "collocations": ["travel broadens one's horizons"]
        },
        {
            "word": "travel on a shoestring",
            "phonetic": "/ˈtrævl ɒn ə ˈʃuːstrɪŋ/",
            "part_of_speech": "idiom",
            "meaning": "Đi du lịch với ngân sách hạn hẹp, tiết kiệm tối đa",
            "context_sentence": "Back when I was a university student, my friends and I traveled on a shoestring by staying in youth hostels and cooking our own meals.",
            "speaking_question": "Do you need a lot of money to travel?",
            "collocations": ["a holiday on a shoestring"]
        }
    ],

    # ==================== CHỦ ĐỀ 5: TECHNOLOGY & SOCIAL MEDIA ====================
    5: [
        {
            "word": "state-of-the-art",
            "phonetic": "/ˌsteɪt əv ði ˈɑːt/",
            "part_of_speech": "adjective",
            "meaning": "Hiện đại tối tân, tiên tiến nhất hiện nay",
            "context_sentence": "Our campus computer science lab is equipped with state-of-the-art workstations and virtual reality simulation gear.",
            "speaking_question": "What technological devices do you use for study?",
            "collocations": ["state-of-the-art technology", "state-of-the-art equipment"]
        },
        {
            "word": "user-friendly",
            "phonetic": "/ˈjuːzə frendli/",
            "part_of_speech": "adjective",
            "meaning": "Dễ sử dụng, thân thiện với người dùng",
            "context_sentence": "The newly upgraded banking application boasts a sleek, user-friendly interface that even senior citizens can navigate smoothly.",
            "speaking_question": "What makes a good mobile app?",
            "collocations": ["intuitive and user-friendly", "user-friendly interface"]
        },
        {
            "word": "technological breakthrough",
            "phonetic": "/ˌteknəˈlɒdʒɪkl ˈbreɪkθruː/",
            "part_of_speech": "collocation",
            "meaning": "Bước đột phá công nghệ mang tính cách mạng",
            "context_sentence": "The rapid emergence of Generative AI represents a monumental technological breakthrough that is reshaping modern education.",
            "speaking_question": "How has technology changed in the last decade?",
            "collocations": ["major technological breakthrough", "pioneering breakthrough"]
        },
        {
            "word": "double-edged sword",
            "phonetic": "/ˌdʌbl edʒd sɔːd/",
            "part_of_speech": "idiom",
            "meaning": "Con dao hai lưỡi (vừa có lợi vừa có hại)",
            "context_sentence": "Social media is undoubtedly a double-edged sword: it keeps people globally connected, yet excessive usage fosters loneliness and social comparison.",
            "speaking_question": "Is social media good or bad for teenagers?",
            "collocations": ["act as a double-edged sword", "prove to be a double-edged sword"]
        },
        {
            "word": "streamline",
            "phonetic": "/ˈstriːmlaɪn/",
            "part_of_speech": "verb",
            "meaning": "Tinh giản, tối ưu hóa quy trình làm việc",
            "context_sentence": "Project management software has streamlined our daily operations, eliminating tedious manual paperwork and boosting productivity.",
            "speaking_question": "How does technology help you with your work?",
            "collocations": ["streamline daily tasks", "streamline the workflow"]
        },
        {
            "word": "glued to screens",
            "phonetic": "/ɡluːd tuː skriːnz/",
            "part_of_speech": "idiom",
            "meaning": "Dán chặt mắt vào màn hình điện thoại / máy tính",
            "context_sentence": "Nowadays, it is distressing to see children constantly glued to screens at dining tables instead of talking with their parents.",
            "speaking_question": "Do children spend too much time on electronic devices?",
            "collocations": ["remain glued to their screens for hours"]
        },
        {
            "word": "indispensable",
            "phonetic": "/ˌɪndɪˈspensəbl/",
            "part_of_speech": "adjective",
            "meaning": "Không thể thiếu được, tối quan trọng",
            "context_sentence": "Smartphones have become an indispensable part of modern living, serving as our communication hub, wallet, and navigation guide.",
            "speaking_question": "Could you live without a smartphone for a week?",
            "collocations": ["an indispensable tool", "play an indispensable role"]
        },
        {
            "word": "cybersecurity",
            "phonetic": "/ˌsaɪbəsɪˈkjʊərəti/",
            "part_of_speech": "noun",
            "meaning": "An ninh mạng, an toàn thông tin số",
            "context_sentence": "With more confidential personal data stored on the cloud, bolstering cybersecurity has become a matter of urgency for financial institutions.",
            "speaking_question": "What is the biggest concern when using the Internet?",
            "collocations": ["cybersecurity measures", "cybersecurity threats"]
        }
    ],

    # ==================== CHỦ ĐỀ 6: FOOD & COOKING ====================
    6: [
        {
            "word": "mouth-watering",
            "phonetic": "/ˈmaʊθ wɔːtərɪŋ/",
            "part_of_speech": "adjective",
            "meaning": "Thơm ngon nức mũi, làm ứa nước miếng",
            "context_sentence": "The bustling street food stalls in the Old Quarter always give off a mouth-watering aroma of grilled lemongrass pork.",
            "speaking_question": "What is your favorite street food?",
            "collocations": ["mouth-watering aroma", "mouth-watering dishes"]
        },
        {
            "word": "delicacy",
            "phonetic": "/ˈdelɪkəsi/",
            "part_of_speech": "noun",
            "meaning": "Món đặc sản tinh tế, cao lương mỹ vị",
            "context_sentence": "Crispy spring rolls and beef pho are world-renowned Vietnamese delicacies that leave a lasting impression on foreign tourists.",
            "speaking_question": "What food is your country famous for?",
            "collocations": ["local delicacy", "traditional delicacy", "rare delicacy"]
        },
        {
            "word": "savory",
            "phonetic": "/ˈseɪvəri/",
            "part_of_speech": "adjective",
            "meaning": "Đậm đà, mặn mà thơm ngon (không ngọt)",
            "context_sentence": "For breakfast, I generally prefer savory dishes like hot noodles or steamed buns over sugary pancakes.",
            "speaking_question": "What do you usually eat for breakfast?",
            "collocations": ["savory snacks", "savory flavor"]
        },
        {
            "word": "culinary skills",
            "phonetic": "/ˈkʌlɪnəri skɪlz/",
            "part_of_speech": "collocation",
            "meaning": "Kỹ năng nấu nướng, tay nghề bếp núc",
            "context_sentence": "Living independently throughout university forced me to hone my culinary skills instead of relying on expensive fast-food deliveries.",
            "speaking_question": "Do you know how to cook?",
            "collocations": ["hone culinary skills", "master basic culinary skills"]
        },
        {
            "word": "balanced diet",
            "phonetic": "/ˈbælənst ˈdaɪət/",
            "part_of_speech": "collocation",
            "meaning": "Chế độ ăn uống cân bằng, lành mạnh",
            "context_sentence": "Incorporating plenty of crisp vegetables, fresh fruits, and lean proteins is essential for sustaining a balanced diet.",
            "speaking_question": "How do you maintain a healthy eating habit?",
            "collocations": ["stick to a balanced diet", "promote a balanced diet"]
        },
        {
            "word": "comfort food",
            "phonetic": "/ˈkʌmfət fuːd/",
            "part_of_speech": "noun",
            "meaning": "Món ăn xoa dịu tâm trạng, gắn liền với ký ức ấm áp",
            "context_sentence": "Whenever I feel down or caught in chilly winter rain, a piping-hot bowl of chicken porridge is my go-to comfort food.",
            "speaking_question": "What do you eat when you feel sad or stressed?",
            "collocations": ["ultimate comfort food", "home-cooked comfort food"]
        },
        {
            "word": "whip up",
            "phonetic": "/wɪp ʌp/",
            "part_of_speech": "phrasal verb",
            "meaning": "Nấu nhanh một bữa ăn trong thời gian ngắn",
            "context_sentence": "When I come home late from overtime work, I usually whip up a quick pasta dish or a colorful vegetable salad within fifteen minutes.",
            "speaking_question": "Do you often cook at home on weekdays?",
            "collocations": ["whip up a quick dinner", "whip up a meal"]
        },
        {
            "word": "staple food",
            "phonetic": "/ˈsteɪpl fuːd/",
            "part_of_speech": "collocation",
            "meaning": "Lương thực chính, thực phẩm thiết yếu hàng ngày",
            "context_sentence": "Rice serves as the irreplaceable staple food across Asian households, accompanying almost every family meal.",
            "speaking_question": "What is the most popular grain in your country?",
            "collocations": ["an essential staple food"]
        }
    ],

    # ==================== CHỦ ĐỀ 7: SHOPPING & FASHION ====================
    7: [
        {
            "word": "shopaholic",
            "phonetic": "/ˌʃɒpəˈhɒlɪk/",
            "part_of_speech": "noun",
            "meaning": "Người nghiện mua sắm không kiểm soát",
            "context_sentence": "I used to be a self-confessed shopaholic, squandering half of my salary on trendy clothes that I barely wore twice.",
            "speaking_question": "Do you like shopping for clothes?",
            "collocations": ["a compulsive shopaholic"]
        },
        {
            "word": "in vogue",
            "phonetic": "/ɪn vəʊɡ/",
            "part_of_speech": "idiom",
            "meaning": "Đang thịnh hành, rất hợp mốt",
            "context_sentence": "Minimalist linen outfits and neutral earthy tones are currently in vogue among fashion-conscious city dwellers.",
            "speaking_question": "Do you follow fashion trends?",
            "collocations": ["remain in vogue", "come back in vogue"]
        },
        {
            "word": "cost an arm and a leg",
            "phonetic": "/kɒst ən ɑːm ænd ə leɡ/",
            "part_of_speech": "idiom",
            "meaning": "Cực kỳ đắt đỏ, tốn kém cả gia tài",
            "context_sentence": "Designer leather jackets from luxury Parisian fashion houses often cost an arm and a leg, so I prefer affordable sustainable alternatives.",
            "speaking_question": "Do you think expensive branded clothes are worth it?",
            "collocations": ["it costs an arm and a leg"]
        },
        {
            "word": "bargain hunter",
            "phonetic": "/ˈbɑːɡən ˈhʌntə/",
            "part_of_speech": "collocation",
            "meaning": "Người săn lùng hàng giảm giá, mua đồ hời",
            "context_sentence": "My mother is an astute bargain hunter who always tracks down the steepest discounts during end-of-season clearance sales.",
            "speaking_question": "Do you enjoy shopping during sales events?",
            "collocations": ["keen bargain hunter", "paradise for bargain hunters"]
        },
        {
            "word": "impulsive buying",
            "phonetic": "/ɪmˈpʌlsɪv ˈbaɪɪŋ/",
            "part_of_speech": "collocation",
            "meaning": "Hành vi mua sắm bốc đồng, tùy hứng",
            "context_sentence": "E-commerce platforms with countdown flash sales often trigger impulsive buying, resulting in drawers full of unused items.",
            "speaking_question": "Have you ever bought something you never used?",
            "collocations": ["resist impulsive buying", "prone to impulsive buying"]
        },
        {
            "word": "timeless classic",
            "phonetic": "/ˈtaɪmləs ˈklæsɪk/",
            "part_of_speech": "collocation",
            "meaning": "Kiểu dáng kinh điển không bao giờ lỗi mốt",
            "context_sentence": "A tailored dark navy blazer paired with comfortable leather loafers is a timeless classic suitable for both business meetings and casual dinners.",
            "speaking_question": "What is your everyday clothing style?",
            "collocations": ["a timeless fashion classic"]
        },
        {
            "word": "brick-and-mortar store",
            "phonetic": "/brɪk ænd ˈmɔːtə stɔː/",
            "part_of_speech": "collocation",
            "meaning": "Cửa hàng bán lẻ truyền thống (có mặt bằng thực tế)",
            "context_sentence": "Despite the dominance of digital shopping, I still favor visiting brick-and-mortar stores to feel fabric textures and verify fits.",
            "speaking_question": "Do you prefer shopping online or in physical stores?",
            "collocations": ["shop at brick-and-mortar stores"]
        },
        {
            "word": "sustainable fashion",
            "phonetic": "/səˈsteɪnəbl ˈfæʃn/",
            "part_of_speech": "collocation",
            "meaning": "Thời trang bền vững, thân thiện với môi trường",
            "context_sentence": "Young consumers are increasingly championing sustainable fashion brands that practice ethical manufacturing and use recycled textiles.",
            "speaking_question": "Has your perception of fashion changed over time?",
            "collocations": ["support sustainable fashion", "embrace sustainable fashion"]
        }
    ],

    # ==================== CHỦ ĐỀ 8: HEALTH & FITNESS ====================
    8: [
        {
            "word": "stamina",
            "phonetic": "/ˈstæmɪnə/",
            "part_of_speech": "noun",
            "meaning": "Sức bền, thể lực dẻo dai",
            "context_sentence": "Jogging five kilometers every morning has substantially enhanced my cardiovascular stamina and overall alertness throughout the workday.",
            "speaking_question": "What exercise do you do to maintain energy?",
            "collocations": ["build physical stamina", "boost cardiovascular stamina"]
        },
        {
            "word": "under the weather",
            "phonetic": "/ˈʌndə ðə ˈweðə/",
            "part_of_speech": "idiom",
            "meaning": "Cảm thấy uể oải, không được khỏe trong người",
            "context_sentence": "Whenever seasonal weather transitions occur, I tend to feel a bit under the weather with a congested nose and slight fatigue.",
            "speaking_question": "What do you do when you catch a cold?",
            "collocations": ["feel slightly under the weather"]
        },
        {
            "word": "mental well-being",
            "phonetic": "/ˈmentl ˌwel ˈbiːɪŋ/",
            "part_of_speech": "collocation",
            "meaning": "Sức khỏe tinh thần, tâm lý an yên",
            "context_sentence": "Allocating thirty minutes every evening to meditation and reading plays an instrumental role in nurturing my mental well-being.",
            "speaking_question": "Why is mental health as important as physical health?",
            "collocations": ["preserve mental well-being", "enhance mental well-being"]
        },
        {
            "word": "in the pink of health",
            "phonetic": "/ɪn ðə pɪŋk əv helθ/",
            "part_of_speech": "idiom",
            "meaning": "Rất khỏe mạnh, tràn đầy sinh lực",
            "context_sentence": "Thanks to disciplined dietary habits and daily morning tai chi, my eighty-year-old grandfather is remarkably in the pink of health.",
            "speaking_question": "How do elderly people in your family stay healthy?",
            "collocations": ["remain in the pink of health"]
        },
        {
            "word": "work out",
            "phonetic": "/wɜːk aʊt/",
            "part_of_speech": "phrasal verb",
            "meaning": "Tập luyện thể dục thể hình",
            "context_sentence": "I make a conscious commitment to work out at least four days a week to build lean muscle and blow off steam.",
            "speaking_question": "How often do you exercise?",
            "collocations": ["work out regularly", "work out at the local gym"]
        },
        {
            "word": "detrimental to health",
            "phonetic": "/ˌdetrɪˈmentl tuː helθ/",
            "part_of_speech": "collocation",
            "meaning": "Có hại, gây tổn hại nghiêm trọng cho sức khỏe",
            "context_sentence": "Chronic sleep deprivation coupled with excessive caffeine consumption is immensely detrimental to long-term immune health.",
            "speaking_question": "What bad habits affect our health the most?",
            "collocations": ["severely detrimental to health"]
        },
        {
            "word": "cut down on",
            "phonetic": "/kʌt daʊn ɒn/",
            "part_of_speech": "phrasal verb",
            "meaning": "Cắt giảm số lượng tiêu thụ (đường, muối, rượu bia)",
            "context_sentence": "My nutritionist strongly advised me to cut down on sugary bubble teas and deep-fried snacks to lower my cholesterol.",
            "speaking_question": "Have you made any dietary adjustments recently?",
            "collocations": ["cut down on sugar intake", "cut down on processed foods"]
        },
        {
            "word": "sedentary habits",
            "phonetic": "/ˈsedntri ˈhæbɪts/",
            "part_of_speech": "collocation",
            "meaning": "Các thói quen ngồi thụ động một chỗ",
            "context_sentence": "Setting hourly reminder alarms to stretch and walk around helps office workers break dangerous sedentary habits.",
            "speaking_question": "How can office workers stay active?",
            "collocations": ["overcome sedentary habits"]
        }
    ],

    # ==================== CHỦ ĐỀ 9: ENVIRONMENT & NATURE ====================
    9: [
        {
            "word": "biodegradable",
            "phonetic": "/ˌbaɪəʊdɪˈɡreɪdəbl/",
            "part_of_speech": "adjective",
            "meaning": "Có khả năng phân hủy sinh học tự nhiên",
            "context_sentence": "Many progressive retailers are replacing petroleum plastic bags with biodegradable packaging manufactured from cassava starch.",
            "speaking_question": "What can individuals do to protect the environment?",
            "collocations": ["biodegradable materials", "100% biodegradable"]
        },
        {
            "word": "carbon footprint",
            "phonetic": "/ˌkɑːbən ˈfʊtprɪnt/",
            "part_of_speech": "collocation",
            "meaning": "Lượng khí thải carbon thải ra môi trường",
            "context_sentence": "Commuting by public transit and incorporating more plant-based meals are effective ways for citizens to shrink their carbon footprint.",
            "speaking_question": "How can we reduce pollution in big cities?",
            "collocations": ["reduce one's carbon footprint", "minimize carbon footprint"]
        },
        {
            "word": "eco-friendly",
            "phonetic": "/ˌiːkəʊ ˈfrendli/",
            "part_of_speech": "adjective",
            "meaning": "Thân thiện với môi trường sinh thái",
            "context_sentence": "Installing rooftop solar panels is an eco-friendly investment that significantly curbs household reliance on coal electricity.",
            "speaking_question": "Do you buy environmentally friendly products?",
            "collocations": ["eco-friendly alternatives", "eco-friendly lifestyle"]
        },
        {
            "word": "depletion of natural resources",
            "phonetic": "/dɪˈpliːʃn əv ˈnætʃrəl rɪˈsɔːsɪz/",
            "part_of_speech": "collocation",
            "meaning": "Sự cạn kiệt tài nguyên thiên nhiên",
            "context_sentence": "Rampant deforestation and unsustainable deep-sea trawling have triggered an alarming depletion of natural resources worldwide.",
            "speaking_question": "What environmental problems are you most worried about?",
            "collocations": ["halt the depletion of natural resources"]
        },
        {
            "word": "endangered species",
            "phonetic": "/ɪnˈdeɪndʒəd ˈspiːʃiːz/",
            "part_of_speech": "collocation",
            "meaning": "Các loài động thực vật có nguy cơ tuyệt chủng",
            "context_sentence": "Strict wildlife sanctuaries and anti-poaching patrol squads are vital to safeguard endangered species like rhinos and pangolins.",
            "speaking_question": "Why is protecting wild animals crucial?",
            "collocations": ["protect endangered species", "on the verge of extinction"]
        },
        {
            "word": "combat climate change",
            "phonetic": "/ˈkɒmbæt ˈklaɪmət tʃeɪndʒ/",
            "part_of_speech": "collocation",
            "meaning": "Chống lại biến đổi khí hậu toàn cầu",
            "context_sentence": "Global leaders must forge binding treaties to combat climate change and mitigate catastrophic extreme weather anomalies.",
            "speaking_question": "Who should take the biggest responsibility for global warming?",
            "collocations": ["concerted efforts to combat climate change"]
        },
        {
            "word": "renewable energy",
            "phonetic": "/rɪˈnjuːəbl ˈenədʒi/",
            "part_of_speech": "collocation",
            "meaning": "Năng lượng tái tạo (gió, mặt trời, thủy điện...)",
            "context_sentence": "Accelerating the national transition toward renewable energy is paramount for attaining net-zero carbon emission targets by 2050.",
            "speaking_question": "What is the future of energy production?",
            "collocations": ["harness renewable energy", "invest in renewable energy"]
        },
        {
            "word": "raise environmental awareness",
            "phonetic": "/reɪz ɪnˌvaɪrənˈmentl əˈweənəs/",
            "part_of_speech": "collocation",
            "meaning": "Nâng cao ý thức bảo vệ môi trường",
            "context_sentence": "Educational school campaigns play a pivotal role in raising environmental awareness and instilling recycling habits in young children.",
            "speaking_question": "How can schools teach kids about nature?",
            "collocations": ["vital to raise environmental awareness"]
        }
    ],

    # ==================== CHỦ ĐỀ 10: TRANSPORT & DRIVING ====================
    10: [
        {
            "word": "rush hour",
            "phonetic": "/ˈrʌʃ aʊə/",
            "part_of_speech": "collocation",
            "meaning": "Giờ cao điểm kẹt xe",
            "context_sentence": "During morning rush hour, arterial roads and bridges in Hanoi turn into suffocating bottlenecks of vehicles.",
            "speaking_question": "What is the traffic like in your city?",
            "collocations": ["stuck in rush hour traffic", "avoid peak rush hour"]
        },
        {
            "word": "traffic congestion",
            "phonetic": "/ˈtræfɪk kənˈdʒestʃən/",
            "part_of_speech": "collocation",
            "meaning": "Sự ùn tắc giao thông nghiêm trọng",
            "context_sentence": "Expanding overhead light rail networks is the most viable long-term solution to alleviate chronic traffic congestion in urban hubs.",
            "speaking_question": "How can cities solve traffic jams?",
            "collocations": ["alleviate traffic congestion", "severe traffic congestion"]
        },
        {
            "word": "commute",
            "phonetic": "/kəˈmjuːt/",
            "part_of_speech": "verb / noun",
            "meaning": "Quãng đường / việc đi lại hàng ngày giữa nhà và chỗ làm",
            "context_sentence": "My daily commute by rapid metro takes only twenty minutes, affording me ample time to read news or listen to podcasts.",
            "speaking_question": "How do you commute to work or university every day?",
            "collocations": ["daily commute", "long commute to work"]
        },
        {
            "word": "bumper to bumper",
            "phonetic": "/ˈbʌmpə tuː ˈbʌmpə/",
            "part_of_speech": "idiom",
            "meaning": "Xe cộ nối đuôi nhau san sát, kẹt cứng",
            "context_sentence": "Due to torrential downpours yesterday evening, private cars and motorbikes were crawling bumper to bumper along the ring road.",
            "speaking_question": "Have you ever been stuck in a terrible traffic jam?",
            "collocations": ["traffic was bumper to bumper"]
        },
        {
            "word": "environmentally friendly transport",
            "phonetic": "/ɪnˌvaɪrənˈmentli ˈfrendli ˈtrænspɔːt/",
            "part_of_speech": "collocation",
            "meaning": "Phương tiện giao thông xanh, thân thiện môi trường",
            "context_sentence": "Electric buses and shared bicycle-docking stations represent convenient and environmentally friendly transport modes.",
            "speaking_question": "Are electric vehicles becoming popular in your country?",
            "collocations": ["encourage environmentally friendly transport"]
        },
        {
            "word": "reckless driving",
            "phonetic": "/ˈrekləs ˈdraɪvɪŋ/",
            "part_of_speech": "collocation",
            "meaning": "Lái xe ẩu thả, bất cẩn gây nguy hiểm",
            "context_sentence": "Stricter surveillance cameras and heftier penalties are essential to deter reckless driving and ensure pedestrian safety.",
            "speaking_question": "Do people in your city obey traffic rules?",
            "collocations": ["penalize reckless driving", "accidents caused by reckless driving"]
        },
        {
            "word": "pedestrian precinct",
            "phonetic": "/pəˈdestriən ˈpriːsɪŋkt/",
            "part_of_speech": "collocation",
            "meaning": "Khu phố đi bộ, cấm xe cơ giới",
            "context_sentence": "Transforming the area around Hoan Kiem Lake into a pedestrian precinct on weekends has created a vibrant cultural open space.",
            "speaking_question": "Do you enjoy walking in your city?",
            "collocations": ["designated pedestrian precinct"]
        },
        {
            "word": "carpooling",
            "phonetic": "/ˈkɑːpuːlɪŋ/",
            "part_of_speech": "noun",
            "meaning": "Đi chung xe với người khác để tiết kiệm chi phí",
            "context_sentence": "Carpooling with office colleagues not only splits high petrol expenses but also minimizes the volume of tailpipe emissions.",
            "speaking_question": "Do you think carpooling is a good practice?",
            "collocations": ["practice carpooling", "carpooling apps"]
        }
    ],

    # ==================== CHỦ ĐỀ 11: MEDIA: BOOKS, MUSIC & MOVIES ====================
    11: [
        {
            "word": "page-turner",
            "phonetic": "/ˈpeɪdʒ tɜːnə/",
            "part_of_speech": "noun",
            "meaning": "Cuốn sách ly kỳ, hấp dẫn đến mức không thể rời mắt",
            "context_sentence": "That psychological thriller novel was an absolute page-turner; I stayed awake until dawn because I couldn't bear to put it down.",
            "speaking_question": "What is the best book you have read recently?",
            "collocations": ["a gripping page-turner"]
        },
        {
            "word": "catchy tune",
            "phonetic": "/ˈkætʃi tjuːn/",
            "part_of_speech": "collocation",
            "meaning": "Giai điệu bắt tai, dễ nhớ và cuốn hút",
            "context_sentence": "The indie pop single went viral globally within hours thanks to its infectious acoustic guitar riff and catchy tune.",
            "speaking_question": "What kind of music gets stuck in your head?",
            "collocations": ["hum a catchy tune", "boast a catchy tune"]
        },
        {
            "word": "blockbuster",
            "phonetic": "/ˈblɒkbʌstə/",
            "part_of_speech": "noun",
            "meaning": "Phim bom tấn điện ảnh, doanh thu khủng",
            "context_sentence": "The latest sci-fi blockbuster shattered international box-office records with its visionary visual effects and stellar soundtrack.",
            "speaking_question": "Do you prefer watching movies at home or in the cinema?",
            "collocations": ["Hollywood blockbuster", "summer blockbuster"]
        },
        {
            "word": "thought-provoking",
            "phonetic": "/ˈθɔːt prəˈvəʊkɪŋ/",
            "part_of_speech": "adjective",
            "meaning": "Kích thích tư duy, gợi mở nhiều suy ngẫm sâu sắc",
            "context_sentence": "It was a remarkably thought-provoking documentary that exposed the hidden human cost behind the fast-fashion manufacturing machine.",
            "speaking_question": "What makes a documentary worth watching?",
            "collocations": ["a thought-provoking theme", "thought-provoking questions"]
        },
        {
            "word": "genre",
            "phonetic": "/ˈʒɑːnrə/",
            "part_of_speech": "noun",
            "meaning": "Thể loại nghệ thuật, âm nhạc hoặc phim ảnh",
            "context_sentence": "While my primary preference is contemporary jazz, my musical taste spans across diverse genres ranging from classical piano to alternative rock.",
            "speaking_question": "What genres of movies or music do you like?",
            "collocations": ["favorite movie genre", "explore different genres"]
        },
        {
            "word": "cliffhanger",
            "phonetic": "/ˈklɪfhæŋə/",
            "part_of_speech": "noun",
            "meaning": "Đoạn kết gay cấn lơ lửng, tạo sự hồi hộp tột cùng",
            "context_sentence": "The drama series season finale concluded on an electrifying cliffhanger, sparking heated fan debates over the protagonist's fate.",
            "speaking_question": "Do you like binge-watching TV series?",
            "collocations": ["end on a dramatic cliffhanger"]
        },
        {
            "word": "avid reader",
            "phonetic": "/ˈævɪd ˈriːdə/",
            "part_of_speech": "collocation",
            "meaning": "Người say mê đọc sách từ lâu năm",
            "context_sentence": "Growing up as an avid reader allowed me to build an expressive vocabulary and cultivate profound empathy for different walks of life.",
            "speaking_question": "How has reading books influenced you?",
            "collocations": ["an avid reader since childhood"]
        },
        {
            "word": "evoke emotional resonance",
            "phonetic": "/ɪˈvəʊk ɪˈməʊʃənl ˈrezənəns/",
            "part_of_speech": "collocation",
            "meaning": "Khơi gợi sự đồng cảm, rung động cảm xúc sâu sắc",
            "context_sentence": "The film's poignant orchestral score and authentic dialogue evoked tremendous emotional resonance among audience members.",
            "speaking_question": "What was the most touching movie you have ever watched?",
            "collocations": ["evoke strong emotional resonance"]
        }
    ],

    # ==================== CHỦ ĐỀ 12: PEOPLE: FAMILY, FRIENDS & ROLE MODELS ====================
    12: [
        {
            "word": "role model",
            "phonetic": "/ˈrəʊl mɒdl/",
            "part_of_speech": "collocation",
            "meaning": "Hình mẫu lý tưởng, tấm gương sáng để noi theo",
            "context_sentence": "My mother has consistently stood as my greatest role model because of her unyielding resilience and unconditional compassion.",
            "speaking_question": "Who is the person you admire most in your family?",
            "collocations": ["an inspiring role model", "act as a positive role model"]
        },
        {
            "word": "flesh and blood",
            "phonetic": "/fleʃ ænd blʌd/",
            "part_of_speech": "idiom",
            "meaning": "Người thân ruột thịt, máu mủ ruột rà",
            "context_sentence": "No matter how bitter a sibling squabble might get, at the end of the day, family members are your own flesh and blood.",
            "speaking_question": "How important is family to you?",
            "collocations": ["your own flesh and blood"]
        },
        {
            "word": "kindred spirit",
            "phonetic": "/ˈkɪndrəd ˈspɪrɪt/",
            "part_of_speech": "noun",
            "meaning": "Tâm hồn đồng điệu, tri kỷ hiểu thấu lòng nhau",
            "context_sentence": "From our very first conversation during orientation camp, I recognized her as a kindred spirit who mirrored my humor and ambitions.",
            "speaking_question": "Can you tell me about your best friend?",
            "collocations": ["find a kindred spirit in someone"]
        },
        {
            "word": "look up to",
            "phonetic": "/lʊk ʌp tuː/",
            "part_of_speech": "phrasal verb",
            "meaning": "Kính trọng, nể phục và ngưỡng mộ ai đó",
            "context_sentence": "Young aspiring entrepreneurs often look up to pioneering leaders who overcome numerous failures to innovate industries.",
            "speaking_question": "Who do young people in your country look up to?",
            "collocations": ["deeply look up to someone"]
        },
        {
            "word": "through thick and thin",
            "phonetic": "/θruː θɪk ænd θɪn/",
            "part_of_speech": "idiom",
            "meaning": "Trải qua mọi thăng trầm, hoạn nạn có nhau",
            "context_sentence": "A genuine childhood friend is someone who stays steadfastly in your corner through thick and thin without any ulterior motives.",
            "speaking_question": "What qualities do you value most in a true friend?",
            "collocations": ["stand by someone through thick and thin"]
        },
        {
            "word": "close-knit family",
            "phonetic": "/ˌkləʊs ˈnɪt ˈfæməli/",
            "part_of_speech": "collocation",
            "meaning": "Gia đình đầm ấm, gắn bó keo sơn",
            "context_sentence": "I am fortunate to be raised in a close-knit family where we gather for candid dinner conversations every single evening.",
            "speaking_question": "Do you spend a lot of time with your family?",
            "collocations": ["belong to a close-knit family"]
        },
        {
            "word": "confide in",
            "phonetic": "/kənˈfaɪd ɪn/",
            "part_of_speech": "phrasal verb",
            "meaning": "Tâm sự, thổ lộ những bí mật và nỗi lòng thầm kín",
            "context_sentence": "Whenever I encounter career dilemmas or emotional distress, my elder sister is the trustworthy confidante I confide in.",
            "speaking_question": "Who do you turn to when you have personal problems?",
            "collocations": ["confide personal secrets in someone"]
        },
        {
            "word": "charismatic personality",
            "phonetic": "/ˌkærɪzˈmætɪk ˌpɜːsəˈnæləti/",
            "part_of_speech": "collocation",
            "meaning": "Tính cách lôi cuốn, có sức hút và thần thái cuốn hút",
            "context_sentence": "His charismatic personality and sharp wit make him an engaging speaker who naturally captures an entire auditorium's attention.",
            "speaking_question": "What personality traits make someone popular?",
            "collocations": ["possess a charismatic personality"]
        }
    ],

    # ==================== CHỦ ĐỀ 13: EVENTS & EXPERIENCES ====================
    13: [
        {
            "word": "milestone",
            "phonetic": "/ˈmaɪlstəʊn/",
            "part_of_speech": "noun",
            "meaning": "Cột mốc lịch sử, bước ngoặt trọng đại",
            "context_sentence": "Passing the university entrance exam with flying colors marked a defining milestone that fundamentally shaped my future path.",
            "speaking_question": "What has been the most important event in your life so far?",
            "collocations": ["a momentous milestone", "reach a major milestone"]
        },
        {
            "word": "unforgettable memory",
            "phonetic": "/ˌʌnfəˈɡetəbl ˈmeməri/",
            "part_of_speech": "collocation",
            "meaning": "Kỷ niệm khắc sâu trong tâm trí, không bao giờ quên",
            "context_sentence": "Watching the lantern festival in Hoi An with my high-school squad remains one of my most cherished and unforgettable memories.",
            "speaking_question": "Can you share a memorable celebration you attended?",
            "collocations": ["create an unforgettable memory"]
        },
        {
            "word": "once-in-a-lifetime experience",
            "phonetic": "/wʌns ɪn ə ˈlaɪftaɪm ɪkˈspɪəriəns/",
            "part_of_speech": "collocation",
            "meaning": "Trải nghiệm ngàn năm có một, hiếm khi lặp lại",
            "context_sentence": "Paragliding over the golden terraced rice fields in Mu Cang Chai was truly a once-in-a-lifetime experience that thrilled my senses.",
            "speaking_question": "Have you ever done something adventurous?",
            "collocations": ["a thrilling once-in-a-lifetime experience"]
        },
        {
            "word": "nerve-wracking",
            "phonetic": "/ˈnɜːv rækɪŋ/",
            "part_of_speech": "adjective",
            "meaning": "Căng thẳng thót tim, đứng ngồi không yên",
            "context_sentence": "Delivering my graduation thesis presentation before a panel of stern professors was nerve-wracking, yet incredibly rewarding.",
            "speaking_question": "Have you ever given a speech in public?",
            "collocations": ["a nerve-wracking moment", "find the interview nerve-wracking"]
        },
        {
            "word": "festive atmosphere",
            "phonetic": "/ˈfestɪv ˈætməsfɪə/",
            "part_of_speech": "collocation",
            "meaning": "Không khí lễ hội hân hoan rực rỡ",
            "context_sentence": "During Lunar New Year preparations, residential alleys are ablaze with red lanterns and kumquat trees, radiating a warm festive atmosphere.",
            "speaking_question": "What is the most popular traditional festival in your country?",
            "collocations": ["soak up the festive atmosphere"]
        },
        {
            "word": "step out of one's comfort zone",
            "phonetic": "/step aʊt əv wʌnz ˈkʌmfət zəʊn/",
            "part_of_speech": "idiom",
            "meaning": "Dũng cảm bước ra khỏi vùng an toàn quen thuộc",
            "context_sentence": "Volunteering to teach in an isolated mountainous village forced me to step out of my comfort zone and discover true resilience.",
            "speaking_question": "Why is trying new things beneficial for self-growth?",
            "collocations": ["willing to step out of your comfort zone"]
        },
        {
            "word": "reminisce about",
            "phonetic": "/ˌremɪˈnɪs əˈbaʊt/",
            "part_of_speech": "verb",
            "meaning": "Bồi hồi hồi tưởng về những kỷ niệm đẹp đã qua",
            "context_sentence": "Whenever my old classmates reunite, we spend entire afternoons reminiscing about our hilarious childhood escapades.",
            "speaking_question": "Do you often look back on your school days?",
            "collocations": ["fondly reminisce about the past"]
        },
        {
            "word": "cherished occasion",
            "phonetic": "/ˈtʃerɪʃt əˈkeɪʒn/",
            "part_of_speech": "collocation",
            "meaning": "Dịp kỷ niệm thiêng liêng được trân quý",
            "context_sentence": "My grandparents' golden wedding anniversary was a cherished occasion that brought together relatives from across the globe.",
            "speaking_question": "What family occasions do you celebrate most enthusiastically?",
            "collocations": ["mark a cherished occasion"]
        }
    ],

    # ==================== CHỦ ĐỀ 14: PLACES & BUILDINGS ====================
    14: [
        {
            "word": "architectural marvel",
            "phonetic": "/ˌɑːkɪˈtektʃərəl ˈmɑːvl/",
            "part_of_speech": "collocation",
            "meaning": "Kỳ quan kiến trúc tráng lệ, kiệt tác xây dựng",
            "context_sentence": "The Sydney Opera House is globally celebrated as an architectural marvel due to its expressive interlocking concrete shell roof.",
            "speaking_question": "Can you tell me about a famous building you like?",
            "collocations": ["a stunning architectural marvel"]
        },
        {
            "word": "bustling city center",
            "phonetic": "/ˈbʌslɪŋ ˈsɪti ˈsentə/",
            "part_of_speech": "collocation",
            "meaning": "Khu trung tâm thành phố sầm uất, náo nhiệt",
            "context_sentence": "The bustling city center is teeming with trendy coffee shops, pedestrian plazas, and illuminated retail department stores.",
            "speaking_question": "Where do people usually hang out in your city?",
            "collocations": ["located right in the bustling city center"]
        },
        {
            "word": "historic landmark",
            "phonetic": "/hɪˈstɒrɪk ˈlændmɑːk/",
            "part_of_speech": "collocation",
            "meaning": "Di tích / địa danh lịch sử nổi tiếng",
            "context_sentence": "The Temple of Literature stands as an illustrious historic landmark commemorating Vietnam's long-standing intellectual heritage.",
            "speaking_question": "What historical places should foreign visitors see in your country?",
            "collocations": ["visit a famous historic landmark"]
        },
        {
            "word": "tranquil oasis",
            "phonetic": "/ˈtræŋkwɪl əʊˈeɪsɪs/",
            "part_of_speech": "collocation",
            "meaning": "Ốc đảo thanh bình, tĩnh lặng giữa lòng đô thị ồn ào",
            "context_sentence": "The city botanical park acts as a tranquil oasis where city dwellers come to jog, sketch, or read quietly away from traffic horns.",
            "speaking_question": "Is there a quiet place in your city where you can rest?",
            "collocations": ["serve as a tranquil oasis"]
        },
        {
            "word": "skyscraper",
            "phonetic": "/ˈskaɪskreɪpə/",
            "part_of_speech": "noun",
            "meaning": "Tòa nhà chọc trời cao vút hiện đại",
            "context_sentence": "The skyline of modern financial hubs is dominated by gleaming glass-and-steel skyscrapers that look spectacular when illuminated at night.",
            "speaking_question": "Do you prefer modern high-rise buildings or traditional houses?",
            "collocations": ["towering skyscraper", "mirrored skyscraper"]
        },
        {
            "word": "state-of-the-art facility",
            "phonetic": "/ˌsteɪt əv ði ˈɑːt fəˈsɪləti/",
            "part_of_speech": "collocation",
            "meaning": "Cơ sở vật chất hiện đại, tiên tiến nhất",
            "context_sentence": "The newly constructed public library offers state-of-the-art facilities, including acoustic study cubicles and digital research terminals.",
            "speaking_question": "What public facilities should cities build more of?",
            "collocations": ["equipped with state-of-the-art facilities"]
        },
        {
            "word": "quaint neighborhood",
            "phonetic": "/kweɪnt ˈneɪbəhʊd/",
            "part_of_speech": "collocation",
            "meaning": "Khu dân cư cổ kính, duyên dáng và yên ả",
            "context_sentence": "I take pleasure in strolling through that quaint neighborhood with its cobblestone pathways and ivy-covered colonial houses.",
            "speaking_question": "Which area in your city has the most unique charm?",
            "collocations": ["wander around a quaint neighborhood"]
        },
        {
            "word": "tourist magnet",
            "phonetic": "/ˈtʊərɪst ˈmæɡnət/",
            "part_of_speech": "collocation",
            "meaning": "Thỏi nam châm thu hút khách du lịch",
            "context_sentence": "Ha Long Bay's emerald waters and limestone islets have established the bay as a perennial tourist magnet in northern Vietnam.",
            "speaking_question": "What is the most popular destination for travelers in your country?",
            "collocations": ["act as a major tourist magnet"]
        }
    ],

    # ==================== CHỦ ĐỀ 15: OBJECTS & POSSESSIONS ====================
    15: [
        {
            "word": "sentimental value",
            "phonetic": "/ˌsentɪˈmentl ˈvæljuː/",
            "part_of_speech": "collocation",
            "meaning": "Giá trị tình cảm, ý nghĩa tinh thần sâu đậm",
            "context_sentence": "Although this vintage mechanical watch is not financially extravagant, it carries immense sentimental value as my grandfather's gift.",
            "speaking_question": "What is an item you own that means a lot to you?",
            "collocations": ["hold great sentimental value", "priceless sentimental value"]
        },
        {
            "word": "cherished keepsake",
            "phonetic": "/ˈtʃerɪʃt ˈkiːpseɪk/",
            "part_of_speech": "collocation",
            "meaning": "Món kỷ vật được trân trọng, nâng niu",
            "context_sentence": "I keep a yellowed handwritten postcard from my childhood best friend tucked in my diary as a cherished keepsake.",
            "speaking_question": "Do you like keeping souvenirs from trips or friends?",
            "collocations": ["preserve as a cherished keepsake"]
        },
        {
            "word": "indispensable gadget",
            "phonetic": "/ˌɪndɪˈspensəbl ˈɡædʒɪt/",
            "part_of_speech": "collocation",
            "meaning": "Thiết bị điện tử hữu ích không thể thiếu",
            "context_sentence": "My active noise-canceling headphones are an indispensable gadget that enables me to concentrate deeply in bustling coffee shops.",
            "speaking_question": "What electronic device do you rely on most?",
            "collocations": ["an indispensable gadget for daily tasks"]
        },
        {
            "word": "heirloom",
            "phonetic": "/ˈeəluːm/",
            "part_of_speech": "noun",
            "meaning": "Vật gia bảo truyền đời của gia đình",
            "context_sentence": "This intricate jade bracelet is a precious family heirloom that has been passed down across four generations of matriarchs.",
            "speaking_question": "Does your family have any items passed down from ancestors?",
            "collocations": ["priceless family heirloom"]
        },
        {
            "word": "price tag",
            "phonetic": "/ˈpraɪs tæɡ/",
            "part_of_speech": "noun",
            "meaning": "Mức giá niêm yết, chi phí mua sắm",
            "context_sentence": "When purchasing work tools, I prioritize durability and ergonomic comfort rather than obsessing over an exorbitant brand price tag.",
            "speaking_question": "How do you decide whether an item is worth buying?",
            "collocations": ["hefty price tag", "look past the price tag"]
        },
        {
            "word": "practicality",
            "phonetic": "/ˌpræktɪˈkæləti/",
            "part_of_speech": "noun",
            "meaning": "Tính thực dụng, giá trị ứng dụng thực tế",
            "context_sentence": "I chose this backpack strictly for its practicality, appreciating its waterproof fabric compartments and balanced weight distribution.",
            "speaking_question": "Do you care more about fashion or practicality when buying things?",
            "collocations": ["valued for its practicality"]
        },
        {
            "word": "prized possession",
            "phonetic": "/praɪzd pəˈzeʃn/",
            "part_of_speech": "collocation",
            "meaning": "Vật sở hữu quý giá nhất, báu vật cá nhân",
            "context_sentence": "My hand-crafted acoustic guitar is my most prized possession; composing melodies on it provides solace from everyday pressures.",
            "speaking_question": "If your house was on fire, what object would you save first?",
            "collocations": ["regard it as a prized possession"]
        },
        {
            "word": "time-saving device",
            "phonetic": "/ˈtaɪm seɪvɪŋ dɪˈvaɪs/",
            "part_of_speech": "collocation",
            "meaning": "Thiết bị giúp tiết kiệm thời gian và công sức",
            "context_sentence": "An automated robotic vacuum cleaner has proven to be an invaluable time-saving device for our busy dual-income household.",
            "speaking_question": "What home appliance do you find most useful?",
            "collocations": ["a handy time-saving device"]
        }
    ],

    # ==================== CHỦ ĐỀ 16: SOCIETY & MODERN LIFE ====================
    16: [
        {
            "word": "fast-paced lifestyle",
            "phonetic": "/ˌfɑːst ˈpeɪst ˈlaɪfstaɪl/",
            "part_of_speech": "collocation",
            "meaning": "Lối sống hối hả, nhịp sống gấp gáp của thời hiện đại",
            "context_sentence": "Living in a bustling financial capital often traps young professionals in a fast-paced lifestyle with virtually no downtime for self-care.",
            "speaking_question": "How has city lifestyle changed compared to the past?",
            "collocations": ["accustomed to a fast-paced lifestyle"]
        },
        {
            "word": "work-life balance",
            "phonetic": "/ˌwɜːk ˈlaɪf ˈbæləns/",
            "part_of_speech": "collocation",
            "meaning": "Sự cân bằng hài hòa giữa công việc và đời sống",
            "context_sentence": "Progressive enterprises are adopting four-day workweeks to help personnel achieve a healthier work-life balance and curb chronic burnout.",
            "speaking_question": "Is it easy to balance work and personal life today?",
            "collocations": ["achieve a healthy work-life balance", "strike a work-life balance"]
        },
        {
            "word": "social cohesion",
            "phonetic": "/ˌsəʊʃl kəʊˈhiːʒn/",
            "part_of_speech": "collocation",
            "meaning": "Sự gắn kết, đoàn kết hài hòa trong cộng đồng xã hội",
            "context_sentence": "Grassroots neighborhood initiatives and volunteer charity kitchens foster mutual empathy and bolster social cohesion across diverse groups.",
            "speaking_question": "How can communities become closer together?",
            "collocations": ["strengthen social cohesion", "promote social cohesion"]
        },
        {
            "word": "wealth disparity",
            "phonetic": "/welθ dɪˈspærəti/",
            "part_of_speech": "collocation",
            "meaning": "Sự chênh lệch, phân hóa giàu nghèo",
            "context_sentence": "Widening wealth disparity remains one of the most pressing socio-economic challenges that governments must address through education equity.",
            "speaking_question": "What social problem needs urgent attention in modern society?",
            "collocations": ["widening wealth disparity", "tackle wealth disparity"]
        },
        {
            "word": "aging population",
            "phonetic": "/ˈeɪdʒɪŋ ˌpɒpjuˈleɪʃn/",
            "part_of_speech": "collocation",
            "meaning": "Hiện tượng già hóa dân số",
            "context_sentence": "A rapidly aging population exerts unprecedented pressure on national healthcare budgets and pension sustainability.",
            "speaking_question": "How will demographic shifts affect future jobs?",
            "collocations": ["face an aging population", "consequences of an aging population"]
        },
        {
            "word": "rat race",
            "phonetic": "/ˈræt reɪs/",
            "part_of_speech": "idiom",
            "meaning": "Cuộc đua ganh đua mệt mỏi, guồng quay mưu sinh khốc liệt",
            "context_sentence": "Many urban millennials are choosing to quit the corporate rat race and embrace simpler lives in peaceful provincial towns.",
            "speaking_question": "Why do some people want to move away from big cities?",
            "collocations": ["escape the corporate rat race"]
        },
        {
            "word": "cultural diversity",
            "phonetic": "/ˈkʌltʃərəl daɪˈvɜːsəti/",
            "part_of_speech": "collocation",
            "meaning": "Sự đa dạng bản sắc văn hóa",
            "context_sentence": "What makes cosmopolitan metropolises profoundly appealing is their rich cultural diversity, reflected vividly in eclectic cuisines and festivities.",
            "speaking_question": "Why is cultural diversity important for a city?",
            "collocations": ["celebrate cultural diversity", "embrace cultural diversity"]
        },
        {
            "word": "sustainable development",
            "phonetic": "/səˌsteɪnəbl dɪˈveləpmənt/",
            "part_of_speech": "collocation",
            "meaning": "Sự phát triển bền vững (hài hòa kinh tế và môi trường)",
            "context_sentence": "Modern urban planners must strike a delicate equilibrium between rapid infrastructure expansion and long-term sustainable development.",
            "speaking_question": "What should cities focus on for future growth?",
            "collocations": ["achieve sustainable development goals"]
        }
    ]
}


def get_vocabularies_for_topic(topic_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách từ vựng chuẩn Band 8.0+ kèm câu ngữ cảnh của 1 chủ đề"""
    return TOPIC_VOCABULARIES.get(topic_id, [])


def search_topic_vocabularies(query: str, topic_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """Tìm kiếm từ vựng theo từ khóa hoặc chủ đề"""
    q = (query or "").strip().lower()
    results = []

    target_topics = [topic_id] if topic_id and topic_id in TOPIC_VOCABULARIES else list(TOPIC_VOCABULARIES.keys())

    for tid in target_topics:
        vocab_list = TOPIC_VOCABULARIES.get(tid, [])
        for item in vocab_list:
            if not q or (q in item["word"].lower() or q in item["meaning"].lower() or q in item["context_sentence"].lower()):
                results.append({
                    **item,
                    "topic_id": tid
                })

    return results
