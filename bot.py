import os
import telebot
import threading
import time
import random
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
user_state = {}

try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

NASAIH = ["a", "b", "c", "d", "e"]

@bot.message_handler(commands=['start'])
def start(m):
    kb = telebot.types.ReplyKeyboardMarkup(True)
    kb.add("moyenne")
    kb.add("nasiha")
    bot.send_message(m.chat.id, "Bot V2 Ready", reply_markup=kb)

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid = m.chat.id
    txt = m.text
    if "moyenne" in txt:
        user_state[cid] = "wait"
        bot.send_message(cid, "send: 15 14 12")
        return
    if user_state.get(cid) == "wait":
        try:
            nums = [float(x) for x in txt.split()]
            moy = sum(nums) / len(nums)
            bot.send_message(cid, f"moy {moy:.2f}")
            user_state.pop(cid)
        except:
            bot.send_message(cid, "numbers only")
        return
    bot.send_message(cid, random.choice(NASAIH))

@app.route('/')
def home():
    return "Bot V2 Live!"

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
