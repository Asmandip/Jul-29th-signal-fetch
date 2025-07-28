### telegram_bot.py
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            return await resp.text()
