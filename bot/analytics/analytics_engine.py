# analytics_engine.py
# Collects and analyzes trade performance and market behavior

import json
import os
import statistics

TRADE_LOG_FILE = "trade_log.json"

class AnalyticsEngine:
    def __init__(self):
        self.trades = self._load_trades()

    def _load_trades(self):
        if not os.path.exists(TRADE_LOG_FILE):
            return []
        try:
            with open(TRADE_LOG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load trade log: {e}")
            return []

    def summarize_trades(self):
        if not self.trades:
            print("[INFO] No trades to analyze.")
            return

        profits = []
        for trade in self.trades:
            if trade['action'] == "SELL":
                entry = trade['entry_price']
                exit = trade['exit_price']
                amount = trade['amount']
                profit = (exit - entry) * amount
                profits.append(profit)

        total_profit = sum(profits)
        average = statistics.mean(profits) if profits else 0
        print("=== TRADE SUMMARY ===")
        print(f"Trades analyzed: {len(profits)}")
        print(f"Total Profit: ${total_profit:.2f}")
        print(f"Average Profit/Trade: ${average:.2f}")

    def get_trade_history(self):
        return self.trades

    def get_last_n_trades(self, n=5):
        return self.trades[-n:] if self.trades else []

    def get_max_drawdown(self):
        # Placeholder for a future implementation
        return None

    def export_to_csv(self, filename="analytics_export.csv"):
        try:
            import csv
            with open(filename, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.trades[0].keys())
                writer.writeheader()
                for trade in self.trades:
                    writer.writerow(trade)
            print(f"[EXPORT] Analytics data exported to {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to export analytics: {e}")
