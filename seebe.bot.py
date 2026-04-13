from flask import Flask
from threading import Thread
import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os
import random

# --- 1. نظام النبض (Keep Alive) للبقاء حياً 24 ساعة ---
app = Flask('')
@app.route('/')
def home(): return "إمبراطورية السبع السوري تعمل! 🦁"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. الإعدادات ---
API_TOKEN = '8783355404:AAHa0cyyFF6-gT8veO4pjOT_JRYnY9iUWNQ'
ADMIN_ID = 8085880852
bot = telebot.TeleBot(API_TOKEN)
stats = {"users": set(), "downloads": 0}

azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"]

def download_content(url, mode='video', search=False):
    ext = 'mp3' if mode == 'audio' else 'mp4'
    ydl_opts = {
        'format': 'bestaudio/best' if mode == 'audio' else 'best',
        'outtmpl': f'sab3_file.%(ext)s',
        'default_search': 'ytsearch1' if search else None,
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url if not search else f"ytsearch1:{url}", download=True)
        filename = ydl.prepare_filename(info)
        return filename, info.get('title', 'محتوى السبع')

# --- 3. تصميم الكبسات (الواجهة اللي تحبها) ---
def get_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = [
        types.InlineKeyboardButton("اليوتيوب 🔴", callback_data="info"),
        types.InlineKeyboardButton("الانستغرام 📸", callback_data="info"),
        types.InlineKeyboardButton("الفيسبوك 💙", callback_data="info"),
        types.InlineKeyboardButton("تيك توك ✨", callback_data="info"),
        types.InlineKeyboardButton("تويتر (X) 🐦", callback_data="info"),
        types.InlineKeyboardButton("سناب شات 💛", callback_data="info"),
        types.InlineKeyboardButton("بينترست 📌", callback_data="info"),
        types.InlineKeyboardButton("لايكي ✨", callback_data="info")
    ]
    markup.add(*btns)
    return markup

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🔍 بحث وصيد"),
        types.KeyboardButton("📿 ذكر اليوم"),
        types.KeyboardButton("📊 الإحصائيات"),
        types.KeyboardButton("📣 مشاركة البوت"),
        types.KeyboardButton("👨‍💻 السبع (المطور)")
    )
    return markup

# --- 4. الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    welcome = (
        "🦁 **مرحباً بك في بوت السبع السوري** 🦁\n\n"
        "يوتيوب، إنستغرام، تيك توك، تويتر (X)، فيسبوك،\n"
        "بينترست، لايكي، سناب شات.\n\n"
        "📌 **الاستخدام في الخاص:**\n"
        "فقط أرسل الرابط مباشرة إلى البوت ليتم التحميل فوراً.\n\n"
        "⚡️ بواسطة: **الخال قصي**"
    )
    bot.reply_to(message, welcome, reply_markup=main_menu_keyboard(), parse_mode='Markdown')
    bot.send_message(message.chat.id, "اختر المنصة أو أرسل الرابط مباشرة:", reply_markup=get_inline_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text
    stats["users"].add(message.from_user.id)

    if text == "📿 ذكر اليوم":
        bot.reply_to(message, f"✨ {random.choice(azkar)}")
    elif text == "📊 الإحصائيات":
        bot.reply_to(message, f"📊 مستخدمين: {len(stats['users'])}\n📥 تحميلات: {stats['downloads']}")
    elif text == "👨‍💻 السبع (المطور)":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("تواصل مع السبع 🦁", url=f"tg://user?id={ADMIN_ID}"))
        bot.reply_to(message, "تواصل مع المطور مباشرة:", reply_markup=markup)
    elif text.startswith("http"):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🎬 فيديو MP4", callback_data=f"dl_video_{text}"),
            types.InlineKeyboardButton("🎵 صوت MP3", callback_data=f"dl_audio_{text}")
        )
        bot.reply_to(message, "🎯 تم رصد الهدف! اختر الصيغة:", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚀 ابدأ البحث والصيد", callback_data=f"sr_{text}"))
        bot.reply_to(message, f"🔎 هل تبحث عن: *{text}*؟", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "💡 أرسل الرابط وسأقوم بصيده تلقائياً!")
    elif call.data.startswith(("dl_", "sr_")):
        # كود التحميل والإرسال...
        bot.edit_message_text("⏳ جاري الصيد... انتظر يا وحش", call.message.chat.id, call.message.message_id)
        # (نفس دالة التحميل السابقة لضمان الإرسال)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
