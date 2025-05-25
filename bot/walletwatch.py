# walletwatch.py
# Track wallet activity for multiple tokens using Helius API

import requests
import time
from config import VALID_USER_TOKENS, HELIUS_API_KEY

BASE_URL = "https://api.helius.xyz/v0/token-transfers"
LAST_SEEN_SIGNATURES = {}

def fetch_wallet_activity(token_mint):
    if not HELIUS_API_KEY:
        print("[WALLETWATCH ERROR] Missing Helius API key.")
        return []

    params = {
        "api-key": HELIUS_API_KEY,
        "limit": 20,
        "mint": token_mint
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        new_trades = []
        last_seen = LAST_SEEN_SIGNATURES.get(token_mint)

        for tx in data:
            sig = tx.get("signature")
            if sig == last_seen:
                break
            new_trades.append(tx)

        if data:
            LAST_SEEN_SIGNATURES[token_mint] = data[0].get("signature")

        return list(reversed(new_trades))  # newest last

    except requests.RequestException as e:
        print(f"[WALLETWATCH ERROR] Helius fetch failed: {e}")
        return []

def print_wallet_trades():
    for token in VALID_USER_TOKENS:
        mint = token["mint"]
        print(f"\n[WALLETWATCH] Checking wallet activity for {token['symbol']}...")
        trades = fetch_wallet_activity(mint)

        if trades:
            for t in trades:
                from_address = t.get("fromUserAccount", "")[:6]
                to_address = t.get("toUserAccount", "")[:6]
                amount = t.get("amount", 0)
                print(f"  From: {from_address}... To: {to_address}... Amount: {amount}")
        else:
            print("  No new trades found.")
