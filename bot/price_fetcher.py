# bot/price_fetcher.py
# Fetches token price (on-chain) and 24h volume (Helius)

import os
from dotenv import load_dotenv
from bot.tracker.token_tracker import get_jupiter_token_metadata, is_token_routable_to_sol
from bot.onchain.onchain_metrics import estimate_24h_volume
from bot.onchain.onchain_price import get_token_price_usd

load_dotenv()

UNSUPPORTED_TOKENS = set()

def fetch_token_metrics(symbol, mint):
    if mint in UNSUPPORTED_TOKENS:
        print(f"[TRACKER] Skipping unsupported token: {symbol}")
        return None

    if not is_token_routable_to_sol(mint):
        print(f"[TRACKER] Warning: {symbol} not routable to SOL. Using fallback only.")
        UNSUPPORTED_TOKENS.add(mint)
        return None

    try:
        price_usd = get_token_price_usd(mint)
        volume_usd = estimate_24h_volume(mint, price_usd)
        meta = get_jupiter_token_metadata(mint)

        return {
            "symbol": symbol,
            "name": meta.get("symbol", symbol) if meta else symbol,
            "price_usd": round(price_usd, 8),
            "liquidity_usd": 0.0,
            "volume_24h": round(volume_usd, 2)
        }

    except Exception as e:
        print(f"[TRACKER WARNING] Failed to fetch metrics for {symbol}: {e}")
        UNSUPPORTED_TOKENS.add(mint)
        return None
