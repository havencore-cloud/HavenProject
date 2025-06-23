# dashboard_gui.py
# GUI-based visualizer for Pulse Trading Bot Analytics

import tkinter as tk
from analytics.analytics_core import get_metrics_snapshot

REFRESH_INTERVAL = 20000  # in milliseconds (20 seconds)

def update_dashboard(window, label):
    snapshot = get_metrics_snapshot()
    content = f"""
Pulse Analytics Dashboard

Total Trades: {snapshot['total_trades']}
Total Profit: ${snapshot['total_profit']:.4f}
Total Gain: ${snapshot['total_gain']:.4f}
Total Loss: ${snapshot['total_loss']:.4f}
Current Position: {snapshot['open_position'] or 'None'}
"""
    label.config(text=content.strip())
    window.after(REFRESH_INTERVAL, update_dashboard, window, label)

def run_dashboard():
    window = tk.Tk()
    window.title("Pulse Trading Dashboard")

    label = tk.Label(window, text="", justify="left", font=("Courier", 12), padx=10, pady=10)
    label.pack()

    update_dashboard(window, label)
    window.mainloop()
