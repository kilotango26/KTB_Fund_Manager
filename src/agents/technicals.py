"""Technical Analysis Agent for KTB Fund Manager."""
import json, os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm

TECHNICAL_PROMPT = '''You are a quantitative analyst specializing in technical indicators.

Key Indicators:
- Moving Averages: 50-day vs 200-day (Golden Cross, Death Cross)
- RSI: <30 oversold, >70 overbought
- MACD: Bullish/bearish divergence
- Support/Resistance: Breakout or breakdown levels
- Volume: Confirming price movement
- Bollinger Bands: Volatility and mean reversion

Signal Rules:
- BUY: RSI < 30, MA crossover, increasing volume
- SELL: RSI > 70, Death cross, bearish divergence
- HOLD: Within normal ranges, no clear signal

Analyze {ticker} from {start_date} to {end_date}.

Output JSON:
{{"signal": "BUY|HOLD|SELL", "confidence": 0-100, "reasoning": "technical analysis", "rsi": 45, "trend": "bullish|bearish|neutral"}}
'''

def technicals_agent(state: AgentState) -> AgentState:
    data = state["data"]
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    llm = get_agent_llm("technicals", model)
    
    from src.data.alphavantage import fetch_ticker_data
    
    signals = {}
    print(f"[Technical Analysis] Analyzing {len(data['tickers'])} tickers...")
    
    for ticker in data["tickers"]:
        ticker_data = fetch_ticker_data(ticker)
        prices = ticker_data.get("prices", {}).get("Time Series (Daily)", {})
        
        price_list = list(prices.items())[:50] if prices else []
        closes = [float(d.get("4. close", 0)) for _, d in price_list]
        volumes = [float(d.get("5. volume", 0)) for _, d in price_list]
        
        price_summary = f"Recent prices: {closes[:10]}" if closes else "No price data"
        
        prompt = TECHNICAL_PROMPT.format(
            ticker=ticker,
            start_date=data["start_date"],
            end_date=data["end_date"]
        ) + f"\n\nPrice Data:\n{price_summary}"
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except:
            signal = {"signal": "HOLD", "confidence": 50, "reasoning": "Analysis error", "rsi": 50, "trend": "neutral"}
        
        signals[ticker] = signal
        print(f"  {ticker}: {signal['signal']} (trend: {signal.get('trend', 'N/A')})")
    
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["technicals"] = signals
    
    return {"messages": state["messages"], "data": data, "metadata": state.get("metadata", {})}
