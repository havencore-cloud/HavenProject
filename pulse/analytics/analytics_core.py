# analytics_core.py
# Central module to share trading metrics across the app

metrics = {
    "total_profit": 0.0,
    "total_trades": 0,
    "total_gain": 0.0,
    "total_loss": 0.0,
    "open_position": None
}

def get_metrics_snapshot():
    return metrics.copy()

def update_metrics(profit, entry_price, exit_price, amount):
    metrics["total_trades"] += 1
    metrics["total_profit"] += profit

    if profit > 0:
        metrics["total_gain"] += profit
    else:
        metrics["total_loss"] += abs(profit)

    metrics["open_position"] = None

def set_open_position(entry_price, amount):
    metrics["open_position"] = {
        "entry_price": entry_price,
        "amount": amount
    }

def clear_open_position():
    metrics["open_position"] = None
