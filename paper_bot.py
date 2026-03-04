balance = 1000
position = None
entry_price = 0

def buy(price):
    global position, entry_price
    position = "LONG"
    entry_price = price
    print("Bought at", price)

def sell(price):
    global position, balance
    if position == "LONG":
        profit = price - entry_price
        balance += profit
        print("Sold at", price, "Profit:", profit)
        position = None

# Fake prices
prices = [100, 102, 105, 103, 108]

for price in prices:
    if position is None:
        buy(price)
    else:
        sell(price)

print("Final balance:", balance)
