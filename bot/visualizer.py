# visualizer.py
# Module to visualize trade analytics and wallet flows (GUI)

import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ANALYTICS_FILE = "analytics.json"

class Visualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pulse Analytics Dashboard")
        self.build_gui()

    def load_analytics(self):
        if not os.path.exists(ANALYTICS_FILE):
            return []
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)

    def build_gui(self):
        btn_profit = tk.Button(self.root, text="Show Trade Performance", command=self.show_trade_performance)
        btn_profit.pack(pady=5)

        btn_flow = tk.Button(self.root, text="Show Wallet Flow", command=self.show_wallet_flow)
        btn_flow.pack(pady=5)

    def show_trade_performance(self):
        data = self.load_analytics()
        if not data:
            messagebox.showinfo("Info", "No analytics data available.")
            return

        df = pd.DataFrame(data)
        df['profit'] = (df['exit_price'] - df['entry_price']) * df['amount']

        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['profit'], marker='o')
        ax.set_title("Profit per Trade Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Profit (USD)")
        fig.autofmt_xdate()

        self.display_plot(fig)

    def show_wallet_flow(self):
        data = self.load_analytics()
        if not data:
            messagebox.showinfo("Info", "No analytics data available.")
            return

        df = pd.DataFrame(data)
        df['wallet_flow'] = df['amount'] * df['exit_price']
        df['wallet'] = df['wallet'] if 'wallet' in df.columns else 'default'

        flow_by_wallet = df.groupby('wallet')['wallet_flow'].sum()

        fig, ax = plt.subplots()
        flow_by_wallet.plot(kind='bar', ax=ax, title="Total Wallet Flow (USD)")
        ax.set_xlabel("Wallet")
        ax.set_ylabel("Flow (USD)")

        self.display_plot(fig)

    def display_plot(self, fig):
        window = tk.Toplevel(self.root)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = Visualizer(root)
    root.mainloop()
