# main_loop.py
import time
from tracker import print_token_metrics, fetch_token_metrics
from trader import Trader
from config import MONITORED_TOKENS

def start_trading_loop():
    trader = Trader()
    last_price = None
    symbol_to_track = "SOL"  # Target token for simulation

    print("[CLI LOOP] Starting live monitoring...\n")

    while True:
        print("========== POLLING ==========")
        print("[TRACKER] Collecting token metrics from all monitored tokens:")

        for token in MONITORED_TOKENS:
            print(f"--- {token['symbol']} ---")
            metrics = fetch_token_metrics(token['symbol'], token['mint'])

            if not metrics:
                print(f"  No data available for {token['symbol']}")
                continue

            for key, value in metrics.items():
                print(f"  {key}: {value}")

            if metrics['symbol'] == symbol_to_track:
                price = metrics['price_usd']
                print(f"[DEBUG] Checking trade logic for {metrics['symbol']} at price: {price}, last: {last_price}")

                if trader.position is None:
                    if last_price is None:
                        last_price = price
                    else:
                        print(f"[DEBUG] Buy Check: price {price} vs target {last_price * 0.999}")
                        if price < last_price * 0.999:
                            trader.buy(metrics['symbol'], price)
                            last_price = None  # Reset after buy
                else:
                    if price > trader.position['entry_price'] * 1.001:
                        trader.sell(price)
                        last_price = None  # Reset after sell

        trader.status()

        print("\n[ANALYTICS] Current Performance Snapshot:")
        print(f"  total_profit: {trader.total_profit}")
        print(f"  total_trades: {len(trader.trade_log)}")
        print(f"  open_position: {trader.position['symbol'] if trader.position else 'None'}")

        time.sleep(30)  # Wait before next polling cycle
