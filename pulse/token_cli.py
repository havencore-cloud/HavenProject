import json
import os

TOKENS_FILE = "monitored_tokens.json"

def load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return []
    with open(TOKENS_FILE, "r") as f:
        return json.load(f)

def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

def add_token():
    symbol = input("Enter token symbol: ").strip().upper()
    mint = input("Enter token mint address: ").strip()
    tokens = load_tokens()

    if any(t["mint"] == mint for t in tokens):
        print("[INFO] Token already exists in the list.")
        return

    tokens.append({"symbol": symbol, "mint": mint})
    save_tokens(tokens)
    print(f"[SUCCESS] Added token {symbol} ({mint})")

def view_tokens():
    tokens = load_tokens()
    if not tokens:
        print("[INFO] No tokens are currently being monitored.")
    else:
        print("[TOKENS]")
        for idx, t in enumerate(tokens, start=1):
            print(f"  {idx}. {t['symbol']} - {t['mint']}")

def select_default_token():
    tokens = load_tokens()
    if not tokens:
        print("[ERROR] No tokens to select from.")
        return

    view_tokens()
    choice = input("Select default token by number: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(tokens)):
        print("[ERROR] Invalid selection.")
        return

    selected = tokens[int(choice) - 1]
    with open("default_token.json", "w") as f:
        json.dump(selected, f)

    print(f"[DEFAULT SET] {selected['symbol']} is now the default token.")

def manage_tokens():
    while True:
        print("\n[TOKEN MANAGER]")
        print("1. View monitored tokens")
        print("2. Add new token")
        print("3. Set default token")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_tokens()
        elif choice == "2":
            add_token()
        elif choice == "3":
            select_default_token()
        elif choice == "4":
            break
        else:
            print("[ERROR] Invalid option.")
