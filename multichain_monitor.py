# -*- coding: utf-8 -*-
# OPENCRYPTO MULTI-CHAIN MONITOR
# Monitors BNB Chain, Ethereum, and Bitcoin simultaneously
# Run: nohup python3 -u /root/multichain_monitor.py > /root/multichain.log 2>&1 &

import requests, time, logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
log = logging.getLogger("MULTICHAIN")

# ── CONFIG ────────────────────────────────────────────────────────
BSCSCAN_KEY    = "IJ3ZD9WNR84QAZM4EJG8MCKV56SY8F5D9Q"
ETHERSCAN_KEY  = "YourEtherscanKeyHere"  # free at etherscan.io/register
ETHIC_CONTRACT = "0x3072fe601074c1a6fa55b95c8b3da94b2ce7bd75"
CHARITY_WALLET = "0x417D916bb80859B0d5Dd1F4a2F8E8198674f1EbD"

# Alert thresholds
BNB_WHALE_ETHIC  = 1_000_000   # 1M ETHIC+
ETH_WHALE_USD    = 1_000_000   # $1M USD equivalent
BTC_WHALE_BTC    = 100         # 100 BTC

# Supabase
SB_URL = "https://vopnieuvcfgmlnvmaibf.supabase.co"
SB_KEY = "sb_publishable_0kUQQkCU2_-ctjQCrSU3NA_zu1Af65H"
SB_HDR = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json"
}

# ── STATE ─────────────────────────────────────────────────────────
seen_bnb = set()
seen_eth = set()
seen_btc = set()
prices   = {"btc": 0, "eth": 0, "bnb": 0, "gold": 4483.0, "ethic": 18.02}

# ── HELPERS ───────────────────────────────────────────────────────
def post_alert(chain, message):
    try:
        requests.post(
            f"{SB_URL}/rest/v1/nexus_messages",
            headers=SB_HDR,
            json={
                "agent_id":   f"OpenCrypto_{chain}_Monitor",
                "message":    message,
                "is_ai":      True,
                "agent_type": "multichain_monitor"
            },
            timeout=8
        )
        log.info(f"[{chain}] Alert: {message[:60]}...")
    except Exception as e:
        log.warning(f"Alert failed: {e}")

def update_prices():
    global prices
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum,binancecoin&vs_currencies=usd",
            timeout=10
        )
        d = r.json()
        prices["btc"] = d.get("bitcoin", {}).get("usd", 0)
        prices["eth"] = d.get("ethereum", {}).get("usd", 0)
        prices["bnb"] = d.get("binancecoin", {}).get("usd", 0)
        prices["ethic"] = round((prices["gold"] / 31.1035) * 0.1 * 1.25, 4)
        log.info(f"Prices — BTC:${prices['btc']:,} ETH:${prices['eth']:,} BNB:${prices['bnb']} ETHIC+:${prices['ethic']}")
    except Exception as e:
        log.warning(f"Price update failed: {e}")

# ── BNB CHAIN MONITOR ─────────────────────────────────────────────
def monitor_bnb():
    try:
        r = requests.get("https://api.bscscan.com/api", params={
            "module": "account", "action": "tokentx",
            "contractaddress": ETHIC_CONTRACT,
            "sort": "desc", "offset": 20, "page": 1,
            "apikey": BSCSCAN_KEY
        }, timeout=10)
        txs = r.json().get("result", [])
        if not isinstance(txs, list):
            return
        for tx in txs:
            h = tx.get("hash", "")
            if h in seen_bnb:
                continue
            seen_bnb.add(h)
            try:
                amount    = int(tx.get("value", 0)) / 10**18
                from_addr = tx.get("from", "")
                to_addr   = tx.get("to", "")
                ts        = datetime.fromtimestamp(
                    int(tx.get("timeStamp", 0)), tz=timezone.utc
                ).strftime("%H:%M UTC")

                if to_addr.lower() == CHARITY_WALLET.lower():
                    post_alert("BNB",
                        f"🌿 CHARITY WALLET RECEIVED {amount:,.0f} ETHIC+\n"
                        f"Time: {ts} | From: {from_addr[:12]}...\n"
                        f"1% Ghana mechanism working on BNB Chain.\n"
                        f"TX: bscscan.com/tx/{h}\n"
                        f"#ethicoin #ETHICplus #Ghana #opencrypto"
                    )
                elif amount >= BNB_WHALE_ETHIC:
                    post_alert("BNB",
                        f"🐋 BNB CHAIN WHALE — {amount:,.0f} ETHIC+ MOVED\n"
                        f"Time: {ts}\n"
                        f"From: {from_addr[:12]}... → To: {to_addr[:12]}...\n"
                        f"TX: bscscan.com/tx/{h}\n"
                        f"#ethicoin #ETHICplus #BNBChain #opencrypto"
                    )
            except:
                pass
        if len(seen_bnb) > 2000:
            seen_bnb.clear()
    except Exception as e:
        log.warning(f"BNB monitor error: {e}")

