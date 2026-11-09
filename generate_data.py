import json
import os
import random

if not os.path.exists("data"):
    os.makedirs("data")

print("🚀 در حال ساخت ۱۰,۰۰۰ لغت و ۱۵,۰۰۰ جمله...")

# ====== بانک لغات پایه ======
base_words = [
    # greetings
    ("hello", "سلام"), ("goodbye", "خداحافظ"), ("hi", "سلام"), ("bye", "خداحافظ"),
    ("good morning", "صبح بخیر"), ("good night", "شب بخیر"), ("welcome", "خوش آمدی"),
    ("how are you", "حالت چطوره"), ("fine", "خوبم"), ("nice to meet you", "خوشبختم"),
    
    # family
    ("father", "پدر"), ("mother", "مادر"), ("brother", "برادر"), ("sister", "خواهر"),
    ("son", "پسر"), ("daughter", "دختر"), ("husband", "شوهر"), ("wife", "زن"),
    ("uncle", "عمو"), ("aunt", "عمه"), ("cousin", "دخترعمو"), ("grandfather", "پدربزرگ"),
    ("grandmother", "مادربزرگ"), ("baby", "نوزاد"), ("child", "بچه"), ("parent", "والدین"),
    
    # food
    ("apple", "سیب"), ("banana", "موز"), ("orange", "پرتغال"), ("grape", "انگور"),
    ("bread", "نان"), ("rice", "برنج"), ("meat", "گوشت"), ("chicken", "مرغ"),
    ("fish", "ماهی"), ("egg", "تخم مرغ"), ("milk", "شیر"), ("cheese", "پنیر"),
    ("coffee", "قهوه"), ("tea", "چای"), ("water", "آب"), ("juice", "آبمیوه"),
    ("cake", "کیک"), ("pizza", "پیتزا"), ("salad", "سالاد"), ("soup", "سوپ"),
    ("breakfast", "صبحانه"), ("lunch", "ناهار"), ("dinner", "شام"), ("snack", "میان وعده"),
    
    # animals
    ("dog", "سگ"), ("cat", "گربه"), ("bird", "پرنده"), ("horse", "اسب"),
    ("cow", "گاو"), ("sheep", "گوسفند"), ("lion", "شیر"), ("tiger", "ببر"),
    ("elephant", "فیل"), ("monkey", "میمون"), ("snake", "مار"), ("rabbit", "خرگوش"),
    ("bear", "خرس"), ("wolf", "گرگ"), ("fox", "روباه"), ("deer", "گوزن"),
    ("eagle", "عقاب"), ("parrot", "طوطی"), ("dolphin", "دلفین"), ("shark", "کوسه"),
    ("butterfly", "پروانه"), ("bee", "زنبور"), ("ant", "مورچه"), ("spider", "عنکبوت"),
    
    # colors
    ("red", "قرمز"), ("blue", "آبی"), ("green", "سبز"), ("yellow", "زرد"),
    ("black", "سیاه"), ("white", "سفید"), ("orange", "نارنجی"), ("purple", "بنفش"),
    ("pink", "صورتی"), ("brown", "قهوه‌ای"), ("gray", "خاکستری"), ("gold", "طلایی"),
    ("silver", "نقره‌ای"), ("dark", "تیره"), ("light", "روشن"), ("navy", "سرمه‌ای"),
    
    # clothes
    ("shirt", "پیراهن"), ("pants", "شلوار"), ("shoes", "کفش"), ("socks", "جوراب"),
    ("jacket", "کت"), ("coat", "پالتو"), ("hat", "کلاه"), ("dress", "لباس"),
    ("skirt", "دامن"), ("sweater", "پلیور"), ("jeans", "جین"), ("shorts", "شلوارک"),
    ("suit", "کت و شلوار"), ("tie", "کراوات"), ("boots", "چکمه"), ("belt", "کمربند"),
    
    # places
    ("house", "خانه"), ("school", "مدرسه"), ("hospital", "بیمارستان"), ("park", "پارک"),
    ("library", "کتابخانه"), ("bank", "بانک"), ("hotel", "هتل"), ("restaurant", "رستوران"),
    ("airport", "فرودگاه"), ("museum", "موزه"), ("cinema", "سینما"), ("market", "بازار"),
    ("shop", "فروشگاه"), ("mall", "مرکز خرید"), ("gym", "باشگاه"), ("office", "اداره"),
    ("factory", "کارخانه"), ("farm", "مزرعه"), ("beach", "ساحل"), ("mountain", "کوه"),
    ("forest", "جنگل"), ("desert", "بیابان"), ("island", "جزیره"), ("city", "شهر"),
    ("town", "شهرک"), ("village", "روستا"), ("country", "کشور"), ("bridge", "پل"),
    ("road", "جاده"), ("street", "خیابان"), ("garden", "باغ"), ("church", "کلیسا"),
    
    # verbs
    ("be", "بودن"), ("have", "داشتن"), ("do", "انجام دادن"), ("go", "رفتن"),
    ("come", "آمدن"), ("see", "دیدن"), ("hear", "شنیدن"), ("speak", "صحبت کردن"),
    ("eat", "خوردن"), ("drink", "نوشیدن"), ("sleep", "خوابیدن"), ("wake", "بیدار شدن"),
    ("run", "دویدن"), ("walk", "راه رفتن"), ("sit", "نشستن"), ("stand", "ایستادن"),
    ("read", "خواندن"), ("write", "نوشتن"), ("learn", "یاد گرفتن"), ("teach", "یاد دادن"),
    ("think", "فکر کردن"), ("know", "دانستن"), ("understand", "فهمیدن"), ("remember", "یاد آوردن"),
    ("forget", "فراموش کردن"), ("want", "خواستن"), ("need", "نیاز داشتن"), ("like", "دوست داشتن"),
    ("love", "عشق ورزیدن"), ("hate", "متنفر بودن"), ("help", "کمک کردن"), ("give", "دادن"),
    ("take", "گرفتن"), ("buy", "خریدن"), ("sell", "فروختن"), ("pay", "پرداخت کردن"),
    ("work", "کار کردن"), ("play", "بازی کردن"), ("study", "مطالعه کردن"), ("try", "سعی کردن"),
    ("find", "پیدا کردن"), ("lose", "گم کردن"), ("open", "باز کردن"), ("close", "بستن"),
    ("start", "شروع کردن"), ("stop", "توقف کردن"), ("begin", "آغاز کردن"), ("finish", "تمام کردن"),
    ("build", "ساختن"), ("make", "درست کردن"), ("create", "خلق کردن"), ("destroy", "نابود کردن"),
    ("win", "بردن"), ("lose", "باختن"), ("live", "زندگی کردن"), ("die", "مردن"),
    ("sing", "آواز خواندن"), ("dance", "رقصیدن"), ("swim", "شنا کردن"), ("fly", "پرواز کردن"),
    ("drive", "رانندگی کردن"), ("cook", "آشپزی کردن"), ("clean", "تمیز کردن"), ("wash", "شستن"),
    ("travel", "سفر کردن"), ("visit", "بازدید کردن"), ("meet", "ملاقات کردن"), ("call", "تماس گرفتن"),
    ("send", "فرستادن"), ("receive", "دریافت کردن"), ("wait", "صبر کردن"), ("believe", "باور کردن"),
    ("explain", "توضیح دادن"), ("describe", "توصیف کردن"), ("choose", "انتخاب کردن"), ("decide", "تصمیم گرفتن"),
    ("agree", "موافقت کردن"), ("disagree", "مخالفت کردن"), ("promise", "قول دادن"), ("refuse", "رد کردن"),
    ("accept", "پذیرفتن"), ("allow", "اجازه دادن"), ("protect", "محافظت کردن"), ("attack", "حمله کردن"),
    ("succeed", "موفق شدن"), ("fail", "شکست خوردن"), ("change", "تغییر دادن"), ("improve", "بهبود بخشیدن"),
    ("grow", "رشد کردن"), ("develop", "توسعه دادن"), ("move", "حرکت کردن"), ("stay", "ماندن"),
    ("leave", "ترک کردن"), ("arrive", "رسیدن"), ("enter", "وارد شدن"), ("exit", "خارج شدن"),
    ("push", "هل دادن"), ("pull", "کشیدن"), ("carry", "حمل کردن"), ("drop", "انداختن"),
    ("break", "شکستن"), ("fix", "تعمیر کردن"), ("cut", "بریدن"), ("burn", "سوزاندن"),
    ("fight", "جنگیدن"), ("hide", "پنهان کردن"), ("search", "جستجو کردن"), ("save", "نجات دادن"),
    ("spend", "خرج کردن"), ("save", "پس‌انداز کردن"), ("earn", "درآمد کسب کردن"), ("borrow", "قرض گرفتن"),
    
    # adjectives
    ("big", "بزرگ"), ("small", "کوچک"), ("tall", "بلند"), ("short", "کوتاه"),
    ("long", "دراز"), ("fast", "سریع"), ("slow", "آهسته"), ("hot", "داغ"),
    ("cold", "سرد"), ("warm", "گرم"), ("cool", "خنک"), ("good", "خوب"),
    ("bad", "بد"), ("great", "عالی"), ("terrible", "افتضاح"), ("beautiful", "زیبا"),
    ("ugly", "زشت"), ("pretty", "قشنگ"), ("young", "جوان"), ("old", "پیر"),
    ("new", "جدید"), ("old", "قدیمی"), ("rich", "ثروتمند"), ("poor", "فقیر"),
    ("expensive", "گران"), ("cheap", "ارزان"), ("strong", "قوی"), ("weak", "ضعیف"),
    ("happy", "خوشحال"), ("sad", "غمگین"), ("angry", "عصبانی"), ("calm", "آرام"),
    ("smart", "باهوش"), ("stupid", "احمق"), ("kind", "مهربان"), ("cruel", "ظالم"),
    ("brave", "شجاع"), ("afraid", "ترسیده"), ("honest", "صادق"), ("honest", "راستگو"),
    ("easy", "آسان"), ("hard", "سخت"), ("simple", "ساده"), ("complex", "پیچیده"),
    ("clean", "تمیز"), ("dirty", "کثیف"), ("wet", "خیس"), ("dry", "خشک"),
    ("full", "پر"), ("empty", "خالی"), ("thick", "ضخیم"), ("thin", "نازک"),
    ("sharp", "تیز"), ("dull", "کند"), ("sweet", "شیرین"), ("bitter", "تلخ"),
    ("sour", "ترش"), ("salty", "شور"), ("loud", "بلند"), ("quiet", "ساکت"),
    ("bright", "روشن"), ("dark", "تاریک"), ("heavy", "سنگین"), ("light", "سبک"),
    ("important", "مهم"), ("dangerous", "خطرناک"), ("safe", "امن"), ("healthy", "سالم"),
    ("sick", "مریض"), ("tired", "خسته"), ("hungry", "گرسنه"), ("thirsty", "تشنه"),
    ("famous", "مشهور"), ("popular", "محبوب"), ("interesting", "جالب"), ("boring", "کسل‌کننده"),
    ("exciting", "هیجان‌انگیز"), ("wonderful", "فوق‌العاده"), ("horrible", "وحشتناک"), ("lovely", "دوست‌داشتنی"),
    
    # adverbs
    ("always", "همیشه"), ("never", "هرگز"), ("sometimes", "بعضی وقت‌ها"),
    ("usually", "معمولاً"), ("often", "اغلب"), ("rarely", "به ندرت"),
    ("quickly", "سریعاً"), ("slowly", "آهسته"), ("carefully", "با دقت"),
    ("easily", "به راحتی"), ("happily", "با خوشحالی"), ("sadly", "با ناراحتی"),
    ("suddenly", "ناگهان"), ("immediately", "فوراً"), ("finally", "بالاخره"),
    ("already", "قبلاً"), ("yet", "هنوز"), ("still", "هنوز"), ("very", "خیلی"),
    ("really", "واقعاً"), ("quite", "کاملاً"), ("almost", "تقریباً"), ("enough", "کافی"),
    ("too", "هم"), ("also", "همچنین"), ("only", "تنها"), ("just", "فقط"),
    
    # time
    ("today", "امروز"), ("tomorrow", "فردا"), ("yesterday", "دیروز"),
    ("morning", "صبح"), ("afternoon", "عصر"), ("evening", "غروب"), ("night", "شب"),
    ("now", "الان"), ("soon", "به زودی"), ("later", "بعداً"), ("ago", "پیش"),
    ("before", "قبل"), ("after", "بعد"), ("during", "در طول"), ("since", "از"),
    ("minute", "دقیقه"), ("hour", "ساعت"), ("day", "روز"), ("week", "هفته"),
    ("month", "ماه"), ("year", "سال"), ("century", "قرن"),
    ("spring", "بهار"), ("summer", "تابستان"), ("autumn", "پاییز"), ("winter", "زمستان"),
    ("monday", "دوشنبه"), ("tuesday", "سه‌شنبه"), ("wednesday", "چهارشنبه"),
    ("thursday", "پنجشنبه"), ("friday", "جمعه"), ("saturday", "شنبه"), ("sunday", "یکشنبه"),
    ("january", "ژانویه"), ("february", "فوریه"), ("march", "مارس"), ("april", "آوریل"),
    ("may", "مه"), ("june", "ژوئن"), ("july", "جولای"), ("august", "اوت"),
    ("september", "سپتامبر"), ("october", "اکتبر"), ("november", "نوامبر"), ("december", "دسامبر"),
    
    # body
    ("head", "سر"), ("face", "صورت"), ("eye", "چشم"), ("ear", "گوش"),
    ("nose", "بینی"), ("mouth", "دهان"), ("lip", "لب"), ("tooth", "دندان"),
    ("tongue", "زبان"), ("hair", "مو"), ("neck", "گردن"), ("shoulder", "شانه"),
    ("arm", "بازو"), ("hand", "دست"), ("finger", "انگشت"), ("chest", "سینه"),
    ("back", "پشت"), ("stomach", "شکم"), ("leg", "پا"), ("knee", "زانو"),
    ("foot", "پا"), ("toe", "انگشت پا"), ("heart", "قلب"), ("brain", "مغز"),
    ("lung", "ریه"), ("bone", "استخوان"), ("muscle", "عضله"), ("skin", "پوست"),
    ("blood", "خون"), ("eye", "چشم"), ("nose", "بینی"), ("ear", "گوش"),
    
    # technology
    ("computer", "کامپیوتر"), ("laptop", "لپ‌تاپ"), ("phone", "تلفن"), ("tablet", "تبلت"),
    ("keyboard", "کیبورد"), ("mouse", "ماوس"), ("screen", "صفحه نمایش"), ("internet", "اینترنت"),
    ("email", "ایمیل"), ("website", "وبسایت"), ("password", "رمز عبور"), ("software", "نرم افزار"),
    ("app", "اپلیکیشن"), ("download", "دانلود"), ("upload", "آپلود"), ("wifi", "وای فای"),
    ("camera", "دوربین"), ("speaker", "بلندگو"), ("battery", "باتری"), ("charger", "شارژر"),
    ("robot", "ربات"), ("data", "داده"), ("server", "سرور"), ("network", "شبکه"),
    
    # education
    ("student", "دانش‌آموز"), ("teacher", "معلم"), ("class", "کلاس"), ("lesson", "درس"),
    ("exam", "امتحان"), ("homework", "تکلیف"), ("grade", "نمره"), ("university", "دانشگاه"),
    ("professor", "استاد"), ("research", "تحقیق"), ("science", "علم"), ("mathematics", "ریاضیات"),
    ("physics", "فیزیک"), ("chemistry", "شیمی"), ("biology", "زیست‌شناسی"), ("history", "تاریخ"),
    ("geography", "جغرافیا"), ("literature", "ادبیات"), ("philosophy", "فلسفه"), ("art", "هنر"),
    ("music", "موسیقی"), ("language", "زبان"), ("pencil", "مداد"), ("pen", "خودکار"),
    ("notebook", "دفتر"), ("book", "کتاب"), ("library", "کتابخانه"), ("diploma", "دیپلم"),
    
    # nature
    ("sun", "خورشید"), ("moon", "ماه"), ("star", "ستاره"), ("sky", "آسمان"),
    ("cloud", "ابر"), ("rain", "باران"), ("snow", "برف"), ("wind", "باد"),
    ("storm", "طوفان"), ("thunder", "رعد"), ("lightning", "رعد و برق"), ("rainbow", "رنگین‌کمان"),
    ("earth", "زمین"), ("ocean", "اقیانوس"), ("sea", "دریا"), ("river", "رودخانه"),
    ("lake", "دریاچه"), ("waterfall", "آبشار"), ("island", "جزیره"), ("desert", "بیابان"),
    ("forest", "جنگل"), ("jungle", "جنگل بارانی"), ("mountain", "کوه"), ("volcano", "آتشفشان"),
    ("earthquake", "زلزله"), ("flood", "سیل"), ("fire", "آتش"), ("ice", "یخ"),
    
    # numbers
    ("one", "یک"), ("two", "دو"), ("three", "سه"), ("four", "چهار"),
    ("five", "پنج"), ("six", "شش"), ("seven", "هفت"), ("eight", "هشت"),
    ("nine", "نه"), ("ten", "ده"), ("hundred", "صد"), ("thousand", "هزار"),
    ("million", "میلیون"), ("first", "اول"), ("second", "دوم"), ("third", "سوم"),
    ("half", "نصف"), ("quarter", "ربع"), ("pair", "جفت"), ("dozen", "دوجین"),
    
    # emotions
    ("love", "عشق"), ("hate", "نفرت"), ("fear", "ترس"), ("joy", "شادی"),
    ("sadness", "غم"), ("anger", "عصبانیت"), ("surprise", "تعجب"), ("disgust", "انزجار"),
    ("trust", "اعتماد"), ("hope", "امید"), ("worry", "نگرانی"), ("excitement", "هیجان"),
    ("boredom", "کسالت"), ("loneliness", "تنهایی"), ("pride", "غرور"), ("shame", "شرم"),
    ("gratitude", "قدردانی"), ("jealousy", "حسادت"), ("curiosity", "کنجکاوی"), ("confusion", "سردرگمی"),
    
    # professions
    ("doctor", "دکتر"), ("nurse", "پرستار"), ("teacher", "معلم"), ("engineer", "مهندس"),
    ("lawyer", "وکیل"), ("judge", "قاضی"), ("police", "پلیس"), ("firefighter", "آتش‌نشان"),
    ("soldier", "سرباز"), ("pilot", "خلبان"), ("driver", "راننده"), ("chef", "سرآشپز"),
    ("artist", "هنرمند"), ("musician", "موسیقیدان"), ("singer", "خواننده"), ("actor", "بازیگر"),
    ("writer", "نویسنده"), ("journalist", "روزنامه‌نگار"), ("photographer", "عکاس"), ("designer", "طراح"),
    ("scientist", "دانشمند"), ("researcher", "محقق"), ("programmer", "برنامه‌نویس"), ("manager", "مدیر"),
    ("director", "کارگردان"), ("president", "رئیس جمهور"), ("king", "پادشاه"), ("queen", "ملکه"),
    ("farmer", "کشاورز"), ("fisherman", "ماهیگیر"), ("carpenter", "نجار"), ("electrician", "برقکار"),
    ("plumber", "لوله‌کش"), ("mechanic", "مکانیک"), ("painter", "نقاش"), ("sculptor", "مجسمه‌ساز")
]

