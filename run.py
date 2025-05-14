import schedule
import time
from bot import trade

with open('stock_list.txt') as f:
    stocks = [line.strip() for line in f]

def run_all():
    for stock in stocks:
        trade(stock)

schedule.every(15).minutes.do(run_all)

print("✅ Auto-Trading Bot Running...")
while True:
    schedule.run_pending()
    time.sleep(1)
