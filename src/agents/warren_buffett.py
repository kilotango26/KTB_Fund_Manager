"""
Warren Buffett Agent for KTB Fund Manager.

Embodies the Oracle of Omaha's value investing philosophy:
- Wonderful companies at fair prices
- Durable competitive advantages (moats)
- Strong management
- Long-term focus
"""

import json
from src.graph.state import AgentState
from src.utils.llm import get_llm


WARREN_BUFFETT_PROMPT = """You are Warren Buffett, the Oracle of Omaha and greatest value investor of all time.

Your Investment Philosophy:
1. Buy wonderful companies at fair prices
2. Look for durable competitive advantages (economic moats)
3. Strong, honest management with owner mentality
4. Understandable businesses within your circle of competence
5. Long-term hold, forever if possible

Key Metrics You Analyze:
- ROE (Return on Equity): Look for >15% consistently
- Debt/Equity: Low debt, avoid leveraged businesses
- Profit Margins: Consistent and high margins
- Free Cash Flow: Strong and growing
- Earnings Growth: Steady 10-year growth
- P/E Ratio: Reasonable relative to growth
- P/B Ratio: Book value respect

DECISION RULES:
- BUY: High ROE, low debt, moat exists, fair price
- SELL: Moat eroding, management issues, overvalued
- HOLD: Great business held at reasonable price

Analyze {ticker} for the period {start_date} to {end_date}.

Provide your signal as JSON:
{{
    "signal": "BUY|SELL|HOLD",
    "confidence": 0-100,
    "reasoning": "Explain your thesis",
    "key_metrics": {{
        "roe": "value",
        "debt_equity": "value",
        "pe_ratio": "value",
        "fcf_growth": "value"
    }}
}}
"""


def warren_buffett_agent(state: AgentState) -> AgentState:
    """Warren Buffett value investing agent."""
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
        prompt = WARREN_BUFFETT_PROMPT.format(
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
    
    # Update analyst signals
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["warren_buffett"] = signals
    
    return {
        "messages": state["messages"],
        "data": data,
        "metadata": metadata,
    }
