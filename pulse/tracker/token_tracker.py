import requests
from pulse.config import VALID_USER_TOKENS
from pulse.onchain.onchain_price import get_token_price_usd
from pulse.onchain.onchain_metrics import estimate_24h_volume

# === Constants ===
SOLANA_MINT = "So11111111111111111111111111111111111111112"
JUP_TOKEN_LIST_API = "https://token.jup.ag/all"
COINGECKO_SOL_PRICE_API = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"

# === Runtime State ===
JUPITER_TOKEN_LIST = None
UNSUPPORTED_TOKENS = set()

# === Utility Functions ===
def safe_float(val):
    try:
        if isinstance(val, dict) and "value" in val:
            return float(val["value"])
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def get_sol_usd_price():
    try:
        response = requests.get(COINGECKO_SOL_PRICE_API, timeout=5)
        response.raise_for_status()
        return response.json().get("solana", {}).get("usd", 0.0)
    except Exception as e:
        print(f"[TRACKER WARNING] Failed to fetch SOL/USD price: {e}")
        return 0.0

# === Jupiter Token Handling ===
def get_jupiter_token_metadata(mint):
    global JUPITER_TOKEN_LIST

    if JUPITER_TOKEN_LIST is None:
        try:
            print("[TRACKER] Fetching Jupiter token list...")
            response = requests.get(JUP_TOKEN_LIST_API, timeout=5)
            response.raise_for_status()
            JUPITER_TOKEN_LIST = response.json()
            print(f"[TRACKER] Jupiter list loaded with {len(JUPITER_TOKEN_LIST)} tokens.")
        except Exception as e:
            print(f"[TRACKER ERROR] Failed to load Jupiter token list: {e}")
            JUPITER_TOKEN_LIST = []

    token = next((t for t in JUPITER_TOKEN_LIST if t["address"] == mint), None)

    if token:
        return token

    print(f"[TRACKER WARNING] No metadata found for mint: {mint}")
    return None

def is_token_routable_to_sol(mint):
    token_meta = get_jupiter_token_metadata(mint)
    return token_meta is not None

# === Primary Entry Point ===
def fetch_token_metrics(symbol, mint):
    if mint in UNSUPPORTED_TOKENS:
        print(f"[TRACKER] Skipping unsupported token: {symbol}")
        return None

    if not is_token_routable_to_sol(mint):
        print(f"[TRACKER] Token {symbol} not routable to SOL. Skipping.")
        UNSUPPORTED_TOKENS.add(mint)
        return None

    price = get_token_price_usd(mint)
    volume = estimate_24h_volume(mint, price)

    if price == 0 and volume == 0:
        UNSUPPORTED_TOKENS.add(mint)
        return None

    return {
        "symbol": symbol,
        "name": symbol,
        "price_usd": round(price, 8),
        "liquidity_usd": 0.0,  # to be filled in screener
        "volume_24h": round(volume, 2)
    }

# === CLI Debug Helper ===
def print_token_metrics():
    print("[TRACKER] Collecting token metrics from all monitored tokens:")
    successful = []
    skipped = []

    for token in VALID_USER_TOKENS:
        print(f"--- {token['symbol']} ---")
        metrics = fetch_token_metrics(token['symbol'], token['mint'])
        if metrics:
            successful.append(token['symbol'])
            for key, value in metrics.items():
                print(f"  {key}: {value}")
        else:
            skipped.append(token['symbol'])
            print(f"  No data available for {token['symbol']}")

    print("\n[TRACKER SUMMARY]")
    if successful:
        print(f"  ✅ Success: {', '.join(successful)}")
    if skipped:
        print(f"  ⛔ Skipped: {', '.join(skipped)}")
