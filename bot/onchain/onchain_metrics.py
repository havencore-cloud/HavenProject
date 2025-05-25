# onchain/onchain_metrics.py
# Estimates token 24h volume using Helius API and actual token price

import os
import requests
from dotenv import load_dotenv

load_dotenv()

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

def estimate_24h_volume(mint_address: str, token_price_usd: float = 0.001) -> float:
    """
    Estimates 24-hour USD volume for a token using Helius transfer logs and current price.
    """
    if not HELIUS_API_KEY:
        print("[HELIUS ERROR] API key not found in .env")
        return 0.0

    url = f"https://api.helius.xyz/v0/tokens/{mint_address}/transfers?type=token&api-key={HELIUS_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[HELIUS ERROR] {response.status_code} response from Helius")
            return 0.0

        data = response.json()
        if not isinstance(data, list):
            print(f"[HELIUS WARNING] Unexpected response format: {data}")
            return 0.0

        total_amount = 0
        for tx in data:
            amount = tx.get("amount", 0)
            try:
                amount = int(amount)
                total_amount += amount
            except Exception as e:
                print(f"[HELIUS WARNING] Skipping invalid amount: {amount}")

        # Convert to USD
        # Many Solana tokens use 6 decimals (adjust if needed)
        usd_volume = (total_amount / 10**6) * (token_price_usd or 0.001)
        return round(usd_volume, 2)

    except Exception as e:
        print(f"[HELIUS EXCEPTION] Failed to fetch volume: {e}")
        return 0.0