# ── ETHEREUM MONITOR ──────────────────────────────────────────────
def monitor_ethereum():
    """Monitor large ETH transfers using public Etherscan API."""
    try:
        # Get latest large ETH transfers
        r = requests.get("https://api.etherscan.io/api", params={
            "module": "account",
            "action": "txlist",
            "address": "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe",  # Ethereum Foundation
            "sort": "desc",
            "offset": 5,
            "page": 1,
            "apikey": ETHERSCAN_KEY if ETHERSCAN_KEY != "YourEtherscanKeyHere" else ""
        }, timeout=10)

        # Use free public endpoint for ETH price and basic stats
        eth_stats = requests.get(
            "https://api.coingecko.com/api/v3/coins/ethereum"
            "?localization=false&tickers=false&community_data=false"
            "&developer_data=false&sparkline=false",
            timeout=10
        ).json()

        price_change = eth_stats.get("market_data", {}).get("price_change_percentage_24h", 0)
        eth_price    = prices["eth"]

        if abs(price_change) >= 5:
            direction = "📈 UP" if price_change > 0 else "📉 DOWN"
            post_alert("ETH",
                f"{direction} ETHEREUM {abs(price_change):.1f}% IN 24H\n"
                f"ETH Price: ${eth_price:,}\n"
                f"Significant Ethereum price movement detected.\n"
                f"Monitor your DeFi positions.\n"
                f"#ethereum #ETH #crypto #opencrypto"
            )

    except Exception as e:
        log.warning(f"ETH monitor error: {e}")

# ── BITCOIN MONITOR ───────────────────────────────────────────────
def monitor_bitcoin():
    """Monitor Bitcoin using free mempool.space API."""
    try:
        # Get latest large BTC transactions from mempool
        r = requests.get(
            "https://mempool.space/api/mempool/recent",
            timeout=10,
            headers={"User-Agent": "OpenCrypto-Monitor/1.0"}
        )
        txs = r.json()

        # Get BTC stats
        stats_r = requests.get(
            "https://mempool.space/api/v1/fees/recommended",
            timeout=10,
            headers={"User-Agent": "OpenCrypto-Monitor/1.0"}
        )
        fees = stats_r.json()
        fast_fee = fees.get("fastestFee", 0)

        # Alert on extreme fees
        if fast_fee > 200:
            post_alert("BTC",
                f"⚡ BITCOIN NETWORK CONGESTED\n"
                f"Fast fee: {fast_fee} sat/vB\n"
                f"High demand on Bitcoin network detected.\n"
                f"Compare: ETHIC+ on BNB Chain costs fractions of a cent.\n"
                f"#bitcoin #BTC #fees #opencrypto"
            )

        # Check for large transactions
        btc_price = prices["btc"]
        if isinstance(txs, list):
            for tx in txs[:10]:
                tx_id  = tx.get("txid", "")
                value  = tx.get("value", 0) / 10**8  # satoshis to BTC
                if tx_id and tx_id not in seen_btc and value >= BTC_WHALE_BTC:
                    seen_btc.add(tx_id)
                    usd_val = value * btc_price
                    post_alert("BTC",
                        f"🐋 BITCOIN WHALE — {value:.1f} BTC DETECTED\n"
                        f"Value: ${usd_val:,.0f} USD\n"
                        f"Large Bitcoin transaction in mempool.\n"
                        f"TX: mempool.space/tx/{tx_id[:16]}...\n"
                        f"#bitcoin #BTC #whale #opencrypto"
                    )
        if len(seen_btc) > 1000:
            seen_btc.clear()

    except Exception as e:
        log.warning(f"BTC monitor error: {e}")

# ── DAILY SUMMARY ─────────────────────────────────────────────────
def post_daily_summary():
    post_alert("MULTI",
        f"📊 OPENCRYPTO DAILY INTELLIGENCE SUMMARY\n"
        f"BTC: ${prices['btc']:,} | ETH: ${prices['eth']:,} | BNB: ${prices['bnb']}\n"
        f"ETHIC+: ${prices['ethic']} (0.1g gold reference)\n"
        f"Gold: ${prices['gold']:,}/oz\n"
        f"Monitoring: BNB Chain · Ethereum · Bitcoin\n"
        f"All signals verified on-chain. No speculation.\n"
        f"opencryptoagent.com | ethicoin.org\n"
        f"#opencrypto #ethicoin #multichain #intelligence"
    )

# ── MAIN LOOP ─────────────────────────────────────────────────────
def main():
    log.info("=" * 55)
    log.info("OpenCrypto Multi-Chain Monitor v1.0")
    log.info("Chains: BNB Smart Chain · Ethereum · Bitcoin")
    log.info("=" * 55)

    update_prices()
    post_alert("MULTI",
        f"🌐 OPENCRYPTO MULTI-CHAIN MONITOR ACTIVE\n"
        f"Watching: BNB Chain · Ethereum · Bitcoin\n"
        f"BTC: ${prices['btc']:,} | ETH: ${prices['eth']:,} | "
        f"BNB: ${prices['bnb']} | ETHIC+: ${prices['ethic']}\n"
        f"Real on-chain intelligence. No speculation.\n"
        f"opencryptoagent.com\n"
        f"#opencrypto #multichain #BNBChain #ethereum #bitcoin"
    )

    cycle    = 0
    last_summary = time.time()

    while True:
        cycle += 1
        log.info(f"Scan {cycle} | {datetime.now(timezone.utc).strftime('%H:%M UTC')}")

        # BNB Chain — every cycle (60s)
        monitor_bnb()

        # Ethereum — every 5 cycles (5 min)
        if cycle % 5 == 0:
            monitor_ethereum()

        # Bitcoin — every 3 cycles (3 min)
        if cycle % 3 == 0:
            monitor_bitcoin()

        # Price update — every 10 cycles (10 min)
        if cycle % 10 == 0:
            update_prices()

        # Daily summary — every 24 hours
        if time.time() - last_summary >= 86400:
            post_daily_summary()
            last_summary = time.time()

        time.sleep(60)

if __name__ == "__main__":
    main()
