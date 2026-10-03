from flask import Flask
import threading
import os
import telebot
from telebot import types

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 حساب المعدل", "🔍 بحث")
    bot.send_message(message.chat.id, "مرحبا بيك في بوت dz-bot 🤖", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📚 حساب المعدل")
def ask_moy(message):
    bot.send_message(message.chat.id, "ابعتلي معدلاتك: 12 14 15.5")
    bot.register_next_step_handler(message, calc_moy)

def calc_moy(message):
    try:
        notes = [float(x) for x in message.text.split()]
        moy = sum(notes) / len(notes)
        bot.send_message(message.chat.id, f"معدلك هو : {moy:.2f} ✅")
    except:
        bot.send_message(message.chat.id, "خطأ ❌ ابعت هكا: 12 14 13")

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    bot.send_message(message.chat.id, "اكتب /start")

def run_bot():
    print("Bot running...")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
