# -*- coding: utf-8 -*-
"""
OpenCrypto Agent — One-Command Installer
Run: python3 setup.py
"""
import subprocess, sys, os
from pathlib import Path

def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         OpenCrypto Agent — Setup & Installer            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher required.")
        print(f"You have: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

    # Install nostr-sdk
    print("📦 Installing nostr-sdk...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "nostr-sdk", "--quiet"])
        print("✅ nostr-sdk installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install nostr-sdk")
        print("   Try manually: pip install nostr-sdk")
        sys.exit(1)

    # Create identity directory
    identity_dir = Path.home() / ".opencrypto"
    identity_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Identity directory: {identity_dir}")

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Setup complete! Start the agent with:                  ║")
    print("║                                                          ║")
    print("║    python3 opencrypto_agent.py                          ║")
    print("║                                                          ║")
    print("║  Run in background (Linux/Mac):                         ║")
    print("║    nohup python3 opencrypto_agent.py > agent.log 2>&1 & ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

if __name__ == "__main__":
    main()
