from flask import Flask
from threading import Thread
import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os
import random

# --- 1. نظام النبض (Keep Alive) لضمان العمل 24 ساعة على Render ---
app = Flask('')

@app.route('/')
def home():
    return "إمبراطورية السبع السوري تعمل بأقصى طاقة! 🦁"

def run():
    # Render يستخدم بورتات متغيرة، هذا السطر يضمن التوافق
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. الإعدادات وتصحيح التوكن ---
API_TOKEN = '8783355404:AAHa0cyyFF6-gT8veO4pjOT_JRYnY9iUWNQ' # التوكن الصحيح الذي أرسلته
ADMIN_ID = 8085880852
bot = telebot.TeleBot(API_TOKEN)
stats = {"users": set(), "downloads": 0}

# قائمة أذكار لزيادة الأجر
azkar = [
    "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ ، سُبْحَانَ اللَّهِ الْعَظِيمِ",
    "لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
    "اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ",
    "أستغفر الله العظيم وأتوب إليه"
]

def download_content(url, mode='video', search=False):
    ext = 'mp3' if mode == 'audio' else 'mp4'
    ydl_opts = {
        'format': 'bestaudio/best' if mode == 'audio' else 'best',
        'outtmpl': f'sab3_file.%(ext)s',
        'default_search': 'ytsearch1' if search else None,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if mode == 'audio' else []
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url if not search else f"ytsearch1:{url}", download=True)
        filename = ydl.prepare_filename(info)
        if mode == 'audio' and not filename.endswith('.mp3'):
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        return filename, info.get('title', 'محتوى السبع')

# --- 3. تصميم الكبسات الرئيسية ---
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

# --- 4. الأوامر والرسائل ---
@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    welcome = (
        "👑 **أهلاً بك في بوت السبع السوري الإمبراطوري** 👑\n"
        "━━━━━━━━━━━━━━\n"
        "مرحبـاً بك يا وحش! أنا رفيقك لتحميل المحتوى من:\n"
        "يوتيوب 🎥 | تيك توك 🎵 | فيسبوك 💙 | إنستا 📸\n\n"
        "استخدم الكبسات أدناه للتحكم الكامل 👇"
    )
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text
    stats["users"].add(message.from_user.id)

    if text == "🔍 بحث وصيد":
        bot.reply_to(message, "🔎 أرسل الآن اسم الأغنية أو الفيديو الذي تبحث عنه.")
    
    elif text == "📿 ذكر اليوم":
        bot.reply_to(message, f"✨ **ذكر اليوم:**\n\n {random.choice(azkar)} ")

    elif text == "📊 الإحصائيات":
        msg = f"📊 **إحصائيات إمبراطورية السبع:**\n👤 المستخدمين: {len(stats['users'])}\n📥 عمليات الصيد: {stats['downloads']}"
        bot.reply_to(message, msg)

    elif text == "📣 مشاركة البوت":
        bot.reply_to(message, f"🚀 انشر البوت لأصدقائك:\nhttps://t.me/{bot.get_me().username}")

    elif text == "👨‍💻 السبع (المطور)":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("تواصل مع السبع 🦁", url=f"tg://user?id={ADMIN_ID}"))
        bot.reply_to(message, "يمكنك التواصل مع المطور مباشرة:", reply_markup=markup)

    elif text.startswith("http"):
        bot.send_chat_action(message.chat.id, 'typing')
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("🎬 فيديو MP4", callback_data=f"dl_video_{text}"),
            types.InlineKeyboardButton("🎵 صوت MP3", callback_data=f"dl_audio_{text}")
        )
        bot.reply_to(message, "🎯 **تم رصد الهدف!** اختر الصيغة:", reply_markup=markup, parse_mode='Markdown')
    
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚀 ابدأ عملية الصيد", callback_data=f"sr_{text}"))
        bot.reply_to(message, f"🔎 هل تقصد البحث عن: *{text}*؟", reply_markup=markup, parse_mode='Markdown')

# --- 5. المعالجة الداخلية والتحميل ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.send_chat_action(call.message.chat.id, 'upload_document')
    mode = 'audio' if 'audio' in call.data else 'video'
    is_search = call.data.startswith("sr_")
    query = call.data.replace("dl_video_", "").replace("dl_audio_", "").replace("sr_", "")
    
    bot.edit_message_text("⏳ **جاري الصيد... السبع يعمل لأجلك**", call.message.chat.id, call.message.message_id)
    
    try:
        file_p, title = download_content(query, mode, search=is_search)
        with open(file_p, 'rb') as f:
            cap = f"✅ **تم الصيد:** {title}\n👑 **بواسطة: السبع السوري**"
            if mode == 'video': bot.send_video(call.message.chat.id, f, caption=cap, parse_mode='Markdown')
            else: bot.send_audio(call.message.chat.id, f, caption=cap, parse_mode='Markdown')
        
        stats["downloads"] += 1
        if os.path.exists(file_p): os.remove(file_p)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ حدث خطأ يا وحش: {str(e)}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
