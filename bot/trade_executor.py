# trade_executor.py
# Executes buy/sell trades in dry-run or live mode

from config import DRY_RUN_MODE
from wallet_manager import get_trade_wallet, get_vault_wallet, transfer_to_vault

class TradeExecutor:
    def __init__(self, trading_api):
        self.api = trading_api

    def execute_buy(self, symbol, amount):
        if DRY_RUN_MODE:
            print(f"[SIMULATION] Would buy {amount} of {symbol}")
            return {'symbol': symbol, 'amount': amount, 'price': 100}  # Simulated price
        else:
            try:
                response = self.api.buy(symbol, amount)
                print(f"[BUY] Bought {amount} of {symbol}")
                return response
            except Exception as e:
                print(f"[ERROR] Buy failed: {e}")
                return None

    def execute_sell(self, symbol, amount, buy_price):
        if DRY_RUN_MODE:
            sell_price = 120  # Simulated sale
            print(f"[SIMULATION] Would sell {amount} of {symbol} at {sell_price}")
            profit = (sell_price - buy_price) * amount

            trade_wallet = get_trade_wallet()
            vault_wallet = get_vault_wallet()
            transfer_to_vault(trade_wallet, vault_wallet, profit)

            print(f"[SIMULATION] Sold {amount} {symbol} successfully and protected profit.")
            return {'symbol': symbol, 'amount': amount, 'price': sell_price}
        else:
            try:
                sell_response = self.api.sell(symbol, amount)
                sell_price = sell_response['price']
                profit = (sell_price - buy_price) * amount

                trade_wallet = get_trade_wallet()
                vault_wallet = get_vault_wallet()
                transfer_to_vault(trade_wallet, vault_wallet, profit)

                print(f"[SELL] Sold {amount} {symbol} successfully and protected profit.")
                return sell_response
            except Exception as e:
                print(f"[ERROR] Sell failed: {e}")
                return None
