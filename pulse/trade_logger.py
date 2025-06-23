# trade_logger.py
# Module to log trade activity to a file for tracking and analysis

import os
from datetime import datetime

LOG_FILE = "trade_log.csv"

# Initialize the log file if it doesn't exist
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("timestamp,action,symbol,entry_price,exit_price,amount,percent_change,reason\n")

# Log a single trade event
def log_trade(action, symbol, entry_price, exit_price, amount, reason):
    timestamp = datetime.utcnow().isoformat()
    percent_change = ((exit_price - entry_price) / entry_price) if entry_price else 0
    line = f"{timestamp},{action},{symbol},{entry_price},{exit_price},{amount},{percent_change:.4f},{reason}\n"

    try:
        with open(LOG_FILE, 'a') as f:
            f.write(line)
        print(f"[LOG] Trade recorded: {action} {symbol} @ {exit_price}")
    except Exception as e:
        print(f"[ERROR] Failed to write to log: {e}")
