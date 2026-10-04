import os, telebot, threading, time, random
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
state = {}

try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

NASAIH = [
"اقرا كل يوم",
"نظم وقتك",
"ركز على هدفك",
"لا تقارن نفسك",
"الاستمرارية مفتاح النجاح",
"نم باكرا",
"راجع دروسك"
]

@bot.message_handler(commands=['start'])
def start(m):
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.add("moyenne", "nasiha")
    bot.send_message(m.chat.id, "مرحبا فتحي! البوت يخدم ✅\nاختر:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "moyenne")
def ask_moy(m):
    state[m.chat.id] = "wait"
    bot.send_message(m.chat.id, "ابعثلي نقاطك هكا: 15 14 16")

@bot.message_handler(func=lambda m: m.text == "nasiha")
def send_n(m):
    bot.send_message(m.chat.id, "💡 " + random.choice(NASAIH))

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid = m.chat.id
    if state.get(cid) == "wait":
        try:
            nums = [float(x) for x in m.text.split()]
            moy = sum(nums) / len(nums)
            bot.send_message(cid, f"معدلك: {moy:.2f}")
            state.pop(cid)
        except:
            bot.send_message(cid, "ارقام فقط: 15 14 12")
        return
    bot.send_message(cid, "دوس /start")

@app.route('/')
def home():
    return "Live!"

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
