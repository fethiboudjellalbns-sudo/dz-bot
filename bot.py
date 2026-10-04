import os
from flask import Flask, request
import telebot
from telebot import types
app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("🧮 حساب المعدل", "📚 بنك البحوث", "📅 تنظيم الوقت", "💡 نصائح للتفوق")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🇩🇿 أهلا بيك في بوت الطالب الجزائري 🤖\n\nاختار من القائمة لتحت 👇", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: "حساب المعدل" in m.text)
def mo3adal(message):
    bot.send_message(message.chat.id, "📊 ابعتلي نقاطك هكا: 16 12 15 14 وانا نحسبلك المعدل")

@bot.message_handler(func=lambda m: "بنك البحوث" in m.text)
def bo7outh(message):
    bot.send_message(message.chat.id, "📚 بنك البحوث:\n\n1. بحث الذكاء الاصطناعي\n2. بحث التنمية المستدامة\n3. بحث التسويق الرقمي\n\nاكتب اسم البحث")

@bot.message_handler(func=lambda m: "تنظيم الوقت" in m.text)
def wa9t(message):
    bot.send_message(message.chat.id, "📅 خطة المراجعة:\nصباح: حفظ\nمساء: فهم\nليل: مراجعة خفيفة")

@bot.message_handler(func=lambda m: "نصائح" in m.text)
def nasa2i7(message):
    bot.send_message(message.chat.id, "💡 نصائح:\n✅ نام 7 سوايع\n✅ ما تحفظش ليلة الرعد\n✅ اشرح لصاحبك")

@bot.message_handler(func=lambda m: True)
def calc(message):
    try:
        nums = [float(x) for x in message.text.split() if x.replace('.','',1).isdigit()]
        if len(nums)>=2:
            bot.send_message(message.chat.id, f"✅ معدلك هو: {sum(nums)/len(nums):.2f}")
    except: pass

@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode('UTF-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def home():
    return "Bot is alive!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))