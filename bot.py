import telebot
from telebot import types
import os

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
        bot.send_message(message.chat.id, f"معدلك هو: {moy:.2f} ✅")
    except:
        bot.send_message(message.chat.id, "خطأ ❌ ابعت هكا: 12 14 13")

@bot.message_handler(func=lambda m: True)
def all_msg(message):
    bot.send_message(message.chat.id, "اكتب /start")

print("Bot running...")
bot.infinity_polling()
