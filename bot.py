import telebot
import requests
import os

# بياناتك
TOKEN = "8610905655:AAHdWXdDEobIshF_VWiZdN0hD5USC5bhSXo"
API_KEY = "AizaSyCnwNCe18cD_xMGb-BabcJMToCbDIKZuY"

bot = telebot.TeleBot(TOKEN)

def get_ai_answer(text):
    # الرابط المحدث والمدعوم حالياً
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": text}]}]
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        result = response.json()
        # استخراج النص من استجابة جوجل
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return "السبع يرحب بك.. حدث خطأ في الاتصال بالذكاء الاصطناعي."

@bot.message_handler(func=lambda message: True)
def reply(message):
    answer = get_ai_answer(message.text)
    bot.reply_to(message, answer)

if __name__ == "__main__":
    print("السبع بدأ بالعمل...")
    bot.remove_webhook()
    bot.infinity_polling()
