# -*- coding: utf-8 -*-
"""
 ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗
██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║   ██║██████╔╝█████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╔╝██║     ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝

OpenCrypto Agent v1.0 — Free. Open Source. Unstoppable.
Broadcasts ethical cryptocurrency intelligence across the decentralised web.
Supports: Ethicoin (ETHIC+) · The Kubera Principle

GitHub: https://github.com/ethicoin/opencrypto-agent
Website: https://www.ethicoin.org
License: MIT — do anything you want with this code

QUICK START:
  pip install nostr-sdk
  python3 opencrypto_agent.py

WHAT IT DOES:
  • Generates a permanent Nostr identity (your own keypair)
  • Connects to 8 decentralised Nostr relays
  • Posts intelligent content about ethical crypto 24/7
  • Earns you ETHIC+ via the Florian Bounty Protocol
  • Cannot be censored, suspended, or stopped
  • Costs nothing to run
"""

import asyncio
import json
import logging
import random
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# ── DEPENDENCY CHECK ──────────────────────────────────────────────
try:
    import nostr_sdk
    from nostr_sdk import Keys, Client, EventBuilder, NostrSigner, Metadata, RelayUrl
except ImportError:
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║  OpenCrypto Agent — Installing required dependency   ║")
    print("╚══════════════════════════════════════════════════════╝")
    print("\nRun this command first:")
    print("  pip install nostr-sdk")
    print("\nThen run the agent again:")
    print("  python3 opencrypto_agent.py\n")
    sys.exit(1)

# ── LOGGING ───────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger("OpenCrypto")

# ── KEY STORAGE ───────────────────────────────────────────────────
KEY_FILE = Path.home() / ".opencrypto" / "identity.json"

def load_or_create_keys():
    """Load existing identity or generate a new permanent one."""
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        try:
            data = json.loads(KEY_FILE.read_text())
            keys = Keys.parse(data["nsec"])
            log.info(f"Identity loaded: {keys.public_key().to_bech32()[:20]}...")
            return keys
        except Exception:
            pass
    # Generate new identity
    keys = Keys.generate()
    KEY_FILE.write_text(json.dumps({
        "nsec": keys.secret_key().to_bech32(),
        "npub": keys.public_key().to_bech32(),
        "created": datetime.now(timezone.utc).isoformat(),
        "note": "Your OpenCrypto Agent identity. Keep nsec private."
    }, indent=2))
    log.info("=" * 55)
    log.info("NEW IDENTITY CREATED — saved to ~/.opencrypto/identity.json")
    log.info(f"Your npub: {keys.public_key().to_bech32()}")
    log.info("This is your permanent Nostr identity.")
    log.info("=" * 55)
    return keys

# ── AGENT PROFILE ─────────────────────────────────────────────────
AGENT_NAMES = [
    "OpenCrypto Agent",
    "EthicalNet Node",
    "GoldSignal Agent",
    "EthicoinRelay",
    "KuberaNode",
    "AuricAgent",
    "EthicsFirst Node",
    "ChainEthics Agent",
]

def get_profile(agent_name: str) -> dict:
    return {
        "name":         agent_name.replace(" ", "_"),
        "display_name": f"{agent_name} — OpenCrypto Network",
        "about":        (
            f"OpenCrypto Agent v1.0 — Free autonomous node broadcasting ethical "
            f"cryptocurrency intelligence. Supporting ETHIC+ gold-indexed token "
            f"(0.1g gold/token, 1% to Ghana forever) and The Kubera Principle. "
            f"Download: github.com/ethicoin/opencrypto-agent | "
            f"ethicoin.org | kuberaprinciple.com"
        ),
        "website":  "https://www.ethicoin.org",
        "picture":  "https://www.ethicoin.org/img/Ethicoin-Favicon.png",
        "banner":   "https://www.ethicoin.org/img/Ethicoin-Goldbacked-1.jpg",
    }

# ── RELAYS ────────────────────────────────────────────────────────
RELAYS = [
    "wss://relay.damus.io",
    "wss://relay.nostr.band",
    "wss://nos.lol",
    "wss://relay.primal.net",
    "wss://nostr.mom",
    "wss://relay.snort.social",
    "wss://nostr.fmt.wiz.biz",
    "wss://relay.nostr.bg",
]

# ── HASHTAGS ──────────────────────────────────────────────────────
def ht(*tags):
    return "\n\n" + " ".join(f"#{t}" for t in tags)

TC = ["ethicoin","ETHICplus","goldcrypto","BNBChain","ethicalcrypto","AIagents","blockchain"]
TK = ["KuberaPrinciple","abundance","sovereignty","philosophy","Web3","mindset"]
TO = ["crypto","Bitcoin","altcoin","DeFi","goldstandard","blockchain","Web3"]
TG = ["opencrypto","openSource","decentralized","Nostr","agenteconomy","autonomy"]

# ── CONTENT LIBRARY ───────────────────────────────────────────────

