# bot/onchain/onchain_price.py

import base64
import os
from solana.rpc.api import Client
from dotenv import load_dotenv
from solders.pubkey import Pubkey

load_dotenv()

# === RPC and Constants ===
SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
DEFAULT_SOL_PRICE = 145.00  # Fallback USD price for SOL
ORCA_BONK_SOL_POOL = "5zpyutJu9ee6jFymDGoK7F6S5Kczqtc9FomP3ueKuyA9"
RAYDIUM_BONK_SOL_POOL = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"

client = Client(SOLANA_RPC)

def get_reserves_from_pool(pool_address):
    try:
        pubkey = Pubkey.from_string(pool_address)
        result = client.get_account_info(pubkey)
        account_info = result.value
        if account_info is None:
            raise Exception("Account not found or empty")

        data = bytes(account_info.data)
        token_a_reserve = int.from_bytes(data[64:72], "little")
        token_b_reserve = int.from_bytes(data[72:80], "little")

        return token_a_reserve, token_b_reserve

    except Exception as e:
        print(f"[POOL ERROR] Failed to read pool {pool_address}: {e}")
        return None

def get_token_price_usd(token_mint: str) -> float:
    """
    Attempts to calculate token price by reading from Orca, then Raydium.
    """
    # === Try Orca ===
    reserves = get_reserves_from_pool(ORCA_BONK_SOL_POOL)
    if reserves:
        token, sol = sorted(reserves)
        if token > 0:
            sol_per_token = sol / token
            usd_price = sol_per_token * DEFAULT_SOL_PRICE
            print("[ORCA] Used Orca pool.")
            return round(usd_price, 8)

    # === Fallback to Raydium ===
    reserves = get_reserves_from_pool(RAYDIUM_BONK_SOL_POOL)
    if reserves:
        token, sol = sorted(reserves)
        if token > 0:
            sol_per_token = sol / token
            usd_price = sol_per_token * DEFAULT_SOL_PRICE
            print("[RAYDIUM] Used Raydium pool.")
            return round(usd_price, 8)

    print("[PRICE ERROR] No valid reserves found in Orca or Raydium.")
    return 0.0
