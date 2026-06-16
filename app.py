from flask import Flask, render_template, jsonify
import time
import threading
import random

app = Flask(__name__)

# بيانات اللعبة
game_state = {
    "timer": 31,
    "last_result": "None"
}

# حلقة اللعبة (تحديث الوقت والنتائج)
def game_loop():
    while True:
        if game_state["timer"] > 0:
            time.sleep(1)
            game_state["timer"] -= 1
        else:
            # انتهاء الجولة: اختيار فائز عشوائي
            teams = ["Real Madrid", "Barcelona", "Liverpool", "PSG", "Juventus", "Man Utd"]
            game_state["last_result"] = random.choice(teams)
            time.sleep(3) # فترة راحة بين الجولات
            game_state["timer"] = 31

threading.Thread(target=game_loop, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_data')
def get_data():
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
