# liquidity/scanner.py

import json
import os
from typing import List

CACHE_FILE = "liquidity/raydium_pools_cache.json"


def load_jupiter_pool_cache() -> List[dict]:
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            return data.get("pools", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] Could not load Jupiter pool cache: {e}")
        return []


def token_has_liquidity(mint_address: str, pools: List[dict]) -> bool:
    for pool in pools:
        if mint_address in (pool.get("inputMint"), pool.get("outputMint")):
            return True
    return False


# Example usage in a scanner module
if __name__ == "__main__":
    # Replace this with a real mint address to test
    mint = "9b8jL2wcVjBFpieC5TUR76BDJ6sW8Eghd3fyq5VJmzir"
    pools = load_jupiter_pool_cache()
    if token_has_liquidity(mint, pools):
        print(f"✅ Token {mint} has active liquidity.")
    else:
        print(f"❌ Token {mint} has NO liquidity.")
