import os
import json
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from data_manager import DataManager
from spaced_repetition import SpacedRepetition
from achievements import AchievementSystem

# ====== توکن (از environment variable خونده میشه) ======
TOKEN = os.environ.get("BOT_TOKEN", "8676945196:AAGw74FdxYTu6CtB3pzv4IDLRvMH_nkItCQ")

# ====== سیستم‌ها ======
dm = DataManager()
sr = SpacedRepetition()
ach = AchievementSystem()

# ====== سطوح ======
LEVELS = {
    "a1": {"name": "🟢 A1 - مبتدی", "words_per_day": 10, "sentences_per_day": 5},
    "a2": {"name": "🟡 A2 - پایه", "words_per_day": 10, "sentences_per_day": 5},
    "b1": {"name": "🟠 B1 - متوسط", "words_per_day": 10, "sentences_per_day": 5},
    "b2": {"name": "🔵 B2 - متوسط رو به بالا", "words_per_day": 10, "sentences_per_day": 5},
    "c1": {"name": "🟣 C1 - پیشرفته", "words_per_day": 10, "sentences_per_day": 5},
    "c2": {"name": "🔴 C2 - تسلط کامل", "words_per_day": 10, "sentences_per_day": 5}
}

# ====== توابع کمکی ======
def get_user(user_id):
    return dm.get_user(user_id)

def save_user(user_id, data):
    dm.update_user(user_id, data)

def reset_daily(user_id):
    user = get_user(user_id)
    today = str(datetime.now().date())
    if user.get("last_reset") != today:
        last_active = datetime.strptime(user.get("last_active", today), "%Y-%m-%d").date()
        yesterday = datetime.now().date() - timedelta(days=1)
        
        if last_active == yesterday:
            user["streak"] = user.get("streak", 0) + 1
        elif last_active < yesterday:
            user["streak"] = 0
        
        user["daily_words"] = 0
        user["daily_sentences"] = 0
        user["last_reset"] = today
        user["last_active"] = today
        save_user(user_id, user)
    return user

def get_unlearned_words(user_id, count=10):
    user = get_user(user_id)
    level = user["level"]
    all_words = dm.load_words(level)
    learned = set(user.get("words_learned", {}).keys())
    available = [w for w in all_words if w["word"] not in learned]
    
    if len(available) < count:
        available = all_words
    
    if not available:
        return []
    
    return random.sample(available, min(count, len(available)))

def get_unlearned_sentences(user_id, count=5):
    user = get_user(user_id)
    level = user["level"]
    all_sentences = dm.load_sentences(level)
    learned = set(user.get("sentences_learned", []))
    available = [s for s in all_sentences if s["english"] not in learned]
    
    if len(available) < count:
        available = all_sentences
    
    if not available:
        return []
    
    return random.sample(available, min(count, len(available)))

def get_review_words(user_id, count=5):
    review_list = sr.get_words_for_review(user_id)
    if len(review_list) > count:
        review_list = random.sample(review_list, count)
    
    user = get_user(user_id)
    level = user["level"]
    all_words = dm.load_words(level)
    
    result = []
    for word in review_list:
        word_info = next((w for w in all_words if w["word"] == word), None)
        if word_info:
            result.append(word_info)
    
    return result

# ====== منوها ======
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
        [InlineKeyboardButton("🎯 تطبیق کلمه", callback_data="quiz_match")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def build_level_menu():
    keyboard = []
    for lk, ld in LEVELS.items():
        keyboard.append([InlineKeyboardButton(ld["name"], callback_data=f"setlevel_{lk}")])
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="settings_menu")])
    return InlineKeyboardMarkup(keyboard)

