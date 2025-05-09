# analytics_visualizer.py
# Handles visualization of trade metrics and price data

import matplotlib.pyplot as plt
import json
import os
import time

from config import ANALYTICS_FILE


def load_trade_metrics():
    if not os.path.exists(ANALYTICS_FILE):
        return None
    with open(ANALYTICS_FILE, 'r') as f:
        return json.load(f)


def plot_trade_summary():
    data = load_trade_metrics()
    if not data:
        print("[INFO] No trade data found to visualize.")
        return

    labels = ['Total Trades', 'Total Gain', 'Total Loss', 'Total Profit']
    values = [
        data.get("total_trades", 0),
        data.get("total_gain", 0),
        data.get("total_loss", 0),
        data.get("total_profit", 0)
    ]

    colors = ['#6c5ce7', '#00cec9', '#d63031', '#0984e3']

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=colors)
    plt.title("Pulse Trade Metrics Summary")
    plt.ylabel("Value")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def live_metric_console():
    print("=== Pulse Live Analytics Console ===")
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            data = load_trade_metrics()
            if data:
                print(f"Total Trades: {data.get('total_trades', 0)}")
                print(f"Total Profit: {data.get('total_profit', 0):.2f}")
                print(f"Total Gain:   {data.get('total_gain', 0):.2f}")
                print(f"Total Loss:   {data.get('total_loss', 0):.2f}")
            else:
                print("No data available.")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped live console view.")
