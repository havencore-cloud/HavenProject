# ember/backend/trust/metadata.py

from solders.pubkey import Pubkey
from solana.rpc.api import Client
from trust.metaplex import decode_metaplex_metadata
import base64

METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

def get_metadata_pda(mint_address: str):
    mint_key = Pubkey.from_string(mint_address)
    seed = [b"metadata", bytes(METADATA_PROGRAM_ID), bytes(mint_key)]
    metadata_pda, _ = Pubkey.find_program_address(seed, METADATA_PROGRAM_ID)
    return metadata_pda

def fetch_metadata_account(mint_address: str, rpc_url="https://api.mainnet-beta.solana.com"):
    client = Client(rpc_url)
    metadata_pda = get_metadata_pda(mint_address)
    resp = client.get_account_info(metadata_pda)
    
    if (
    not resp.value or
    not hasattr(resp.value, "data") or
    not resp.value.data or
    not isinstance(resp.value.data, (list, tuple)) or
    len(resp.value.data) < 1
):
        return None
    
    raw_data = base64.b64decode(resp.value.data[0])
    return raw_data

def parse_update_authority(raw_data: bytes):
    if not raw_data or len(raw_data) < 33:
        return "Unknown"
    try:
        return str(Pubkey.from_bytes(raw_data[1:33]))
    except Exception:
        return "Unknown"

def assess_trust(update_authority_str):
    if update_authority_str in ["11111111111111111111111111111111", "Unknown"]:
        return "✅ Immutable Metadata"
    return "⚠️ Update Authority Active"

def check_token_trust(mint):
    # === Step 1: Try on-chain raw fetch
    data = fetch_metadata_account(mint)
    if data is not None:
        update_auth = parse_update_authority(data)
        trust_status = assess_trust(update_auth)
        print(f"[TRUST] On-chain authority via RPC: {update_auth} → {trust_status}")
        return trust_status, update_auth

    # === Step 2: Fallback to Metaplex decode
    print(f"[TRUST] RPC fetch failed — falling back to decode_metaplex_metadata()")
    meta = decode_metaplex_metadata(mint)

    if meta and "updateAuthority" in meta:
        fallback_auth = meta["updateAuthority"]
        trust_status = assess_trust(fallback_auth)
        print(f"[TRUST] Fallback authority from Metaplex decode: {fallback_auth} → {trust_status}")
        return trust_status, fallback_auth

    print(f"[TRUST] Fallback decode failed. No valid metadata found.")
    return "❓ No Metadata Found", "Unknown"