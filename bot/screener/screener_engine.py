# screener_engine.py
# Central intelligence layer for token screening

import time
from price_fetcher import fetch_token_metrics
from liquidity.liquidity_lookup import estimate_token_liquidity
from tracker.token_tracker import get_jupiter_token_metadata, is_token_routable_to_sol

def get_token_profile(symbol: str, mint: str, include_logs: bool = False) -> dict:
    token_info = {
        "symbol": symbol,
        "mint": mint,
        "name": symbol,
        "price_usd": 0.0,
        "volume_24h": 0.0,
        "liquidity_usd": 0.0,
        "routable": False,
        "whitelisted": False,  # Future logic placeholder
        "risk_score": 0,       # Placeholder until logic added
        "timestamp": int(time.time())
    }

    # --- Step 1: Get token metrics (price + volume from on-chain) ---
    metrics = fetch_token_metrics(symbol, mint)
    token_info["price_usd"] = metrics.get("price_usd", 0.0)
    token_info["volume_24h"] = metrics.get("volume_24h", 0.0)

    # --- Step 2: Estimate liquidity from Jupiter indexed pools ---
    token_info["liquidity_usd"] = estimate_token_liquidity(mint)

    # --- Step 3: Get name from Jupiter token metadata ---
    metadata = get_jupiter_token_metadata(mint)
    if metadata:
        token_info["name"] = metadata.get("name", symbol)

    # --- Step 4: Routability check (used in both scoring and display) ---
    token_info["routable"] = is_token_routable_to_sol(mint)

    # --- Step 5: Basic risk scoring ---
    if token_info["volume_24h"] < 5000:
        token_info["risk_score"] += 1
    if token_info["liquidity_usd"] < 1000:
        token_info["risk_score"] += 1
    if token_info["price_usd"] == 0:
        token_info["risk_score"] += 1
    if not token_info["routable"]:
        token_info["risk_score"] += 1

    if include_logs:
        print(f"[SCREENER] Profile for {symbol}:")
        for k, v in token_info.items():
            print(f"  {k}: {v}")

    return token_info


def screen_token_list(token_list: list, show_all=False) -> list:
    """
    Accepts a list of {"symbol": "BONK", "mint": "..."} dicts.
    Returns enriched list with screener metrics.
    """
    results = []
    for token in token_list:
        result = get_token_profile(token["symbol"], token["mint"])
        if show_all or result["risk_score"] <= 2:
            results.append(result)
    return results

