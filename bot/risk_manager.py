# risk_manager.py
# Handles trade sizing, cooldowns, and loss limits

import time

class RiskManager:
    def __init__(self):
        self.last_trade_time = 0
        self.daily_loss = 0.0
        self.cooldown_seconds = 60
        self.max_daily_loss = 200.0  # example threshold
        self.loss_streak = 0
        self.last_result = None
        self.last_loss_time = None
        self.pause_until = None

    def record_trade_time(self):
        self.last_trade_time = time.time()

    def check_cooldown(self):
        now = time.time()
        if self.pause_until and now < self.pause_until:
            return False, f"[RISK] Bot paused due to losses. Wait {int(self.pause_until - now)}s."
        if now - self.last_trade_time < self.cooldown_seconds:
            return False, f"[RISK] Cooldown in effect. Wait {int(self.cooldown_seconds - (now - self.last_trade_time))}s."
        return True, "OK"

    def check_daily_loss_limit(self):
        if self.daily_loss > self.max_daily_loss:
            return False, f"[RISK] Daily loss limit exceeded: ${self.daily_loss:.2f}"
        return True, "OK"

    def check_position_size(self, trade_value):
        max_allowed = 1000  # USD
        if trade_value > max_allowed:
            return False, f"[RISK] Trade value ${trade_value:.2f} exceeds max allowed (${max_allowed})."
        return True, "OK"

    def get_adjusted_trade_amount(self, base_amount):
        if self.loss_streak == 0:
            return base_amount
        elif self.loss_streak == 1:
            return base_amount
        elif self.loss_streak == 2:
            return base_amount * 0.5
        elif self.loss_streak == 3:
            return base_amount * 0.25
        else:
            self.pause_until = time.time() + 3600  # 1 hour pause
            return 0

    def update_trade_result(self, profit):
        if profit < 0:
            self.loss_streak += 1
            self.last_result = "loss"
            self.last_loss_time = time.time()
            self.daily_loss += abs(profit)
        else:
            self.loss_streak = 0
            self.last_result = "win"
            self.daily_loss = max(0, self.daily_loss - profit * 0.5)  # Slowly reduce loss if profitable
