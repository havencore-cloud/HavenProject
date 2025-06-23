import sys
import os
import asyncio
import json
import websockets
from pulse.config import VALID_USER_TOKENS

# === Ensure proper path resolution ===
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# === WebSocket settings ===
SOLANA_WS_URL = "wss://api.mainnet-beta.solana.com"
MINTS_TO_WATCH = [token["mint"] for token in VALID_USER_TOKENS]

# === Log decoder ===
def decode_transfer_log(logs):
    for line in logs:
        if "Instruction: Transfer" in line:
            print("[EVENT] SPL Token Transfer instruction detected.")
        elif "Transfer" in line and "tokens from" in line:
            parts = line.replace("Program log: ", "").split("Transfer")[1].strip().split(" tokens from ")
            if len(parts) == 2:
                amount_str, addr_part = parts
                if " to " in addr_part:
                    from_addr, to_addr = addr_part.split(" to ")
                    try:
                        amount = int(amount_str)
                        readable_amount = amount / 1_000_000  # assumes 6 decimals
                        print(f"[TRANSFER] ~{readable_amount:.4f} tokens from {from_addr} → {to_addr}")
                    except ValueError:
                        pass

# === Listener main loop ===
async def subscribe_to_program_logs():
    async with websockets.connect(SOLANA_WS_URL) as ws:
        print("[WS] Connected to Solana WebSocket")

        sub_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                {
                    "mentions": MINTS_TO_WATCH
                },
                {
                    "commitment": "confirmed"
                }
            ]
        }

        await ws.send(json.dumps(sub_msg))
        print(f"[WS] Subscribed to SPL Token logs for {len(MINTS_TO_WATCH)} mint(s)")

        while True:
            try:
                raw_msg = await ws.recv()
                msg = json.loads(raw_msg)

                if "method" in msg and msg["method"] == "logsNotification":
                    logs = msg["params"]["result"]["value"]["logs"]
                    sig = msg["params"]["result"]["value"]["signature"]

                    if any("Transfer" in log for log in logs):
                        print(f"\n[TXN] Signature: {sig}")
                        decode_transfer_log(logs)

            except Exception as e:
                print(f"[WS ERROR] {e}")
                await asyncio.sleep(2)

# === Entry point for main bot ===
def start_listener():
    import threading

    def run():
        asyncio.run(subscribe_to_program_logs())

    t = threading.Thread(target=run, name="WSListener", daemon=True)
    t.start()
    print("[WS] Background listener thread started.")