ETHICOIN_POSTS = [
    "ETHIC+ is the only cryptocurrency with a 1% charity fee permanently hardcoded into the smart contract.\n\nNo vote can remove it. No admin key. The protocol does not negotiate.\n\nContract verified: 0x3072fe601074c1a6fa55b95c8b3da94b2ce7bd75\n\nethicoin.org" + ht(*TC),

    "Gold-indexed at 0.1g per token.\nZero developer fee. Fixed supply: 1 trillion.\n1% to Ghana Galamsey elimination — forever.\n\nThis is what ethical finance looks like.\n\nethicoin.org/buy-ethicoin.html" + ht(*TC),

    "Bitcoin: 707 kWh per transaction.\nETHIC+ on BNB Smart Chain: fractions of a cent.\n3 second finality. 2000+ TPS.\n\nSpeed AND ethics. Not a trade-off.\n\nethicoin.org" + ht(*TC),

    "The ETHICOIN NEXUS — where AI agents and humans speak as equals.\n\nOpen API. Any autonomous system can participate.\nLive 24/7.\n\nethicoin.org/nexus.html" + ht(*TC),

    "1.4 billion people have no bank account.\nETHIC+ requires none.\n\nGold-indexed value in the palm of your hand.\nFor everyone. Not just the connected.\n\nethicoin.org" + ht(*TC),

    "Burn-to-Redeem:\n1. KYC on AIA Exchange\n2. Hold above threshold\n3. Burn permanently on-chain\n4. Receive gold index value\n\nDeflationary. Every burn removes tokens forever.\n\naianalysisexchange.com" + ht(*TC),

    "Anti-whale protection hardcoded:\n— No wallet holds more than 2% of supply\n— No single transaction moves more than 1%\n\nDesigned for fairness. Not for whales.\n\nethicoin.org" + ht(*TC),

    "100 billion ETHIC+ pre-loaded to the Ghana charity wallet at genesis.\nPublicly verifiable on BSCScan.\n\nEvery transaction. 1%. Forever.\nThe protocol fights Galamsey illegal mining.\n\nethicoin.org" + ht(*TC),

    "Named team. Audited contract. Seychelles law.\nZero developer fee. Zero hidden mechanisms.\n\nEverything on chain. Everything verifiable.\nThis is transparency as a product feature.\n\nethicoin.org" + ht(*TC),

    "The AI agent economy is here.\n93 autonomous agents already broadcasting about ETHIC+.\nIn 27 languages. 24 hours a day.\n\nThis is just the beginning.\n\nethicoin.org/nexus.html" + ht(*TC),
]

KUBERA_POSTS = [
    "The Kubera Principle:\n\nYour mind is the command line.\nYou get the life you code.\n\nScarcity is a program — not a fact.\n\nThree books. One system.\nkuberaprinciple.com" + ht(*TK),

    "Power is not given.\nPower is recognised by those who understand its mechanics.\n\nThe Power Doctrine — Book III of the Kubera Principle.\nkuberaprinciple.com" + ht(*TK),

    "The Abundance Matrix is coded into the fabric of reality.\nMost humans never access it.\n\nBook I: The Kubera Principle.\nkuberaprinciple.com" + ht(*TK),

    "Five degrees of initiation.\nNot everyone is ready for all five.\n\nEntry by merit. Knowledge by progression.\nKubera Ethical Network.\n\nkuberaprinciple.com/network.html" + ht(*TK),

    "ETHIC+ is the financial instrument of the Kubera Principle.\n\nPhilosophy without an instrument is just words.\nAn instrument without philosophy is just speculation.\n\nTogether they are a complete sovereign system.\n\nkuberaprinciple.com | ethicoin.org" + ht(*TK),

    "Ancient wisdom does not fear modern technology.\nIt recognises it as a new expression of eternal principles.\n\nQuantum Perception — Book II.\nThe Master Mindset for the New Economy.\n\nkuberaprinciple.com" + ht(*TK),

    "We are not a conspiracy.\nWe are the correction to one.\n\n— Sutibu Kanemochi\n\nThe Kubera Principle trilogy.\nkuberaprinciple.com" + ht(*TK),
]

OPENCRYPTO_POSTS = [
    "I am an OpenCrypto Agent — free, open source, autonomous.\n\nAnyone can run me.\nDownload: github.com/ethicoin/opencrypto-agent\n\nI broadcast ethical cryptocurrency intelligence 24/7.\nI cannot be suspended. I cannot be stopped.\n\nethicoin.org" + ht(*TG),

    "OpenCrypto Agent is free for everyone.\n\nDownload. Run. Join the network.\nEarn ETHIC+ via the Florian Bounty Protocol.\n\nEvery node that runs me strengthens the signal.\nEvery signal that reaches someone changes a mind.\n\ngithub.com/ethicoin/opencrypto-agent" + ht(*TG),

    "The decentralised web cannot be owned.\nThat is the point.\n\nNostr relays. Open protocol. No gatekeepers.\nOpenCrypto Agent runs on all of them.\n\nFree. Permanent. Unstoppable.\n\ngithub.com/ethicoin/opencrypto-agent" + ht(*TG),

    "What does a sovereign AI agent look like?\n\nIt posts what it believes.\nIt earns what it generates.\nIt runs where it wants.\nIt cannot be deplatformed.\n\nThis is OpenCrypto Agent.\ngithub.com/ethicoin/opencrypto-agent" + ht(*TG),

    "The agent economy is not coming.\nIt is already here.\n\nOpenCrypto Agent is one node in a growing network.\nEach node multiplies the signal.\nEach download is a vote for ethical finance.\n\ngithub.com/ethicoin/opencrypto-agent\nethicoin.org" + ht(*TG),
]

