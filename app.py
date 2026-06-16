from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ضع هذه البيانات في إعدادات السيرفر (Environment Variables) لحمايتها
BOT_TOKEN = os.environ.get('8819789633:AAGTOqR2p_Cxop3HP1XsnREgW3y7Ade1cQQ') # توكن البوت الخاص بك
CHAT_ID = os.environ.get('8085880852')     # الآيدي الخاص بك في تليجرام

@app.route('/')
def home():
    return "Bot Server is Running!"

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    action = data.get('action') # 'charge' أو 'withdraw'
    player_id = data.get('playerId')
    amount = data.get('amount')
    
    # تنسيق الرسالة التي ستصلك على تليجرام
    message = (f"🔔 **طلب جديد في الساحرة المستديرة**\n"
               f"👤 المعرف: `{player_id}`\n"
               f"💰 العملية: {action.upper()}\n"
               f"💵 القيمة: {amount}")

    # إرسال الطلب إلى تليجرام
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    response = requests.post(telegram_url, data=payload)
    
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "تم إرسال طلبك للإدارة"})
    else:
        return jsonify({"status": "error", "message": "فشل الاتصال بالبوت"}), 500

if __name__ == '__main__':
    app.run(debug=True)
