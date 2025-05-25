# ember/backend/trust/jupiter.py

import requests

JUPITER_TOKEN_LIST_API = "https://token.jup.ag/all"
JUPITER_TOKEN_LIST = None

def load_jupiter_token_list():
    global JUPITER_TOKEN_LIST
    if JUPITER_TOKEN_LIST is None:
        try:
            print("[JUPITER] Fetching token list...")
            response = requests.get(JUPITER_TOKEN_LIST_API, timeout=5)
            response.raise_for_status()
            JUPITER_TOKEN_LIST = response.json()
            print(f"[JUPITER] Loaded {len(JUPITER_TOKEN_LIST)} tokens.")
        except Exception as e:
            print(f"[JUPITER ERROR] Failed to load list: {e}")
            JUPITER_TOKEN_LIST = []

def get_token_metadata(mint: str):
    load_jupiter_token_list()
    return next((token for token in JUPITER_TOKEN_LIST if token["address"] == mint), None)

def is_token_routable(mint: str):
    return get_token_metadata(mint) is not None
