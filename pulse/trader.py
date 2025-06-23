# trader.py
import time

class Trader:
    def __init__(self, starting_balance=1000.0):
        self.balance = starting_balance  # in USDC
        self.position = None  # { 'symbol': ..., 'entry_price': ..., 'amount': ..., 'timestamp': ... }
        self.trade_log = []
        self.total_profit = 0.0
        self.log_file = "trade_log.json"

    def buy(self, symbol, price):
        if self.position is not None:
            return  # already holding

        amount = self.balance / price
        self.position = {
            'symbol': symbol,
            'entry_price': price,
            'amount': amount,
            'timestamp': time.time()
        }
        self.balance = 0.0
        print(f"[TRADE] Bought {amount:.4f} {symbol} at ${price:.4f}")

    def sell(self, price):
        if self.position is None:
            return

        proceeds = self.position['amount'] * price
        profit = proceeds - (self.position['amount'] * self.position['entry_price'])
        self.total_profit += profit
        self.balance = proceeds

        print(f"[TRADE] Sold {self.position['amount']:.4f} {self.position['symbol']} at ${price:.4f} (P/L: ${profit:.2f})")

        entry = {
           'symbol': self.position['symbol'],
           'buy_price': self.position['entry_price'],
           'sell_price': price,
           'profit': profit,
           'timestamp': time.time()
        }
        self.trade_log.append(entry)
        self.save_trade(entry)
        self.position = None

    def should_buy(self, price, last_price):
        return price < last_price * 0.95  # Buy on 5% drop

    def should_sell(self, price):
        if not self.position:
            return False
        return price > self.position['entry_price'] * 1.05  # Sell on 5% gain

    def status(self):
        print("\n[TRADER STATUS]")
        print(f"  Balance: ${self.balance:.2f}")
        if self.position:
            print(f"  Holding: {self.position['amount']:.4f} {self.position['symbol']} @ ${self.position['entry_price']:.4f}")
        else:
            print("  Holding: None")
        print(f"  Total Profit: ${self.total_profit:.2f}")

    def save_trade(self, entry):

        import json
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"[ERROR] Failed to log trade: {e}")
