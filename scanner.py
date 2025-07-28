import aiohttp
import asyncio
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

async def fetch_symbols():
    url = "https://api.bitget.com/api/v2/mix/market/tickers"
params = {"productType": "umcbl"}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                logging.info(f"✅ Bitget raw data: {data}")
                if "data" in data:
                    symbols = [item["symbol"] for item in data["data"]]
                    return symbols
                else:
                    logging.error("❌ No 'data' key in response")
                    return []
    except Exception as e:
        logging.error(f"❌ Bitget ticker fetch failed: {e}")
        return []

async def run_scanner():
    symbols = await fetch_symbols()
    logging.info(f"✅ Total Symbols Fetched: {len(symbols)}")
    logging.info(f"📊 Symbols: {symbols[:10]}")  # Preview first 10

if __name__ == "__main__":
    asyncio.run(run_scanner())