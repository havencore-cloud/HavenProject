import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey

RAYDIUM_AMM_V4 = "RVKd61ztZW9pVSVfVGnHJAWvMRtd9bZijBtkzjXkzDS"
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
client = Client(SOLANA_RPC_URL)


def get_raydium_liquidity(mint_address: str):
    try:
        mint_address = mint_address.strip().lower()
        # Fetch all pool IDs
        ids_response = requests.get("https://api-v3.raydium.io/pools/info/ids", timeout=7)
        ids_response.raise_for_status()
        pool_ids = ids_response.json()

        matched_pools = []
        total_liquidity = 0.0

        for pool_id in pool_ids:
            # Fetch detailed info for each pool
            pool_response = requests.get(f"https://api-v3.raydium.io/pools/key/ids?ids={pool_id}", timeout=7)
            pool_response.raise_for_status()
            pool_data = pool_response.json()

            for pool in pool_data:
                token0 = (pool.get("token0Mint") or "").lower()
                token1 = (pool.get("token1Mint") or "").lower()

                if mint_address in [token0, token1]:
                    liquidity = float(pool.get("liquidityUsd", 0) or 0)
                    symbol0 = pool.get("token0Symbol") or "?"
                    symbol1 = pool.get("token1Symbol") or "?"
                    pair_label = f"{symbol0}/{symbol1}"

                    matched_pools.append({
                        "pair": pair_label,
                        "liquidity_usd": liquidity,
                        "token0": token0,
                        "token1": token1
                    })

                    total_liquidity += liquidity

        if not matched_pools:
            print(f"[LIQUIDITY] No Raydium pool found for mint {mint_address}")
            return {
                "found": False,
                "liquidity_usd": 0,
                "pair": "Not found",
                "pools": [],
                "warnings": ["Pool not detected on Raydium"]
            }

        # Deepest pool used as label for the highest liquidity pairing
        deepest_pool = max(matched_pools, key=lambda p: p["liquidity_usd"])

        return {
            "found": True,
            "liquidity_usd": round(total_liquidity, 2),
            "pair": deepest_pool["pair"],
            "pools": matched_pools,
            "warnings": []
        }

    except requests.exceptions.RequestException as e:
        print(f"[LIQUIDITY ERROR] Request failed: {e}")
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "Error",
            "pools": [],
            "warnings": [f"Network error: {str(e)}"]
        }
    except Exception as e:
        print(f"[LIQUIDITY ERROR] Unexpected: {e}")
        return {
            "found": False,
            "liquidity_usd": 0,
            "pair": "Error",
            "pools": [],
            "warnings": [f"Unexpected error: {str(e)}"]
        }