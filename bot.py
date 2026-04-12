import telebot
import requests
import os
from flask import Flask, request

# بياناتك
TOKEN = "8610905655:AAHdWXdDEobIshF_VWiZdDosLgQcpND_vlM"
API_KEY = "AIzaSyCnwNCe18cD_xMGb-BabcCJmT0cbDIKZuY"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def get_ai_answer(text):
    # استخدام المسار المستقر v1beta لتجنب خطأ الموديل
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": text}]}]}
    try:
        response = requests.post(url, json=data, timeout=30)
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "السبع يرحب بك.. السيرفر مشغول قليلاً."

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, get_ai_answer(message.text))

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    return "The Sab3-Bot is Live!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
