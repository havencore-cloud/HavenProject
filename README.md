# Pulse Core

**Pulse** is an ethical crypto trading assistant designed to protect users from volatility, manipulation, and fraudulent tokens. Built for the Solana ecosystem, Pulse simulates and executes trades using transparent strategies, token risk filters, and automated logic—all grounded in safety and clarity.

## 🌱 Phase 1 Complete:
- Real-time token tracking (Dexscreener + Jupiter integration)
- Modular trading strategy engine
- Simulation logic with customizable trade signals

## 🔜 In Progress:
- Live trade execution via Jupiter Swap
- Token risk filter (liquidity, mintability, blacklistable)
- Profit/loss tracking with gas and slippage included

## 🛡️ Coming Soon: Pulse Verified (via Ember)
Pulse will integrate with **Ember**, a trust layer that scores tokens and wallets based on transparency, behavior, and user protections. Together, they form the foundation of the Haven ecosystem.

## 👁️ Vision
We believe trading shouldn’t be a gamble. Pulse exists to make wealth-building safer, more ethical, and more accessible—for everyone, not just whales.

---

### 🔗 Resources
- [Landing Page](https://yourusername.github.io/pulse-core) (GitHub Pages)
- [Solana](https://solana.com/)
- [Dexscreener](https://dexscreener.com/)
- [Jupiter Aggregator](https://jup.ag/)

---

### 🔧 Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/pulse-core.git
cd pulse-core

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the main tracker
python tracker.py
