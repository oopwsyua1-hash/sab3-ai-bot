from flask import Flask, render_template, jsonify, request
import threading
import time
import random

app = Flask(__name__)

# إعدادات اللعبة
game_state = {
    "timer": 31,
    "last_result": None,
    "odds": {"Juve": 4, "Real": 40, "Barca": 40, "Liverpool": 12, "PSG": 12, "Milan": 6, "Bayern": 6, "ManU": 4}
}

def game_loop():
    while True:
        if game_state["timer"] > 0:
            time.sleep(1)
            game_state["timer"] -= 1
        else:
            # انتهاء الجولة - اختيار فائز عشوائي
            game_state["last_result"] = random.choice(list(game_state["odds"].keys()))
            time.sleep(3)
            game_state["timer"] = 31

threading.Thread(target=game_loop, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_data')
def get_data():
    return jsonify(game_state)

# معالجة الرهان
@app.route('/place_bet', methods=['POST'])
def place_bet():
    data = request.json
    team = data.get('team')
    amount = int(data.get('amount'))
    # هنا يجب ربط هذا بقاعدة بيانات المستخدمين
    return jsonify({"status": "success", "message": f"تم الرهان بـ {amount} على {team}"})

if __name__ == '__main__':
    app.run()
