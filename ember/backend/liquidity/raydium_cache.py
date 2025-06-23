import os
import json
import requests
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CACHE_FILE = "liquidity/raydium_pools_cache.json"

# --- Jupiter Fallback ---

def fetch_jupiter_indexed_pools() -> List[Dict]:
    url = "https://lite-api.jup.ag/tokens/v1/mints/tradable"
    try:
        print("[FETCH] Requesting Jupiter indexed Raydium pools...")
        response = requests.get(url)
        response.raise_for_status()
        pools = response.json()
        print(f"[FETCH] Retrieved {len(pools)} pools.")
        return pools
    except Exception as e:
        print(f"[ERROR] Failed to fetch Jupiter pools: {e}")
        return []

def update_raydium_cache() -> None:
    print("[CACHE] Fetching Raydium pool data from Jupiter...")
    pools = fetch_jupiter_indexed_pools()
    print(f"[DEBUG] Writing Raydium cache to: {os.path.abspath(CACHE_FILE)}")
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "pools": pools
            }, f)
        print(f"[CACHE] Saved {len(pools)} pools to cache.")
    except Exception as e:
        print(f"[CACHE ERROR] Failed to save cache: {e}")

# --- Liquidity Scanner ---

def load_jupiter_tokens() -> Dict[str, str]:
    try:
        url = "https://cache.jup.ag/tokens"
        print("[JUPITER] Fetching token list...")
        resp = requests.get(url)
        resp.raise_for_status()
        token_list = resp.json()
        return {entry["symbol"].lower(): entry["address"].lower() for entry in token_list}
    except Exception as e:
        print(f"[ERROR] Failed to fetch Jupiter token list: {e}")
        return {}


def load_raydium_cache() -> List[Dict]:
    if not os.path.exists(CACHE_FILE):
        print("[CACHE] No cache found.")
        return []
    try:
        with open(CACHE_FILE, "r") as f:
            data = json.load(f)
            return data.get("pools", [])
    except Exception as e:
        print(f"[CACHE ERROR] Failed to load cache: {e}")
        return []

def get_raydium_liquidity_from_cache(mint_address: str) -> dict:
    try:
        with open("liquidity/raydium_pools_cache.json", "r") as f:
            data = json.load(f)
            pools = data.get("pools", [])
            print(f"[DEBUG] Loaded {len(pools)} Raydium pools from cache")
    except Exception as e:
        print(f"[ERROR] Could not load Raydium cache: {e}")
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": None,
            "warnings": ["Raydium cache is empty or failed to load"]
        }

    for pool in pools:
        pair_id = pool.get("pair_id", "")
        if mint_address in pair_id:
            print(f"[MATCH FOUND] ✅ {mint_address} in {pair_id}")
            return {
                "found": True,
                "liquidity_usd": float(pool.get("liquidity", 0)),
                "pair": pool.get("name", "Unknown"),
                "warnings": []
            }

    print(f"[NO MATCH] ❌ No pool pair found for {mint_address}")
    return {
        "found": False,
        "liquidity_usd": 0,
        "pair": None,
        "warnings": ["Token not found in Raydium pairs"]
    }
