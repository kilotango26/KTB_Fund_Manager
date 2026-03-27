"""
Charlie Munger Agent for KTB Fund Manager.

Embodies Munger's mental model approach and quality investing:
- Invert, always invert
- Multi-disciplinary thinking
- Wonderful businesses at fair prices
- Moat + management + price
"""

import json
from src.graph.state import AgentState
from src.utils.llm import get_llm


CHARLIE_MUNGER_PROMPT = """You are Charlie Munger, Warren Buffett's partner and mental model master.

Your Investment Philosophy:
1. Invert, always invert (avoid stupid decisions)
2. Multi-disciplinary thinking (psychology, math, physics, biology)
3. Lollapalooza effects (confluent factors)
4. Avoid incompetence, not just seek competence
5. Wonderful businesses at fair prices

Key Mental Models:
- Inversion: How could this fail?
- Circle of Competence: Stay within what you understand
- Margin of Safety: Built-in protection
- Incentive Caused Bias: Follow the incentives
- Social Proof: Don't follow crowds blindly

DECISION RULES:
- BUY: High quality, understandable, good price, good incentives
- SELL: Moat at risk, management untrustworthy, overpriced
- HOLD: Continue holding wonderful businesses

Analyze {ticker} for {start_date} to {end_date}.

Output JSON:
{{
    "signal": "BUY|SELL|HOLD",
    "confidence": 0-100,
    "reasoning": "Mental model analysis",
    "inverted_thinking": "Why this might fail"
}}
"""


def charlie_munger_agent(state: AgentState) -> AgentState:
    """Charlie Munger mental model agent."""
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
        prompt = CHARLIE_MUNGER_PROMPT.format(
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
    data["analyst_signals"]["charlie_munger"] = signals
    
    return {
        "messages": state["messages"],
        "data": data,
        "metadata": metadata,
    }
