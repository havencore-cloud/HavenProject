from solana.rpc.api import Client
from solders.pubkey import Pubkey
import base64
from base58 import b58decode
from borsh_construct import CStruct, String, U16, U8

# Metaplex program ID
METADATA_PROGRAM_ID = Pubkey.from_string("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

def clean_bytes(b) -> str:
    if isinstance(b, bytes):
        return b.decode("utf-8", errors="ignore").rstrip("\x00").strip()
    return b.strip().rstrip("\x00")


# === Metaplex Borsh Layout ===
DataLayout = CStruct(
    "name" / String,
    "symbol" / String,
    "uri" / String,
    "seller_fee_basis_points" / U16,
    "has_creator" / U8,
)

def get_metadata_pda(mint_address: str) -> Pubkey:
    mint_key = Pubkey.from_string(mint_address)
    seeds = [b"metadata", bytes(METADATA_PROGRAM_ID), bytes(mint_key)]
    metadata_pda, _ = Pubkey.find_program_address(seeds, METADATA_PROGRAM_ID)
    return metadata_pda

def decode_metaplex_metadata(mint_address: str, rpc_url="https://api.mainnet-beta.solana.com"):
    print("[DEBUG] decode_metaplex_metadata was called ✅")
    client = Client(rpc_url)
    metadata_pda = get_metadata_pda(mint_address)
    print("[DEBUG] PDA for", mint_address, "is", metadata_pda)

    resp = client.get_account_info(metadata_pda)
    print("[DEBUG] RPC Response:", resp)

    if not resp.value or not resp.value.data:
        print("[DEBUG] No metadata account found.")
        return None
    try:
        # Convert directly from list of ints to bytes
        raw_data = bytes(resp.value.data)
        print("[DEBUG] Raw data length:", len(raw_data))
        print("[DEBUG] Raw data (first 100 bytes):", raw_data[:100])

    except Exception as e:
        print("[DEBUG] Failed base64 decode:", e)
        return None

    try:
        print("[DEBUG] Beginning metadata parse...")
        update_authority = Pubkey.from_bytes(raw_data[1:33])
        mint = Pubkey.from_bytes(raw_data[33:65])
        decoded = DataLayout.parse(raw_data[65:])
        print("[DEBUG] Decoded Borsh fields:", decoded)

        return {
            "updateAuthority": str(update_authority),
            "mint": str(mint),
            "name": clean_bytes(decoded.name),
            "symbol": clean_bytes(decoded.symbol),
            "uri": clean_bytes(decoded.uri),
            "sellerFeeBasisPoints": decoded.seller_fee_basis_points
        }
        
    except Exception as e:
        print("[DEBUG] Failed to parse metadata layout:", e)
        return None
