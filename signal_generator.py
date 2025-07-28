### signal_generator.py
import aiohttp
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import AverageTrueRange

async def fetch_klines(symbol):
    url = f"https://api.bitget.com/api/v2/mix/market/candles?symbol={symbol}&granularity=180&limit=100"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data['data']

def apply_indicators(df):
    df['close'] = df['close'].astype(float)
    rsi = RSIIndicator(df['close'], window=14)
    macd = MACD(df['close'])
    ema = EMAIndicator(df['close'], window=21)
    atr = AverageTrueRange(df['high'], df['low'], df['close'], window=14)
    df['rsi'] = rsi.rsi()
    df['macd'] = macd.macd_diff()
    df['ema'] = ema.ema_indicator()
    df['atr'] = atr.average_true_range()
    return df

async def generate_signal(symbol):
    try:
        raw_data = await fetch_klines(symbol)
        df = pd.DataFrame(raw_data, columns=['timestamp','open','high','low','close','volume'])
        df = apply_indicators(df)

        rsi = df['rsi'].iloc[-1]
        macd = df['macd'].iloc[-1]
        ema = df['ema'].iloc[-1]
        price = float(df['close'].iloc[-1])

        confirmations = 0
        if rsi < 30: confirmations += 1
        if macd > 0: confirmations += 1
        if price > ema: confirmations += 1

        if confirmations >= 2:
            return f"✅ Signal: {symbol}\nPrice: {price}\nRSI: {rsi:.2f}\nMACD: {macd:.4f}\nEMA: {ema:.2f}"
    except Exception as e:
        print(f"Error for {symbol}: {e}")
    return None
