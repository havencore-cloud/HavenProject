# Pulse Core

**Pulse** is an ethical crypto trading assistant built to protect users from manipulation, rugpulls, and misinformation in the Solana ecosystem. Pulse uses **real on-chain liquidity pools**, transparent trading logic, and a modular architecture to make crypto safer and smarter.

---

## ✅ Phase 1 Complete (MVP Milestone)

- 🧠 Real-time token price parsing from **Orca and Raydium pools**
- 🔄 Automatic fallback system (tries Orca first, then Raydium)
- 🧪 Strategy simulation engine (buy/hold/sell logic)
- 📦 Modular token/project config with pool mapping (`projects.json`)
- 🧠 Strategy engine with customizable buy/sell decision tree
- 🔍 WebSocket token activity tracking
- 🔧 Integrated logging, config, and dry-run modes

---

## 🔧 Currently In Progress

- 💸 Live trade execution engine (Jupiter, Phantom, or native)
- 📊 Real-time liquidity and volume scoring
- 🧠 Token safety scoring (Ember integration)
- 📈 Profit/loss tracking with gas and slippage factored in
- 🧩 Plugin-ready architecture for strategy packs and alerts

---

## 🔐 Coming Soon: **Pulse Verified** (via Ember)

Pulse will integrate with **Ember**, a decentralized trust layer that scores:
- Token mint rules (freeze authority, mintable flags)
- Wallet behavior (whale dominance, malicious movement)
- Community trust and transparency factors

Together, Pulse + Ember will form the heartbeat of the **Haven ecosystem**.

---

## 👁️ Vision

> “We believe trading shouldn’t be a gamble.”

Pulse is here to rebalance the playing field. This isn't about chasing hype — it's about giving everyone, not just whales, the tools to trade safely, ethically, and confidently.

---

## 🔧 Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/pulse-core.git
cd pulse-core

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install required packages
pip install -r bot/utilities/requirements.txt

# Set your .env file
cp .env.example .env
# Add your Helius API key and RPC URL

# Run the bot
python -m bot.main
