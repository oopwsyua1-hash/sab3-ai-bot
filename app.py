from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # هذا ضروري جداً ليسمح للعبة بالاتصال بالسيرفر

# البيانات تُجلب من إعدادات Render (Environment Variables)
BOT_TOKEN = os.environ.get('8819789633:AAGTOqR2p_Cxop3HP1XsnREgW3y7Ade1cQQ')
CHAT_ID = os.environ.get('8085880852')

@app.route('/', methods=['GET'])
def home():
    return "Bot Server is Running!"

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    action = data.get('action') # 'charge' أو 'withdraw'
    player_id = data.get('playerId')
    amount = data.get('amount')
    
    # تنسيق الرسالة التي ستصلك
    message = (f"🔔 **طلب جديد من الساحرة**\n"
               f"👤 المعرف: `{player_id}`\n"
               f"💰 العملية: {action.upper()}\n"
               f"💵 القيمة: {amount}")

    # إرسال إلى تليجرام
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, json={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
    
    if res.status_code == 200:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run()
