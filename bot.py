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

NASAIH = ["اقرا كل يوم","نظم وقتك","ركز على هدفك","الاستمرارية"]
MOLAKHASAT = {
"رياضيات": "📐 رياضيات:\n- النهايات\n- الاشتقاق\n- التكامل",
"فيزياء": "⚛️ فيزياء:\n- F=m.a\n- الطاقة",
"علوم": "🧬 علوم:\n- الخلية\n- ADN",
"تاريخ": "📚 تاريخ:\n- ثورة 1954",
"انجليزية": "🇬🇧 انجليزية:\n- Present/Past"
}

@bot.message_handler(commands=['start'])
def start(m):
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    kb.add("moyenne", "nasiha")
    kb.add("ملخصات")
    bot.send_message(m.chat.id, "مرحبا فتحي! ✅\nاختر:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "moyenne")
def ask_moy(m):
    state[m.chat.id] = "wait"
    bot.send_message(m.chat.id, "ابعث نقاطك: 15 14 16")

@bot.message_handler(func=lambda m: m.text == "nasiha")
def send_n(m):
    bot.send_message(m.chat.id, "💡 " + random.choice(NASAIH))

@bot.message_handler(func=lambda m: m.text == "ملخصات")
def molakhas_menu(m):
    kb = telebot.types.ReplyKeyboardMarkup(True, True)
    for k in MOLAKHASAT.keys():
        kb.add(k)
    kb.add("رجوع")
    bot.send_message(m.chat.id, "اختر المادة:", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in MOLAKHASAT)
def send_mol(m):
    bot.send_message(m.chat.id, MOLAKHASAT[m.text])

@bot.message_handler(func=lambda m: m.text == "رجوع")
def back(m):
    start(m)

@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid = m.chat.id
    if state.get(cid) == "wait":
        try:
            nums = [float(x) for x in m.text.split()]
            moy = sum(nums)/len(nums)
            bot.send_message(cid, f"معدلك: {moy:.2f}")
            state.pop(cid)
        except:
            bot.send_message(cid, "ارقام فقط")
        return
    bot.send_message(cid, "دوس /start")

@app.route('/')
def home():
    return "Bot V3 Live!"

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
