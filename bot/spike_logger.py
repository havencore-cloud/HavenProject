# spike_logger.py
# Log detected volume or liquidity spikes with timestamp and reason

import time
import os

SPIKE_LOG_FILE = "spike_log.txt"

def log_spike_event(reason, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    line = f"[{timestamp}] Spike - Reason: {reason} | Value: {value}\n"
    try:
        with open(SPIKE_LOG_FILE, "a") as f:
            f.write(line)
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to write to spike log: {e}")
