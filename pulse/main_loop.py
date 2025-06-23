# main_loop.py
import time
from utilities.io import load_projects
from strategy_engine import StrategyEngine
from price_fetcher import fetch_token_metrics
from trader import Trader
import logger  # assumes you have a logger module that defines logger.log()

def start_trading_loop():
    trader = Trader()
    engine = StrategyEngine()
    last_price = {}
    
    print("[LOOP] Starting live strategy polling...\n")
    projects = load_projects()

    while True:
        print("========== POLLING ==========")

        for token in projects:
            symbol = token['symbol']
            mint = token['mint']
            strategy = token.get('strategy', {})
            auto_trade = strategy.get('auto_trade', False)

            print(f"--- {symbol} | Auto-Trade: {auto_trade} ---")
            metrics = fetch_token_metrics(symbol, mint)

            if not metrics:
                print(f"  No data available for {symbol}")
                continue

            price = metrics['price_usd']
            print(f"  Current Price: ${price:.8f}")

            # Smart Trade Logic
            if auto_trade:
                prev_price = last_price.get(symbol)

                # BUY
                if trader.position is None and engine.should_buy(symbol, mint, metrics, prev_price):
                    trader.buy(symbol, price)
                    logger.log(f"[TRADE] Bought {symbol} at ${price:.8f}")
                    last_price[symbol] = None  # Reset

                # STORE PRICE IF NOT READY
                elif trader.position is None:
                    last_price[symbol] = price

                # SELL
                elif trader.position and trader.position['symbol'] == symbol:
                    entry = trader.position['entry_price']
                    if price > entry * 1.001:
                        trader.sell(price)
                        logger.log(f"[TRADE] Sold {symbol} at ${price:.8f}")
                        last_price[symbol] = None
            else:
                print(f"  Skipping trade logic (auto_trade disabled)")

        trader.status()

        print("\n[ANALYTICS] Performance Snapshot:")
        print(f"  total_profit: {trader.total_profit}")
        print(f"  total_trades: {len(trader.trade_log)}")
        print(f"  open_position: {trader.position['symbol'] if trader.position else 'None'}")

        time.sleep(30)