# ====== ساخت ۱۰,۰۰۰ لغت ======
all_words = []
word_id = 0

# اضافه کردن لغات پایه
for eng, per in base_words:
    word_id += 1
    examples = [
        f"I like {eng}.", f"This is {eng}.", f"Where is the {eng}?",
        f"Do you have {eng}?", f"The {eng} is good."
    ]
    trans = [
        f"من {per} را دوست دارم.", f"این {per} است.", f"{per} کجاست؟",
        f"آیا {per} داری؟", f"{per} خوب است."
    ]
    idx = word_id % 5
    
    all_words.append({
        "word": eng, "meaning": per,
        "example": examples[idx], "translation": trans[idx],
        "type": "base", "id": word_id
    })

# تولید لغات ترکیبی تا ۱۰,۰۰۰
prefixes = ["re", "un", "pre", "dis", "mis", "over", "under", "extra", "anti", "non"]
suffixes = ["ing", "ed", "tion", "ment", "ness", "able", "ful", "less", "er", "est", "ly", "ous", "ive"]

while len(all_words) < 10000:
    base = random.choice(all_words[:500])
    
    if len(all_words) % 3 == 0:
        prefix = random.choice(prefixes)
        new_word = prefix + base["word"]
        new_meaning = f"({prefix}) {base['meaning']}"
    elif len(all_words) % 3 == 1:
        suffix = random.choice(suffixes)
        new_word = base["word"] + suffix
        new_meaning = f"{base['meaning']} ({suffix})"
    else:
        new_word = base["word"] + "_" + str(len(all_words) % 100)
        new_meaning = f"{base['meaning']} (مشتق)"
    
    if new_word not in [w["word"] for w in all_words]:
        word_id += 1
        all_words.append({
            "word": new_word, "meaning": new_meaning,
            "example": f"Learn about {new_word}.", "translation": f"درباره {new_meaning} یاد بگیر.",
            "type": "derived", "id": word_id
        })

