import telebot
from flask import Flask

# بياناتك التي أرسلتها لي
TOKEN = "8559531063:AAHn-_tRhF3GTAevMpZd4IhU0bP2tC4hy9k"
MY_ID = "8085880852"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    # هذا يرسل لك رسالة تليجرام فوراً عند فتح السيرفر
    bot.send_message(MY_ID, "👑 سيرفر السبع الملكي بدأ العمل بنجاح!")
    return "<h1>Sabaa Server is Active ✅</h1>"

if __name__ == "__main__":
    # هذا البورت ضروري ليعمل السيرفر على Render
    app.run(host="0.0.0.0", port=10000)
