# gui_visualizer.py
# Provides a simple dashboard window for monitoring activity and price

import tkinter as tk
import time
import threading
import json
import os

PRICE_CACHE_FILE = "price_cache.json"
TRADE_LOG_FILE = "trade_log.txt"

class DashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pulse: Trading Dashboard")

        self.price_label = tk.Label(root, text="Fetching price...", font=("Arial", 16))
        self.price_label.pack(pady=10)

        self.trade_label = tk.Label(root, text="Last Trades:", font=("Arial", 14, "bold"))
        self.trade_label.pack()

        self.trade_log = tk.Text(root, height=15, width=60)
        self.trade_log.pack(padx=10, pady=10)

        self.update_dashboard()

    def load_price(self):
        if not os.path.exists(PRICE_CACHE_FILE):
            return "N/A"
        try:
            with open(PRICE_CACHE_FILE, 'r') as f:
                data = json.load(f)
                return f"${data.get('price', 'N/A'):.8f}"
        except Exception:
            return "Error"

    def load_trade_log(self):
        if not os.path.exists(TRADE_LOG_FILE):
            return ["[INFO] No trades logged yet."]
        try:
            with open(TRADE_LOG_FILE, 'r') as f:
                return f.readlines()[-5:]  # Show last 5 trades
        except Exception:
            return ["[ERROR] Could not read trade log."]

    def update_dashboard(self):
        self.price_label.config(text=f"Current BONK Price: {self.load_price()}")
        self.trade_log.delete(1.0, tk.END)
        for line in self.load_trade_log():
            self.trade_log.insert(tk.END, line)
        self.root.after(20000, self.update_dashboard)  # Update every 20 seconds


def launch_dashboard():
    root = tk.Tk()
    app = DashboardGUI(root)
    root.mainloop()