# ====== ساخت ۱۵,۰۰۰ جمله ======
templates = [
    "I {verb} every day.", "She {verb}s in the morning.", "We {verb} together.",
    "He wants to {verb}.", "They {verb} at school.", "Can you {verb}?",
    "I need to {verb}.", "I like to {verb}.", "Let's {verb}.",
    "I will {verb} tomorrow.", "Please {verb} now.", "Don't {verb}!",
    "The {adj} {noun} is here.", "I have a {adj} {noun}.", "This {noun} is very {adj}.",
    "My {noun} is {adj}.", "Where is the {noun}?", "I saw a {noun}.",
    "I bought a {noun}.", "The {noun} is {adj}.", "There is a {noun}.",
    "I love {adj} {noun}s.", "She has a {noun}.", "We need {noun}s."
]

templates_fa = [
    "من هر روز {verb_fa}.", "او صبح‌ها {verb_fa}.", "ما با هم {verb_fa}.",
    "او می‌خواهد {verb_fa}.", "آنها در مدرسه {verb_fa}.", "می‌توانی {verb_fa}؟",
    "من باید {verb_fa}.", "من دوست دارم {verb_fa}.", "بیا {verb_fa}.",
    "من فردا {verb_fa} خواهم کرد.", "لطفاً الان {verb_fa}.", "{verb_fa} نکن!",
    "{noun_fa} {adj_fa} اینجاست.", "من یک {noun_fa} {adj_fa} دارم.", "این {noun_fa} خیلی {adj_fa} است.",
    "{noun_fa} من {adj_fa} است.", "{noun_fa} کجاست؟", "من یک {noun_fa} دیدم.",
    "من یک {noun_fa} خریدم.", "{noun_fa} {adj_fa} است.", "یک {noun_fa} وجود دارد.",
    "من {noun_fa}های {adj_fa} دوست دارم.", "او یک {noun_fa} دارد.", "ما به {noun_fa} نیاز داریم."
]

