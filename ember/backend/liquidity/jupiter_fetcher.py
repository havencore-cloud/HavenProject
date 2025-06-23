import requests
import json
import os
from datetime import datetime, timezone

CACHE_FILE = "liquidity/jupiter_pools_cache.json"
JUPITER_INDEXED_POOLS_URL = "https://stats.jup.ag/api/indexed-pools"

def fetch_jupiter_indexed_pools():
    try:
        print("[FETCH] Fetching Jupiter indexed pools...")
        response = requests.get(JUPITER_INDEXED_POOLS_URL, timeout=10)
        response.raise_for_status()
        pools = response.json()
        print(f"[FETCH] Got {len(pools)} pools.")
        return pools
    except Exception as e:
        print(f"[ERROR] Failed to fetch indexed pools: {e}")
        return []

def save_cache(pools):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "pools": pools
            }, f)
        print(f"[SAVE] Jupiter pool cache saved: {CACHE_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not save pool cache: {e}")

def run():
    pools = fetch_jupiter_indexed_pools()
    if pools:
        save_cache(pools)

if __name__ == "__main__":
    run()
