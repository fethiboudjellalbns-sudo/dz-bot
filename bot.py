import telebot, sqlite3, os, time, threading
from flask import Flask
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot V2 Live! ⛏️ HAMMAMET"

# --- قاعدة البيانات ---
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, balance INTEGER, last_mine REAL, ref_by INTEGER)''')
# محاولة إضافة عمود الإحالة إذا كان الجدول قديم
try:
    c.execute("ALTER TABLE users ADD COLUMN ref_by INTEGER")
    conn.commit()
except:
    pass

def get_main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("⛏️ تعدين"),
        types.KeyboardButton("💼 رصيدي")
    )
    markup.add(
        types.KeyboardButton("👥 رابط الإحالة"),
        types.KeyboardButton("🏆 المتصدرين")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    user_id = m.from_user.id
    name = m.from_user.first_name
    ref_id = None
    # إذا دخل برابط إحالة
    parts = m.text.split()
    if len(parts) > 1:
        try:
            ref_id = int(parts[1])
            if ref_id == user_id: ref_id = None
        except: pass

    c.execute("SELECT id FROM users WHERE id=?", (user_id,))
    is_new = c.fetchone() is None

    if is_new:
        c.execute("INSERT INTO users (id, balance, last_mine, ref_by) VALUES (?,?,?,?)", (user_id, 100, 0, ref_id))
        if ref_id:
            c.execute("UPDATE users SET balance = balance + 50 WHERE id=?", (ref_id,))
            try:
                bot.send_message(ref_id, f"🎉 مبروك! صديقك {name} دخل برابطك، ربحت 50 عملة!")
            except: pass
        conn.commit()
        bot.send_message(user_id, f"أهلا {name} في منجم HAMMAMET ⛏️\n\n🎁 هديتك: 100 عملة\n\nدوس على الأزرار لتحت باش تعدّن 👇", reply_markup=get_main_markup())
    else:
        bot.send_message(user_id, f"مرحبا بعودتك {name} 👋\nدوس تعدين باش تربح!", reply_markup=get_main_markup())

@bot.message_handler(func=lambda m: m.text == "⛏️ تعدين")
@bot.message_handler(commands=['mine'])
def mine(m):
    user_id = m.from_user.id
    c.execute("SELECT last_mine, balance FROM users WHERE id=?", (user_id,))
    data = c.fetchone()
    if not data:
        bot.send_message(user_id, "دير /start أولا", reply_markup=get_main_markup())
        return
    last_mine, bal = data
    now = time.time()
    wait = 21600 # 6 سوايع

    if now - last_mine < wait:
        remain = wait - (now - last_mine)
        h = int(remain // 3600)
        mn = int((remain % 3600) // 60)
        bot.send_message(user_id, f"⏳ مازال تستنى {h} ساعة و {mn} دقيقة باش تعاود تعدّن!")
        return

    new_bal = bal + 50
    c.execute("UPDATE users SET balance=?, last_mine=? WHERE id=?", (new_bal, now, user_id))
    conn.commit()
    bot.send_message(user_id, f"✅ عدّنت 50 HAMMAMET!\n💼 رصيدك الجديد: {new_bal} عملة")

@bot.message_handler(func=lambda m: m.text == "💼 رصيدي")
@bot.message_handler(commands=['balance'])
def bal(m):
    c.execute("SELECT balance FROM users WHERE id=?", (m.from_user.id,))
    row = c.fetchone()
    balance = row[0] if row else 0
    bot.send_message(m.from_user.id, f"💼 رصيدك: {balance} HAMMAMET\n\nاستمر في التعدين كل 6 سوايع!")

@bot.message_handler(func=lambda m: m.text == "👥 رابط الإحالة")
def ref_link(m):
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start={m.from_user.id}"
    # نحسب شحال جاب
    c.execute("SELECT COUNT(*) FROM users WHERE ref_by=?", (m.from_user.id,))
    count = c.fetchone()[0]
    bot.send_message(m.from_user.id, f"🔗 رابط الإحالة تاعك:\n\n{link}\n\n👥 جبت: {count} أشخاص\n💰 تربح 50 عملة على كل واحد يدخل!\n\nابعثو لصحابك في حمامات!")

@bot.message_handler(func=lambda m: m.text == "🏆 المتصدرين")
@bot.message_handler(commands=['top'])
def top(m):
    c.execute("SELECT id, balance FROM users ORDER BY balance DESC LIMIT 10")
    rows = c.fetchall()
    txt = "🏆 طابلو المتصدرين - منجم حمامات ⛏️\n\n"
    for i, (uid, bal) in enumerate(rows, 1):
        txt += f"{i}. ID:{uid} - {bal} 💰\n"
    bot.send_message(m.from_user.id, txt)

# تشغيل البوت + الويب
def run_bot():
    try: bot.remove_webhook()
    except: pass
    time.sleep(2)
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))