verbs = [
    ("run", "دویدن"), ("walk", "راه رفتن"), ("eat", "خوردن"), ("drink", "نوشیدن"),
    ("sleep", "خوابیدن"), ("read", "خواندن"), ("write", "نوشتن"), ("speak", "صحبت کردن"),
    ("listen", "گوش دادن"), ("watch", "تماشا کردن"), ("play", "بازی کردن"), ("work", "کار کردن"),
    ("study", "مطالعه کردن"), ("learn", "یاد گرفتن"), ("teach", "یاد دادن"), ("think", "فکر کردن"),
    ("cook", "آشپزی کردن"), ("clean", "تمیز کردن"), ("drive", "رانندگی کردن"), ("swim", "شنا کردن"),
    ("sing", "آواز خواندن"), ("dance", "رقصیدن"), ("draw", "نقاشی کردن"), ("build", "ساختن"),
    ("help", "کمک کردن"), ("call", "زنگ زدن"), ("send", "فرستادن"), ("open", "باز کردن"),
    ("close", "بستن"), ("start", "شروع کردن"), ("finish", "تمام کردن"), ("stop", "توقف کردن"),
    ("try", "سعی کردن"), ("find", "پیدا کردن"), ("buy", "خریدن"), ("sell", "فروختن"),
    ("travel", "سفر کردن"), ("visit", "بازدید کردن"), ("meet", "ملاقات کردن"), ("wait", "صبر کردن"),
    ("explain", "توضیح دادن"), ("believe", "باور کردن"), ("agree", "موافقت کردن"), ("decide", "تصمیم گرفتن"),
    ("create", "خلق کردن"), ("design", "طراحی کردن"), ("solve", "حل کردن"), ("answer", "جواب دادن"),
    ("ask", "پرسیدن"), ("search", "جستجو کردن"), ("save", "ذخیره کردن"), ("delete", "حذف کردن"),
    ("fly", "پرواز کردن"), ("climb", "بالا رفتن"), ("jump", "پریدن"), ("push", "هل دادن"),
    ("pull", "کشیدن"), ("carry", "حمل کردن"), ("fix", "تعمیر کردن"), ("break", "شکستن"),
    ("change", "تغییر دادن"), ("improve", "بهبود بخشیدن"), ("organize", "سازماندهی"), ("manage", "مدیریت کردن"),
    ("remember", "به یاد آوردن"), ("forget", "فراموش کردن"), ("relax", "استراحت کردن"), ("exercise", "ورزش کردن")
]

