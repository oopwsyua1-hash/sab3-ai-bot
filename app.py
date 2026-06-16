from flask import Flask, render_template, jsonify, request
import threading, time, random, sqlite3

app = Flask(__name__)

# إنشاء قاعدة بيانات حقيقية للعبة
def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS game (id INTEGER PRIMARY KEY, balance INTEGER)')
    c.execute('INSERT OR IGNORE INTO game (id, balance) VALUES (1, 1000000)')
    conn.commit()
    conn.close()

init_db()

game_state = {"timer": 31, "last_result": "None", "is_active": True}

def game_engine():
    while True:
        if game_state["timer"] > 0:
            time.sleep(1)
            game_state["timer"] -= 1
        else:
            teams = ["ريال", "برشلونة", "باريس", "ليفربول", "ميلان", "بايرن", "يوفنتوس", "يونايتد"]
            game_state["last_result"] = random.choice(teams)
            time.sleep(5)
            game_state["timer"] = 31

threading.Thread(target=game_engine, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(game_state)

@app.route('/bet', methods=['POST'])
def bet():
    data = request.json
    return jsonify({"status": "تم تأكيد الرهان", "team": data['team']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
