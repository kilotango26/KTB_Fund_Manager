"""Sentiment Analysis Agent for KTB Fund Manager."""
import json, os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm

SENTIMENT_PROMPT = '''You are a sentiment analyst tracking market perception.

Sources to Consider:
- News sentiment: Positive vs negative coverage
- Analyst ratings: Buy/Sell consensus
- Social sentiment: Twitter/X, Reddit trends
- Insider activity: Buying or selling
- Short interest: High shorting = bearish
- Institutional flow: Smart money moves

Sentiment Scale:
- Very Bullish: >75 positive indicators
- Bullish: 60-75 positive
- Neutral: 40-60
- Bearish: 25-40
- Very Bearish: <25

For {ticker}:
- Research current sentiment
- Check analyst ratings
- Consider market momentum

Output JSON:
{"signal": "BUY|HOLD|SELL", "confidence": 0-100, "reasoning": "sentiment analysis", "sentiment_score": 65, "trend": "improving|stable|deteriorating"}
'''

def sentiment_agent(state: AgentState) -> AgentState:
    data = state["data"]
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("sentiment", model)
    
    signals = {}
    print(f"[Sentiment] Analyzing {len(data['tickers'])} tickers...")
    
    for ticker in data["tickers"]:
        prompt = SENTIMENT_PROMPT.format(ticker=ticker)
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except:
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Sentiment neutral", "sentiment_score": 50, "trend": "stable"}
        
        signals[ticker] = signal
        print(f"  {ticker}: {signal['signal']} (sentiment: {signal.get('sentiment_score', 50)})")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["sentiment"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
