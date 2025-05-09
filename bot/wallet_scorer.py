# wallet_scorer.py
# Module to assign behavior scores and tags to wallets based on trading history

import random
import time
from trade_logger import load_trade_log

class WalletScorer:
    def __init__(self):
        self.trade_data = load_trade_log()

    def score_wallet(self, wallet_address):
        trades = [t for t in self.trade_data if t.get("wallet") == wallet_address]
        if not trades:
            return {
                "score": 0,
                "tag": "Unknown",
                "details": "No data available"
            }

        profit_trades = [t for t in trades if t.get("exit_price", 0) > t.get("entry_price", 0)]
        loss_trades = [t for t in trades if t.get("exit_price", 0) < t.get("entry_price", 0)]

        consistency = len(profit_trades) / len(trades)
        avg_hold_time = self._average_hold_duration(trades)
        timing_score = self._calculate_timing_score(trades)
        volatility = self._calculate_volatility_score(trades)

        score = round((consistency * 40) + (timing_score * 30) + (volatility * 15) + (100 - avg_hold_time) * 0.15)

        tag = self._assign_tag(score, consistency, volatility)

        return {
            "score": score,
            "tag": tag,
            "details": {
                "consistency": round(consistency, 2),
                "avg_hold_time": avg_hold_time,
                "timing_score": timing_score,
                "volatility": volatility,
            }
        }

    def _average_hold_duration(self, trades):
        durations = []
        for t in trades:
            if t.get("entry_time") and t.get("exit_time"):
                try:
                    durations.append(t["exit_time"] - t["entry_time"])
                except:
                    continue
        if durations:
            return sum(durations) / len(durations)
        return 100  # Penalize unknowns

    def _calculate_timing_score(self, trades):
        # Placeholder: Simulate smart timing between 0.3 and 1.0
        return random.uniform(0.3, 1.0)

    def _calculate_volatility_score(self, trades):
        # Placeholder: simulate 0 (calm) to 1.0 (erratic)
        return random.uniform(0.0, 1.0)

    def _assign_tag(self, score, consistency, volatility):
        if score > 85 and consistency > 0.75:
            return "Smart Money"
        elif consistency > 0.85:
            return "Diamond Hands"
        elif volatility > 0.8:
            return "FOMO Buyer"
        elif score < 30:
            return "Degen Gambler"
        elif consistency > 0.7 and score < 60:
            return "Swing Trader"
        else:
            return "Neutral"

# Example usage:
# scorer = WalletScorer()
# result = scorer.score_wallet("0x123abc...")
# print(result)
