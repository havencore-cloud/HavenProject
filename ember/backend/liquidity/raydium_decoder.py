import base64
import requests
from solders.pubkey import Pubkey
from construct import Struct, Int8ul, Int64ul, Bytes, ConstructError

# Struct layout for Raydium AMM V4 pool accounts
Int128ul = Bytes(16)
LIQUIDITY_STATE_LAYOUT_V4 = Struct(
    "status" / Int64ul,
    "nonce" / Int64ul,
    "max_order" / Int64ul,
    "depth" / Int64ul,
    "base_mint" / Bytes(32),
    "quote_mint" / Bytes(32),
    "lp_mint" / Bytes(32),
    "open_orders" / Bytes(32),
    "target_orders" / Bytes(32),
    "base_vault" / Bytes(32),
    "quote_vault" / Bytes(32),
    "market_id" / Bytes(32),
    "market_program_id" / Bytes(32),
    "base_decimals" / Int8ul,
    "quote_decimals" / Int8ul,
    "lp_decimals" / Int8ul,
    "padding" / Bytes(1),
    "base_reserve" / Int128ul,
    "quote_reserve" / Int128ul
)

# Your Helius API key (move this to .env later)
HELIUS_KEY = "your-helius-api-key"
HELIUS_RPC = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_KEY}"

# --- Fetch & Decode One Pool --- #
def fetch_single_pool(account_address: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [account_address, {"encoding": "base64"}]
    }

    try:
        resp = requests.post(HELIUS_RPC, json=payload).json()
        encoded_data = resp["result"]["value"]["data"][0]
        raw_data = base64.b64decode(encoded_data)
        parsed = LIQUIDITY_STATE_LAYOUT_V4.parse(raw_data)

        return {
            "baseMint": str(Pubkey.from_bytes(parsed.base_mint)),
            "quoteMint": str(Pubkey.from_bytes(parsed.quote_mint)),
            "lpMint": str(Pubkey.from_bytes(parsed.lp_mint)),
            "baseReserve": int.from_bytes(parsed.base_reserve, "little"),
            "quoteReserve": int.from_bytes(parsed.quote_reserve, "little"),
        }
    except (KeyError, IndexError, ConstructError, TypeError) as e:
        print(f"[ERROR] Failed to parse pool {account_address}: {e}")
        return None

# --- Calculate Trust Score --- #
def get_liquidity_score(pool_address: str):
    result = fetch_single_pool(pool_address)
    if result:
        base = result["baseReserve"]
        quote = result["quoteReserve"]
        total = base + quote
        score = (
            100 if total > 1_000_000 else
            60 if total > 100_000 else
            30 if total > 10_000 else
            5
        )
        return {
            "score": score,
            "baseMint": result["baseMint"],
            "quoteMint": result["quoteMint"],
            "baseReserve": base,
            "quoteReserve": quote,
            "lpMint": result["lpMint"]
        }

    return {
        "score": 0,
        "error": "No pool found or decode failed"
    }

# --- Example Usage --- #
if __name__ == "__main__":
    test_pool = "8HoQnePLqPj4M7PUDzfw8e3Ymdwgc7NLGnaTUapubyvu"  # WSOL/USDC
    result = get_liquidity_score(test_pool)
    print(result)
