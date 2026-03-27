#!/usr/bin/env python3
"""
KTB Fund Manager - Main Entry Point

An AI-powered hedge fund simulation using free OpenRouter models.
No API key required to start - test immediately with free tier.
"""

import sys
import argparse
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from colorama import Fore, Style, init

from src.utils.llm import list_free_models, DEFAULT_MODEL
from src.utils.display import print_trading_output

# Load environment variables
load_dotenv()
init(autoreset=True)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="KTB Fund Manager - AI Hedge Fund Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (free, no API key needed)
  poetry run python src/main.py --ticker AAPL,MSFT,NVDA
  
  # Use specific model
  DEFAULT_MODEL=llama poetry run python src/main.py --ticker AAPL
  
  # Full options
  poetry run python src/main.py --ticker AAPL --start-date 2024-01-01 --end-date 2024-12-31
        """
    )
    
    parser.add_argument(
        "--ticker", "-t",
        type=str,
        required=True,
        help="Comma-separated stock tickers (e.g., AAPL,MSFT,NVDA)"
    )
    
    parser.add_argument(
        "--start-date", "-s",
        type=str,
        default=(datetime.now() - relativedelta(months=3)).strftime("%Y-%m-%d"),
        help="Start date for analysis (YYYY-MM-DD). Default: 3 months ago"
    )
    
    parser.add_argument(
        "--end-date", "-e",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date for analysis (YYYY-MM-DD). Default: today"
    )
    
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=os.getenv("DEFAULT_MODEL", DEFAULT_MODEL),
        choices=["nemotron", "llama", "gpt_oss", "qwen", "trinity"],
        help="LLM model to use (free tier available for all). Default: nemotron"
    )
    
    parser.add_argument(
        "--analysts", "-a",
        type=str,
        default="all",
        help='Analysts to run (comma-separated). Options: warren_buffett,charlie_munger,ben_graham,all. Default: all'
    )
    
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all available free models and exit"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test OpenRouter connection and exit"
    )
    
    return parser.parse_args()


def run_hedge_fund(tickers, start_date, end_date, model, analysts="all"):
    """
    Run the hedge fund simulation.
    
    This is a simplified version for testing OpenRouter integration.
    Full LangGraph implementation can be enabled later.
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"KTB Fund Manager - AI Hedge Fund Simulation")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    print(f"Using model: {Fore.GREEN}{model}{Style.RESET_ALL}")
    print(f"Tickers: {Fore.YELLOW}{', '.join(tickers)}{Style.RESET_ALL}")
    print(f"Period: {start_date} to {end_date}")
    print(f"Analysts: {analysts}")
    print()
    
    # Simulated results for now
    print(f"{Fore.YELLOW}Note: Running with mock data for development.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Install yfinance for real market data.{Style.RESET_ALL}\n")
    
    results = {
        "decisions": {},
        "analyst_signals": {}
    }
    
    for ticker in tickers:
        results["decisions"][ticker] = {
            "action": "HOLD",
            "confidence": 50,
            "reasoning": "Development mode - real analysis requires yfinance integration",
            "price": "N/A"
        }
    
    print_trading_output(results)
    
    return results


def main():
    """Main entry point."""
    args = parse_args()
    
    # Handle special commands
    if args.list_models:
        print(f"\n{Fore.CYAN}Available Free Models on OpenRouter:{Style.RESET_ALL}\n")
        print("-" * 70)
        models = list_free_models()
        for key, info in models.items():
            print(f"\n{Fore.GREEN}{key}{Style.RESET_ALL}")
            print(f"  Name: {info['name']}")
            print(f"  Context: {info['context']:,} tokens")
            print(f"  Note: {info['note']}")
        print(f"\n{Fore.YELLOW}No API key required for free models!{Style.RESET_ALL}\n")
        return 0
    
    if args.test:
        print(f"\n{Fore.CYAN}Testing OpenRouter connection...{Style.RESET_ALL}\n")
        from src.utils.llm import test_connection
        
        model = args.model
        print(f"Testing with model: {model}")
        
        if test_connection(model):
            print(f"\n{Fore.GREEN}SUCCESS! OpenRouter is working.{Style.RESET_ALL}")
            api_key = os.getenv("OPENROUTER_API_KEY", "")
            if api_key:
                print(f"{Fore.GREEN}API key detected - higher rate limits enabled.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No API key - using free tier (may have rate limits).{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Get free key: https://openrouter.ai/keys{Style.RESET_ALL}")
            return 0
        else:
            print(f"\n{Fore.RED}FAILED. Check internet connection.{Style.RESET_ALL}")
            return 1
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Print header
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"KTB Fund Manager - AI Hedge Fund Simulation")
    print(f"{'='*60}{Style.RESET_ALL}\n")
    
    print(f"Model: {Fore.GREEN}{args.model}{Style.RESET_ALL}")
    print(f"Tickers: {Fore.YELLOW}{', '.join(tickers)}{Style.RESET_ALL}")
    print()
    
    # Run simulation
    try:
        results = run_hedge_fund(
            tickers=tickers,
            start_date=args.start_date,
            end_date=args.end_date,
            model=args.model,
            analysts=args.analysts
        )
        return 0
    except Exception as e:
        print(f"\n{Fore.RED}Error running hedge fund: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
