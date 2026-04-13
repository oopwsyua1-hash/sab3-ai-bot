from flask import Flask
from threading import Thread
import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os
import random

# --- 1. نظام النبض للبقاء حياً على Render ---
app = Flask('')
@app.route('/')
def home(): return "إمبراطورية السبع تعمل بنجاح! 🦁"

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

# دالة التحميل المطورة لتجنب الحظر
def download_content(url, mode='video', search=False):
    ext = 'mp3' if mode == 'audio' else 'mp4'
    ydl_opts = {
        'format': 'bestaudio/best' if mode == 'audio' else 'best',
        'outtmpl': f'sab3_file.%(ext)s',
        'default_search': 'ytsearch1' if search else None,
        'quiet': True,
        'no_warnings': True,
        # إضافة User-Agent لتجنب رسالة "لم أستطع صيد الرابط"
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    if mode == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url if not search else f"ytsearch1:{url}", download=True)
        filename = ydl.prepare_filename(info)
        if mode == 'audio' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return filename, info.get('title', 'محتوى السبع')

# --- 3. الواجهات (الكبسات) ---
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
        types.KeyboardButton("👨‍💻 السبع (المطور)")
    )
    return markup

# --- 4. معالجة الرسائل ---
@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    welcome = (
        "🦁 **مرحباً بك في بوت السبع السوري** 🦁\n\n"
        "يوتيوب، إنستغرام، تيك توك، فيسبوك، والمزيد.\n\n"
        "📌 **فقط أرسل الرابط مباشرة للتحميل فوراً.**\n\n"
        "⚡️ بواسطة: **السبع ابو نمر**"
    )
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')
    bot.send_message(message.chat.id, "اختر المنصة أو أرسل الرابط:", reply_markup=get_inline_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    stats["users"].add(message.from_user.id)

    if text.startswith("http"):
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🎬 فيديو MP4", callback_data=f"dl_video_{text}"),
            types.InlineKeyboardButton("🎵 صوت MP3", callback_data=f"dl_audio_{text}")
        )
        bot.reply_to(message, "🎯 **تم رصد الهدف!** اختر الصيغة المطلوبة:", reply_markup=markup, parse_mode='Markdown')
    
    elif text == "📿 ذكر اليوم":
        bot.reply_to(message, f"✨ {random.choice(azkar)}")
    
    elif text == "📊 الإحصائيات":
        bot.reply_to(message, f"📊 المستخدمين: {len(stats['users'])}\n📥 التحميلات: {stats['downloads']}")
    
    elif text == "👨‍💻 السبع (المطور)":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("تواصل مع السبع ابو نمر 🦁", url=f"tg://user?id={ADMIN_ID}"))
        bot.reply_to(message, "يمكنك مراسلة المطور مباشرة:", reply_markup=markup)
    
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚀 ابدأ البحث والصيد", callback_data=f"sr_{text}"))
        bot.reply_to(message, f"🔎 هل تبحث عن: *{text}*؟", reply_markup=markup, parse_mode='Markdown')

# --- 5. تنفيذ الصيد (فيديو/صوت) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "أرسل الرابط مباشرة وسأقوم بالصيد!")
    
    elif call.data.startswith(("dl_", "sr_")):
        mode = 'audio' if 'audio' in call.data else 'video'
        is_search = call.data.startswith("sr_")
        query = call.data.replace("dl_video_", "").replace("dl_audio_", "").replace("sr_", "")
        
        bot.edit_message_text("⏳ **جاري الصيد والتحميل... انتظر قليلاً**", call.message.chat.id, call.message.message_id)
        
        try:
            file_path, title = download_content(query, mode, search=is_search)
            with open(file_path, 'rb') as f:
                caption = f"✅ **تم الصيد:** {title}\n🦁 بواسطة: **السبع ابو نمر**"
                if mode == 'video':
                    bot.send_video(call.message.chat.id, f, caption=caption, parse_mode='Markdown')
                else:
                    bot.send_audio(call.message.chat.id, f, caption=caption, parse_mode='Markdown')
            
            stats["downloads"] += 1
            if os.path.exists(file_path): os.remove(file_path)
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            bot.send_message(call.message.chat.id, "❌ العذر منك، لم أستطع صيد هذا الرابط. تأكد منه مجدداً.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
