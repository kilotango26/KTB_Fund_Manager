#!/usr/bin/env python3
"""Real Backtest - Run All Agents with Alpha Vantage Data"""

import os, json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import agents
from src.agents.warren_buffett import warren_buffett_agent
from src.agents.charlie_munger import charlie_munger_agent
from src.agents.ben_graham import ben_graham_agent
from src.agents.peter_lynch import peter_lynch_agent
from src.agents.technicals import technicals_agent
from src.agents.fundamentals import fundamentals_agent
from src.agents.sentiment import sentiment_agent
from src.agents.valuation import valuation_agent
from src.graph.state import AgentState
from src.data.alphavantage import fetch_ticker_data, calculate_metrics
from src.utils.llm import DEFAULT_MODEL

ALL_AGENTS = [
    warren_buffett_agent,
    charlie_munger_agent,
    ben_graham_agent,
    peter_lynch_agent,
    technicals_agent,
    fundamentals_agent,
    sentiment_agent,
    valuation_agent,
]


def aggregate_signals(analyst_signals):
    """Aggregate all agent signals into final decision."""
    ticker_signals = {}
    
    for agent_name, signals in analyst_signals.items():
        for ticker, signal in signals.items():
            if ticker not in ticker_signals:
                ticker_signals[ticker] = []
            ticker_signals[ticker].append({
                "agent": agent_name,
                "signal": signal.get("signal", "HOLD"),
                "confidence": signal.get("confidence", 50),
                "reasoning": signal.get("reasoning", "")
            })
    
    final_decisions = {}
    for ticker, signals in ticker_signals.items():
        buys = sum(1 for s in signals if s["signal"] == "BUY")
        sells = sum(1 for s in signals if s["signal"] == "SELL")
        holds = sum(1 for s in signals if s["signal"] == "HOLD")
        
        avg_confidence = sum(s["confidence"] for s in signals) / len(signals)
        
        if buys > sells and buys > holds:
            action = "BUY"
            position = min(25, 5 + buys * 3)
        elif sells > buys and sells > holds:
            action = "SELL"
            position = 0
        else:
            action = "HOLD"
            position = min(10, 5 + holds)
        
        final_decisions[ticker] = {
            "action": action,
            "confidence": int(avg_confidence),
            "position_size": position,
            "agent_votes": {"buy": buys, "hold": holds, "sell": sells},
            "signals": signals
        }
    
    return final_decisions


def run_full_backtest(tickers, start_date=None, end_date=None, api_key=None):
    """Run all agents with Alpha Vantage data."""
    
    print("="*70)
    print("  KTB FUND MANAGER - REAL-TIME BACKTEST")
    print("="*70)
    
    if api_key:
        os.environ["ALPHA_VANTAGE_API_KEY"] = api_key
    
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
    if api_key == "demo":
        print("\n⚠️  WARNING: Using DEMO mode (limited to IBM, AAPL, MSFT)")
        print("   Get API key: https://www.alphavantage.co/support/#api-key")
        print()
    
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n  Tickers:  {', '.join(tickers)}")
    print(f"  Period:   {start_date} to {end_date}")
    print(f"  Model:    {DEFAULT_MODEL}")
    print(f"  Agents:   {len(ALL_AGENTS)} value investing strategies")
    print()
    
    # Fetch prices
    print("  📊 Fetching Alpha Vantage Data...")
    prices = {}
    for ticker in tickers:
        data = fetch_ticker_data(ticker)
        m = calculate_metrics(data)
        prices[ticker] = m.get("price", 0)
    
    # Run agents
    initial_state: AgentState = {
        "messages": [],
        "data": {"tickers": tickers, "start_date": start_date, "end_date": end_date},
        "metadata": {"model": DEFAULT_MODEL}
    }
    
    print(f"\n  🤖 Running {len(ALL_AGENTS)} AI Agents...")
    print("-"*70)
    
    for agent in ALL_AGENTS:
        try:
            initial_state = agent(initial_state)
        except Exception as e:
            print(f"    ⚠️  Agent error: {e}")
    
    # Aggregate
    print("\n  📈 Aggregating Signals...")
    analyst_signals = initial_state["data"].get("analyst_signals", {})
    final_decisions = aggregate_signals(analyst_signals)
    
    # Output
    print("\n" + "="*70)
    print("  PORTFOLIO DECISIONS")
    print("="*70)
    
    buy_count = hold_count = sell_count = 0
    
    for ticker, decision in final_decisions.items():
        action = decision["action"]
        emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🟡"
        
        if action == "BUY":
            buy_count += 1
        elif action == "SELL":
            sell_count += 1
        else:
            hold_count += 1
        
        print(f"\n  {emoji} {ticker}")
        print(f"     Price:        ${prices.get(ticker, 0):.2f}")
        print(f"     Action:       {action} (confidence: {decision['confidence']}%)")
        print(f"     Position:     {decision['position_size']}%")
        print(f"     Votes:        {decision['agent_votes']}")
    
    print("\n" + "="*70)
    print(f"  SUMMARY: {buy_count} BUY 🟢 | {hold_count} HOLD 🟡 | {sell_count} SELL 🔴")
    print("="*70)
    
    return {
        "success": True,
        "tickers": tickers,
        "prices": prices,
        "analyst_signals": analyst_signals,
        "final_decisions": final_decisions,
        "summary": {"buy": buy_count, "hold": hold_count, "sell": sell_count}
    }


if __name__ == "__main__":
    import sys
    tickers = sys.argv[1].split(",") if len(sys.argv) > 1 else ["AAPL", "MSFT"]
    result = run_full_backtest(tickers)
    
    # Save results
    with open("/tmp/ktb_backtest_results.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n  ✅ Results saved to: /tmp/ktb_backtest_results.json")
