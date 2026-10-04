import os
import threading
import sqlite3
import time
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive! ⛏️"

conn = sqlite3.connect('miners.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, balance INTEGER, last_mine REAL, referrals INTEGER)')
conn.commit()

def get_user(uid):
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    return c.fetchone()

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    name = m.from_user.username or m.from_user.first_name
    if not get_user(uid):
        c.execute("INSERT INTO users VALUES (?,?,?,?,?)", (uid, name, 100, 0, 0))
        conn.commit()
    bot.send_message(m.chat.id, f"أهلا {name} في منجم HAMMAMET ⛏️\nهدية: 100 عملة\n/mine - عدّن كل 6 سوايع\n/balance - شوف رصيدك")

@bot.message_handler(commands=['mine'])
def mine(m):
    u = get_user(m.from_user.id)
    if not u: return
    now = time.time()
    if now - u[3] < 21600:
        bot.send_message(m.chat.id, f"⏳ مازال {(21600 - (now - u[3]))/60:.0f} دقيقة"); return
    c.execute("UPDATE users SET balance=balance+50, last_mine=? WHERE user_id=?", (now, m.from_user.id))
    conn.commit()
    bot.send_message(m.chat.id, "✅ عدنت 50 HAMMAMET!")

@bot.message_handler(commands=['balance'])
def bal(m):
    u = get_user(m.from_user.id)
    bot.send_message(m.chat.id, f"💼 رصيدك: {u[2]} HAMMAMET")

def run_bot():
    try: bot.remove_webhook()
    except: pass
    bot.infinity_polling()

threading.Thread(target=run_bot).start()
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))