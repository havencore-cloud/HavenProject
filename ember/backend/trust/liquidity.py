import os
from dotenv import load_dotenv
from liquidity.raydium_decoder import fetch_single_pool

load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

if not HELIUS_API_KEY:
    raise RuntimeError("Helius API key not found in .env")

def get_liquidity_score(pool_address: str):
    print(f"[LIQUIDITY SCORE] Running for pool: {pool_address}")
    try:
        pool_data = fetch_single_pool(pool_address)
        if not pool_data:
            raise ValueError("No data returned for pool")

        base = pool_data.get("baseReserve", 0)
        quote = pool_data.get("quoteReserve", 0)
        liquidity = base + quote

        token0 = pool_data.get("baseMint", "?")
        token1 = pool_data.get("quoteMint", "?")
        pair_label = f"{token0[-4:]}/{token1[-4:]}"  # Shorten for readability

        score = (
            1 if liquidity > 1_000_000 else
            0.7 if liquidity > 100_000 else
            0.3 if liquidity > 10_000 else
            0
        )

        return {
            "score": score,
            "baseMint": token0,
            "quoteMint": token1,
            "baseReserve": base,
            "quoteReserve": quote,
            "pair": pair_label
        }

    except Exception as e:
        print(f"[ERROR] Liquidity scoring failed: {e}")
        return {
            "score": 0,
            "error": str(e)
        }
