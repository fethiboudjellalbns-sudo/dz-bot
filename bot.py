import os, telebot, random
from flask import Flask
import threading, time

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
user_state = {}

try:
    bot.remove_webhook()
    time.sleep(1)
except:
    pass

NASAIH = [
    "💡 اقرا كل يوم ولو 30 دقيقة، الاستمرارية أهم من الكمية!",
    "🎯 حدد هدفك من الصباح: واش راح تكمل اليوم؟",
    "📵 حط تيليفونك في وضع صامت كي تقرا، التركيز هو السر!",
    "🧠 اشرح الدرس لصاحبك، إذا فهمتو معناها انت فهمتو 100%",
    "☕️ نوض بكري، ساعة قراية الصباح = 3 ساعات في الليل",
    "📝 لخص دروسك بيدك، الكتابة تثبت المعلومة 10 مرات"
]

@bot.message_handler(commands=['start'])
def start(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📊 حساب المعدل", "📚 بنك البحوث")
    markup.add("⏰ تنظيم الوقت", "💡 نصائح للتفوق")
    bot.send_message(msg.chat.id, "🔥 أهلا فتحي! بوت الطالب الجزائري V2\n\nاختر من القائمة 👇", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(msg):
    chat_id = msg.chat.id
    t = msg.text

    if "معدل" in t:
        user_state[chat_id] = "moyenne"
        bot.send_message(chat_id, "📊 **حساب المعدل**\n\nابعثلي علاماتك مفصولة بفراغ:\nمثال: `15 14 12.5 16 13`\n\nوأنا نحسبلك المعدل فورا!")
        return

    if chat_id in user_state and user_state[chat_id] == "moyenne":
        try:
            notes = [float(x.replace(',', '.')) for x in t.split()]
            moy = sum(notes) / len(notes)
            if moy >= 10:
                res = f"✅ معدلك: **{moy:.2f}/20**\n🎉 ناجح! الله يبارك فتحي!"
            else:
                res = f"⚠️ معدلك: **{moy:.2f}/20**\n💪 مازال كاين أمل، شد حيلك!"
            bot.send_message(chat_id, res, parse_mode="Markdown")
            del user_state[chat_id]
        except:
            bot.send_message(chat_id, "❌ خطأ! ابعث أرقام فقط مفصولة بفراغ\nمثال: 15 14 12")
        return

    if "بحوث" in t:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📄 بحث التنمية المستدامة", url="https://t.me/"))
        markup.add(telebot.types.InlineKeyboardButton("📄 بحث التلوث", url="https://t.me/"))
        bot.send_message(chat_id, "📚 **بنك البحوث الجاهزة**\n\nاختر البحث:", reply_markup=markup)
    elif "الوقت" in t:
        bot.send_message(chat_id, "⏰ **طريقة Pomodoro للمراجعة**\n\n1️⃣ اقرا 25 دقيقة تركيز كامل\n2️⃣ راحة 5 دقائق\n3️⃣ عاود 4 مرات\n4️⃣ راحة طويلة 30 دقيقة\n\nجربها اليوم راح تشوف الفرق!")
    elif "نصائح" in t:
        bot.send_message(chat_id, random.choice(NASAIH))
    else:
        bot.send_message(chat_id, "اختار من الأزرار لتحت 👇")

@app.route('/')
def index(): return "Bot V2 Live!"

def run_bot():
    bot.remove_webhook()
    time.sleep(2)
    bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))