# cli_loop.py
# Command-line loop to monitor token metrics, wallet activity, and analytics every N seconds

import time
from tracker import print_token_metrics
# from walletwatch import print_wallet_trades
from analytics.analytics_core import get_metrics_snapshot

POLL_INTERVAL = 60  # seconds

def start_monitoring_loop():
    print("[CLI LOOP] Starting live monitoring...")
    while True:
        print("\n========== POLLING ==========")

        # Token metrics (price, volume, liquidity)
        print_token_metrics()

        # Wallet activity (buys/sells)
        # print_wallet_trades()

        # Analytics dashboard
        metrics = get_metrics_snapshot()
        print("[ANALYTICS] Current Performance Snapshot:")
        for k, v in metrics.items():
            print(f"  {k}: {v}")

        time.sleep(POLL_INTERVAL)
