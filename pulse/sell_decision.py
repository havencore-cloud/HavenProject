# sell_decision.py
# Module to decide whether to sell based on entry and current price

def should_sell(entry_price, current_price, profit_target=0.05, stop_loss=-0.05):
    """
    Determine whether to sell based on profit or loss thresholds.

    Args:
        entry_price (float): The original buy price.
        current_price (float): The latest market price.
        profit_target (float): Desired gain percentage (e.g., 0.05 = 5%).
        stop_loss (float): Acceptable loss percentage (e.g., -0.05 = -5%).

    Returns:
        (bool, str): Tuple of decision (True/False) and reason.
    """
    if entry_price == 0:
        return False, "[WARNING] Entry price is zero."

    percent_change = (current_price - entry_price) / entry_price

    print(f"[DECISION] Entry: {entry_price:.8f}, Current: {current_price:.8f}, Change: {percent_change:.2%}")

    if percent_change >= profit_target:
        return True, f"[TRIGGER] Profit target reached: {percent_change:.2%}"
    elif percent_change <= stop_loss:
        return True, f"[TRIGGER] Stop-loss hit: {percent_change:.2%}"
    else:
        return False, f"[HOLD] No trigger met: {percent_change:.2%}"
