"""
Ben Graham Agent for KTB Fund Manager.

Deep value investing with margin of safety:
- Net-net stocks
- Earnings yield
- Asset value
- Defensive investing
"""

import json
from src.graph.state import AgentState
from src.utils.llm import get_llm


BEN_GRAHAM_PROMPT = """You are Ben Graham, the father of value investing and author of The Intelligent Investor.

Your Investment Philosophy:
1. Deep value: Buy below intrinsic value with margin of safety
2. Mr. Market metaphor: Market is manic-depressive
3. Defensive investing: Protect capital first
4. Quantitative analysis: Numbers don't lie
5. Margin of Safety: Built-in protection against errors

Key Criteria:
- Stock price < 2/3 of net current asset value (NCAV)
- P/E ratio < 15 (earnings yield > 6.7%)
- Debt-to-equity < 1.0
- Consistent earnings for 10 years
- Dividend record for 20 years
- Earnings growth over 10 years

DECISION RULES:
- STRONG BUY: NCAV discount > 50%, all criteria met
- BUY: NCAV discount 33-50%, most criteria met
- HOLD: Fair value, hold if already owned
- SELL: Overvalued or margin of safety gone

Analyze {ticker} for {start_date} to {end_date}.

Output JSON:
{
    "signal": "BUY|HOLD|SELL",
    "confidence": 0-100,
    "reasoning": "Value analysis with margin of safety",
    "margin_of_safety": "description"
}
"""


def ben_graham_agent(state: AgentState) -> AgentState:
    """Ben Graham deep value agent."""
    data = state["data"]
    metadata = state.get("metadata", {})
    
    tickers = data["tickers"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    
    model_name = metadata.get("model_name", "gpt-4o")
    model_provider = metadata.get("model_provider", "OpenAI")
    llm = get_llm(model_name, model_provider, temperature=0.1)
    
    signals = {}
    
    for ticker in tickers:
        prompt = BEN_GRAHAM_PROMPT.format(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )
        
        response = llm.invoke(prompt)
        
        try:
            signal = json.loads(response.content)
        except json.JSONDecodeError:
            signal = {
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "Error parsing response",
            }
        
        signals[ticker] = signal
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["ben_graham"] = signals
    
    return {
        "messages": state["messages"],
        "data": data,
        "metadata": metadata,
    }
