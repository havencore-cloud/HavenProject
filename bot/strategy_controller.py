# strategy_controller.py
# Coordinates all modules into a clean trading decision engine

import time
from price_fetcher import PriceFetcher
from sell_decision import should_sell
from trade_logger import log_trade
from risk_manager import RiskManager
from wallet_manager import get_trade_wallet, get_vault_wallet, deposit_to_trade_wallet
from trade_executor import TradeExecutor
from config import DRY_RUN_MODE, MONITORED_MODE, STOP_LOSS_PERCENTAGE, TRADE_AMOUNT, MONITORED_TOKENS
from analytics.analytics_core import set_open_position, update_metrics, clear_open_position

class StrategyController:
    def __init__(self, trading_api=None):
        self.executor = TradeExecutor(trading_api)
        self.risk = RiskManager()
        self.trade_wallet = get_trade_wallet()
        self.vault_wallet = get_vault_wallet()

        from strategy_engine import StrategyEngine
        self.strategy_engine = StrategyEngine()

    def simulate_trade_cycle(self):
        for token in MONITORED_TOKENS:
            symbol = token["symbol"]
            mint = token["mint"]
            print(f"\n[SIMULATION] Starting trade cycle for {symbol}...")

            fetcher = PriceFetcher(token_mint=mint)
            hold_delay = fetcher.polling_delay

            amount = self.risk.get_adjusted_trade_amount(TRADE_AMOUNT)
            if amount <= 0:
                print("[RISK] Trade amount reduced to zero. Skipping.")
                continue

            entry_price = fetcher.get_current_price()
            if entry_price is None:
                continue

            print(f"[ENTRY] Simulating buy of {amount} {symbol} @ {entry_price}")

            if DRY_RUN_MODE:
                deposit_to_trade_wallet(self.trade_wallet, amount)
            elif MONITORED_MODE:
                print("[MONITORED] Simulated buy — wallet unchanged.")

            set_open_position(entry_price, amount)

            while True:
                current_price = fetcher.get_current_price()
                if current_price is None:
                    continue

                percent_change = (current_price - entry_price) / entry_price
                print(f"[PRICE WATCH] Entry: {entry_price:.8f}, Current: {current_price:.8f}, Change: {percent_change:.2%}")

                decision = self.strategy_engine.choose_strategy({
                    "price": current_price,
                    "entry_price": entry_price,
                    "volume_1h": None,
                    "volume_change_1h": None
                })

                if decision == "sell":
                    reason = f"[STRATEGY] Engine advised to SELL. Change: {percent_change:.2%}"
                    break

                print("[HOLD] Strategy advises HOLD...")
                fetcher.cache_price(current_price)
                self.risk.check_cooldown()
                time.sleep(hold_delay)

            trade_value = amount * current_price
            ok, msg = self.risk.check_position_size(trade_value)
            if not ok:
                print(msg)
                continue

            ok, msg = self.risk.check_daily_loss_limit()
            if not ok:
                print(msg)
                continue

            ok, msg = self.risk.check_cooldown()
            if not ok:
                print(msg)
                continue

            result = self.executor.execute_sell(symbol, amount, entry_price)
            self.risk.record_trade_time()

            log_trade(
                action="SELL",
                symbol=symbol,
                entry_price=entry_price,
                exit_price=current_price,
                amount=amount,
                reason=reason
            )

            profit = (current_price - entry_price) * amount
            self.risk.update_trade_result(profit)
            update_metrics(profit, entry_price, current_price, amount)
            clear_open_position()
