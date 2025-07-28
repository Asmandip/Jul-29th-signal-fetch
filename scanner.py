### scanner.py
import os
import aiohttp
import asyncio
from dotenv import load_dotenv
from signal_generator import generate_signal
from telegram_bot import send_telegram_message

load_dotenv()

async def fetch_symbols():
    url = "https://api.bitget.com/api/v2/mix/market/tickers?productType=umcbl"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return [item['symbol'] for item in data['data'][:100]]

async def run_scanner():
    symbols = await fetch_symbols()
    while True:
        tasks = [generate_signal(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        for res in results:
            if res:
                await send_telegram_message(res)
        await asyncio.sleep(60)

