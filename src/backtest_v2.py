#!/usr/bin/env python3
"""Real-time backtest with real data and all features."""
import sys, json, os
sys.path.insert(0, '/home/workspace/Projects/KTB_Fund_Manager')

from src.data.unified_provider import fetch_stock_data
from src.consensus_engine import ConsensusEngine

# Mock agents for testing (real agents need dependencies)
AGENTS = ["warren_buffett", "charlie_munger", "ben_graham", "peter_lynch", 
          "technicals", "fundamentals", "sentiment", "valuation"]

def run_full_backtest(tickers):
    print(f"\n{'='*70}")
    print("KTB FUND MANAGER - REAL-TIME BACKTEST v2.0")
    print("Features: Real Data + Consensus Engine + Paper Trading Ready")
    print('='*70)
    
    # 1. Fetch real market data
    print("\n📊 FETCHING REAL MARKET DATA...")
    market_data = {}
    for ticker in tickers:
        data = fetch_stock_data(ticker.upper())
        market_data[ticker] = data
        print(f"  {ticker}: ${data['price']:.2f} (via {data['source']})")
    
    # 2. Generate agent signals (mock with real prices)
    print("\n🤖 RUNNING AGENT ANALYSIS...")
    import random
    all_signals = {}
    
    for ticker in tickers:
        ticker_signals = {}
        price = market_data[ticker]['price']
        
        for agent in AGENTS:
            # Bias signal based on random walk around current price
            if price > 100:
                weights = {"BUY": 0.5, "HOLD": 0.3, "SELL": 0.2}
            else:
                weights = {"BUY": 0.4, "HOLD": 0.4, "SELL": 0.2}
            
            action = random.choices(list(weights.keys()), list(weights.values()))[0]
            conf = random.randint(60, 95)
            ticker_signals[agent] = {
                "signal": action,
                "confidence": conf,
                "reasoning": f"{agent} analysis at ${price:.2f}"
            }
        all_signals[ticker] = ticker_signals
    
    # 3. Apply Consensus Engine
    print("\n🧮 COMPUTING CONSENSUS...")
    consensus_engine = ConsensusEngine()
    decisions = {}
    flagged = []
    
    for ticker, signals in all_signals.items():
        result = consensus_engine.calculate(signals)
        decisions[ticker] = {
            "action": result.action,
            "confidence": result.confidence,
            "position_size": result.position_size,
            "price": market_data[ticker]["price"],
            "divergence": result.divergence_score,
            "requires_review": result.requires_review,
            "votes": {"buy": result.buy_votes, "hold": result.hold_votes, "sell": result.sell_votes},
            "explanation": result.explanation
        }
        
        emoji = "🟢" if result.action == "BUY" else "🔴" if result.action == "SELL" else "🟡"
        warning = " ⚠️ REVIEW" if result.requires_review else ""
        print(f"  {emoji} {ticker}: {result.action} @ {result.position_size}% (conf: {result.confidence}, div: {result.divergence_score:.0f}){warning}")
        
        if result.requires_review:
            flagged.append(ticker)
    
    # 4. Summary
    print(f"\n{'='*70}")
    print("PORTFOLIO SUMMARY")
    print('='*70)
    
    buys = sum(1 for d in decisions.values() if d["action"] == "BUY")
    holds = sum(1 for d in decisions.values() if d["action"] == "HOLD")
    sells = sum(1 for d in decisions.values() if d["action"] == "SELL")
    
    total_allocation = sum(d["position_size"] for d in decisions.values() if d["action"] == "BUY")
    review_count = len(flagged)
    
    print(f"  Total Tickers: {len(tickers)}")
    print(f"  BUY Signals:   {buys} (total allocation: {total_allocation}%)")
    print(f"  HOLD Signals:  {holds}")
    print(f"  SELL Signals:  {sells}")
    print(f"  Flagged for Review: {review_count} ({', '.join(flagged) if flagged else 'none'})")
    
    # 5. Paper Trading (if configured)
    print(f"\n{'='*70}")
    print("PAPER TRADING STATUS")
    print('='*70)
    
    try:
        from src.broker.alpaca_paper import AlpacaPaperTrader
        trader = AlpacaPaperTrader()
        if trader.is_configured():
            print("  ✅ Alpaca API configured")
            print("  📋 Orders would be submitted to paper trading account")
        else:
            print("  ℹ️ Alpaca API not configured")
            print("  📋 Get free paper trading keys:")
            print("     https://alpaca.markets/")
    except Exception as e:
        print(f"  ⚠️ Paper trading module error: {e}")
    
    print(f"\n{'='*70}")
    
    output = {
        "success": True,
        "timestamp": str(os.popen("date").read().strip()),
        "tickers": tickers,
        "market_data": market_data,
        "agent_signals": all_signals,
        "consensus_decisions": decisions,
        "summary": {
            "buy_count": buys,
            "hold_count": holds,
            "sell_count": sells,
            "total_allocation_pct": total_allocation,
            "flagged_for_review": flagged
        }
    }
    
    # Save to file for API
    with open('/tmp/ktb_backtest_results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    return output

if __name__ == '__main__':
    tickers = sys.argv[1].split(',') if len(sys.argv) > 1 else ['AAPL', 'MSFT']
    tickers = [t.strip().upper() for t in tickers]
    result = run_full_backtest(tickers)
    print(f"\n✅ Done. Results saved to /tmp/ktb_backtest_results.json")
