"""Sentiment Analysis Agent"""
from src.graph.state import AgentState

def sentiment_agent(state: AgentState) -> AgentState:
    data = state["data"]
    tickers = data["tickers"]
    signals = {ticker: {"signal": "HOLD", "confidence": 50, "reasoning": "Sentiment analysis pending"} for ticker in tickers}
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["sentiment"] = signals
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
