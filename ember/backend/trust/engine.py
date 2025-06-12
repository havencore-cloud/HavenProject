from trust.metadata import check_token_trust
from trust.jupiter import get_token_metadata, is_token_routable
from trust.metaplex import decode_metaplex_metadata
from trust.liquidity import get_raydium_liquidity
from database import get_cached_report, save_report
from liquidity.raydium_cache import get_raydium_liquidity_from_cache


def generate_trust_report(mint: str, force: bool = False):
    if not force:
        cached = get_cached_report(mint)
        if cached:
            print(f"[CACHE] Returning cached report for {mint}")
            return cached

    print(f"[SCAN] Running full trust report for {mint}")
    badges = []
    flags = []

    # === Liquidity Check ===
    liquidity_info = get_raydium_liquidity_from_cache(mint)
    if liquidity_info["found"]:
        badges.append(f"💧 Liquidity Found: ${liquidity_info['liquidity_usd']}")
    else:
        flags.extend(liquidity_info["warnings"])

    # === Metaplex Metadata ===
    meta = decode_metaplex_metadata(mint)
    declared_authority = meta.get("updateAuthority") if meta else "Unknown"

    if meta:
        if "fallback_keys" in meta:
            suspected = meta["fallback_keys"]
            if suspected:
                flags.append("⚠️ Hidden update authority detected.")
                meta["suspected_update_authorities"] = suspected
            del meta["fallback_keys"]

        if declared_authority != "Unknown":
            if declared_authority == "11111111111111111111111111111111":
                badges.append("✅ Immutable Metadata")
            else:
                badges.append("⚠️ Metadata can still be changed.")
        else:
            flags.append("❌ Metadata unreadable")
    else:
        flags.append("❌ No metadata account found.")

    # === On-chain Update Authority (RPC-level trust check) ===
    trust_status, on_chain_authority = check_token_trust(mint)
    if trust_status != "✅ Immutable Metadata":
        flags.append("Update authority not burned.")
    badges.append(trust_status)

    # Flag mismatch if authorities differ
    if on_chain_authority != declared_authority and declared_authority != "Unknown":
        flags.append("⚠️ Mismatch between declared and on-chain update authority!")

    # === Jupiter Token Metadata ===
    token_meta = get_token_metadata(mint)
    if not token_meta:
        flags.append("Token not found in Jupiter list.")
    elif not is_token_routable(mint):
        flags.append("Token is not routable to SOL.")
    else:
        badges.append("🌐 Routable via Jupiter")

    # === Assemble Final Report ===
    report = {
        "mint": mint,
        "update_authority": {
            "on_chain": on_chain_authority,
            "declared": declared_authority,
        },
        "badges": sorted(set(badges)),
        "flags": sorted(set(flags)),
        "token_metadata": {
            k: v for k, v in meta.items() if k not in ["updateAuthority", "mint"]
        } if meta else {},
        "liquidity": liquidity_info,
    }

    save_report(mint, report)
    print(f"[CACHE] Saved fresh report for {mint}")
    return report