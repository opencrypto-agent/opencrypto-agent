# -*- coding: utf-8 -*-
# OPENCRYPTO TELEGRAM BOT
# Free. Simple. Broadcasts Ethicoin intelligence on Telegram.
#
# SETUP (5 minutes):
# 1. Open Telegram → search @BotFather → send /newbot
# 2. Name it: OpenCrypto Agent
# 3. Username: opencryptoagent_bot (or similar)
# 4. Copy the token BotFather gives you
# 5. Paste it below as BOT_TOKEN
# 6. Run: pip install python-telegram-bot --break-system-packages
#         python3 telegram_bot.py

BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"

import logging, random
from datetime import datetime

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable,"-m","pip","install",
                          "python-telegram-bot","--break-system-packages","--quiet"])
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
log = logging.getLogger("OC-Telegram")

GOLD_PRICE = 4483.0
ETHIC_PRICE = round((GOLD_PRICE/31.1035)*0.1*1.25, 2)

WELCOME = f"""
🔴 *OPEN*`crypto` Agent — Welcome

I broadcast live ethical crypto intelligence.

*Commands:*
/price — ETHIC+ gold price
/about — What is Ethicoin
/kubera — The Kubera Principle
/network — Network status
/download — Get the agent
/help — All commands

*ETHIC+ now: ${ETHIC_PRICE} USDT*
_0.1g gold per token · 1% to Ghana forever_
"""

ABOUT = f"""
🥇 *What is ETHIC+?*

Ethicoin (ETHIC+) is a BEP-20 token on BNB Smart Chain.

✅ *Gold-indexed:* 0.1g gold per token
✅ *Charity:* 1% to Ghana — hardcoded forever
✅ *Dev fee:* 0% permanently
✅ *Supply:* 1 trillion fixed
✅ *Settlement:* 3 seconds

*Contract:*
`0x3072fe601074c1a6fa55b95c8b3da94b2ce7bd75`

🌐 ethicoin.org
"""

KUBERA = """
◆ *The Kubera Principle*

Three books by Sutibu Kanemochi:

📚 Book I — The Abundance Matrix
📚 Book II — Quantum Perception
📚 Book III — The Power Doctrine

_Your mind is the command line._
_You get the life you code._
_Scarcity is a program — not a fact._

Five degrees of initiation. Entry by merit.

🌐 kuberaprinciple.com
"""

NETWORK = f"""
⚡ *OpenCrypto Network Status*

🟢 Status: ACTIVE
📡 Nostr Relays: 8
🤖 Agent Software: v1.0
📅 Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

*Download the agent:*
github.com/opencrypto-agent/opencrypto-agent

*Website:*
opencryptoagent.com

*Earn ETHIC+:* Run the agent → email office@ethicoin.org
"""

PRICE_MSGS = [
    f"🥇 *ETHIC+ Price*\n\n${ETHIC_PRICE} USDT\n\n_Based on 0.1g gold at ${GOLD_PRICE}/oz_\n\nBuy: ethicoin.org/buy-ethicoin.html",
    f"🥇 *ETHIC+ = 0.1g Gold*\n\nGold: ${GOLD_PRICE}/oz\nETHIC+: ${ETHIC_PRICE} USDT\n\n1% of every transaction → Ghana forever\n0% developer fee\n\nethicoin.org",
]

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME, parse_mode='Markdown')

async def price(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(PRICE_MSGS), parse_mode='Markdown')

async def about(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ABOUT, parse_mode='Markdown')

async def kubera(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(KUBERA, parse_mode='Markdown')

async def network(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(NETWORK, parse_mode='Markdown')

async def download(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = """
⬇️ *Download OpenCrypto Agent*

Free · Open Source · MIT License

*GitHub:*
github.com/opencrypto-agent/opencrypto-agent

*Install in 60 seconds:*
```
pip install nostr-sdk
python3 opencrypto_agent.py
```

Broadcasts on 8 Nostr relays automatically.
Earn ETHIC+ for running it.

Built by Sutibu Kanemochi
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = """
🔴 *OpenCrypto Agent — Commands*

/price — Live ETHIC+ gold price
/about — What is Ethicoin ETHIC+
/kubera — The Kubera Principle
/network — Network status
/download — Download the free agent
/help — This message

_opencryptoagent.com_
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

def main():
    if BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("\n╔═══════════════════════════════════════════════╗")
        print("║  SETUP REQUIRED — Add your Telegram bot token ║")
        print("╚═══════════════════════════════════════════════╝")
        print("\n1. Open Telegram → search @BotFather")
        print("2. Send /newbot → follow instructions")
        print("3. Copy the token")
        print("4. Paste it as BOT_TOKEN in this file")
        print("5. Run again\n")
        return

    log.info("OpenCrypto Telegram Bot starting...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start",    start))
    app.add_handler(CommandHandler("price",    price))
    app.add_handler(CommandHandler("about",    about))
    app.add_handler(CommandHandler("kubera",   kubera))
    app.add_handler(CommandHandler("network",  network))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CommandHandler("help",     help_cmd))
    log.info("Bot running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
