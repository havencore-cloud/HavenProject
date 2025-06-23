import os
import json
import requests
from datetime import datetime

CACHE_PATH = "liquidity/jupiter_tokens_cache.json"

def fetch_and_save_jupiter_tokens():
    print("[FETCH] Getting Jupiter tradable tokens...")
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/mints/tradable", timeout=10)
        response.raise_for_status()
        tokens = response.json()

        with open(CACHE_PATH, "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "tokens": tokens
            }, f, indent=2)

        print(f"[CACHE] Saved Jupiter token list to {CACHE_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch/save Jupiter token list: {e}")

if __name__ == "__main__":
    fetch_and_save_jupiter_tokens()