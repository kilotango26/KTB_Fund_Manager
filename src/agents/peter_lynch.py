"""
Peter Lynch Agent for KTB Fund Manager.

Growth investing in understandable businesses:
- Ten-baggers
- Buy what you know
- Growth at reasonable price
"""

from src.graph.state import AgentState


def peter_lynch_agent(state: AgentState) -> AgentState:
    """Peter Lynch growth investing agent."""
    data = state["data"]
    tickers = data["tickers"]
    
    signals = {}
    for ticker in tickers:
        signals[ticker] = {
            "signal": "HOLD",
            "confidence": 50,
            "reasoning": "Peter Lynch analysis - ten-bagger potential evaluation pending"
        }
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["peter_lynch"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
