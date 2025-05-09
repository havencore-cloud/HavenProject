# pulse_dashboard.py
# Minimal CLI dashboard for Pulse — the HavenBot trading monitor using shared price cache

import time
import os
import json
from trade_logger import LOG_FILE
from analytics import TradeAnalytics

PRICE_CACHE_FILE = "price_cache.json"

class Pulse:
    def __init__(self):
        self.analytics = TradeAnalytics()

    def read_cached_price(self):
        if not os.path.exists(PRICE_CACHE_FILE):
            return None
        try:
            with open(PRICE_CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("price")
        except Exception:
            return None

    def show_price(self):
        price = self.read_cached_price()
        try:
            return f"Current BONK Price: ${price:.8f}"
        except (TypeError, ValueError):
            return "[ERROR] BONK price unavailable (likely rate limit or cache error)."

    def show_recent_trades(self, limit=5):
        if not os.path.exists(LOG_FILE):
            return ["[INFO] No trades logged yet."]

        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            if len(lines) <= 1:
                return ["[INFO] Log exists but no trades yet."]
            entries = lines[1:]  # skip header
            return entries[-limit:]

    def show_analytics(self):
        summary = self.analytics.get_summary()
        return [
            f"Total Trades: {summary['total_trades']}",
            f"Total Profit: ${summary['total_profit']}",
            f"Win Rate: {summary['win_rate']}%",
            f"Best Trade: {round(summary['best_trade']['change'] * 100, 2)}%" if summary['best_trade'] else "Best Trade: N/A",
            f"Worst Trade: {round(summary['worst_trade']['change'] * 100, 2)}%" if summary['worst_trade'] else "Worst Trade: N/A"
        ]

    def run(self, refresh_interval=20):
        print("=== PULSE: Trading Dashboard ===")
        try:
            while True:
                print("[DEBUG] Refreshing dashboard...")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("=== PULSE: Trading Dashboard ===\n")
                print(self.show_price())

                print("\nLast Trades:")
                for line in self.show_recent_trades():
                    print("-", line.strip())

                print("\nAnalytics:")
                for line in self.show_analytics():
                    print("*", line)

                print(f"\n(Refreshing every {refresh_interval} seconds)")
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            print("\n[EXIT] Dashboard closed.")

if __name__ == "__main__":
    pulse = Pulse()
    pulse.run()