def build_settings_menu():
    keyboard = [
        [InlineKeyboardButton("⚙️ تغییر سطح", callback_data="change_level")],
        [InlineKeyboardButton("📊 آمار کامل", callback_data="full_stats")],
        [InlineKeyboardButton("🔄 ریست پیشرفت", callback_data="reset_progress")],
        [InlineKeyboardButton("🔙 برگشت", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== Handlerها ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    user_data = get_user(user_id)
    level = user_data.get("level", "a1")
    streak = user_data.get("streak", 0)
    total_words = len(user_data.get("words_learned", {}))
    total_sentences = len(user_data.get("sentences_learned", []))
    
    welcome = f"""
🎓 **به ربات جامع آموزش زبان انگلیسی خوش اومدی {user.first_name}!**

🔥 **استریک فعلی:** {streak} روز
📚 **لغات یادگرفته:** {total_words}
📝 **جملات یادگرفته:** {total_sentences}
🎯 **سطح:** {LEVELS[level]['name']}

✨ **امکانات پیشرفته:**
• 📚 ۱۰ لغت جدید روزانه با مثال
• 📝 ۵ جمله کاربردی با ترجمه
• 🔄 مرور هوشمند (Spaced Repetition)
• 🎯 ۴ نوع تمرین مختلف
• 🏆 سیستم نشان‌های افتخار
• 📊 نمودار پیشرفت
• 🔥 پیگیری استریک روزانه

🎮 شروع کن 👇
"""
    await update.message.reply_text(welcome, reply_markup=build_main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text("🎮 **منوی اصلی:**", reply_markup=build_main_menu())
    
    elif data == "daily_words":
        user = reset_daily(user_id)
        words = get_unlearned_words(user_id, 10)
        
        if not words:
            await query.edit_message_text("⚠️ لغتی موجود نیست.", reply_markup=build_main_menu())
            return
        
        response = f"📚 **لغات امروز - {LEVELS[user['level']]['name']}**\n\n"
        words_learned = user.get("words_learned", {})
        
        for i, w in enumerate(words, 1):
            response += f"**{i}. {w['word']}** = {w['meaning']}\n"
            response += f"   📖 {w.get('example', '')}\n"
            response += f"   🔄 {w.get('translation', '')}\n\n"
            words_learned[w["word"]] = str(datetime.now().date())
            sr.add_word(user_id, w["word"])
        
        user["words_learned"] = words_learned
        user["daily_words"] = user.get("daily_words", 0) + len(words)
        user["score"] = user.get("score", 0) + len(words) * 2
        
        new_ach = ach.check_achievements(user)
        if new_ach:
            for a in new_ach:
                a_info = ach.get_achievement_info(a)
                user["achievements"] = user.get("achievements", []) + [a]
                response += f"\n🎉 **نشان جدید:** {a_info['icon']} {a_info['name']}!"
        
        save_user(user_id, user)
        
        response += f"\n✅ {len(words)} لغت اضافه شد | ⭐ +{len(words)*2} امتیاز"
        response += f"\n📊 امروز: {user['daily_words']}/10 | 🔥 استریک: {user.get('streak', 0)} روز"
        
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "daily_sentences":
        user = reset_daily(user_id)
        sentences = get_unlearned_sentences(user_id, 5)
        
        if not sentences:
            await query.edit_message_text("⚠️ جمله‌ای موجود نیست.", reply_markup=build_main_menu())
            return
        
        response = f"📝 **جملات امروز - {LEVELS[user['level']]['name']}**\n\n"
        sent_learned = user.get("sentences_learned", [])
        
        for i, s in enumerate(sentences, 1):
            response += f"**{i}.** {s['english']}\n"
            response += f"   🔄 {s['persian']}\n"
            if s.get('grammar'):
                response += f"   📚 {s['grammar']}\n"
            response += "\n"
            sent_learned.append(s["english"])
        
        user["sentences_learned"] = sent_learned
        user["daily_sentences"] = user.get("daily_sentences", 0) + len(sentences)
        user["score"] = user.get("score", 0) + len(sentences) * 3
        save_user(user_id, user)
        
        response += f"✅ {len(sentences)} جمله اضافه شد | ⭐ +{len(sentences)*3} امتیاز"
        
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "smart_review":
        user = get_user(user_id)
        review_words = get_review_words(user_id, 5)
        
        if not review_words:
            await query.edit_message_text(
                "🎉 هیچ کلمه‌ای برای مرور امروز نداری!\nهمه لغات رو خوب بلدی! 👏",
                reply_markup=build_main_menu()
            )
            return
        
        response = "🔄 **مرور هوشمند امروز**\n\n"
        for i, w in enumerate(review_words, 1):
            response += f"**{i}. {w['word']}**\n"
            response += f"   معنی: {w['meaning']}\n"
            response += f"   مثال: {w.get('example', '')}\n\n"
        
        stats = sr.get_stats(user_id)
        response += f"\n📊 آمار مرور: {stats['mastered']} مسلط | {stats['learning']} در حال یادگیری"
        
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "quiz_menu":
        await query.edit_message_text("🎯 **انتخاب نوع تمرین:**", reply_markup=build_quiz_menu())
    
    elif data == "quiz_word":
        user = get_user(user_id)
        level = user["level"]
        words = dm.load_words(level)
        
        if len(words) < 4:
            await query.edit_message_text("⚠️ لغات کافی نیست.", reply_markup=build_main_menu())
            return
        
        word = random.choice(words)
        options = [word["meaning"]]
        others = [w for w in words if w["word"] != word["word"]]
        options.extend(random.sample([w["meaning"] for w in others], min(3, len(others))))
        random.shuffle(options)
        
        context.user_data["quiz_answer"] = word["meaning"]
        context.user_data["quiz_word"] = word["word"]
        
        keyboard = []
        for opt in options:
            keyboard.append([InlineKeyboardButton(opt, callback_data=f"ans_{opt[:20]}")])
        keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")])
        
        response = f"🎯 **معنی این کلمه چیه؟**\n\n📖 **{word['word']}**"
        await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "quiz_sentence":
        user = get_user(user_id)
        level = user["level"]
        sentences = dm.load_sentences(level)
        
        if len(sentences) < 2:
            await query.edit_message_text("⚠️ جملات کافی نیست.", reply_markup=build_main_menu())
            return
        
        sentence = random.choice(sentences)
        words_in = sentence["english"].split()
        if len(words_in) > 3:
            idx = random.randint(0, len(words_in)-1)
            missing = words_in[idx]
            words_in[idx] = "_____"
            incomplete = " ".join(words_in)
        else:
            missing = words_in[-1]
            incomplete = " ".join(words_in[:-1]) + " _____"
        
        context.user_data["quiz_answer"] = missing
        context.user_data["quiz_sentence"] = sentence["english"]
        
        keyboard = [
            [InlineKeyboardButton("🔍 جواب", callback_data="show_answer")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")]
        ]
        
        response = f"📝 **جمله رو کامل کن:**\n\n{incomplete}\n\n🔄 {sentence['persian']}"
        await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "quiz_translate":
        user = get_user(user_id)
        level = user["level"]
        sentences = dm.load_sentences(level)
        
        if not sentences:
            await query.edit_message_text("⚠️ جملات کافی نیست.", reply_markup=build_main_menu())
            return
        
        sentence = random.choice(sentences)
        context.user_data["quiz_answer"] = sentence["english"]
        
        keyboard = [
            [InlineKeyboardButton("🔍 جواب", callback_data="show_answer")],
            [InlineKeyboardButton("🔙 برگشت", callback_data="quiz_menu")]
        ]
        
        response = f"🔄 **ترجمه کن به انگلیسی:**\n\n📝 {sentence['persian']}"
        await query.edit_message_text(response, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data == "quiz_match":
        user = get_user(user_id)
        level = user["level"]
        words = dm.load_words(level)
        
        if len(words) < 3:
            await query.edit_message_text("⚠️ لغات کافی نیست.", reply_markup=build_main_menu())
            return
        
        match_words = random.sample(words, min(3, len(words)))
        
        response = "🎯 **کلمه رو به معنی وصل کن:**\n\n"
        for i, w in enumerate(match_words, 1):
            response += f"{i}. {w['word']}\n"
        response += "\n"
        meanings = [w["meaning"] for w in match_words]
        random.shuffle(meanings)
        for j, m in enumerate(meanings, 1):
            response += f"{chr(64+j)}) {m}\n"
        
        response += "\n✍️ جواب رو تو پیام بعدی بگو! (مثال: 1a, 2b, 3c)"
        
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "show_answer":
        answer = context.user_data.get("quiz_answer", "")
        
        if "quiz_sentence" in context.user_data:
            full = context.user_data.get("quiz_sentence", "")
            response = f"✅ **جواب:** {answer}\n📝 جمله: {full}"
        else:
            response = f"✅ **ترجمه:** {answer}"
        
        response += "\n\n⭐ +2 امتیاز"
        user = get_user(user_id)
        user["score"] = user.get("score", 0) + 2
        
        new_ach = ach.check_achievements(user)
        if new_ach:
            for a in new_ach:
                a_info = ach.get_achievement_info(a)
                user["achievements"] = user.get("achievements", []) + [a]
                response += f"\n🎉 نشان: {a_info['icon']} {a_info['name']}"
        
        save_user(user_id, user)
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data.startswith("ans_"):
        user_answer = data.replace("ans_", "")
        correct = context.user_data.get("quiz_answer", "")
        
        user = get_user(user_id)
        
        if user_answer == correct:
            user["score"] = user.get("score", 0) + 5
            response = f"✅ **آفرین!** 🎉\n\n⭐ +5 امتیاز\n🏆 کل: {user['score']}"
            sr.update_word(user_id, context.user_data.get("quiz_word", ""), True)
        else:
            response = f"❌ **اشتباه**\n✅ درست: {correct}"
            sr.update_word(user_id, context.user_data.get("quiz_word", ""), False)
            weak = user.get("weak_words", [])
            if context.user_data.get("quiz_word") not in weak:
                weak.append(context.user_data.get("quiz_word"))
            user["weak_words"] = weak
        
        save_user(user_id, user)
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "progress":
        user = get_user(user_id)
        level = user["level"]
        words_count = len(user.get("words_learned", {}))
        sent_count = len(user.get("sentences_learned", []))
        weak_count = len(user.get("weak_words", []))
        ach_count = len(user.get("achievements", []))
        sr_stats = sr.get_stats(user_id)
        
        response = f"""
📊 **گزارش پیشرفت**

🎯 سطح: {LEVELS[level]['name']}
📚 لغات: {words_count} (مسلط: {sr_stats['mastered']})
📝 جملات: {sent_count}
⚠️ لغات ضعیف: {weak_count}
🏆 نشان‌ها: {ach_count}
⭐ امتیاز: {user.get('score', 0)}
🔥 استریک: {user.get('streak', 0)} روز
📅 لغات امروز: {user.get('daily_words', 0)}/10
📅 جملات امروز: {user.get('daily_sentences', 0)}/5
"""
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "achievements":
        user = get_user(user_id)
        user_ach = user.get("achievements", [])
        
        response = "🏆 **نشان‌های شما**\n\n"
        
        all_ach = ach.ACHIEVEMENTS
        earned = 0
        for key, info in all_ach.items():
            status = "✅" if key in user_ach else "🔒"
            response += f"{info['icon']} {status} {info['name']}: {info['desc']}\n"
            if key in user_ach:
                earned += 1
        
        response += f"\n🎖️ {earned}/{len(all_ach)} نشان دریافت شده"
        
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "daily_report":
        user = get_user(user_id)
        today = str(datetime.now().date())
        words_today = user.get("daily_words", 0)
        sent_today = user.get("daily_sentences", 0)
        
        if user.get("last_reset") != today:
            words_today = 0
            sent_today = 0
        
        remaining_words = 10 - words_today
        remaining_sent = 5 - sent_today
        
        response = f"""
📋 **گزارش امروز** ({datetime.now().strftime('%Y/%m/%d')})

📚 لغات: {words_today}/10 {"✅ کامل" if words_today >= 10 else f"⏳ {remaining_words} تا باقی‌مونده"}
📝 جملات: {sent_today}/5 {"✅ کامل" if sent_today >= 5 else f"⏳ {remaining_sent} تا باقی‌مونده"}
🔥 استریک: {user.get('streak', 0)} روز
⭐ امتیاز امروز: {words_today * 2 + sent_today * 3}

{"🎉 امروز رو کامل کردی! آفرین!" if words_today >= 10 and sent_today >= 5 else "💪 ادامه بده، هنوز تموم نشده!"}
"""
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "settings_menu":
        await query.edit_message_text("⚙️ **تنظیمات:**", reply_markup=build_settings_menu())
    
    elif data == "change_level":
        await query.edit_message_text("🎯 **سطح جدید رو انتخاب کن:**", reply_markup=build_level_menu())
    
    elif data.startswith("setlevel_"):
        level = data.replace("setlevel_", "")
        user = get_user(user_id)
        user["level"] = level
        user["words_learned"] = {}
        user["sentences_learned"] = []
        user["daily_words"] = 0
        user["daily_sentences"] = 0
        user["weak_words"] = []
        save_user(user_id, user)
        
        await query.edit_message_text(
            f"✅ سطح به **{LEVELS[level]['name']}** تغییر کرد!",
            reply_markup=build_main_menu()
        )
    
    elif data == "full_stats":
        user = get_user(user_id)
        level = user["level"]
        
        response = f"""
📊 **آمار کامل**

🎯 سطح: {LEVELS[level]['name']}
📚 کل لغات: {len(user.get('words_learned', {}))}
📝 کل جملات: {len(user.get('sentences_learned', []))}
⚠️ لغات ضعیف: {len(user.get('weak_words', []))}
🏆 نشان‌ها: {len(user.get('achievements', []))}
⭐ امتیاز: {user.get('score', 0)}
🔥 بهترین استریک: {user.get('streak', 0)}
📖 لغات مسلط: {sr.get_stats(user_id)['mastered']}
"""
        await query.edit_message_text(response, reply_markup=build_main_menu())
    
    elif data == "reset_progress":
        keyboard = [
            [InlineKeyboardButton("⚠️ بله، مطمئنم", callback_data="confirm_reset")],
            [InlineKeyboardButton("🔙 لغو", callback_data="settings_menu")]
        ]
        await query.edit_message_text(
            "⚠️ **هشدار:** با این کار همه پیشرفتت پاک میشه!\nمطمئنی؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "confirm_reset":
        user = get_user(user_id)
        user["words_learned"] = {}
        user["sentences_learned"] = []
        user["score"] = 0
        user["weak_words"] = []
        user["streak"] = 0
        user["achievements"] = []
        save_user(user_id, user)
        
        await query.edit_message_text("🔄 همه چیز ریست شد.", reply_markup=build_main_menu())

# ====== راه‌اندازی ======
def main():
    print("🎓 ربات پیشرفته آموزش زبان انگلیسی")
    print(f"📖 لغات: {dm.get_all_words_count()}")
    print(f"📝 جملات: {dm.get_all_sentences_count()}")
    print(f"👥 کاربران: {len(dm.users)}")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ ربات آماده و در حال اجراست!")
    app.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    main()