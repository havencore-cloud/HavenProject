# dry_run_simulator.py
# Runs HavenBot in dry mode for 1 hour continuously

import time
from strategy_controller import StrategyController

DURATION_MINUTES = 60
TRADE_AMOUNT = 1000000

if __name__ == "__main__":
    print("=== HavenBot Dry Run Mode — 1 Hour ===")
    controller = StrategyController()
    start_time = time.time()

    cycle = 1
    while (time.time() - start_time) < DURATION_MINUTES * 60:
        print(f"\n--- Simulated Trade #{cycle} ---")
        controller.simulate_trade_cycle(amount=TRADE_AMOUNT)
        cycle += 1
