"""
LLM utilities for KTB Fund Manager.

Provides unified interface for different LLM providers.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


def get_llm(model_name: str = "gpt-4o", provider: str = "OpenAI", temperature: float = 0.0):
    """
    Get an LLM instance based on provider and model name.
    
    Args:
        model_name: Name of the model to use
        provider: Provider name (OpenAI, Anthropic)
        temperature: Sampling temperature
    
    Returns:
        Chat model instance
    """
    if provider.lower() == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
        )
    
    elif provider.lower() == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        return ChatAnthropic(
            model=model_name,
            temperature=temperature,
            api_key=api_key,
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_default_llm(temperature: float = 0.0):
    """Get the default LLM based on available API keys."""
    if os.getenv("OPENAI_API_KEY"):
        return get_llm("gpt-4o", "OpenAI", temperature)
    elif os.getenv("ANTHROPIC_API_KEY"):
        return get_llm("claude-3-5-sonnet-20241022", "Anthropic", temperature)
    else:
        raise ValueError("No API key found for OpenAI or Anthropic")
