from flask import Flask, jsonify
import time
import threading
import random

app = Flask(__name__)

# متغيرات اللعبة
game_state = {
    "timer": 31,
    "last_result": None
}

def game_loop():
    while True:
        if game_state["timer"] > 0:
            time.sleep(1)
            game_state["timer"] -= 1
        else:
            # انتهاء الوقت: توليد نتيجة عشوائية
            teams = ["Real Madrid", "Barcelona", "Liverpool", "PSG", "Juventus", "Man Utd", "Bayern"]
            game_state["last_result"] = random.choice(teams)
            game_state["timer"] = 31 # إعادة التوقيت

# تشغيل حلقة اللعبة في الخلفية
threading.Thread(target=game_loop, daemon=True).start()

@app.route('/')
def index():
    return jsonify({
        "message": "Game Server is Running",
        "timer": game_state["timer"],
        "last_result": game_state["last_result"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
