import os
import json
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "8676945196:AAGw74FdxYTu6CtB3pzv4IDLRvMH_nkItCQ")

# ====== DataManager ======
class DataManager:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.users_file = f"{self.data_dir}/users.json"
        self.users = self.load_users()
    
    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id):
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                "level": "a1", "words_learned": {}, "sentences_learned": [],
                "daily_words": 0, "daily_sentences": 0, "last_reset": str(datetime.now().date()),
                "score": 0, "streak": 0, "last_active": str(datetime.now().date()),
                "achievements": [], "weak_words": [], "joined_date": str(datetime.now().date())
            }
            self.save_users()
        return self.users[user_id]
    
    def update_user(self, user_id, data):
        self.users[str(user_id)] = data
        self.save_users()
    
    def load_words(self, level):
        try:
            with open(f"{self.data_dir}/words_{level}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def load_sentences(self, level):
        try:
            with open(f"{self.data_dir}/sentences_{level}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def get_all_words_count(self):
        count = 0
        for level in ["a1", "a2", "b1", "b2", "c1", "c2"]:
            count += len(self.load_words(level))
        return count
    
    def get_all_sentences_count(self):
        count = 0
        for level in ["a1", "a2", "b1", "b2", "c1", "c2"]:
            count += len(self.load_sentences(level))
        return count

# ====== SpacedRepetition ======
class SpacedRepetition:
    INTERVALS = [1, 3, 7, 14, 30]
    
    def __init__(self):
        self.review_data = {}
    
    def add_word(self, user_id, word):
        user_id = str(user_id)
        if user_id not in self.review_data:
            self.review_data[user_id] = {}
        self.review_data[user_id][word] = {
            "level": 0, "next_review": str(datetime.now().date() + timedelta(days=1)),
            "correct_count": 0, "wrong_count": 0, "last_reviewed": str(datetime.now().date())
        }
    
    def get_words_for_review(self, user_id):
        user_id = str(user_id)
        today = str(datetime.now().date())
        review_words = []
        if user_id in self.review_data:
            for word, data in self.review_data[user_id].items():
                if data["next_review"] <= today:
                    review_words.append(word)
        return review_words
    
    def update_word(self, user_id, word, was_correct):
        user_id = str(user_id)
        if user_id in self.review_data and word in self.review_data[user_id]:
            data = self.review_data[user_id][word]
            if was_correct:
                data["correct_count"] += 1
                if data["level"] < len(self.INTERVALS) - 1:
                    data["level"] += 1
            else:
                data["wrong_count"] += 1
                data["level"] = 0
            data["last_reviewed"] = str(datetime.now().date())
            data["next_review"] = str(datetime.now().date() + timedelta(days=self.INTERVALS[data["level"]]))
    
    def get_stats(self, user_id):
        user_id = str(user_id)
        if user_id not in self.review_data:
            return {"total": 0, "mastered": 0, "learning": 0}
        total = len(self.review_data[user_id])
        mastered = sum(1 for d in self.review_data[user_id].values() if d["level"] >= 4)
        return {"total": total, "mastered": mastered, "learning": total - mastered}

# ====== AchievementSystem ======
class AchievementSystem:
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
    }
    
    def check_achievements(self, user_data):
        new_achievements = []
        user_achievements = user_data.get("achievements", [])
        words_count = len(user_data.get("words_learned", {}))
        streak = user_data.get("streak", 0)
        
        word_milestones = {"first_word": 1, "10_words": 10, "50_words": 50, "100_words": 100, "500_words": 500, "1000_words": 1000}
        for key, count in word_milestones.items():
            if words_count >= count and key not in user_achievements:
                new_achievements.append(key)
        
        streak_milestones = {"streak_3": 3, "streak_7": 7, "streak_30": 30}
        for key, count in streak_milestones.items():
            if streak >= count and key not in user_achievements:
                new_achievements.append(key)
        
        return new_achievements
    
    def get_achievement_info(self, key):
        return self.ACHIEVEMENTS.get(key, {"name": key, "desc": "", "icon": "❓"})

# ====== مقداردهی اولیه ======
dm = DataManager()
sr = SpacedRepetition()
ach = AchievementSystem()

LEVELS = {
    "a1": {"name": "🟢 A1 - مبتدی"}, "a2": {"name": "🟡 A2 - پایه"},
    "b1": {"name": "🟠 B1 - متوسط"}, "b2": {"name": "🔵 B2 - متوسط رو به بالا"},
    "c1": {"name": "🟣 C1 - پیشرفته"}, "c2": {"name": "🔴 C2 - تسلط کامل"}
}

def get_user(user_id): return dm.get_user(user_id)
def save_user(user_id, data): dm.update_user(user_id, data)

def reset_daily(user_id):
    user = get_user(user_id)
    today = str(datetime.now().date())
    if user.get("last_reset") != today:
        last_active = datetime.strptime(user.get("last_active", today), "%Y-%m-%d").date()
        yesterday = datetime.now().date() - timedelta(days=1)
        if last_active == yesterday: user["streak"] = user.get("streak", 0) + 1
        elif last_active < yesterday: user["streak"] = 0
        user["daily_words"] = 0; user["daily_sentences"] = 0
        user["last_reset"] = today; user["last_active"] = today
        save_user(user_id, user)
    return user

def get_unlearned_words(user_id, count=10):
    user = get_user(user_id)
    all_words = dm.load_words(user["level"])
    learned = set(user.get("words_learned", {}).keys())
    available = [w for w in all_words if w["word"] not in learned]
    if len(available) < count: available = all_words
    return random.sample(available, min(count, len(available))) if available else []

def get_unlearned_sentences(user_id, count=5):
    user = get_user(user_id)
    all_sentences = dm.load_sentences(user["level"])
    learned = set(user.get("sentences_learned", []))
    available = [s for s in all_sentences if s["english"] not in learned]
    if len(available) < count: available = all_sentences
    return random.sample(available, min(count, len(available))) if available else []

def build_main_menu():
    keyboard = [
        [InlineKeyboardButton("📚 لغات امروز (۱۰ عدد)", callback_data="daily_words")],
        [InlineKeyboardButton("📝 جملات امروز (۵ عدد)", callback_data="daily_sentences")],
        [InlineKeyboardButton("🔄 مرور هوشمند", callback_data="smart_review")],
        [InlineKeyboardButton("🎯 تمرین و کوئیز", callback_data="quiz_menu")],
        [InlineKeyboardButton("📊 پیشرفت من", callback_data="progress")],
        [InlineKeyboardButton("🏆 نشان‌ها", callback_data="achievements")],
        [InlineKeyboardButton("📋 گزارش روزانه", callback_data="daily_report")],
        [InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def build_quiz_menu():
    keyboard = [
        [InlineKeyboardButton("📖 معنی کلمه", callback_data="quiz_word")],
        [InlineKeyboardButton("📝 کامل کردن جمله", callback_data="quiz_sentence")],
        [InlineKeyboardButton("🔄 ترجمه جمله", callback_data="quiz_translate")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def build_level_menu():
    keyboard = [[InlineKeyboardButton(ld["name"], callback_data=f"setlevel_{lk}")] for lk, ld in LEVELS.items()]
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="settings_menu")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_data = get_user(user_id)
    welcome = f"""
🎓 **به ربات جامع آموزش زبان انگلیسی خوش اومدی!**

🔥 استریک: {user_data.get('streak', 0)} روز
📚 لغات: {len(user_data.get('words_learned', {}))}
🎯 سطح: {LEVELS[user_data.get('level', 'a1')]['name']}

📖 **{dm.get_all_words_count()}+ لغت** | 📝 **{dm.get_all_sentences_count()}+ جمله**
"""
    await update.message.reply_text(welcome, reply_markup=build_main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text("🎮 منوی اصلی:", reply_markup=build_main_menu())
    
    elif data == "daily_words":
        user = reset_daily(user_id)
        words = get_unlearned_words(user_id, 10)
        if not words:
            await query.edit_message_text("⚠️ لغتی موجود نیست.", reply_markup=build_main_menu())
            return
        
        response = f"📚 **لغات امروز**\n\n"
        wl = user.get("words_learned", {})
        for i, w in enumerate(words, 1):
            response += f"**{i}. {w['word']}** = {w['meaning']}\n   📖 {w.get('example','')}\n\n"
            wl[w["word"]] = str(datetime.now().date())
            sr.add_word(user_id, w["word"])
        
        user["words_learned"] = wl
        user["daily_words"] = user.get("daily_words", 0) + len(words)
        user["score"] = user.get("score", 0) + len(words) * 2
        
        new_ach = ach.check_achievements(user)
        for a in new_ach:
            user["achievements"] = user.get("achievements", []) + [a]
            response += f"🎉 نشان: {ach.get_achievement_info(a)['icon']} {ach.get_achievement_info(a)['name']}\n"
        
        save_user(user_id, user)
        response += f"\n✅ {len(words)} لغت | ⭐ +{len(words)*2}"
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "daily_sentences":
        user = reset_daily(user_id)
        sentences = get_unlearned_sentences(user_id, 5)
        if not sentences:
            await query.edit_message_text("⚠️ جمله‌ای نیست.", reply_markup=build_main_menu())
            return
        
        response = f"📝 **جملات امروز**\n\n"
        sl = user.get("sentences_learned", [])
        for i, s in enumerate(sentences, 1):
            response += f"**{i}.** {s['english']}\n   🔄 {s['persian']}\n\n"
            sl.append(s["english"])
        
        user["sentences_learned"] = sl
        user["daily_sentences"] = user.get("daily_sentences", 0) + len(sentences)
        user["score"] = user.get("score", 0) + len(sentences) * 3
        save_user(user_id, user)
        response += f"✅ {len(sentences)} جمله | ⭐ +{len(sentences)*3}"
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "smart_review":
        review_words = sr.get_words_for_review(user_id)
        if not review_words:
            await query.edit_message_text("🎉 همه لغات رو بلدی!", reply_markup=build_main_menu())
            return
        await query.edit_message_text(f"🔄 **{len(review_words)} کلمه برای مرور داری!**\nبرو به بخش لغات.", reply_markup=build_main_menu())
    
    elif data == "quiz_menu":
        await query.edit_message_text("🎯 انتخاب کن:", reply_markup=build_quiz_menu())
    
    elif data == "quiz_word":
        user = get_user(user_id)
        words = dm.load_words(user["level"])
        if len(words) < 4:
            await query.edit_message_text("⚠️ لغات کافی نیست.", reply_markup=build_main_menu())
            return
        word = random.choice(words)
        options = [word["meaning"]]
        others = [w for w in words if w["word"] != word["word"]]
        options.extend(random.sample([w["meaning"] for w in others], min(3, len(others))))
        random.shuffle(options)
        context.user_data["answer"] = word["meaning"]
        keyboard = [[InlineKeyboardButton(o, callback_data=f"ans_{o[:20]}")] for o in options]
        keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")])
        await query.edit_message_text(f"🎯 معنی **{word['word']}** چیه؟", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("ans_"):
        user_answer = data.replace("ans_", "")
        correct = context.user_data.get("answer", "")
        user = get_user(user_id)
        if user_answer == correct:
            user["score"] = user.get("score", 0) + 5
            response = f"✅ آفرین! ⭐ +5"
        else:
            response = f"❌ جواب: {correct}"
        save_user(user_id, user)
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "quiz_sentence":
        user = get_user(user_id)
        sentences = dm.load_sentences(user["level"])
        if len(sentences) < 2:
            await query.edit_message_text("⚠️ جملات کافی نیست.", reply_markup=build_main_menu())
            return
        s = random.choice(sentences)
        words_in = s["english"].split()
        if len(words_in) > 3:
            idx = random.randint(0, len(words_in)-1)
            missing = words_in[idx]
            words_in[idx] = "_____"
            incomplete = " ".join(words_in)
        else:
            missing = words_in[-1]
            incomplete = " ".join(words_in[:-1]) + " _____"
        context.user_data["answer"] = missing
        keyboard = [[InlineKeyboardButton("🔍 جواب", callback_data="show_ans")], [InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")]]
        await query.edit_message_text(f"📝 کامل کن:\n{incomplete}\n🔄 {s['persian']}", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "quiz_translate":
        user = get_user(user_id)
        sentences = dm.load_sentences(user["level"])
        if not sentences:
            await query.edit_message_text("⚠️ جملات کافی نیست.", reply_markup=build_main_menu())
            return
        s = random.choice(sentences)
        context.user_data["answer"] = s["english"]
        keyboard = [[InlineKeyboardButton("🔍 جواب", callback_data="show_ans")], [InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")]]
        await query.edit_message_text(f"🔄 ترجمه کن:\n📝 {s['persian']}", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "show_ans":
        answer = context.user_data.get("answer", "")
        user = get_user(user_id)
        user["score"] = user.get("score", 0) + 2
        save_user(user_id, user)
        await query.edit_message_text(f"✅ {answer}\n⭐ +2", reply_markup=build_main_menu())
    
    elif data == "progress":
        user = get_user(user_id)
        response = f"""📊 **پیشرفت**
🎯 سطح: {LEVELS[user['level']]['name']}
📚 لغات: {len(user.get('words_learned', {}))}
📝 جملات: {len(user.get('sentences_learned', []))}
⭐ امتیاز: {user.get('score', 0)}
🔥 استریک: {user.get('streak', 0)} روز
"""
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "achievements":
        user = get_user(user_id)
        ua = user.get("achievements", [])
        response = "🏆 **نشان‌ها**\n\n"
        for k, v in ach.ACHIEVEMENTS.items():
            response += f"{v['icon']} {'✅' if k in ua else '🔒'} {v['name']}\n"
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "daily_report":
        user = get_user(user_id)
        w = user.get("daily_words", 0)
        s = user.get("daily_sentences", 0)
        response = f"📋 **گزارش امروز**\n📚 لغات: {w}/10\n📝 جملات: {s}/5\n🔥 استریک: {user.get('streak', 0)}"
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "settings_menu":
        keyboard = [
            [InlineKeyboardButton("⚙️ تغییر سطح", callback_data="change_level")],
            [InlineKeyboardButton("🔄 ریست", callback_data="reset_progress")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
        ]
        await query.edit_message_text("⚙️ تنظیمات:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "change_level":
        await query.edit_message_text("🎯 سطح:", reply_markup=build_level_menu())
    
    elif data.startswith("setlevel_"):
        level = data.replace("setlevel_", "")
        user = get_user(user_id)
        user["level"] = level
        save_user(user_id, user)
        await query.edit_message_text(f"✅ سطح: {LEVELS[level]['name']}", reply_markup=build_main_menu())
    
    elif data == "reset_progress":
        user = get_user(user_id)
        user["words_learned"] = {}
        user["sentences_learned"] = []
        user["score"] = 0
        user["streak"] = 0
        save_user(user_id, user)
        await query.edit_message_text("🔄 ریست شد!", reply_markup=build_main_menu())

def main():
    print(f"📖 لغات: {dm.get_all_words_count()}")
    print(f"📝 جملات: {dm.get_all_sentences_count()}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ ربات آماده!")
    app.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    main()