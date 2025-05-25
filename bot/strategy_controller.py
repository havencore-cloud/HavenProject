# strategy_controller.py
# Coordinates all modules into a clean trading decision engine

import time
from bot.sell_decision import should_sell
from bot.trade_logger import log_trade
from bot.risk_manager import RiskManager
from bot.wallet_manager import get_trade_wallet, get_vault_wallet, deposit_to_trade_wallet
from bot.onchain.onchain_price import get_token_price_usd
from bot.trade_executor import TradeExecutor
from bot.config import DRY_RUN_MODE, MONITORED_MODE, STOP_LOSS_PERCENTAGE, TRADE_AMOUNT, VALID_USER_TOKENS
from bot.analytics.analytics_core import set_open_position, update_metrics, clear_open_position

class StrategyController:
    def __init__(self, trading_api=None):
        self.executor = TradeExecutor(trading_api)
        self.risk = RiskManager()
        self.trade_wallet = get_trade_wallet()
        self.vault_wallet = get_vault_wallet()

        from bot.strategy_engine import StrategyEngine
        self.strategy_engine = StrategyEngine()

    def simulate_trade_cycle(self):
     for token in VALID_USER_TOKENS:
        symbol = token["symbol"]
        mint = token["mint"]
        print(f"\n[SIMULATION] Starting trade cycle for {symbol}...")

        polling_delay = 20  # Replace fetcher.polling_delay
        amount = self.risk.get_adjusted_trade_amount(TRADE_AMOUNT)
        if amount <= 0:
            print("[RISK] Trade amount reduced to zero. Skipping.")
            continue

        entry_price = get_token_price_usd(mint)
        if entry_price is None or entry_price == 0:
            print(f"[PRICE ERROR] Could not fetch entry price for {symbol}")
            continue

        print(f"[ENTRY] Simulating buy of {amount} {symbol} @ {entry_price}")

        if DRY_RUN_MODE:
            deposit_to_trade_wallet(self.trade_wallet, amount)
        elif MONITORED_MODE:
            print("[MONITORED] Simulated buy — wallet unchanged.")

        set_open_position(entry_price, amount)

        while True:
            current_price = get_token_price_usd(mint)
            if current_price is None or current_price == 0:
                time.sleep(polling_delay)
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
            self.risk.check_cooldown()
            time.sleep(polling_delay)
