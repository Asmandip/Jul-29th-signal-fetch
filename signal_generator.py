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
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df['macd'] = MACD(df['close']).macd_diff()
    df['ema'] = EMAIndicator(df['close'], window=21).ema_indicator()
    df['atr'] = AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
    df['candle'] = df['close'] - df['open']  # Bullish if positive
    df['volume_change'] = df['volume'].pct_change()

    return df

async def generate_signal(symbol):
    try:
        raw_data = await fetch_klines(symbol)
        df = pd.DataFrame(raw_data)
        df = apply_indicators(df)
        latest = df.iloc[-1]

        # Indicators
        rsi = latest['rsi']
        macd = latest['macd']
        ema = latest['ema']
        price = latest['close']
        candle = latest['candle']
        volume_change = latest['volume_change']

        confirmations = 0
        reasons = []

        if rsi < 30:
            confirmations += 1
            reasons.append("🔽 RSI Oversold")

        if macd > 0:
            confirmations += 1
            reasons.append("📈 MACD Bullish")

        if price > ema:
            confirmations += 1
            reasons.append("📊 Above EMA")

        if candle > 0:
            confirmations += 1
            reasons.append("🕯️ Bullish Candle")

        if volume_change > 0.05:
            confirmations += 1
            reasons.append("💥 Volume Surge")

        if confirmations >= 4:
            return (
                f"✅ Buy Signal on {symbol}\n"
                f"📍 Price: {price:.4f}\n"
                f"📊 RSI: {rsi:.2f}, MACD: {macd:.4f}, EMA: {ema:.2f}\n"
                f"🧠 Confirmations: {confirmations} - {', '.join(reasons)}"
            )

    except Exception as e:
        print(f"Error for {symbol}: {e}")
    return None