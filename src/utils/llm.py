"""
LLM utilities for KTB Fund Manager using OpenRouter.

Provides unified interface for free and paid LLM models via OpenRouter.
No API key required for free models (zero-cost testing).
"""

import os
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI


# OpenRouter base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Recommended free models for financial analysis
FREE_MODELS = {
    "nemotron": {
        "id": "nvidia/nemotron-3-super-120b-a12b:free",
        "name": "NVIDIA Nemotron 3 Super",
        "context": 262000,
        "note": "#24 in Finance, 120B params"
    },
    "llama": {
        "id": "meta-llama/llama-3.3-70b-instruct:free", 
        "name": "Llama 3.3 70B",
        "context": 66000,
        "note": "Strong reasoning, 70B params"
    },
    "gpt_oss": {
        "id": "openai/gpt-oss-120b:free",
        "name": "gpt-oss-120b",
        "context": 131000,
        "note": "OpenAI open model, reasoning"
    },
    "qwen": {
        "id": "qwen/qwen3-coder:free",
        "name": "Qwen3 Coder 480B",
        "context": 262000,
        "note": "480B MoE, best for coding"
    },
    "trinity": {
        "id": "arcee-ai/trinity-large-preview:free",
        "name": "Arcee Trinity Large",
        "context": 131000,
        "note": "#27 in Finance, 400B MoE"
    },
}

DEFAULT_MODEL = "nemotron"  # Best for finance tasks


def get_llm(
    model_name: str = DEFAULT_MODEL,
    temperature: float = 0.1,
    max_tokens: Optional[int] = None,
    api_key: Optional[str] = None
) -> ChatOpenAI:
    """
    Get an LLM instance via OpenRouter.
    
    Args:
        model_name: Key from FREE_MODELS or full model ID
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens to generate
        api_key: Optional OpenRouter API key for higher limits
                  
    Returns:
        ChatOpenAI instance configured for OpenRouter
        
    Note:
        Free models work without API key. Optional OPENROUTER_API_KEY
        in .env for higher rate limits.
    """
    # Look up model ID from FREE_MODELS or use as-is if not found
    model_id = FREE_MODELS.get(model_name, {}).get("id", model_name)
    
    # Get API key - OpenRouter works without key for free models
    # but recommends one for higher limits
    openrouter_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
    
    # Configure ChatOpenAI with OpenRouter
    llm = ChatOpenAI(
        model=model_id,
        temperature=temperature,
        max_tokens=max_tokens or 4096,
        openai_api_key=openrouter_key if openrouter_key else "sk-or-none",
        openai_api_base=OPENROUTER_BASE_URL,
        # OpenRouter-specific headers (optional but recommended)
        model_kwargs={
            "extra_headers": {
                "HTTP-Referer": "https://casualhero.zo.space/ktb-fund-manager",
                "X-Title": "KTB Fund Manager"
            }
        } if openrouter_key else {}
    )
    
    return llm


def list_free_models() -> Dict[str, Any]:
    """List all available free models with their details."""
    return FREE_MODELS


def test_connection(model: str = DEFAULT_MODEL) -> bool:
    """
    Test if OpenRouter connection works.
    
    Returns True if successful, False otherwise.
    """
    try:
        llm = get_llm(model_name=model)
        # Simple test message
        response = llm.invoke("Say hello")
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False


class LLMResponse:
    """Wrapper for LLM responses with additional metadata."""
    
    def __init__(
        self,
        content: str,
        model: str,
        usage: Optional[Dict] = None,
        reasoning: Optional[str] = None
    ):
        self.content = content
        self.model = model
        self.usage = usage or {}
        self.reasoning = reasoning
        
    def __str__(self) -> str:
        return self.content


class FinancialLLM:
    """
    High-level interface for financial analysis LLM calls.
    
    Handles agent-specific configurations and prompt optimization.
    """
    
    def __init__(self, agent_name: str, model: str = DEFAULT_MODEL):
        self.agent_name = agent_name
        self.model = model
        self.llm = get_llm(model_name=model, temperature=0.1)
        
    def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Run a financial analysis prompt.
        
        Args:
            prompt: The main prompt content
            system_prompt: Optional system instructions
            
        Returns:
            String response content
        """
        if system_prompt:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            response = self.llm.invoke(messages)
        else:
            response = self.llm.invoke(prompt)
            
        return response.content


def get_agent_llm(agent_name: str, model_preference: str = DEFAULT_MODEL) -> FinancialLLM:
    """
    Get a FinancialLLM instance configured for a specific agent.
    
    Args:
        agent_name: Name of the agent (e.g., "warren_buffett")
        model_preference: Preferred model key from FREE_MODELS
        
    Returns:
        FinancialLLM instance
    """
    return FinancialLLM(agent_name, model_preference)
