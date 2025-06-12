import json
import os
from typing import List, Dict
from datetime import datetime
from .raydium_decoder import fetch_all_raydium_pools
from dotenv import load_dotenv
load_dotenv()

CACHE_FILE = "raydium_pools_cache.json"

def get_raydium_liquidity_from_cache(mint_address: str) -> Dict:
    pools = load_raydium_cache()
    if not pools:
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "Error",
            "warnings": ["Raydium cache is empty or failed to load"]
        }
    return find_liquidity_for_mint(mint_address, pools)

def update_raydium_cache() -> None:
    rpc_url = os.getenv("HELIUS_RPC_URL")
    if not rpc_url:
        print("[CACHE ERROR] No RPC URL found in environment.")
        return
    print("[CACHE] Fetching Raydium pool data from chain...")
    pools = fetch_all_raydium_pools(rpc_url)
    print(f"[DEBUG] Writing Raydium cache to: {os.path.abspath(CACHE_FILE)}")
    with open(CACHE_FILE, "w") as f:
        json.dump({
            "timestamp": datetime.utcnow().isoformat(),
            "pools": pools
        }, f)
    print(f"[CACHE] Saved {len(pools)} pools to cache.")


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


def find_liquidity_for_mint(mint_address: str, cached_pools: List[Dict]) -> Dict:
    mint_address = mint_address.lower()
    matches = []
    total_liquidity = 0

    for pool in cached_pools:
        base = (pool.get("baseMint") or "").lower()
        quote = (pool.get("quoteMint") or "").lower()
        if mint_address in [base, quote]:
            base_amt = pool.get("baseReserve", 0)
            quote_amt = pool.get("quoteReserve", 0)
            liquidity = float(base_amt + quote_amt)
            symbol = f"{base[:4]}.../{quote[:4]}..."
            matches.append({
                "pair": symbol,
                "liquidity_usd": liquidity
            })
            total_liquidity += liquidity

    if not matches:
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "Not found",
            "warnings": ["Pool not detected on Raydium"]
        }

    deepest = max(matches, key=lambda p: p["liquidity_usd"])
    return {
        "found": True,
        "liquidity_usd": round(total_liquidity, 2),
        "pair": deepest["pair"],
        "pools": matches,
        "warnings": []
    }