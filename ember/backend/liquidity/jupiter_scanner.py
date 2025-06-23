# jupiter_scanner.py

import requests
import json
import os
from trust.metadata import decode_metaplex_metadata
from trust.metaplex import clean_bytes
from datetime import datetime, timezone
from typing import List, Dict

CACHE_FILE = "liquidity/raydium_pools_cache.json"
TRADABLE_POOLS_API = "https://lite-api.jup.ag/tokens/v1/mints/tradable"

def fetch_tradable_pools() -> List[str]:
    try:
        print("[FETCH] Fetching pool mint list from Jupiter...")
        resp = requests.get(TRADABLE_POOLS_API, timeout=7)
        resp.raise_for_status()
        mints = resp.json()
        print(f"[FETCH] Received {len(mints)} tradable mints.")
        return mints
    except Exception as e:
        print(f"[ERROR] Fetch tradable mints failed: {e}")
        return []

def normalize_pools(mints: List[str]) -> List[Dict]:
    # Create a simple structure where base_mint is the token itself
    print("[PROCESS] Normalizing pool data...")
    return [{"mint": m, "liquidityUSD": 0} for m in mints]

def save_cache(pools: List[Dict]):
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pools": pools
    }
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)
        print(f"[CACHE] Saved {len(pools)} pools to {CACHE_FILE}")
    except Exception as e:
        print(f"[ERROR] Saving cache failed: {e}")

def load_cache() -> List[Dict]:
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            return data.get("pools", [])
    except Exception as e:
        print(f"[CACHE] Load cache failed: {e}")
        return []

def refresh_cache_if_needed():
    pools = fetch_tradable_pools()
    if pools:
        normalized = normalize_pools(pools)
        save_cache(normalized)

def get_liquidity_info_for_token(mint: str) -> Dict:
    pools = load_cache()
    if not pools:
        refresh_cache_if_needed()
        pools = load_cache()

    # --- Get symbol from Metaplex Metadata ---
    meta = decode_metaplex_metadata(mint)
    symbol = clean_bytes(meta.get("symbol", "")) if isinstance(meta, dict) else None

    if not symbol:
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "None",
            "pools": [],
            "warnings": [f"Could not decode symbol from Metaplex metadata"]
        }

    matched_pools = [p for p in pools if symbol.lower() in p.get("name", "").lower()]

    if not matched_pools:
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "None",
            "pools": [],
            "warnings": [f"No pool found matching symbol '{symbol}'"]
        }

    best_pool = max(matched_pools, key=lambda x: x.get("liquidity", 0))
    return {
        "found": True,
        "liquidity_usd": best_pool.get("liquidity", 0),
        "pair": best_pool.get("name", "Unknown"),
        "pools": matched_pools,
        "warnings": [],
        "amm_id": best_pool.get("amm_id")
    }