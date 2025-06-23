# analytics.py
# Module to calculate trade performance analytics from trade_log.csv

import csv
import os

LOG_FILE = "trade_log.csv"

class TradeAnalytics:
    def __init__(self, log_file=LOG_FILE):
        self.log_file = log_file
        self.trades = []
        self._load_trades()

    def _load_trades(self):
        if not os.path.exists(self.log_file):
            return
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    entry_price = float(row["entry_price"])
                    exit_price = float(row["exit_price"])
                    amount = float(row["amount"])
                    percent_change = float(row.get("percent_change", (exit_price - entry_price) / entry_price))
                    self.trades.append({
                        "entry": entry_price,
                        "exit": exit_price,
                        "amount": amount,
                        "change": percent_change
                    })
                except Exception:
                    continue

    def get_summary(self):
        if not self.trades:
            return {
                "total_trades": 0,
                "total_profit": 0.0,
                "win_rate": 0.0,
                "best_trade": None,
                "worst_trade": None
            }

        total_profit = 0.0
        wins = 0
        best = None
        worst = None

        for t in self.trades:
            profit = (t["exit"] - t["entry"]) * t["amount"]
            total_profit += profit
            if profit > 0:
                wins += 1

            if best is None or t["change"] > best["change"]:
                best = t
            if worst is None or t["change"] < worst["change"]:
                worst = t

        win_rate = (wins / len(self.trades)) * 100

        return {
            "total_trades": len(self.trades),
            "total_profit": round(total_profit, 4),
            "win_rate": round(win_rate, 2),
            "best_trade": best,
            "worst_trade": worst
        }