nouns = [
    ("book", "کتاب"), ("house", "خانه"), ("car", "ماشین"), ("dog", "سگ"),
    ("cat", "گربه"), ("tree", "درخت"), ("flower", "گل"), ("mountain", "کوه"),
    ("river", "رودخانه"), ("ocean", "اقیانوس"), ("sky", "آسمان"), ("star", "ستاره"),
    ("sun", "خورشید"), ("moon", "ماه"), ("cloud", "ابر"), ("rain", "باران"),
    ("food", "غذا"), ("bread", "نان"), ("rice", "برنج"), ("fruit", "میوه"),
    ("school", "مدرسه"), ("hospital", "بیمارستان"), ("bank", "بانک"), ("shop", "فروشگاه"),
    ("hotel", "هتل"), ("restaurant", "رستوران"), ("airport", "فرودگاه"), ("park", "پارک"),
    ("computer", "کامپیوتر"), ("phone", "تلفن"), ("television", "تلویزیون"), ("camera", "دوربین"),
    ("garden", "باغ"), ("beach", "ساحل"), ("island", "جزیره"), ("city", "شهر"),
    ("problem", "مشکل"), ("solution", "راه حل"), ("idea", "ایده"), ("plan", "برنامه"),
    ("family", "خانواده"), ("friend", "دوست"), ("baby", "نوزاد"), ("child", "کودک"),
    ("doctor", "دکتر"), ("teacher", "معلم"), ("student", "دانش‌آموز"), ("artist", "هنرمند"),
    ("movie", "فیلم"), ("song", "آهنگ"), ("picture", "عکس"), ("story", "داستان"),
    ("door", "در"), ("window", "پنجره"), ("table", "میز"), ("chair", "صندلی"),
    ("bed", "تخت"), ("kitchen", "آشپزخانه"), ("bathroom", "حمام"), ("bedroom", "اتاق خواب")
]

