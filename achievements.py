from datetime import datetime

class AchievementSystem:
    """سیستم نشان‌های افتخار"""
    
    ACHIEVEMENTS = {
        "first_word": {"name": "🌱 اولین قدم", "desc": "اولین لغت رو یاد گرفتی!", "icon": "🌱"},
        "10_words": {"name": "📚 کتاب‌خوان", "desc": "۱۰ لغت یاد گرفتی!", "icon": "📚"},
        "50_words": {"name": "📖 دانشجو", "desc": "۵۰ لغت یاد گرفتی!", "icon": "📖"},
        "100_words": {"name": "🎓 دانش‌آموخته", "desc": "۱۰۰ لغت یاد گرفتی!", "icon": "🎓"},
        "500_words": {"name": "🧠 نابغه", "desc": "۵۰۰ لغت یاد گرفتی!", "icon": "🧠"},
        "1000_words": {"name": "👑 استاد", "desc": "۱۰۰۰ لغت یاد گرفتی!", "icon": "👑"},
        "streak_3": {"name": "🔥 ۳ روز", "desc": "۳ روز پشت سر هم مطالعه کردی!", "icon": "🔥"},
        "streak_7": {"name": "💪 ۷ روز", "desc": "یک هفته کامل مطالعه کردی!", "icon": "💪"},
        "streak_30": {"name": "⭐ ۳۰ روز", "desc": "یک ماه کامل مطالعه کردی!", "icon": "⭐"},
        "perfect_quiz": {"name": "🎯 تیرانداز", "desc": "کوئیز رو بدون اشتباه جواب دادی!", "icon": "🎯"},
        "all_levels": {"name": "🏆 قهرمان", "desc": "همه سطوح رو کامل کردی!", "icon": "🏆"}
    }
    
    def check_achievements(self, user_data):
        """بررسی و اعطای نشان‌های جدید"""
        new_achievements = []
        user_achievements = user_data.get("achievements", [])
        words_count = len(user_data.get("words_learned", {}))
        streak = user_data.get("streak", 0)
        
        # بررسی نشان‌های تعداد لغت
        word_milestones = {
            "first_word": 1, "10_words": 10, "50_words": 50,
            "100_words": 100, "500_words": 500, "1000_words": 1000
        }
        
        for key, count in word_milestones.items():
            if words_count >= count and key not in user_achievements:
                new_achievements.append(key)
        
        # بررسی نشان‌های استریک
        streak_milestones = {"streak_3": 3, "streak_7": 7, "streak_30": 30}
        for key, count in streak_milestones.items():
            if streak >= count and key not in user_achievements:
                new_achievements.append(key)
        
        return new_achievements
    
    def get_achievement_info(self, key):
        return self.ACHIEVEMENTS.get(key, {"name": key, "desc": "", "icon": "❓"})