import requests
import time
import telebot
from telebot import types

# ضع توكن البوت الخاص بك هنا ليعمل تلقائياً
TOKEN = "8610905655:AAHdWXdDEobIshF_VWiZdN0hD5USC5bhSXo"
bot = telebot.TeleBot(TOKEN)

# زر المبرمج
call5 = types.InlineKeyboardButton(text="Programmer", url="https://t.me/deadcode_22")

@bot.message_handler(commands=['start'])
def start(message):  
    Keyy = types.InlineKeyboardMarkup()
    Keyy.add(call5) 
    welcome_msg = (
        f"𝐇𝐄𝐋𝐋𝐎 @{message.from_user.username},\n"
        f"𝐈 𝐂𝐀𝐍 𝐇𝐄𝐋𝐏 𝐘𝐎𝐔 \n"
        f"اختر من الازرار بالاسفل لصنع استضافات \n"
        f"PYTHON AND PHP ❤️‍🔥🛡\n"
        f"/python    |     /php"
    )
    bot.reply_to(message, welcome_msg, reply_markup=Keyy)

@bot.message_handler(commands=['python'])
def python(message):
    Keyy = types.InlineKeyboardMarkup()
    Keyy.add(call5)  
    bot.send_message(message.chat.id, "👨‍💻 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓...")
    time.sleep(2)
    try:
        # محاولة جلب البيانات من السيرفر
        r = requests.get('https://mr-abood.herokuapp.com/Create/Python/Hosting', timeout=20).json()
        a = (
            f"⌯ email successful ✅ ⌯\n"
            f". ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .\n"
            f"⌯ Username ➥ {r.get('username')}\n"
            f"⌯ Password ➥ {r.get('password')}\n"
            f"⌯ Link Login ➥ {r.get('login')}\n"
            f"⌯ Email ➥ {r.get('email')}\n"
            f". ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .\n"
            f"⚖️ Tele : @DEADCODE_22"
        )
        bot.send_message(message.chat.id, f"✅ 𝐃𝐎𝐍𝐄 𝐆𝐄𝐓 𝐈𝐍𝐅𝐎 ❤️‍🔥\n────── • ✧✧ • ──────\n{a}\n────── • ✧✧ • ──────\n- ᴅᴇᴠ • @S7C_Z", reply_markup=Keyy)
    except:
        h = '𝐀𝐍 𝐄𝐑𝐑𝐎𝐑 𝐎𝐂𝐂𝐔𝐑𝐄𝐃 𝐏𝐋𝐄𝐀𝐒𝐄 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍'
        bot.send_message(message.chat.id, f"❌ ❤️‍🔥\n────────── • ✧✧ • ──────────\n{h}\n────────── • ✧✧ • ──────────\n- ᴅᴇᴠ • @S7C_Z", reply_markup=Keyy)

@bot.message_handler(commands=['php'])     
def php(message):
    Keyy = types.InlineKeyboardMarkup()
    Keyy.add(call5)
    bot.send_message(message.chat.id, "👨‍💻 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓...")
    time.sleep(2) 
    try:
        r = requests.get('https://mr-abood.herokuapp.com/Create/PHP/Hosting', timeout=20).json()
        a = (
            f"⌯ email successful ✅ ⌯\n"
            f". ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .\n"
            f"⌯ Username ➥ {r.get('username')}\n"
            f"⌯ Password ➥ {r.get('password')}\n"
            f"⌯ Website ➥ {r.get('website')}\n"
            f"⌯ Panel ➥ {r.get('panel')}\n"
            f". ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .\n"
            f"⚖️ Tele : @DEADCODE_22"
        )
        bot.send_message(message.chat.id, f"✅ 𝐃𝐎𝐍𝐄 𝐆𝐄𝐓 𝐈𝐍𝐅𝐎 ❤️‍🔥\n────── • ✧✧ • ──────\n{a}\n────── • ✧✧ • ──────\n- ᴅᴇᴠ • @S7C_Z", reply_markup=Keyy)
    except:
        h = '𝐀𝐍 𝐄𝐑𝐑𝐎𝐑 𝐎𝐂𝐂𝐔𝐑𝐄𝐃 𝐏𝐋𝐄𝐀𝐒𝐄 𝐓𝐑𝐘 𝐀𝐆𝐀𝐈𝐍'
        bot.send_message(message.chat.id, f"❌ ❤️‍🔥\n────────── • ✧✧ • ──────────\n{h}\n────────── • ✧✧ • ──────────\n- ᴅᴇᴠ • @S7C_Z", reply_markup=Keyy)

if __name__ == "__main__":
    print("البوت يعمل الآن على الاستضافة...")
    bot.remove_webhook()
    bot.infinity_polling()
