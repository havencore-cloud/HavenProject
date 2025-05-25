# bot/liquidity/liquidity_lookup.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
DAS_ADDRESS_URL = "https://api.helius.xyz/v0/addresses"

def get_token_metadata(mint_address):
    url = f"{DAS_ADDRESS_URL}/{mint_address}?api-key={HELIUS_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("tokenInfo", {})
    except Exception as e:
        print(f"[LIQUIDITY ERROR] Metadata fetch failed for {mint_address}: {e}")
    return None

def estimate_token_liquidity(mint_address):
    metadata = get_token_metadata(mint_address)
    if not metadata:
        print(f"[LIQUIDITY] No metadata found for {mint_address}")
        return 0.0

    decimals = metadata.get("decimals", 6)
    fallback_price = 0.001
    simulated_reserve = 1_000_000 * (10 ** decimals)
    usd_value = simulated_reserve / (10 ** decimals) * fallback_price
    return round(usd_value, 2)
