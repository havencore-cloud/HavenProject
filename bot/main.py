# main.py
# Entry point for Pulse trading bot

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import threading
import time
from strategy_controller import StrategyController
from main_loop import start_trading_loop
from config import TRADE_AMOUNT
from gui.dashboard_gui import run_dashboard  # <-- Make sure this matches your file structure

start_trading_loop()

def run_dry_mode(duration_seconds=3600):
    print("=== HavenBot Dry Run Mode — 1 Hour ===")
    controller = StrategyController()
    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        print("\n--- Simulated Trade ---")
        controller.simulate_trade_cycle(amount=TRADE_AMOUNT)
        time.sleep(5)

if __name__ == "__main__":
    # Run dry mode in a background thread
    bot_thread = threading.Thread(target=run_dry_mode, args=(3600,))
    bot_thread.daemon = True
    bot_thread.start()

    # Start the GUI
    run_dashboard()
