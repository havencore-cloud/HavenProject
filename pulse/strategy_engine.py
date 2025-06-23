# strategy_engine.py
# Module to define trading patterns and signals

from pulse.logger import log

class StrategyEngine:
    def __init__(self):
        pass

    def find_trade_opportunity(self):
        """
        Placeholder for future scanning logic across all tokens.
        """
        log("Scanning for trade opportunities...")
        pass

    def should_buy(self, symbol, mint, metrics, previous_price):
        """
        Decision logic for entering a new trade.
        """

        price = metrics.get("price_usd", 0)
        volume = metrics.get("volume_24h", 0)
        liquidity = metrics.get("liquidity_usd", 0)

        # Rule 1: Volume threshold
        if volume < 5000:
            log(f"[FILTER] {symbol} volume too low: {volume}")
            return False

        # Rule 2: Spike avoidance
        if previous_price:
            change = (price - previous_price) / previous_price
            if change > 0.05:
                log(f"[FILTER] {symbol} price already spiked: {change:.2%}")
                return False

        # Rule 3: Liquidity check
        if liquidity < 2000:
            log(f"[FILTER] {symbol} liquidity too low: {liquidity}")
            return False

        # Passed all checks
        log(f"[STRATEGY] {symbol} passed buy conditions.")
        return True

    def choose_strategy(self, context):
        """
        Very simple real-time strategy evaluator.
        Returns 'sell' if price has increased by 1.5%, else 'hold'.
        """
        price = context.get("price")
        entry = context.get("entry_price")

        if not price or not entry:
            return "hold"

        change = (price - entry) / entry

        if change > 0.015:  # +1.5% profit
            return "sell"

        return "hold"
