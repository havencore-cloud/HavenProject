from trust.metadata import check_token_trust
from trust.jupiter import get_token_metadata, is_token_routable
from trust.metaplex import decode_metaplex_metadata
from trust.liquidity import get_raydium_liquidity

def generate_trust_report(mint: str):
    badges = []
    flags = []

    # === Raydium Liquidity Check ===
    liquidity_info = get_raydium_liquidity(mint)
    if liquidity_info["found"]:
        badges.append(f"💧 Liquidity Found: ${liquidity_info['liquidity_usd']}")
    else:
        flags.extend(liquidity_info["warnings"])

    # === Metaplex Metadata ===
    meta = decode_metaplex_metadata(mint)

    if meta:
        if "fallback_keys" in meta:
            suspected = meta["fallback_keys"]
            if suspected:
                flags.append("⚠️ Hidden update authority detected.")
                meta["suspected_update_authorities"] = suspected
            del meta["fallback_keys"]

        # Show status badge based on whether updateAuthority is readable
        if meta["updateAuthority"] != "Unknown":
            if meta["updateAuthority"] == "11111111111111111111111111111111":
                badges.append("✅ Immutable Metadata")
            else:
                badges.append("⚠️ Metadata can still be changed.")
        else:
            flags.append("❌ Metadata unreadable")
    else:
        flags.append("❌ No metadata account found.")

    # === On-chain Update Authority (extra verification) ===
    trust_status, update_authority = check_token_trust(mint)
    if trust_status != "✅ Immutable Metadata":
        flags.append("Update authority not burned.")
    badges.append(trust_status)

    # === Jupiter Token List ===
    token_meta = get_token_metadata(mint)
    if not token_meta:
        flags.append("Token not found in Jupiter list.")
    elif not is_token_routable(mint):
        flags.append("Token is not routable to SOL.")
    else:
        badges.append("🌐 Routable via Jupiter")

        return {
    "mint": mint,
    "update_authority": {
        "on_chain": update_authority,
        "declared": meta.get("updateAuthority") if meta else "Unknown"
    },
    "badges": list(set(badges)),
    "flags": list(set(flags)),
    "token_metadata": {
        k: v for k, v in meta.items() if k not in ["updateAuthority", "mint"]
    } if meta else {},
    "liquidity": liquidity_info,
}
