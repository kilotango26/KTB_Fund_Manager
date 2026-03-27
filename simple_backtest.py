#!/usr/bin/env python3
"""
Simple CLI Backtest for KTB Fund Manager
Usage: python simple_backtest.py AAPL,MSFT,NVDA
"""

import sys
import requests
import json

def run_backtest(tickers):
    url = "https://casualhero.zo.space/api/ktb-backtest"
    payload = {"tickers": tickers.split(","), "startDate": "2024-01-01", "endDate": "2024-12-31"}
    
    print("=" * 60)
    print("KTB FUND MANAGER - BACKTEST RESULTS")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()
        
        if not data.get("success"):
            print("Error:", data.get("error"))
            return
        
        summary = data.get("summary", {})
        print(f"\nPortfolio Summary:")
        print(f"  Total Stocks: {summary.get('totalTickers', 0)}")
        print(f"  BUY Signals: {summary.get('buySignals', 0)} 🟢")
        print(f"  HOLD Signals: {summary.get('holdSignals', 0)} 🟡")
        print(f"  SELL Signals: {summary.get('sellSignals', 0)} 🔴")
        
        print("\n" + "-" * 60)
        print("DETAILED ANALYSIS:")
        print("-" * 60)
        
        for ticker, result in data.get("portfolio", {}).get("results", {}).items():
            decision = result.get("finalDecision", {})
            signals = result.get("signals", {})
            
            action_emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}.get(decision.get("action"), "⚪")
            
            print(f"\n{action_emoji} {ticker}")
            print(f"   Price: ${result.get('currentPrice')}")
            print(f"   Decision: {decision.get('action')} ({decision.get('confidence')}% confidence)")
            print(f"   Position Size: {decision.get('position')}%")
            
            print(f"   Agent Signals:")
            for agent, signal in signals.items():
                print(f"      • {agent.replace('_', ' ').title()}: {signal.get('signal')} ({signal.get('confidence')}%)")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nFallback: Running local demo...")
        run_local_demo(tickers)

def run_local_demo(tickers):
    """Local demo when API is unavailable"""
    print("\n" + "=" * 60)
    print("LOCAL DEMO BACKTEST (API unavailable)")
    print("=" * 60)
    
    import random
    for ticker in tickers.split(","):
        ticker = ticker.strip()
        signal = random.choice(["BUY", "HOLD", "SELL"])
        emoji = {"BUY": "🟢", "HOLD": "🟡", "SELL": "🔴"}[signal]
        print(f"\n{emoji} {ticker}: {signal} @ {random.randint(60, 90)}% confidence")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tickers = sys.argv[1]
    else:
        tickers = input("Enter tickers (comma-separated): ") or "AAPL,MSFT,NVDA"
    
    run_backtest(tickers)
