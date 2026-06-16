from flask import Flask, render_template, request, jsonify, session
import sqlite3, random, datetime, uuid

app = Flask(__name__)
app.secret_key = "غير_هاد_السر_لشي_قوي_عندك"

def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, coins INTEGER, last_claim TEXT)''')
    conn.commit()
    conn.close()
init_db()

TEAMS = [
    {"name":"النسر", "multiplier":40},
    {"name":"الأسد", "multiplier":12},
    {"name":"الذئب", "multiplier":12},
    {"name":"الصقر", "multiplier":6},
    {"name":"الفهد", "multiplier":6},
    {"name":"الثعلب", "multiplier":4},
    {"name":"الدب", "multiplier":4},
    {"name":"النمر", "multiplier":4},
]

@app.route('/')
def index():
    if 'user_id' not in session:
        conn = sqlite3.connect('game.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (coins, last_claim) VALUES (100,?)",
                  (datetime.date.today().isoformat(),))
        session['user_id'] = c.lastrowid
        conn.commit()
        conn.close()
    return render_template('index.html', teams=TEAMS)

@app.route('/claim_daily')
def claim_daily():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT last_claim, coins FROM users WHERE id=?", (session['user_id'],))
    last, coins = c.fetchone()
    if last!= datetime.date.today().isoformat():
        coins += 100
        c.execute("UPDATE users SET coins=?, last_claim=? WHERE id=?",
                  (coins, datetime.date.today().isoformat(), session['user_id']))
        conn.commit()
    conn.close()
    return jsonify({"coins": coins, "msg":"تم استلام 100 كونزة مجاني"})

@app.route('/buy_package', methods=['POST'])
def buy_package():
    # هون بتربط Stripe أو PayPal
    # حالياً رح نزيد الكونزات دايركت للتجربة
    data = request.json
    package = data['package'] # 100, 600, 1500

    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT coins FROM users WHERE id=?", (session['user_id'],))
    coins = c.fetchone()[0] + package
    c.execute("UPDATE users SET coins=? WHERE id=?", (coins, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({"coins": coins, "msg":f"تم شحن {package} كونزة"})

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    team_index = int(data['team'])
    bet = int(data['bet'])

    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT coins FROM users WHERE id=?", (session['user_id'],))
    coins = c.fetchone()[0]

    if coins < bet:
        return jsonify({"error":"كونزاتك ما بتكفي"})

    # نسبة ربح انت بتتحكم فيها. 48% ربح = هامش ربح إلك 4%
    win = random.random() < 0.48

    if win:
        multiplier = TEAMS[team_index]["multiplier"]
        coins = coins - bet + (bet * multiplier)
        result = f"مبروك ربحت x{multiplier}"
    else:
        coins = coins - bet
        result = "حظ أوفر المرة الجاية"

    c.execute("UPDATE users SET coins=? WHERE id=?", (coins, session['user_id']))
    conn.commit()
    conn.close()

    return jsonify({"result": result, "coins": coins})

if __name__ == '__main__':
    app.run(debug=True)
