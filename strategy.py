import ccxt
import pandas as pd

exchange = ccxt.binance()

candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=20)
df = pd.DataFrame(candles, columns=['time','open','high','low','close','volume'])

last_close = df['close'].iloc[-1]
prev_close = df['close'].iloc[-2]

if last_close > prev_close:
    print("BUY SIGNAL 🚀")
else:
    print("SELL SIGNAL 🔻")
