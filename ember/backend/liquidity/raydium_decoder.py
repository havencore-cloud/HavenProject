import base58
import base64
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from construct import Struct, Int8ul, Int64ul, Bytes
from solana.rpc.types import MemcmpOpts, DataSliceOpts

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

def fetch_all_raydium_pools(rpc_url: str):
    print("[DECODER] Requesting program accounts...")
    client = Client(rpc_url)

    # status = 6 (active), little-endian u64 encoded as base58
    status_bytes = (6).to_bytes(8, "little")
    status_base58 = base58.b58encode(status_bytes).decode()

    filters = [
    MemcmpOpts(
        offset=0,
        bytes=status_base58
    )
]

    resp = client.get_program_accounts(
    Pubkey.from_string("RVKd61ztZW9pVSVfVGnHJAWvMRtd9bZijBtkzjXkzDS"),
    encoding="base64",
    filters=filters  # ✅ all filters together
)

    pools = []
    for acct in resp.value:
        try:
            encoded_data = acct.account.data[0]
            decoded_data = base64.b64decode(encoded_data)
            decoded = LIQUIDITY_STATE_LAYOUT_V4.parse(decoded_data)

            pools.append({
                "baseMint": str(Pubkey.from_bytes(decoded.base_mint)),
                "quoteMint": str(Pubkey.from_bytes(decoded.quote_mint)),
                "lpMint": str(Pubkey.from_bytes(decoded.lp_mint)),
                "baseReserve": int.from_bytes(decoded.base_reserve, "little"),
                "quoteReserve": int.from_bytes(decoded.quote_reserve, "little"),
            })
        except Exception as e:
            print(f"[PARSE ERROR] {e}")
            continue

    print(f"[DECODER] Parsed {len(pools)} pools from chain.")
    return pools
