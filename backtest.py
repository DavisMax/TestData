# ===== RULE SETTINGS =====
stop_loss_percent = 0.01
take_profit_percent = 0.02
risk_per_trade = 0.01


import ccxt
import pandas as pd

# Connect to exchange
exchange = ccxt.binance()

# Get historical candles (bigger = longer backtest)
candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=500)

# Convert to DataFrame
df = pd.DataFrame(candles, columns=[
    'time', 'open', 'high', 'low', 'close', 'volume'
])

# Fake wallet
balance = 1000
position = None
entry_price = 0

print("Starting balance:", balance)

# Loop through history
for i in range(1, len(df)):
    prev_close = df['close'].iloc[i - 1]
    current_close = df['close'].iloc[i]

    # SIMPLE STRATEGY
    # Buy if price rising
    if current_close > prev_close and position is None:
        position = "LONG"
        entry_price = current_close
        
        # Set SL & TP prices
        stop_loss_price = entry_price * (1 - stop_loss_percent)
        take_profit_price = entry_price * (1 + take_profit_percent)

    # Sell if price falling
    elif current_close < prev_close and position == "LONG":
        profit = current_close - entry_price
        balance += profit
        position = None

print("Final balance:", round(balance, 2))
print("Profit:", round(balance - 1000, 2))
