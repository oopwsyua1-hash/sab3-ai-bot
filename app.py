from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__, template_folder='templates')

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
    print(">>> index route called") # هاد لحتى نشوف بالـ Logs
    return render_template('index.html')

@app.route('/api/crystals')
def get_crystals():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id=1")
    crystals = c.fetchone()[0]
    conn.close()
    return jsonify({'crystals': crystals})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
