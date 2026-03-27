"""
Analyst definitions and configuration for KTB Fund Manager.

Maps analyst names to their respective agent functions.
"""

from typing import Dict, Tuple, Callable
from src.agents.warren_buffett import warren_buffett_agent
from src.agents.charlie_munger import charlie_munger_agent
from src.agents.ben_graham import ben_graham_agent
from src.agents.peter_lynch import peter_lynch_agent
from src.agents.cathie_wood import cathie_wood_agent
from src.agents.michael_burry import michael_burry_agent
from src.agents.stanley_druckenmiller import stanley_druckenmiller_agent
from src.agents.fundamentals import fundamentals_agent
from src.agents.technicals import technicals_agent
from src.agents.sentiment import sentiment_agent
from src.agents.valuation import valuation_agent


# Analyst order for display purposes
ANALYST_ORDER = [
    "warren_buffett",
    "charlie_munger",
    "ben_graham",
    "peter_lynch",
    "cathie_wood",
    "michael_burry",
    "stanley_druckenmiller",
    "fundamentals",
    "technicals",
    "sentiment",
    "valuation",
]

# Analyst display names
ANALYST_DISPLAY_NAMES = {
    "warren_buffett": "Warren Buffett (Value)",
    "charlie_munger": "Charlie Munger (Quality)",
    "ben_graham": "Ben Graham (Deep Value)",
    "peter_lynch": "Peter Lynch (Growth)",
    "cathie_wood": "Cathie Wood (Innovation)",
    "michael_burry": "Michael Burry (Contrarian)",
    "stanley_druckenmiller": "Stanley Druckenmiller (Macro)",
    "fundamentals": "Fundamentals Analyst",
    "technicals": "Technical Analyst",
    "sentiment": "Sentiment Analyst",
    "valuation": "Valuation Analyst",
}


def get_analyst_nodes() -> Dict[str, Tuple[str, Callable]]:
    """
    Get all analyst node definitions.
    
    Returns a dictionary mapping analyst keys to (node_name, node_function) tuples.
    """
    return {
        "warren_buffett": ("warren_buffett_agent", warren_buffett_agent),
        "charlie_munger": ("charlie_munger_agent", charlie_munger_agent),
        "ben_graham": ("ben_graham_agent", ben_graham_agent),
        "peter_lynch": ("peter_lynch_agent", peter_lynch_agent),
        "cathie_wood": ("cathie_wood_agent", cathie_wood_agent),
        "michael_burry": ("michael_burry_agent", michael_burry_agent),
        "stanley_druckenmiller": ("stanley_druckenmiller_agent", stanley_druckenmiller_agent),
        "fundamentals": ("fundamentals_agent", fundamentals_agent),
        "technicals": ("technicals_agent", technicals_agent),
        "sentiment": ("sentiment_agent", sentiment_agent),
        "valuation": ("valuation_agent", valuation_agent),
    }


def get_analyst_display_name(analyst_key: str) -> str:
    """Get the display name for an analyst."""
    return ANALYST_DISPLAY_NAMES.get(analyst_key, analyst_key)


def get_analyst_description(analyst_key: str) -> str:
    """Get the description for an analyst."""
    descriptions = {
        "warren_buffett": "Focuses on quality companies with durable competitive advantages",
        "charlie_munger": "Uses mental models to identify wonderful businesses",
        "ben_graham": "Seeks deep value with significant margin of safety",
        "peter_lynch": "Looks for growth opportunities in understandable businesses",
        "cathie_wood": "Invests in disruptive innovation and exponential growth",
        "michael_burry": "Finds contrarian deep value opportunities",
        "stanley_druckenmiller": "Seeks asymmetric risk/reward opportunities",
        "fundamentals": "Analyzes financial statements and key metrics",
        "technicals": "Uses price action and technical indicators",
        "sentiment": "Analyzes market sentiment and news flow",
        "valuation": "Calculates intrinsic value and fair price",
    }
    return descriptions.get(analyst_key, "Investment analyst")
