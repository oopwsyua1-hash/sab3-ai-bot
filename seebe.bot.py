from flask import Flask
from threading import Thread
import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os
import random

# --- 1. نظام النبض (Keep Alive) لضمان العمل 24 ساعة ---
app = Flask('')
@app.route('/')
def home(): return "إمبراطورية السبع السوري تعمل بأقصى طاقة! 🦁"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. الإعدادات والتوكن الصحيح ---
API_TOKEN = '8783355404:AAHa0cyyFF6-gT8veO4pjOT_JRYnY9iUWNQ'
ADMIN_ID = 8085880852
bot = telebot.TeleBot(API_TOKEN)
stats = {"users": set(), "downloads": 0}

azkar = ["سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ", "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ"]

# دالة الصيد (فيديو أو صوت)
def download_content(url, mode='video'):
    ext = 'mp3' if mode == 'audio' else 'mp4'
    ydl_opts = {
        'format': 'bestaudio/best' if mode == 'audio' else 'best',
        'outtmpl': f'sab3_hunt.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    if mode == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # تصحيح الامتداد في حال تحويل الصوت
        if mode == 'audio' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return filename, info.get('title', 'محتوى السبع')

# --- 3. الواجهات والأزرار ---
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

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("🔍 بحث وصيد"),
        types.KeyboardButton("📿 ذكر اليوم"),
        types.KeyboardButton("📊 الإحصائيات"),
        types.KeyboardButton("📣 مشاركة البوت"),
        types.KeyboardButton("👨‍💻 الخال قصي (المطور)")
    )
    return markup

# --- 4. الأوامر ومعالجة الروابط ---
@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    welcome = (
        "🦁 **مرحباً بك في بوت السبع السوري** 🦁\n\n"
        "أرسل الرابط مباشرة ليتم الصيد فوراً.\n\n"
        "⚡️ بواسطة: **الخال قصي**"
    )
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')
    bot.send_message(message.chat.id, "اختر المنصة أو أرسل الرابط:", reply_markup=get_inline_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    if text.startswith("http"):
        # عند إرسال رابط، تظهر كبسات اختيار النوع فوراً
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🎬 تحميل كفيديو MP4", callback_data=f"dl_video_{text}"),
            types.InlineKeyboardButton("🎵 تحميل كصوت MP3", callback_data=f"dl_audio_{text}")
        )
        bot.reply_to(message, "🎯 **تم رصد الرابط!**\nماذا تريد أن أصيد لك؟", reply_markup=markup, parse_mode='Markdown')
    elif text == "📿 ذكر اليوم":
        bot.reply_to(message, f"✨ {random.choice(azkar)}")
    elif text == "📊 الإحصائيات":
        bot.reply_to(message, f"📊 عدد المستخدمين: {len(stats['users'])}\n📥 إجمالي التحميلات: {stats['downloads']}")
    elif text == "👨‍💻 الخال قصي (المطور)":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("تواصل مع الخال قصي 🦁", url=f"tg://user?id={ADMIN_ID}"))
        bot.reply_to(message, "يمكنك مراسلة المطور من هنا:", reply_markup=markup)

# --- 5. تنفيذ الصيد (فيديو/صوت) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "أرسل الرابط مباشرة وسأقوم بالتحميل!")
    
    elif call.data.startswith("dl_"):
        mode = 'audio' if 'audio' in call.data else 'video'
        url = call.data.replace("dl_video_", "").replace("dl_audio_", "")
        
        bot.edit_message_text("⏳ **جاري الصيد والتحميل... انتظر قليلاً**", call.message.chat.id, call.message.message_id)
        bot.send_chat_action(call.message.chat.id, 'upload_document')
        
        try:
            file_path, title = download_content(url, mode)
            with open(file_path, 'rb') as f:
                caption = f"✅ **تم الصيد بنجاح:**\n📝 {title}\n🦁 بواسطة: **الخال قصي**"
                if mode == 'video':
                    bot.send_video(call.message.chat.id, f, caption=caption, parse_mode='Markdown')
                else:
                    bot.send_audio(call.message.chat.id, f, caption=caption, parse_mode='Markdown')
            
            stats["downloads"] += 1
            if os.path.exists(file_path): os.remove(file_path)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ العذر منك، لم أستطع صيد هذا الرابط.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
