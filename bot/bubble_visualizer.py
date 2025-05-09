# bubble_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt

class BubbleVisualizer:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_wallet(self, wallet_id, balance, wallet_type='normal'):
        self.G.add_node(wallet_id, size=balance, type=wallet_type)

    def add_transfer(self, from_wallet, to_wallet, amount):
        self.G.add_edge(from_wallet, to_wallet, weight=amount)

    def update_wallet_balance(self, wallet_id, new_balance):
        if wallet_id in self.G.nodes:
            self.G.nodes[wallet_id]['size'] = new_balance

    def draw(self):
        sizes = [self.G.nodes[n]['size'] * 10 for n in self.G.nodes]
        colors = [
            'green' if self.G.nodes[n]['type'] == 'normal' else 'red'
            for n in self.G.nodes
        ]
        pos = nx.spring_layout(self.G, k=0.5)
        nx.draw(self.G, pos, with_labels=False, node_size=sizes, node_color=colors, arrows=True)
        plt.show()
