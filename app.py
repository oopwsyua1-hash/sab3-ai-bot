from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3, random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, crystals INTEGER DEFAULT 1000)')
    c.execute('INSERT OR IGNORE INTO users (id, crystals) VALUES (1, 1000)')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/bet', methods=['POST'])
def bet():
    data = request.json
    amount = int(data.get('amount', 0))

    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id=1")
    crystals = c.fetchone()[0]

    if amount > crystals:
        return jsonify({'error': 'الكرستال غير كافي'}), 400

    crystals -= amount
    win = random.random() < 0.45 # 45% نسبة فوز
    multipliers = {'x40':40, 'x12':12, 'x6':6, 'x4':4}
    mult = random.choice(list(multipliers.values())) if win else 0
    win_amount = amount * mult

    if win: crystals += win_amount
    c.execute("UPDATE users SET crystals=? WHERE id=1", (crystals,))
    conn.commit()
    conn.close()

    return jsonify({'win': win, 'multiplier': mult, 'crystals': crystals})

@app.route('/api/crystals')
def get_crystals():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    crystals = c.execute("SELECT crystals FROM users WHERE id=1").fetchone()[0]
    conn.close()
    return jsonify({'crystals': crystals})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
