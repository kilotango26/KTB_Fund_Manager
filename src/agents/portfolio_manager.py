"""
Portfolio Manager Agent for KTB Fund Manager.

Makes final trading decisions based on analyst signals and risk constraints.
"""

import json
from src.graph.state import AgentState
from src.utils.llm import get_llm


PORTFOLIO_MANAGER_PROMPT = """You are the Portfolio Manager for KTB Fund Manager, an AI-powered hedge fund.

Your role is to make final trading decisions based on the signals from multiple analysts
and the risk management constraints provided.

INPUT DATA:
- Tickers: {tickers}
- Current Portfolio: {portfolio}
- Analyst Signals: {analyst_signals}
- Risk Assessment: {risk_assessment}
- Market Data Period: {start_date} to {end_date}

DECISION FRAMEWORK:
1. Review all analyst signals and their confidence levels
2. Consider the risk management constraints (position limits, max exposure)
3. Make final BUY, SELL, or HOLD decisions for each ticker
4. Determine appropriate position sizes

OUTPUT FORMAT:
Provide your decisions as a JSON object:
{{
    "TICKER": {{
        "action": "BUY|SELL|HOLD",
        "quantity": <number_of_shares>,
        "price": <limit_price_or_market>,
        "confidence": "HIGH|MEDIUM|LOW",
        "reasoning": "Brief explanation of decision"
    }},
    ...
}}

GUIDELINES:
- Only BUY if you have conviction from multiple analysts
- SELL when analysts signal weakness or to rebalance
- HOLD when signals are mixed or unclear
- Respect risk limits: max position size, diversification
- Consider current portfolio composition
"""


def portfolio_management_agent(state: AgentState) -> AgentState:
    """
    Portfolio Manager agent that makes final trading decisions.
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with trading decisions
    """
    data = state["data"]
    metadata = state.get("metadata", {})
    
    tickers = data["tickers"]
    portfolio = data["portfolio"]
    analyst_signals = data.get("analyst_signals", {})
    start_date = data["start_date"]
    end_date = data["end_date"]
    
    # Get LLM
    model_name = metadata.get("model_name", "gpt-4o")
    model_provider = metadata.get("model_provider", "OpenAI")
    llm = get_llm(model_name, model_provider, temperature=0.1)
    
    # Build the prompt
    prompt = PORTFOLIO_MANAGER_PROMPT.format(
        tickers=tickers,
        portfolio=json.dumps(portfolio, indent=2),
        analyst_signals=json.dumps(analyst_signals, indent=2),
        risk_assessment="Position limits enforced by Risk Manager",
        start_date=start_date,
        end_date=end_date,
    )
    
    # Get decision from LLM
    response = llm.invoke(prompt)
    
    # Parse the response
    try:
        decisions = json.loads(response.content)
    except json.JSONDecodeError:
        # If JSON parsing fails, create a default hold decision
        decisions = {
            ticker: {
                "action": "HOLD",
                "quantity": 0,
                "price": "market",
                "confidence": "LOW",
                "reasoning": "Could not parse LLM response, defaulting to HOLD"
            }
            for ticker in tickers
        }
    
    # Add decisions to messages
    from langchain_core.messages import AIMessage
    
    return {
        "messages": [AIMessage(content=json.dumps(decisions))],
        "data": data,
        "metadata": metadata,
    }
