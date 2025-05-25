# config.py
import os
import json
from dotenv import load_dotenv
from bot.utilities.token_manager import load_tokens

# === Load .env settings ===
load_dotenv()

# === API Keys ===
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", None)

# === USER TOKEN MANAGEMENT ===
USER_TOKENS = load_tokens()
print(f"[DEBUG] Raw USER_TOKENS: {USER_TOKENS}")

# Filter out malformed or incomplete tokens
VALID_USER_TOKENS = []
for t in USER_TOKENS:
    if "mint" in t and len(t["mint"]) >= 32:
        VALID_USER_TOKENS.append({
            "symbol": t.get("symbol", t.get("name", "UNKNOWN")).upper(),
            "mint": t["mint"]
        })

print(f"[CONFIG] Loaded {len(VALID_USER_TOKENS)} valid user tokens.")

# Legacy alias
MONITORED_TOKENS = VALID_USER_TOKENS

# === Default Token Logic ===
DEFAULT_TOKEN = VALID_USER_TOKENS[0] if VALID_USER_TOKENS else {
    "symbol": "SOL",
    "mint": "So11111111111111111111111111111111111111112"
}

# === Runtime settings ===
DRY_RUN_MODE = os.getenv("DRY_RUN_MODE", "true").lower() == "true"
MONITORED_MODE = os.getenv("MONITORED_MODE", "false").lower() == "true"
STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", 0.02))
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 10))

# === Main config object ===
CONFIG = {
    "RPC_ENDPOINT": os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com"),
    "TRADE_TOKEN": {
        "SYMBOL": DEFAULT_TOKEN["symbol"],
        "ADDRESS": DEFAULT_TOKEN["mint"]
    },
    "TRADING": {
        "SLIPPAGE": 0.01,
        "TRADE_AMOUNT_USD": TRADE_AMOUNT,
        "PROFIT_TARGET": 0.05,
        "STOP_LOSS": STOP_LOSS_PERCENTAGE
    },
    "LOG_LEVEL": "INFO",
    "DEBUG": True
}

# === Module exports ===
__all__ = [
    "CONFIG",
    "DRY_RUN_MODE",
    "MONITORED_MODE",
    "STOP_LOSS_PERCENTAGE",
    "TRADE_AMOUNT",
    "HELIUS_API_KEY",
    "USER_TOKENS",
    "VALID_USER_TOKENS",
    "MONITORED_TOKENS"
]
