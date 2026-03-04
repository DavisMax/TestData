import ccxt

exchange = ccxt.binance()

# Get BTC price
ticker = exchange.fetch_ticker('BTC/USDT')

print("BTC Price:", ticker['last'])
