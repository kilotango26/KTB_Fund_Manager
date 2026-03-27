"""Valuation Analysis Agent for KTB Fund Manager."""
import json, os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm

VALUATION_PROMPT = '''You are a valuation specialist using multiple methods.

Valuation Methods:
1. DCF: Discounted Cash Flow - intrinsic value
2. P/E Ratio: Compare to sector average
3. P/B Ratio: Asset-based valuation
4. PEG Ratio: GARP valuation
5. EV/EBITDA: Enterprise value
6. Discount to 52-week range

Fair Value Calculation:
- Determine intrinsic value
- Compare to current price
- Calculate upside/downside potential

Thresholds:
- Undervalued: Price < 80% of fair value
- Fairly Valued: 80-120% of fair value  
- Overvalued: >120% of fair value

Company Data:
{company_data}

Output JSON:
{"signal": "BUY|HOLD|SELL", "confidence": 0-100, "reasoning": "valuation analysis", "fair_value": 150.00, "current_price": 178.00, "upside_potential": -15.7}
'''

def valuation_agent(state: AgentState) -> AgentState:
    data = state["data"]
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("valuation", model)
    
    from src.data.alphavantage import fetch_ticker_data, calculate_metrics, format_for_agent
    
    signals = {}
    print(f"[Valuation] Analyzing {len(data['tickers'])} tickers...")
    
    for ticker in data["tickers"]:
        ticker_data = fetch_ticker_data(ticker)
        metrics = calculate_metrics(ticker_data)
        company_data = format_for_agent(ticker_data, metrics)
        
        prompt = VALUATION_PROMPT.format(company_data=company_data)
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except:
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Valuation pending", "fair_value": 0, "current_price": 0, "upside_potential": 0}
        
        signals[ticker] = signal
        print(f"  {ticker}: {signal['signal']} (upside: {signal.get('upside_potential', 'N/A')}%)")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["valuation"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
