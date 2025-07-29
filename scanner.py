import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def fetch_symbols():
    url = "https://api.bitget.com/api/v2/mix/market/tickers?productType=USDT-FUTURES"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                logging.info(f"✅ Bitget raw data: {data}")
                
                if data.get("code") == "00000" and data.get("data"):
                    symbols = [item["symbol"] for item in data["data"]]
                    return symbols
                else:
                    logging.error("❌ Invalid response or missing 'data'")
                    return []
    except Exception as e:
        logging.error(f"❌ Bitget ticker fetch failed: {e}")
        return []

async def run_scanner():
    symbols = await fetch_symbols()
    logging.info(f"✅ Total Symbols Fetched: {len(symbols)}")
    logging.info(f"📊 Sample symbols: {symbols[:10]}")
    # Continue your scanner logic here...

if __name__ == "__main__":
    asyncio.run(run_scanner())