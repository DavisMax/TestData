import MetaTrader5 as mt5
import pandas as pd
import time

symbol = "XAUUSD"
lot = 0.01
max_positions = 5
timeframe = mt5.TIMEFRAME_M5

def check_signal():
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 150)
    if rates is None:
        return None

    df = pd.DataFrame(rates)

    # EMAs
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()

    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    last = df.iloc[-1]

    print("----------------------------------")
    print("Price:", round(last['close'], 2))
    print("EMA20:", round(last['ema20'], 2))
    print("EMA50:", round(last['ema50'], 2))
    print("RSI:", round(last['rsi'], 2))

    # BUY
    if (
        last['ema20'] > last['ema50'] and
        last['rsi'] > 55 and
        last['close'] > last['ema50']
    ):
        return "buy"

    # SELL
    if (
        last['ema20'] < last['ema50'] and
        last['rsi'] < 45 and
        last['close'] < last['ema50']
    ):
        return "sell"

    return None




def place_trade(signal):
    tick = mt5.symbol_info_tick(symbol)

    if signal == "buy":
        price = tick.ask
        sl = price - 20.0
        tp = price + 40.0
        order_type = mt5.ORDER_TYPE_BUY
    else:
        price = tick.bid
        sl = price + 10.0
        tp = price - 20.0
        order_type = mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "EMA Loop Bot",
        "type_time": mt5.ORDER_TIME_GTC,
    }

    result = mt5.order_send(request)
    print("Trade placed:", result)

# --- CONNECT ---
if not mt5.initialize():
    print("Initialization failed")
    quit()

print("Bot running... Watching market 👀")

while True:
    positions = mt5.positions_get(symbol=symbol)

    if positions is not None and len(positions) < max_positions:
        signal = check_signal()

        if signal:
            print("Signal detected:", signal)
            place_trade(signal)
        else:
            print("No crossover signal.")

    else:
        print("Max positions reached.")

    time.sleep(60)
print("EMA20:", last['ema20'], "EMA50:", last['ema50'])
# -- play 

