# main.py
# Entry point for Pulse trading bot

from bot.strategy_controller import StrategyController
from bot.realtime.solana_ws_listener import start_listener
from time import sleep
from bot.config import CONFIG

def main():
    print("[MAIN] Starting HavenBot Trading Engine...")
    start_listener()

    # Example loop or controller
    strategy = StrategyController()
    print("[LOOP] Starting live strategy polling...\n")

    while True:
        strategy.simulate_trade_cycle()
        sleep(10)  # or whatever your delay is

if __name__ == "__main__":
    main()
