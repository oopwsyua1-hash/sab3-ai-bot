import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os

# توكن البوت الخاص بك
API_TOKEN = '8783355404:AAHa0cyyFF6-gT8veO4pjOT_JRYnY9iUWNQ'
bot = telebot.TeleBot(API_TOKEN)

# دالة التحميل الذكية
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@bot.message_handler(commands=['start'])
def start(message):
    # تصميم الأزرار كما في الصورة
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_yt = types.InlineKeyboardButton("اليوتيوب 🔴", callback_data="info")
    btn_ig = types.InlineKeyboardButton("الانستقرام 📸", callback_data="info")
    btn_fb = types.InlineKeyboardButton("الفيسبوك 💙", callback_data="info")
    btn_tk = types.InlineKeyboardButton("تيك توك 🖤", callback_data="info")
    btn_x = types.InlineKeyboardButton("تويتر (X) 🐦", callback_data="info")
    btn_sc = types.InlineKeyboardButton("سناب شات 💛", callback_data="info")
    btn_pn = types.InlineKeyboardButton("بنترست 📌", callback_data="info")
    btn_ly = types.InlineKeyboardButton("لايكي ✨", callback_data="info")
    
    markup.add(btn_yt, btn_ig, btn_fb, btn_tk, btn_x, btn_sc, btn_pn, btn_ly)

    welcome_text = (
        "🦁 **مرحباً بك في بوت السبع السوري** 🦁\n\n"
        "يوتيوب، إنستغرام، تيك توك، تويتر (X)، فيسبوك، بنترست، لايكي، سناب شات.\n\n"
        "📌 **الاستخدام في الخاص:**\n"
        "فقط أرسل الرابط مباشرة إلى البوت ليتم التحميل فوراً.\n\n"
        "بواسطة: **السبع ابو نمر** ⚡️"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.answer_callback_query(call.id, "أرسل الرابط وسأقوم بصيده تلقائياً! 🦁")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if url.startswith("http"):
        process_msg = bot.reply_to(message, "جاري الصيد من المنصة.. انتظر قليلاً 🛠️🦁")
        try:
            download_video(url)
            with open('video.mp4', 'rb') as video:
                bot.send_video(
                    message.chat.id, 
                    video, 
                    caption="✅ تم الصيد بنجاح بواسطة: **السبع السوري** 🦁🇸🇾\nالمطور: **Al-Khal Qusai**"
                )
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, process_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"عذراً يا وحش، حدث خطأ: {str(e)}", message.chat.id, process_msg.message_id)
    else:
        bot.reply_to(message, "أرسل رابطاً صحيحاً لنبدأ العمل 😒")

if __name__ == "__main__":
    print("بوت السبع السوري يعمل الآن...")
    bot.infinity_polling()
