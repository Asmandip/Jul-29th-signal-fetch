import asyncio
import threading
import os
from flask import Flask
from scanner import run_scanner  # Ensure scanner.py exists and has run_scanner()

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ AsmanDip Future Trade Scanner is running!"

def start_bot():
    try:
        asyncio.run(run_scanner())
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
    
    # Use PORT from environment (for Render) or default 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)