import os
import telebot
from flask import Flask
import threading
import time

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# مسح الـ Webhook باش ما يصيرش Conflict 409
try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 حساب المعدل", "📚 بنك البحوث")
    markup.add("⏰ تنظيم الوقت", "💡 نصائح للتفوق")
    bot.send_message(msg.chat.id, "أهلا فتحي! البوت يخدم 🔥\nاختر 👇", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(msg):
    t = msg.text
    if "معدل" in t:
        bot.send_message(msg.chat.id, "ابعثلي العلامات: مثال\n16 15 14 13")
    elif "بحوث" in t:
        bot.send_message(msg.chat.id, "📚 بنك البحوث قريبا...")
    elif "الوقت" in t:
        bot.send_message(msg.chat.id, "⏰ 25 د قراية / 5 د راحة")
    elif "نصائح" in t:
        bot.send_message(msg.chat.id, "💡 اقرا كل يوم ولو شوية!")
    else:
        bot.send_message(msg.chat.id, "اختار من القائمة 👇")

@app.route('/')
def index():
    return "Bot is Live!"

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
