import os
from flask import Flask, request
import telebot
from telebot import types
app=Flask(__name__)
TOKEN=os.environ.get("BOT_TOKEN")
bot=telebot.TeleBot(TOKEN)
URL="https://dz-bot-v4i9.onrender.com/"
try:
 bot.remove_webhook()
 bot.set_webhook(url=URL)
except:
 pass
def kb():
 m=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
 m.add("حساب المعدل","بنك البحوث")
 m.add("تنظيم الوقت","نصائح للتفوق")
 return m
@bot.message_handler(commands=['start'])
def start(m):
 bot.send_message(m.chat.id,"اهلا بيك في بوت الطالب الجزائري\nاختار من القائمة:",reply_markup=kb())
@bot.message_handler(func=lambda m:"حساب المعدل" in m.text)
def c1(m):
 bot.send_message(m.chat.id,"ابعتلي نقاطك هكا: 16 12 15 14")
@bot.message_handler(func=lambda m:"بنك البحوث" in m.text)
def c2(m):
 bot.send_message(m.chat.id,"بنك البحوث:\n1- الذكاء الاصطناعي\n2- التنمية المستدامة\n3- التسويق الرقمي")
@bot.message_handler(func=lambda m:"تنظيم الوقت" in m.text)
def c3(m):
 bot.send_message(m.chat.id,"خطة المراجعة:\nصباح حفظ\nمساء فهم\nليل مراجعة")
@bot.message_handler(func=lambda m:True)
def all_msg(m):
 try:
  nums=[float(x) for x in m.text.split() if x.replace('.','',1).isdigit()]
  if len(nums)>=2:
   bot.send_message(m.chat.id,f"معدلك هو: {sum(nums)/len(nums):.2f}")
 except:
  pass
@app.route('/',methods=['POST'])
def wh():
 u=telebot.types.Update.de_json(request.get_data().decode('UTF-8'))
 bot.process_new_updates([u])
 return 'ok',200
@app.route('/')
def home():
 return "Bot is alive!"
if __name__=='__main__':
 app.run(host='0.0.0.0',port=int(os.environ.get("PORT",10000)))
