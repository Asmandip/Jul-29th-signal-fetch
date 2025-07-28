### main.py
import asyncio
import threading
import os
from flask import Flask
from scanner import run_scanner

app = Flask(__name__)

@app.route('/')
def home():
    return "AsmanDip Future Scanner is running ✅"

def start_bot():
    asyncio.run(run_scanner())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

