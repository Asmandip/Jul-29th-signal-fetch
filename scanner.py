### scanner.py
import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from signal_generator import generate_signal
from telegram_bot import send_telegram_message

load_dotenv()

async def fetch_symbols():
    url = "https://api.bitget.com/api/v2/market/tickers?productType=umcbl"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if not data or 'data' not in data:
                    logging.error("❌ Bitget API returned no data or malformed response")
                    return []
                return [item['symbol'] for item in data['data'][:100]]
    except Exception as e:
        logging.error(f"❌ Bitget ticker fetch failed: {e}")
        return []

async def run_scanner():
    symbols = await fetch_symbols()
    while True:
        tasks = [generate_signal(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        for res in results:
            if res:
                await send_telegram_message(res)
        await asyncio.sleep(60)

