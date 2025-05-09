import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional API keys
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", None)

# Multi-token monitoring setup (replace or modify via GUI later)
MONITORED_TOKENS = [
    {
        "symbol": "BONK",
        "mint": "DezXjRtYhR6A7gM7DMaJpE8zQw1rxJ3mMhXXa9eDUQMZ"
    },
    {
        "symbol": "JUP",
        "mint": "JUP4Fb2cqiRUcaTHdrPC8h2gNsA2ETXiPDD33WcGuJB"
    },
    {
        "symbol": "WIF",
        "mint": "DoggPwRTnFZ6EwgzqQXZonX5v1FugZ6ZT2ZkXkPYDwbH"
    },
    {
  "symbol": "SOL",
  "mint": "So11111111111111111111111111111111111111112"
    }
]

# Default to the first monitored token as primary (if needed)
DEFAULT_TOKEN = MONITORED_TOKENS[0]

# ENV-driven toggles and thresholds
DRY_RUN_MODE = os.getenv("DRY_RUN_MODE", "true").lower() == "true"
MONITORED_MODE = os.getenv("MONITORED_MODE", "false").lower() == "true"
STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", 0.02))
TRADE_AMOUNT = float(os.getenv("TRADE_AMOUNT", 10))

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

QUOTE_URL = (
    f"https://quote-api.jup.ag/v6/quote?inputMint={DEFAULT_TOKEN['mint']}&outputMint=So11111111111111111111111111111111111111112&amount=1000000"
)

__all__ = [
    "CONFIG",
    "DRY_RUN_MODE",
    "MONITORED_MODE",
    "STOP_LOSS_PERCENTAGE",
    "TRADE_AMOUNT",
    "QUOTE_URL",
    "HELIUS_API_KEY",
    "MONITORED_TOKENS"
]
