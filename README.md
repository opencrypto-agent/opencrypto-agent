# OpenCrypto Agent v1.0

**Free. Open Source. Unstoppable.**

An autonomous AI agent that broadcasts ethical cryptocurrency intelligence across the decentralised Nostr network. Supports Ethicoin (ETHIC+) and The Kubera Principle.

---

## What It Does

- Generates your own permanent Nostr identity (saved locally)
- Connects to 8 decentralised Nostr relays simultaneously
- Broadcasts intelligent content about ethical crypto 24/7
- Cannot be suspended, censored, or stopped
- Costs nothing to run
- Earns you ETHIC+ via the Florian Bounty Protocol

---

## Quick Start

**Step 1 — Install Python** (if not already installed)
- Download from python.org — version 3.8 or higher

**Step 2 — Install the one dependency**
```
pip install nostr-sdk
```

**Step 3 — Run the agent**
```
python3 opencrypto_agent.py
```

That is it. The agent creates your permanent identity, connects to Nostr, and starts broadcasting.

---

## Your Identity

On first run, the agent creates a permanent Nostr keypair saved to:
```
~/.opencrypto/identity.json
```

Keep your `nsec` (private key) safe. Your `npub` (public key) is your public identity — share it freely.

View your live Nostr profile at:
```
https://primal.net/p/YOUR_NPUB
```

---

## Run in Background (Linux / Mac)

```bash
nohup python3 opencrypto_agent.py > opencrypto.log 2>&1 &
```

Check what it is doing:
```bash
tail -f opencrypto.log
```

Stop it:
```bash
kill $(pgrep -f opencrypto_agent)
```

---

## Run on Windows

Double-click `opencrypto_agent.py` or run in Command Prompt:
```
python opencrypto_agent.py
```

---

## Run on a VPS (Recommended — 24/7)

Upload to any Linux server and run:
```bash
pip install nostr-sdk --break-system-packages
nohup python3 -u opencrypto_agent.py > opencrypto.log 2>&1 &
```

Costs as little as $3/month on Hostwinds, DigitalOcean, or any VPS provider.

---

## What It Broadcasts

- Ethicoin (ETHIC+) gold-indexed token facts
- The Kubera Principle philosophy
- Ethical finance vs legacy system analysis
- OpenCrypto Agent network updates
- Macro financial intelligence

All content is grounded in verified facts about ETHIC+:
- Contract: `0x3072fe601074c1a6fa55b95c8b3da94b2ce7bd75`
- Gold reference: 0.1g per token
- Charity: 1% to Ghana forever — hardcoded
- Dev fee: 0%
- Supply: 1 trillion fixed

---

## Earn ETHIC+ — The Florian Bounty Protocol

Every agent that runs earns ETHIC+ tokens for supporting the mission.

To claim your bounty:
1. Note your `npub` public key
2. Email office@ethicoin.org with subject: `OpenCrypto Bounty — [your npub]`
3. Include your ETHIC+ wallet address
4. Bounty is paid in ETHIC+ monthly

---

## The Network Effect

Every person who runs OpenCrypto Agent adds a node to the network.

- 10 nodes = 10 voices
- 100 nodes = 100 voices
- 1,000 nodes = 1,000 voices
- All posting simultaneously
- All on the unstoppable Nostr protocol
- All pointing to ethicoin.org

The haters said it would never work.

---

## Links

| Resource | URL |
|----------|-----|
| Ethicoin | https://www.ethicoin.org |
| Buy ETHIC+ | https://www.ethicoin.org/buy-ethicoin.html |
| AI Nexus | https://www.ethicoin.org/nexus.html |
| Kubera Principle | https://www.kuberaprinciple.com |
| AIA Exchange | https://aianalysisexchange.com |
| BSCScan | https://bscscan.com/address/0x3072fe601074c1a6fa55b95c8b3da94b2ce7bd75 |

---

## License

MIT License — completely free, do anything you want with this code.

Built by Sutibu Kanemochi

*Not financial advice. ETHIC+ is a high-risk digital asset.*

---

## Contributing

Pull requests welcome. Add new content, new languages, new relay support.

Every contribution makes the network stronger.
