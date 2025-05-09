# logger.py
# Logging module for Haven Trading Bot

import datetime

def log(message):
    """
    Simple logger that timestamps messages.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")
