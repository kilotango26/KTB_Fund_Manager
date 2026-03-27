"""
Agent State definition for KTB Fund Manager

Defines the state structure used throughout the LangGraph workflow.
"""

from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage


def merge_dicts(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two dictionaries recursively."""
    result = left.copy()
    for key, value in right.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


class AgentState(TypedDict):
    """State for the hedge fund agent system."""
    messages: Annotated[List[BaseMessage], lambda x, y: x + y]
    data: Annotated[Dict[str, Any], merge_dicts]
    metadata: Annotated[Dict[str, Any], merge_dicts]
