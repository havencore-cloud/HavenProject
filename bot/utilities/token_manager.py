import os
import json

# Base paths (ensures cross-platform compatibility and clarity)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
PROJECTS_FILE = os.path.join(BASE_DIR, "projects.json")
DEFAULT_FILE = os.path.join(BASE_DIR, "default_token.json")

# === File I/O ===

def load_tokens():
    if not os.path.exists(PROJECTS_FILE):
        print("[WARN] No projects.json file found.")
        return []
    with open(PROJECTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse projects.json.")
            return []

def save_tokens(tokens):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"[SAVE] Updated projects.json with {len(tokens)} token(s).")

# === Token Management ===

def add_token(symbol, mint, extra_fields=None):
    symbol = symbol.strip().upper()
    mint = mint.strip()
    tokens = load_tokens()

    if any(t["mint"] == mint for t in tokens):
        print(f"[INFO] Token {symbol} already exists.")
        return

    token_data = {
        "symbol": symbol,
        "name": symbol,
        "mint": mint,
        "whitelisted": False,
        "notes": "",
        "strategy": {
            "track_pnl": False,
            "watch_whales": False,
            "auto_trade": False
        }
    }

    if extra_fields:
        token_data.update(extra_fields)

    tokens.append(token_data)
    save_tokens(tokens)
    print(f"[SUCCESS] Added token {symbol} ({mint})")

def remove_token(mint):
    tokens = load_tokens()
    new_tokens = [t for t in tokens if t["mint"] != mint]
    if len(new_tokens) == len(tokens):
        print(f"[INFO] Token with mint {mint} not found.")
    else:
        save_tokens(new_tokens)
        print(f"[SUCCESS] Removed token with mint: {mint}")

# === Default Token Helpers ===

def set_default_token(mint):
    tokens = load_tokens()
    match = next((t for t in tokens if t["mint"] == mint), None)
    if not match:
        print("[ERROR] Token not found in project list.")
        return
    with open(DEFAULT_FILE, "w") as f:
        json.dump(match, f, indent=2)
    print(f"[DEFAULT SET] {match['symbol']} is now the default token.")

def get_default_token():
    if not os.path.exists(DEFAULT_FILE):
        print("[INFO] No default token set.")
        return None
    with open(DEFAULT_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("[ERROR] Failed to parse default_token.json.")
            return None
