import glob
import os
from flask import Flask
from threading import Thread
from telebot import bot
from sys import argv
from telethon import TelegramClient
from telebot.telebotConfig import Var
from telebot.utils import load_module, start_mybot, load_pmbot
from pathlib import Path
import telethon.utils
from telebot import CMD_HNDLR

# --- إضافة السيرفر لضمان بقاء الحالة Live على Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Sabaa Server is Live and Running!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر في خلفية الكود
Thread(target=run_server).start()
# --------------------------------------------------

TELE = Var.PRIVATE_GROUP_ID
BOTNAME = Var.TG_BOT_USER_NAME_BF_HER
LOAD_MYBOT = Var.LOAD_MYBOT

async def add_bot(bot_token):
    await bot.start(bot_token)
    bot.me = await bot.get_me()
    bot.uid = telethon.utils.get_peer_id(bot.me)

async def startup_log_all_done():
    try:
        await bot.send_message(TELE, f"**TeleBot has been deployed.\nSend** `{CMD_HNDLR}alive` **to see if the bot is working.**")
    except BaseException:
        print("Either PRIVATE_GROUP_ID is wrong or you have left the group.")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    if Var.TG_BOT_USER_NAME_BF_HER is not None:
        print("Initiating Inline Bot")
        bot.tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=Var.APP_ID,
            api_hash=Var.API_HASH
        ).start(bot_token=Var.TG_BOT_TOKEN_BF_HER)
        bot.loop.run_until_complete(add_bot(Var.TG_BOT_USER_NAME_BF_HER))
    else:
        bot.start()

# تحميل الإضافات
path = 'telebot/plugins/*.py'
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

# تشغيل البوت النهائي
print("TeleBot has been fully deployed!")
bot.loop.run_until_complete(startup_log_all_done())

if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.run_until_disconnected()
