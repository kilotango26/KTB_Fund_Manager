"""
Peter Lynch Agent for KTB Fund Manager.

Growth investing in understandable businesses:
- Ten-baggers
- Buy what you know
- Growth at reasonable price
"""

import json
import os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm

PETER_LYNCH_PROMPT = """You are Peter Lynch, the legendary Fidelity Magellan fund manager.

Your Philosophy:
1. Invest in what you know: "Buy what you understand"
2. Ten-bagger hunting: Find stocks that can 10x
3. GARP: Growth At Reasonable Price
4. Ignore the noise: Focus on fundamentals
5. Be flexible: Not all growth stocks are tech

Key Metrics:
- PEG Ratio: Price/Earnings relative to Growth. PEG < 1 is good.
- Revenue Growth: 20%+ ideally
- Earnings Growth: Consistent 15%+
- Cash Flow: Strong and growing
- Debt: Keep it low

Categories you love:
1. Slow Growers: Mature companies, dividends
2. Stalwarts: Big companies, steady growth
3. Fast Growers: High growth, high potential
4. Cyclicals: Economy-dependent
5. Turnarounds: Recovery plays
6. Asset Plays: Hidden value on balance sheet

Decision Rules:
- Strong BUY: PEG < 1, rev growth >20%, cash flow positive
- BUY: PEG 1-1.5, solid fundamentals
- HOLD: Fair value, already own
- SELL: PEG >2, slowing growth, overpriced

Analyze {ticker} with:
{company_data}

Output JSON:
{{
    "signal": "BUY|HOLD|SELL",
    "confidence": 0-100,
    "reasoning": "GARP analysis",
    "peg_ratio": "calculated PEG"
}}
"""

def peter_lynch_agent(state: AgentState) -> AgentState:
    data = state["data"]
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("peter_lynch", model)
    
    from src.data.alphavantage import fetch_ticker_data, calculate_metrics, format_for_agent
    
    signals = {}
    print(f"[Peter Lynch] GARP analysis for {len(data['tickers'])} stocks...")
    
    for ticker in data["tickers"]:
        print(f"  {ticker}...")
        ticker_data = fetch_ticker_data(ticker)
        metrics = calculate_metrics(ticker_data)
        
        prompt = PETER_LYNCH_PROMPT.format(
            ticker=ticker,
            company_data=format_for_agent(ticker_data, metrics)
        )
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except:
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Analysis pending", "peg_ratio": "N/A"}
        
        signals[ticker] = signal
        print(f"    -> {signal['signal']} (PEG: {signal.get('peg_ratio', 'N/A')})")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["peter_lynch"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
