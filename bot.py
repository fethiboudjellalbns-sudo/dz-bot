import os
import telebot
from flask import Flask
import threading

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 حساب المعدل", "📚 بنك البحوث")
    markup.add("⏰ تنظيم الوقت", "💡 نصائح للتفوق")
    bot.send_message(msg.chat.id, "مرحبا فتحي! البوت يخدم ✅\nاختر:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(msg):
    t = msg.text
    if "معدل" in t:
        bot.send_message(msg.chat.id, "أرسل معدلاتك مثلا: 14 15 16")
    elif "بحوث" in t:
        bot.send_message(msg.chat.id, "بنك البحوث جاهز")
    elif "الوقت" in t:
        bot.send_message(msg.chat.id, "25د قراية 5د راحة")
    else:
        bot.send_message(msg.chat.id, "اكتب /start")

@app.route('/')
def index():
    return "Bot is Live!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
