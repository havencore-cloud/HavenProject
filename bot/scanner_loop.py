# scanner_loop.py
import time
from config import TOKENS_TO_MONITOR
from price_fetcher import fetch_token_metrics
from .liquidity.liquidity_lookup import estimate_token_liquidity

def run_scanner_loop(interval_seconds=30):
    print("[SCANNER] Starting real-time token scanner...\n")

    while True:
        print("========== SCAN START ==========")
        for symbol, mint in TOKENS_TO_MONITOR.items():
            print(f"\n--- {symbol} ---")
            metrics = fetch_token_metrics(symbol, mint)

            if metrics:
                # Add liquidity from Jupiter pool data
                liquidity = estimate_token_liquidity(mint)
                metrics["liquidity_usd"] = liquidity

                print(f"[{symbol}] Price: ${metrics['price_usd']}")
                print(f"[{symbol}] Volume (24h): ${metrics['volume_24h']}")
                print(f"[{symbol}] Liquidity: ${metrics['liquidity_usd']}")
            else:
                print(f"[{symbol}] No metrics found or token is unsupported.")

        print("\n========== SCAN COMPLETE ==========\n")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_scanner_loop()
