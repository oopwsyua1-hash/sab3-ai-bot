import os
from flask import Flask
from telethon import TelegramClient, events

# إعدادات السيرفر لـ Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Sabaa Server is Live!"

# إعدادات البوت (استبدل القيم ببياناتك من my.telegram.org)
API_ID = 1234567  # ضع API ID الخاص بك هنا
API_HASH = 'your_api_hash' # ضع API HASH الخاص بك هنا
BOT_TOKEN = '8559531063:AAHn-_tRhF3GTAevMpZd4IhU0bP2tC4hy9k'

bot = TelegramClient('sabaa_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('👑 أهلاً بك في نسخة بوت السبع المعدلة!')

if __name__ == '__main__':
    # تشغيل البوت في الخلفية
    import threading
    threading.Thread(target=lambda: bot.run_until_disconnected()).start()
    
    # تشغيل السيرفر على بورت Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
