import telebot
from telebot import types
from flask import Flask
from threading import Thread
from yt_dlp import YoutubeDL
import os, random

# --- نظام النبض ---
app = Flask('')
@app.route('/')
def home(): return "إمبراطورية السبع تعمل! 🦁"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- الإعدادات (التوكن الصحيح) ---
API_TOKEN = '8783355404:AAHa0cyyFF6-gT8veO4pjOT_JRYnY9iUWNQ'
ADMIN_ID = 8085880852
bot = telebot.TeleBot(API_TOKEN)
active_chatters = set()

# --- دالة الصيد المطورة ---
def download_content(url, mode='video'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'sab3_file.%(ext)s',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info), info.get('title', 'محتوى السبع')

# --- الأزرار والقوائم ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("💬 دخول الدردشة", "🔍 بحث وصيد", "📿 ذكر اليوم", "❌ خروج", "👨‍💻 المطور")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🦁 **أهلاً بك في إمبراطورية السبع**\nصيد ودردشة في مكان واحد!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    uid = message.from_user.id
    text = message.text

    if text == "💬 دخول الدردشة":
        active_chatters.add(uid)
        bot.reply_to(message, "🔥 دخلت دردشة الوحوش! شاركنا أفكارك.")
    elif text == "❌ خروج":
        active_chatters.discard(uid)
        bot.reply_to(message, "👋 خرجت من الدردشة.")
    elif text.startswith("http"):
        # خيارات الصيد (فيديو/صوت)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎬 فيديو", callback_data=f"v_{text}"), 
                   types.InlineKeyboardButton("🎵 صوت", callback_data=f"a_{text}"))
        bot.reply_to(message, "🎯 رصدت الهدف! ماذا نصيد؟", reply_markup=markup)
    elif uid in active_chatters:
        # إرسال الرسالة للجميع
        for user in active_chatters:
            if user != uid: bot.send_message(user, f"👤 **وحش يقول:**\n{text}")
    elif text == "📿 ذكر اليوم":
        bot.reply_to(message, f"✨ {random.choice(['سبحان الله', 'الحمد لله'])}")

# (أضف هنا معالج الـ callback للتحميل كما في الأكواد السابقة)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
