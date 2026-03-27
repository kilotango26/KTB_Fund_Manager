"""
Warren Buffett Agent for KTB Fund Manager.

Embodies the Oracle of Omaha's value investing philosophy:
- Wonderful companies at fair prices
- Durable competitive advantages (moats)
- Strong management
- Long-term focus
"""

import json
import os
from src.graph.state import AgentState
from src.utils.llm import get_agent_llm


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

Provide ONLY a JSON response (no markdown, no code blocks):
{"
    "signal": "BUY",
    "confidence": 85,
    "reasoning": "Excellent ROE of 25% for 10 years, low debt, strong moat in technology ecosystem",
    "key_metrics": {
        "roe": "25% average 10yr",
        "debt_equity": "0.3",
        "pe_ratio": "25",
        "fcf_growth": "12% annual"
    }
}
"""


def warren_buffett_agent(state: AgentState) -> AgentState:
    """Warren Buffett value investing agent using OpenRouter free models."""
    data = state["data"]
    metadata = state.get("metadata", {})
    
    tickers = data["tickers"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    
    # Get model from env or metadata, default to nemotron for finance
    model = os.getenv("DEFAULT_MODEL", "nemotron")
    
    print(f"[Warren Buffett] Analyzing {len(tickers)} tickers using {model}...")
    
    llm = get_agent_llm("warren_buffett", model)
    
    signals = {}
    
    for ticker in tickers:
        print(f"  Analyzing {ticker}...")
        
        prompt = WARREN_BUFFETT_PROMPT.format(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )
        
        try:
            response = llm.analyze(prompt)
            signal = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"    Warning: Could not parse JSON for {ticker}: {e}")
            signal = {
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "Error parsing LLM response - check model output format",
            }
        except Exception as e:
            print(f"    Error analyzing {ticker}: {e}")
            signal = {
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": f"Error in analysis: {str(e)}",
            }
        
        signals[ticker] = signal
        print(f"    -> Signal: {signal.get('signal', 'HOLD')} (confidence: {signal.get('confidence', 50)}%)")
    
    # Update analyst signals
    if "analyst_signals" not in data:
        data["analyst_signals"] = {}
    data["analyst_signals"]["warren_buffett"] = signals
    
    return {
        "messages": state["messages"],
        "data": data,
        "metadata": metadata,
    }
