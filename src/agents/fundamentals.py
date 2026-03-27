"""Fundamentals Analysis Agent for KTB Fund Manager."""
import json, os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm

FUNDAMENTALS_PROMPT = '''You are a fundamental analyst focused on financial health.

Key Metrics:
- ROE/ROA: Return metrics >15%
- Margins: Operating and profit margins stable
- Debt: Low debt-to-equity (<0.5), debt coverage
- Cash Flow: Free cash flow positive and growing
- Growth: Revenue and earnings growth 10%+
- Efficiency: Asset turnover, inventory turnover

Scoring:
- Strong (>70): All metrics healthy, consistent
- Moderate (50-70): Most metrics good, some concerns
- Weak (<50): Multiple red flags

Company Data:\n{company_data}

Output JSON:
{{"signal": "BUY|HOLD|SELL", "confidence": 0-100, "reasoning": "fundamental analysis", "financial_health_score": 75}}
'''

def fundamentals_agent(state: AgentState) -> AgentState:
    data = state["data"]
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("fundamentals", model)
    
    from src.data.alphavantage import fetch_ticker_data, calculate_metrics, format_for_agent
    
    signals = {}
    print(f"[Fundamentals] Analyzing {len(data['tickers'])} tickers...")
    
    for ticker in data["tickers"]:
        ticker_data = fetch_ticker_data(ticker)
        metrics = calculate_metrics(ticker_data)
        company_data = format_for_agent(ticker_data, metrics)
        
        prompt = FUNDAMENTALS_PROMPT.format(company_data=company_data)
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except:
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Error", "financial_health_score": 50}
        
        signals[ticker] = signal
        print(f"  {ticker}: {signal['signal']} (health: {signal.get('financial_health_score', 'N/A')})")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["fundamentals"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
