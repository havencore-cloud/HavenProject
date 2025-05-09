# profit_protection.py

from wallet_manager import transfer_to_vault

PROFIT_THRESHOLD_USD = 5  # Minimum profit to trigger protection
PROFIT_SAVE_PERCENTAGE = 0.7  # 70% of profit gets moved to vault

def protect_profit(profit_amount_usd, trade_wallet_address, vault_wallet_address):
    if profit_amount_usd < PROFIT_THRESHOLD_USD:
        return False  # Not enough profit to bother protecting

    amount_to_save = profit_amount_usd * PROFIT_SAVE_PERCENTAGE

    try:
        success = transfer_to_vault(trade_wallet_address, vault_wallet_address, amount_to_save)
        return success
    except Exception as e:
        # Log error
        print(f"[ERROR] Profit protection failed: {e}")
        return False

# Integration snippet for trade_executor.py
#
# from profit_protection import protect_profit
#
# After selling:
# profit = calculate_profit()  # however you're tracking it
# trade_wallet = get_trade_wallet()
# vault_wallet = get_vault_wallet()
#
# protect_profit(profit, trade_wallet, vault_wallet)
