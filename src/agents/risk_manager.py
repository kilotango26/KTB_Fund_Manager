"""
Risk Manager Agent for KTB Fund Manager.

Calculates risk metrics and sets position limits for the portfolio.
"""

import json
from src.graph.state import AgentState
from src.utils.llm import get_llm


RISK_MANAGER_PROMPT = """You are the Risk Manager for KTB Fund Manager.

Your role is to assess portfolio risk and set position limits based on:
1. Individual position concentration
2. Sector exposure
3. Correlation between holdings
4. Market volatility
5. Portfolio margin usage

INPUT DATA:
- Tickers: {tickers}
- Current Portfolio: {portfolio}
- Analyst Signals: {analyst_signals}

RISK CONSTRAINTS:
- Maximum single position: 25% of portfolio
- Maximum sector exposure: 40% of portfolio
- Maximum margin usage: 50% of portfolio value
- Minimum cash reserve: 10% of portfolio

OUTPUT FORMAT:
Provide risk assessment as JSON:
{{
    "risk_level": "LOW|MEDIUM|HIGH",
    "position_limits": {{
        "TICKER": {{
            "max_shares": <number>,
            "max_notional": <dollar_amount>
        }}
    }},
    "recommendations": ["List of risk-related recommendations"]
}}

Focus on protecting capital while allowing alpha generation.
"""


def risk_management_agent(state: AgentState) -> AgentState:
    """
    Risk Manager agent that assesses and manages portfolio risk.
    
    Args:
        state: Current agent state
    
    Returns:
        Updated state with risk assessment
    """
    data = state["data"]
    metadata = state.get("metadata", {})
    
    tickers = data["tickers"]
    portfolio = data["portfolio"]
    analyst_signals = data.get("analyst_signals", {})
    
    # Get LLM
    model_name = metadata.get("model_name", "gpt-4o")
    model_provider = metadata.get("model_provider", "OpenAI")
    llm = get_llm(model_name, model_provider, temperature=0.1)
    
    # Build prompt
    prompt = RISK_MANAGER_PROMPT.format(
        tickers=tickers,
        portfolio=json.dumps(portfolio, indent=2),
        analyst_signals=json.dumps(analyst_signals, indent=2),
    )
    
    # Get risk assessment
    response = llm.invoke(prompt)
    
    # Store risk assessment in data
    try:
        risk_assessment = json.loads(response.content)
    except json.JSONDecodeError:
        risk_assessment = {
            "risk_level": "MEDIUM",
            "position_limits": {},
            "recommendations": ["Use default risk limits"]
        }
    
    # Merge risk assessment into data
    data["risk_assessment"] = risk_assessment
    
    return {
        "messages": state["messages"],
        "data": data,
        "metadata": metadata,
    }
