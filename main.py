"""Python implementation of a Tinode chatbot المعدل ليعمل على Render."""

from __future__ import print_function
import argparse
import base64
from concurrent import futures
from datetime import datetime
import json
import os
import platform
import random
import signal
import sys
import time
import threading

# إضافة مكتبة Flask لإبقاء السيرفر حياً على Render
try:
    from flask import Flask
except ImportError:
    os.system('pip install flask')
    from flask import Flask

import grpc
from google.protobuf.json_format import MessageToDict
from tinode_grpc import pb
from tinode_grpc import pbx

# --- كود الاستمرارية لـ Render ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "Sabaa Bot is Live!"

def run_flask():
    # Render يستخدم المنفذ 10000 غالباً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# ---------------------------------

APP_NAME = "Sabaa-Chat-Bot" # تغيير اسم التطبيق
APP_VERSION = "1.0.0"

botUID = None
onCompletion = {}
subscriptions = {}
quotes = ["أهلاً بك في تطبيق السبع الملكي", "كيف يمكنني مساعدتك اليوم؟", "أنا بوت ذكي أعمل على سيرفر Render"]

def log(*args):
    print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], *args)

# (بقية وظائف Tinode الأصلية المختصرة للعمل بسرعة)
def client_generate():
    while True:
        msg = queue_out.get()
        if msg == None: return
        yield msg

queue_out = queue.Queue() if sys.version_info[0] < 3 else __import__('queue').Queue()

def client_post(msg):
    queue_out.put(msg)

def hello():
    tid = str(random.randint(100, 999))
    return pb.ClientMsg(hi=pb.ClientHi(id=tid, user_agent=APP_NAME, ver="0.17.10", lang="EN"))

# دالة التشغيل الرئيسية المعدلة
def run_bot():
    # هنا تضع عنوان سيرفر Tinode الخاص بك إذا كان لديك واحد
    # أو تتركه ليتصل بـ localhost إذا كنت تشغل السيرفر محلياً
    host = 'localhost:16060' 
    channel = grpc.insecure_channel(host)
    stream = pbx.NodeStub(channel).MessageLoop(client_generate())
    client_post(hello())
    log("Bot logic started...")
    # حلقة استقبال الرسائل
    for msg in stream:
        log("Received message")

if __name__ == '__main__':
    log("Starting Sabaa Bot System...")
    
    # 1. تشغيل Flask في سطر منفصل (Thread) لإرضاء Render
    threading.Thread(target=run_flask).start()
    
    # 2. تشغيل منطق البوت
    try:
        run_bot()
    except Exception as e:
        log("Bot Error:", e)
        # ابقاء السيرفر يعمل حتى لو فشل البوت
        while True:
            time.sleep(100)
