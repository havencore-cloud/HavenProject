# wallet_manager.py

from config import DRY_RUN_MODE


# Fake wallets storage
wallets = {
    '0xYourTradeWalletAddress': 0,
    '0xYourVaultWalletAddress': 0,
}

def get_trade_wallet():
    return '0xYourTradeWalletAddress'


def get_vault_wallet():
    return '0xYourVaultWalletAddress'

def deposit_to_trade_wallet(wallet_address, amount):
    if DRY_RUN_MODE:
        wallets[wallet_address] = wallets.get(wallet_address, 0) + amount
        print(f"[SIMULATION] Deposited {amount} units to Trade Wallet: {wallet_address}")
    else:
        raise NotImplementedError("Live deposits not implemented yet.")


def transfer_to_vault(from_wallet, to_wallet, amount):
    if DRY_RUN_MODE:
        print(f"[SIMULATION] Transferring {amount} units from {from_wallet} to {to_wallet}")

        # Update fake balances
        wallets[from_wallet] = wallets.get(from_wallet, 0) - amount
        wallets[to_wallet] = wallets.get(to_wallet, 0) + amount

        print(f"[SIMULATION] New Balances -> Trade Wallet: {wallets[from_wallet]}, Vault Wallet: {wallets[to_wallet]}")
        return True
    else:
        # Here you would put real blockchain transfer logic
        raise NotImplementedError("Live transfers not implemented yet.")