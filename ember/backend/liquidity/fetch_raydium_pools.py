# fetch_raydium_pools.py
import requests, json
from datetime import datetime

url = "https://api.raydium.io/pairs"
print("[FETCH] Getting Raydium liquidity pools...")
response = requests.get(url)
pools = response.json()

with open("liquidity/raydium_pools_cache.json", "w") as f:
    json.dump({
        "timestamp": datetime.utcnow().isoformat(),
        "pools": pools
    }, f)

print(f"[SAVE] {len(pools)} pools saved to raydium_pools_cache.json")