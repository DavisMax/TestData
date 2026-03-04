import ccxt
import pandas as pd

exchange = ccxt.binance()

# Get 1 minute candles
candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=100)

df = pd.DataFrame(candles, columns=[
    'time', 'open', 'high', 'low', 'close', 'volume'
])

print(df.tail())
