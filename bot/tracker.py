# tracker.py
import requests
import time
from config import MONITORED_TOKENS

HEADERS = {"accept": "application/json"}

SOLANA_MINT = "So11111111111111111111111111111111111111112"
JUP_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUP_TOKEN_LIST_API = "https://cache.jup.ag/tokens"
JUP_ROUTE_API = "https://quote-api.jup.ag/v6/quote"
COINGECKO_SOL_PRICE = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"

# Runtime memory
JUPITER_TOKEN_LIST = None
UNSUPPORTED_TOKENS = set()

# Manual fallback metadata for unsupported tokens
MANUAL_TOKEN_METADATA = {
    "DezXjRtYhR6A7gM7DMaJpE8zQw1rxJ3mMhXXa9eDUQMZ": {"symbol": "BONK", "decimals": 5},
    "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB": {"symbol": "JUP", "decimals": 6},
    "DoggPwRTnFZ6EwgzqQXZonX5v1FugZ6ZT2ZkXkPYDwbH": {"symbol": "WIF", "decimals": 6},
}

def safe_float(val):
    try:
        if isinstance(val, dict) and "value" in val:
            return float(val["value"])
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def get_sol_usd_price():
    try:
        r = requests.get(COINGECKO_SOL_PRICE, timeout=5)
        r.raise_for_status()
        return r.json().get("solana", {}).get("usd", 0.0)
    except:
        return 0.0

def get_jupiter_token_metadata(mint):
    global JUPITER_TOKEN_LIST

    if JUPITER_TOKEN_LIST is None:
        try:
            print("[TRACKER] Fetching Jupiter token list...")
            r = requests.get(JUP_TOKEN_LIST_API, timeout=5)
            r.raise_for_status()
            JUPITER_TOKEN_LIST = r.json()
        except Exception as e:
            print(f"[TRACKER ERROR] Failed to fetch Jupiter token list: {e}")
            JUPITER_TOKEN_LIST = []

    return next((t for t in JUPITER_TOKEN_LIST if t["address"] == mint), MANUAL_TOKEN_METADATA.get(mint))

def is_token_routable_to_sol(mint):
    try:
        token_meta = get_jupiter_token_metadata(mint)
        if not token_meta:
            return False

        decimals = token_meta.get("decimals", 6)
        amount = int(10 * (10 ** decimals))  # 10 tokens

        url = f"{JUP_ROUTE_API}?inputMint={mint}&outputMint={SOLANA_MINT}&amount={amount}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def fetch_from_dexscreener(symbol, mint):
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{mint}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        pairs = response.json().get("pairs", [])
        if not pairs:
            print(f"[TRACKER ERROR] Dexscreener returned no pairs for {symbol}")
            return None

        best_pair = pairs[0]
        return {
            "symbol": best_pair.get("baseToken", {}).get("symbol", symbol),
            "name": best_pair.get("baseToken", {}).get("name", symbol),
            "price_usd": safe_float(best_pair.get("priceUsd")),
            "liquidity_usd": safe_float(best_pair.get("liquidity")),
            "volume_24h": safe_float(best_pair.get("volume"))
        }
    except Exception as e:
        print(f"[TRACKER ERROR] Dexscreener failed for {symbol}: {e}")
        return None

def fetch_from_jupiter(symbol, mint):
    try:
        token_meta = get_jupiter_token_metadata(mint)
        if not token_meta:
            raise ValueError(f"Token metadata not found for mint: {mint}")

        decimals = token_meta.get("decimals", 6)
        base_amount = 10  # quote 10 tokens instead of 1 to avoid tiny amount errors
        amount = int(base_amount * (10 ** decimals))

        url = f"{JUP_QUOTE_API}?inputMint={mint}&outputMint={SOLANA_MINT}&amount={amount}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        out_amount = data.get("outAmount")
        output_decimals = data.get("outputTokenInfo", {}).get("decimals", 9)
        sol_price = int(out_amount) / (10 ** output_decimals)

        sol_usd = get_sol_usd_price()
        price_usd = sol_price * sol_usd / base_amount  # convert back to per-token

        return {
            "symbol": symbol,
            "name": symbol,
            "price_usd": round(price_usd, 8),
            "liquidity_usd": 0.0,
            "volume_24h": 0.0
        }

    except Exception as e:
        print(f"[TRACKER WARNING] Jupiter fallback failed for {symbol}: {e}")
        return None

def fetch_token_metrics(symbol, mint):
    if mint in UNSUPPORTED_TOKENS:
        print(f"[TRACKER] Skipping unsupported token: {symbol}")
        return None

    data = fetch_from_dexscreener(symbol, mint)
    if data:
        return data

    print(f"[TRACKER] Dexscreener fallback engaged for {symbol}.")

    if not is_token_routable_to_sol(mint):
        print(f"[TRACKER] Token {symbol} not routable to SOL. Skipping.")
        UNSUPPORTED_TOKENS.add(mint)
        return None

    fallback_data = fetch_from_jupiter(symbol, mint)

    if fallback_data is None:
        UNSUPPORTED_TOKENS.add(mint)

    return fallback_data

def print_token_metrics():
    print("[TRACKER] Collecting token metrics from all monitored tokens:")
    successful = []
    skipped = []

    for token in MONITORED_TOKENS:
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
