import json
from trust.metadata import decode_metaplex_metadata, check_token_trust, assess_trust
from trust.jupiter import is_token_routable
from trust.metaplex import clean_bytes
from report_cache import save_report, get_cached_report
from liquidity.jupiter_scanner import get_liquidity_info_for_token
from trust.liquidity import get_liquidity_score

def get_update_authority_with_fallback(mint: str):
    print(f"[TRUST] RPC fetch failed — falling back to decode_metaplex_metadata()")
    meta = decode_metaplex_metadata(mint)
    if meta and "updateAuthority" in meta:
        fallback_auth = meta["updateAuthority"]
        trust_status = assess_trust(fallback_auth)
        print(f"[TRUST] Fallback authority from Metaplex decode: {fallback_auth} → {trust_status}")
        return trust_status, fallback_auth
    return "❓ No Metadata Found", "Unknown"

def generate_trust_report(mint: str, force: bool = False):
    print(f"[DEBUG] Starting trust report for mint: {mint}")
    try:
        cached = get_cached_report(mint)
        if cached and not force:
            print(f"[CACHE] Returning cached report for {mint}")
            return cached

        print(f"[SCAN] Running full trust report for {mint}")
        badges = []
        flags = []

        # === Liquidity Check ===
        liquidity_info = {
            "found": False,
            "liquidity_usd": 0,
            "pair": "None",
            "pools": [],
            "warnings": ["Liquidity lookup skipped or failed"]
        }
        pool_score = {"score": 0, "error": "lookup failed"}

        try:
            liquidity_info = get_liquidity_info_for_token(mint)
            print(f"[DEBUG] Jupiter liquidity info: {json.dumps(liquidity_info, indent=2)}")

            if liquidity_info.get("pools"):
                first_pool = liquidity_info["pools"][0]
                pool_address = first_pool.get("amm_id")

                print(f"[DEBUG] Pool JSON: {json.dumps(first_pool, indent=2)}")
                print(f"[TRACE] Calling get_liquidity_score with pool_address = {pool_address}")
                print(f"[TRACE] Full first_pool object:\n{json.dumps(first_pool, indent=2)}")

                if pool_address:
                    pool_score = get_liquidity_score(pool_address)
                    print(f"[DEBUG] Raydium pool trust score: {pool_score}")
                else:
                    print("[INFO] No Raydium pool address found in pool object.")
            else:
                print("[INFO] No pools returned from Jupiter.")
        except Exception as e:
            print(f"[ERROR] Raydium pool scoring failed: {e}")
            pool_score = {"score": 0, "error": str(e)}

        # === Metadata Check ===
        meta = decode_metaplex_metadata(mint)
        declared = meta.get("updateAuthority") if isinstance(meta, dict) else "Unknown"
        name = clean_bytes(meta.get("name", "")) if isinstance(meta, dict) else ""
        symbol = clean_bytes(meta.get("symbol", "")) if isinstance(meta, dict) else ""

        if declared == "11111111111111111111111111111111":
            badges.append("✅ Immutable Metadata")
        elif declared != "Unknown":
            badges.append("⚠️ Metadata can still be changed.")
        else:
            flags.append("❌ Metadata unreadable")

        try:
            trust_status, on_chain = check_token_trust(mint)
        except:
            trust_status, on_chain = get_update_authority_with_fallback(mint)

        if trust_status != "✅ Immutable Metadata":
            flags.append("Update authority not burned.")
        badges.append(trust_status)

        if on_chain != declared and declared != "Unknown":
            flags.append("⚠️ Mismatch between declared and on-chain update authority!")

        liquidity_usd = liquidity_info.get("liquidity_usd", 0.0)
        pool_pair = liquidity_info.get("pair", "None")

        # === Jupiter Check ===
        jupiter = is_token_routable(mint)
        if jupiter:
            badges.append("🌐 Tradable via Jupiter")
        else:
            flags.append("⚠️ Token not listed in Jupiter tradable tokens")

        # === Final Report ===
        report = {
            "mint": mint,
            "update_authority": {
                "on_chain": on_chain,
                "declared": declared,
            },
            "badges": sorted(set(badges)),
            "flags": sorted(set(flags)),
            "token_metadata": {
                "name": name,
                "symbol": symbol,
            },
            "liquidity": {
                "found": liquidity_info.get("found", False),
                "pair": pool_pair,
                "liquidity_usd": liquidity_usd,
                "trust_score": pool_score,
                "warnings": liquidity_info.get("warnings", [])
            },
            "jupiter_tradable": jupiter,
        }

        save_report(mint, report)
        print(f"[FINAL REPORT JSON]\n{json.dumps(report, indent=2)}")
        return report

    except Exception as e:
        print(f"[ERROR] Trust report generation failed: {e}")
        return {"error": f"Failed to generate trust report: {e}"}
