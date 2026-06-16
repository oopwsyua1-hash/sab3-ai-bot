from flask import Flask, render_template, request, jsonify
import sqlite3, random, time

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, crystals INTEGER DEFAULT 1000)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/bet', methods=['POST'])
def bet():
    data = request.json
    team = data.get('team')
    amount = int(data.get('amount', 0))

    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id=1")
    row = c.fetchone()
    crystals = row[0] if row else 1000

    if amount > crystals:
        return jsonify({'error': 'الكرستال غير كافي'}), 400

    crystals -= amount
    win = random.choice([True, False])
    multiplier = random.choice([4, 6, 12, 40]) if win else 0
    win_amount = amount * multiplier

    if win:
        crystals += win_amount

    c.execute("INSERT OR REPLACE INTO users (id, crystals) VALUES (1,?)", (crystals,))
    conn.commit()
    conn.close()

    return jsonify({
        'win': win,
        'multiplier': multiplier,
        'win_amount': win_amount,
        'crystals': crystals
    })

@app.route('/api/crystals')
def get_crystals():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id=1")
    row = c.fetchone()
    crystals = row[0] if row else 1000
    conn.close()
    return jsonify({'crystals': crystals})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
