# price_fetcher.py
# Fetches real-time token price using Jupiter Aggregator quote endpoint

import requests
import time
import json
import os

PRICE_CACHE_FILE = "price_cache.json"
CACHE_EXPIRY_SECONDS = 10

class PriceFetcher:
    def __init__(self, token_mint="38PgzpJYu2HkiYvV8qePFakB8tuobPdGm2FFEn7Dpump", polling_delay=20):
        self.token_mint = token_mint
        self.polling_delay = polling_delay
        self.api_url = f"https://quote-api.jup.ag/v6/quote?inputMint={self.token_mint}&outputMint=So11111111111111111111111111111111111111112&amount=1000000"

    def cache_price(self, price):
        try:
            with open(PRICE_CACHE_FILE, 'w') as f:
                json.dump({"price": price, "timestamp": time.time()}, f)
        except Exception as e:
            print(f"[ERROR] Failed to cache price: {e}")

    def load_cached_price(self):
        if not os.path.exists(PRICE_CACHE_FILE):
            return None
        try:
            with open(PRICE_CACHE_FILE, 'r') as f:
                data = json.load(f)
                if time.time() - data.get("timestamp", 0) < CACHE_EXPIRY_SECONDS:
                    return data.get("price")
        except Exception as e:
            print(f"[ERROR] Failed to load cached price: {e}")
        return None

    def get_sol_usd_price(self):
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd")
            response.raise_for_status()
            data = response.json()
            return data.get("solana", {}).get("usd", 0.0)
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch SOL/USD price: {e}")
            return 0.0

    def get_current_price(self):
        cached = self.load_cached_price()
        if cached is not None:
            return cached

        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                print("[ERROR] Invalid response format.")
                return None
            out_amount = data.get("outAmount")
            if out_amount is not None:
                decimals = data.get("outputTokenInfo", {}).get("decimals", 9)
                price_in_sol = int(out_amount) / (10 ** decimals)
                sol_usd = self.get_sol_usd_price()
                price = price_in_sol * sol_usd
                self.cache_price(price)
                return price
            else:
                print(f"[ERROR] Quote API did not return outAmount.")
                return None
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch price: {e}")
            return None

    def wait_for_price_change(self, entry_price, change_threshold=0.05, timeout=300):
        start_time = time.time()
        print(f"[WATCHING] Waiting for {self.token_mint} price to move {change_threshold * 100:.2f}% from entry: {entry_price}")

        while (time.time() - start_time) < timeout:
            current_price = self.get_current_price()
            if current_price is None:
                time.sleep(self.polling_delay)
                continue

            percent_change = (current_price - entry_price) / entry_price
            print(f"[PRICE CHECK] Current: {current_price:.8f} | Change: {percent_change:.2%}")

            if abs(percent_change) >= change_threshold:
                print(f"[TRIGGER] Price moved by {percent_change:.2%}, exiting wait loop.")
                return current_price

            time.sleep(self.polling_delay)

        print("[TIMEOUT] No significant price movement detected.")
        return self.get_current_price()