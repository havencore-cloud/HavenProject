import requests
import json
from datetime import datetime, UTC
import os

CACHE_FILE = "liquidity/raydium_pools_cache.json"
POOL_API = "https://lite-api.jup.ag/tokens/v1/mints/tradable"

def fetch_raydium_pools():
    try:
        print("[FETCH] Requesting Jupiter indexed Raydium pools...")
        resp = requests.get(POOL_API)
        resp.raise_for_status()
        pools = resp.json()
        print(f"[FETCH] Got {len(pools)} Raydium pools.")
        return pools
    except Exception as e:
        print(f"[ERROR] Failed to fetch Jupiter pools: {e}")
        return []

def normalize_pools(raw_pools):
    print("[PROCESS] Normalizing pool data...")
    formatted = []
    for pool in raw_pools:
        try:
            base_mint, quote_mint = pool["pair_id"].split("-")
            formatted.append({
                "name": pool.get("name"),
                "pair_id": pool.get("pair_id"),
                "base_mint": base_mint,
                "quote_mint": quote_mint,
                "lp_mint": pool.get("lp_mint"),
                "liquidity": pool.get("liquidity", 0),
                "price": pool.get("price"),
                "amm_id": pool.get("amm_id"),
                "volume_24h": pool.get("volume_24h"),
                "fee_24h": pool.get("fee_24h"),
            })
        except Exception as e:
            print(f"[SKIP] Malformed pool: {e}")
    return formatted

def save_cache(pools):
    print(f"[SAVE] Writing to cache: {os.path.abspath(CACHE_FILE)}")
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({"timestamp": datetime.now(datetime.UTC).isoformat(),
                       "pools": pools}, f)
        print(f"[SAVE] Saved {len(pools)} pools.")
    except Exception as e:
        print(f"[ERROR] Couldn’t save cache: {e}")

def run():
    raw_pools = fetch_raydium_pools()
    if raw_pools:
        normalized = normalize_pools(raw_pools)
        save_cache(normalized)

if __name__ == "__main__":
    run()
