#!/usr/bin/env python3
"""
Test script for KTB Fund Manager OpenRouter integration.

Verifies that free models work without API key, and tests basic
LLM connectivity.
"""

import sys
from src.utils.llm import get_llm, list_free_models, test_connection, DEFAULT_MODEL

def main():
    print("=" * 60)
    print("KTB Fund Manager - OpenRouter Test")
    print("=" * 60)
    print()
    
    # List available free models
    print("Available Free Models:")
    print("-" * 60)
    models = list_free_models()
    for key, info in models.items():
        print(f"  {key:12} -> {info['name']}")
        print(f"                   {info['note']}")
        print(f"                   Context: {info['context']:,} tokens")
        print()
    
    # Test connection with default model (no API key)
    print("-" * 60)
    print(f"Testing connection with default model: {DEFAULT_MODEL}")
    print("(This works WITHOUT an API key for free models)")
    print("-" * 60)
    
    success = test_connection(DEFAULT_MODEL)
    
    if success:
        print("SUCCESS! OpenRouter connection working.")
        print("\nYou can now run the hedge fund:")
        print("  poetry run python src/main.py --ticker AAPL")
        return 0
    else:
        print("FAILED. Check your internet connection.")
        print("\nTroubleshooting:")
        print("1. Check internet connection")
        print("2. Verify OpenRouter is accessible: https://openrouter.ai")
        print("3. Try a different model: DEFAULT_MODEL=llama python test_openrouter.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