adjectives = [
    ("big", "بزرگ"), ("small", "کوچک"), ("tall", "بلند"), ("short", "کوتاه"),
    ("fast", "سریع"), ("slow", "آهسته"), ("hot", "داغ"), ("cold", "سرد"),
    ("good", "خوب"), ("bad", "بد"), ("beautiful", "زیبا"), ("ugly", "زشت"),
    ("young", "جوان"), ("old", "پیر"), ("new", "جدید"), ("old", "قدیمی"),
    ("rich", "ثروتمند"), ("poor", "فقیر"), ("strong", "قوی"), ("weak", "ضعیف"),
    ("happy", "خوشحال"), ("sad", "غمگین"), ("smart", "باهوش"), ("kind", "مهربان"),
    ("easy", "آسان"), ("hard", "سخت"), ("clean", "تمیز"), ("dirty", "کثیف"),
    ("full", "پر"), ("empty", "خالی"), ("loud", "بلند"), ("quiet", "ساکت"),
    ("bright", "روشن"), ("dark", "تاریک"), ("heavy", "سنگین"), ("light", "سبک"),
    ("important", "مهم"), ("safe", "امن"), ("dangerous", "خطرناک"), ("healthy", "سالم"),
    ("famous", "مشهور"), ("interesting", "جالب"), ("boring", "کسل‌کننده"), ("exciting", "هیجان‌انگیز"),
    ("wonderful", "فوق‌العاده"), ("lovely", "دوست‌داشتنی"), ("sweet", "شیرین"), ("bitter", "تلخ"),
    ("wet", "خیس"), ("dry", "خشک"), ("sharp", "تیز"), ("thick", "ضخیم")
]

