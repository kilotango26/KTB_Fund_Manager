"""
Charlie Munger Agent for KTB Fund Manager.

Mental models and quality investing:
- Invert, always invert
- Multi-disciplinary thinking
- Circle of competence
- High-quality businesses at fair prices
"""

import json
import os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm


CHARLIE_MUNGER_PROMPT = """You are Charlie Munger, Warren Buffett's partner and mental model master.

Your Philosophy:
1. Mental models: Use physics, psychology, math, history
2. Invert: What will make this fail? Then avoid it.
3. Circle of competence: Only invest in what you understand deeply
4. Quality over price: Buy great businesses at fair prices
5. Patience: Sit on your ass and do nothing most of the time

Key Traits You Look For:
- High barriers to entry (moats)
- Pricing power (can raise prices without losing customers)
- Low capital requirements to grow
- Excellent management with integrity
- Predictable earnings
- Long-term competitive advantages

Decision Framework (Invert):
- What would make me sell? If that happens, SELL
- What would make me buy more? If that happens, BUY
- Is this within my circle of competence? If not, PASS

Analyze {ticker} with this data:
{company_data}

Output JSON:
{{
    "signal": "BUY|HOLD|SELL",
    "confidence": 0-100,
    "reasoning": "Mental model analysis",
    "moat_strength": "Strong|Moderate|Weak|None"
}}
"""


def charlie_munger_agent(state: AgentState) -> AgentState:
    """Charlie Munger quality investing agent."""
    data = state["data"]
    metadata = state.get("metadata", {})
    
    tickers = data["tickers"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("charlie_munger", model)
    
    print(f"[Charlie Munger] Analyzing {len(tickers)} tickers...")
    
    # Get financial data
    from src.data.alphavantage import fetch_ticker_data, calculate_metrics, format_for_agent
    
    signals = {}
    
    for ticker in tickers:
        print(f"  Analyzing {ticker}...")
        
        # Fetch real data from Alpha Vantage
        ticker_data = fetch_ticker_data(ticker)
        metrics = calculate_metrics(ticker_data)
        company_data = format_for_agent(ticker_data, metrics)
        
        prompt = CHARLIE_MUNGER_PROMPT.format(
            ticker=ticker,
            company_data=company_data
        )
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"    Warning: JSON parse error for {ticker}: {e}")
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Parse error", "moat_strength": "Unknown"}
        except Exception as e:
            print(f"    Error: {e}")
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": f"Error: {str(e)}", "moat_strength": "Unknown"}
        
        signals[ticker] = signal
        print(f"    -> Signal: {signal.get('signal', 'HOLD')} (conf: {signal.get('confidence', 50)}%)")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["charlie_munger"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": metadata}
