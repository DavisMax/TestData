import ccxt

exchange = ccxt.binance()

timeframes = ['1h', '5m', '1m']

for tf in timeframes:
    candles = exchange.fetch_ohlcv('BTC/USDT', timeframe=tf, limit=2)
    last_close = candles[-1][4]
    prev_close = candles[-2][4]

    trend = "UP" if last_close > prev_close else "DOWN"
    print(tf, "trend:", trend)