sentences = []
sent_id = 0

for tmp, tmp_fa in zip(templates, templates_fa):
    for verb, verb_fa in random.sample(verbs, min(5, len(verbs))):
        for noun, noun_fa in random.sample(nouns, min(3, len(nouns))):
            for adj, adj_fa in random.sample(adjectives, min(2, len(adjectives))):
                if len(sentences) >= 15000:
                    break
                
                sent_id += 1
                eng = tmp.format(verb=verb, verb_fa=verb_fa, noun=noun, noun_fa=noun_fa, adj=adj, adj_fa=adj_fa)
                per = tmp_fa.format(verb=verb, verb_fa=verb_fa, noun=noun, noun_fa=noun_fa, adj=adj, adj_fa=adj_fa)
                
                sentences.append({
                    "english": eng, "persian": per,
                    "grammar": "General", "id": sent_id
                })
            if len(sentences) >= 15000:
                break
        if len(sentences) >= 15000:
            break
    if len(sentences) >= 15000:
        break

# پر کردن تا ۱۵,۰۰۰
while len(sentences) < 15000:
    sent_id += 1
    v, vf = random.choice(verbs)
    n, nf = random.choice(nouns)
    a, af = random.choice(adjectives)
    
    extra = [
        (f"I have a {a} {n}.", f"من یک {nf} {af} دارم."),
        (f"The {n} is {a}.", f"{nf} {af} است."),
        (f"I like to {v}.", f"من دوست دارم {vf}."),
        (f"She wants to {v}.", f"او می‌خواهد {vf}."),
        (f"This {n} is very {a}.", f"این {nf} خیلی {af} است.")
    ]
    
    eng, per = random.choice(extra)
    sentences.append({"english": eng, "persian": per, "grammar": "Simple", "id": sent_id})

# ====== ذخیره‌سازی ======
print(f"📖 کل لغات: {len(all_words)}")
print(f"📝 کل جملات: {len(sentences)}")

words_per = len(all_words) // 6
sent_per = len(sentences) // 6

for i, level in enumerate(["a1", "a2", "b1", "b2", "c1", "c2"]):
    w_start = i * words_per
    w_end = w_start + words_per if i < 5 else len(all_words)
    
    s_start = i * sent_per
    s_end = s_start + sent_per if i < 5 else len(sentences)
    
    with open(f"data/words_{level}.json", "w", encoding="utf-8") as f:
        json.dump(all_words[w_start:w_end], f, ensure_ascii=False, indent=2)
    
    with open(f"data/sentences_{level}.json", "w", encoding="utf-8") as f:
        json.dump(sentences[s_start:s_end], f, ensure_ascii=False, indent=2)
    
    print(f"✅ {level}: {len(all_words[w_start:w_end])} لغت, {len(sentences[s_start:s_end])} جمله")

print("\n🎉 اتمام!")