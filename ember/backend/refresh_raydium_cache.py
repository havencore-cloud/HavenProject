from liquidity.raydium_cache import update_raydium_cache

if __name__ == "__main__":
    RPC_URL = "https://api.mainnet-beta.solana.com"  # You can swap in a custom one later
    update_raydium_cache()