# token_safety.py
# Checks token mint authority, freeze flags, and optional trust whitelist

import requests
import base64
from solana.rpc.api import Client
import os
from dotenv import load_dotenv

load_dotenv()

# === Solana RPC setup ===
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
solana_client = Client(SOLANA_RPC_URL)

# === Optional: Manual Trust Lists ===
WHITELISTED_TOKENS = set([
    # "So11111111111111111111111111111111111111112",  # SOL
])

BLACKLISTED_TOKENS = set([
    # "SomeSketchyMintAddressHere"
])

def get_trust_status(mint: str) -> str:
    if mint in WHITELISTED_TOKENS:
        return "whitelisted"
    elif mint in BLACKLISTED_TOKENS:
        return "blacklisted"
    return "unknown"

def decode_token_account_data(data_base64: str):
    try:
        raw_data = base64.b64decode(data_base64)
        mint_authority_option = int.from_bytes(raw_data[0:4], "little")
        mint_authority = raw_data[4:36] if mint_authority_option else None
        supply = int.from_bytes(raw_data[36:44], "little")
        decimals = raw_data[44]
        is_initialized = raw_data[45] != 0
        freeze_authority_option = int.from_bytes(raw_data[46:50], "little")
        freeze_authority = raw_data[50:82] if freeze_authority_option else None

        return {
            "mintable": mint_authority is not None,
            "mint_authority": mint_authority.hex() if mint_authority else None,
            "freeze_authority": freeze_authority.hex() if freeze_authority else None,
            "decimals": decimals,
            "supply": supply,
            "initialized": is_initialized
        }
    except Exception as e:
        print(f"[SAFETY ERROR] Failed to decode account data: {e}")
        return {}

def get_token_authority_flags(mint_address: str) -> dict:
    try:
        response = solana_client.get_account_info(mint_address, encoding="base64")
        data = response.get("result", {}).get("value", {}).get("data", [None])[0]
        if not data:
            print(f"[SAFETY] No data found for token {mint_address}")
            return {}

        decoded = decode_token_account_data(data)
        decoded["trust_status"] = get_trust_status(mint_address)
        return decoded
    except Exception as e:
        print(f"[SAFETY ERROR] Failed to get authority flags: {e}")
        return {}

# Example Usage (you can delete or move this):
if __name__ == "__main__":
    from config import VALID_USER_TOKENS
    for token in VALID_USER_TOKENS:
        print("\n---", token["symbol"])
        print(get_token_authority_flags(token["mint"]))