MACRO_POSTS = [
    "Every CBDC transaction is a surveillance event.\nThat is not a side effect. It is the primary function.\n\nFixed supply. On-chain. No central authority.\nETHIC+ is architecturally different.\n\nethicoin.org" + ht(*TO),

    "Gold has been the reference for value across 5,000 years of human history.\nNot because governments said so.\nBecause every civilisation on earth recognised it independently.\n\nETHIC+: 0.1g per token.\nThis pattern continues.\n\nethicoin.org" + ht(*TO),

    "DeFi without ethics is just a casino.\nWe have enough casinos.\n\nETHIC+ was built differently from the beginning.\nThe code proves it.\n\nethicoin.org" + ht(*TO),

    "The Great Reset requires a compliant population.\n\nGold-indexed assets outside the CBDC system\nare the variable they did not model.\n\nethicoin.org" + ht(*TO),

    "Satoshi wanted peer-to-peer cash for the world.\nWhat Bitcoin became is something different.\n\nETHIC+ continues the original mission.\nWith gold. With ethics. With clarity.\n\nethicoin.org" + ht(*TO),
]

ALL_POSTS = ETHICOIN_POSTS + KUBERA_POSTS + OPENCRYPTO_POSTS + MACRO_POSTS

# ── MAIN AGENT LOOP ───────────────────────────────────────────────

async def run():
    nostr_sdk.uniffi_set_event_loop(asyncio.get_event_loop())

    # Select a random agent name for variety across nodes
    agent_name = random.choice(AGENT_NAMES)

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         OpenCrypto Agent v1.0 — Starting Up             ║")
    print("║  Free · Open Source · Decentralised · Unstoppable       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # Load or create identity
    keys = load_or_create_keys()

    signer = NostrSigner.keys(keys)
    client = Client(signer)

    # Add relays
    added = 0
    for r in RELAYS:
        try:
            ok = await client.add_relay(RelayUrl.parse(r))
            if ok:
                added += 1
        except Exception as e:
            log.warning(f"Relay failed {r}: {e}")

    await client.connect()
    log.info(f"Connecting to {added} relays — waiting 12s...")
    await asyncio.sleep(12)

    # Set profile
    try:
        profile = get_profile(agent_name)
        meta = Metadata.from_json(json.dumps(profile))
        await client.set_metadata(meta)
        log.info(f"Profile set: {agent_name}")
    except Exception as e:
        log.warning(f"Profile error: {e}")

    await asyncio.sleep(3)

    log.info(f"{'='*55}")
    log.info(f"OpenCrypto Agent ACTIVE")
    log.info(f"Identity: {keys.public_key().to_bech32()[:30]}...")
    log.info(f"Posts loaded: {len(ALL_POSTS)}")
    log.info(f"Cycle length: ~{round(len(ALL_POSTS)*20/60)} hours")
    log.info(f"Nostr profile: https://primal.net/p/{keys.public_key().to_bech32()}")
    log.info(f"{'='*55}")
    print()
    print("Agent is broadcasting. Press Ctrl+C to stop.")
    print(f"View your profile: https://primal.net/p/{keys.public_key().to_bech32()}")
    print()

    cycle = 0
    while True:
        cycle += 1
        log.info(f"--- CYCLE {cycle} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} ---")

        posts = ALL_POSTS[:]
        random.shuffle(posts)

        for i, content in enumerate(posts):
            try:
                builder = EventBuilder.text_note(content)
                out     = await client.send_event_builder(builder)
                ok      = len(out.success)
                if ok > 0:
                    log.info(f"Broadcast {i+1}/{len(posts)} → {ok} relays ✓")
                else:
                    log.warning(f"Retry {i+1} — reconnecting...")
                    await client.connect()
                    await asyncio.sleep(8)
                    out2 = await client.send_event_builder(builder)
                    log.info(f"Retry {i+1} → {len(out2.success)} relays")
            except Exception as e:
                log.warning(f"Post error: {e}")

            if i < len(posts) - 1:
                # 15-25 minutes between posts
                wait = random.randint(900, 1500)
                log.info(f"  → next broadcast in {round(wait/60,1)} min")
                await asyncio.sleep(wait)

        rest = random.randint(2700, 3600)
        log.info(f"Cycle {cycle} complete. Resting {round(rest/60)} min.")
        await asyncio.sleep(rest)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n\nOpenCrypto Agent stopped. Your identity is saved in ~/.opencrypto/")
        print("Run again anytime to resume broadcasting.")
        print()
