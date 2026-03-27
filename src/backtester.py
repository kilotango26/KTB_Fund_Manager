"""
KTB Fund Manager - Backtester

Backtesting framework for evaluating trading strategies.
"""

import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.main import run_hedge_fund

init(autoreset=True)
console = Console()


def run_backtest(
    tickers: list[str],
    start_date: str,
    end_date: str,
    initial_cash: float = 100000.0,
    selected_analysts: list[str] = None,
    model_name: str = "gpt-4o",
    model_provider: str = "OpenAI",
):
    """Run a backtest simulation."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]KTB Fund Manager - Backtest Results[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    # Initialize portfolio
    portfolio = {
        "cash": initial_cash,
        "margin_requirement": 0.0,
        "margin_used": 0.0,
        "positions": {
            ticker: {
                "long": 0,
                "short": 0,
                "long_cost_basis": 0.0,
                "short_cost_basis": 0.0,
                "short_margin_used": 0.0,
            }
            for ticker in tickers
        },
        "realized_gains": {
            ticker: {"long": 0.0, "short": 0.0}
            for ticker in tickers
        },
    }
    
    # Run the hedge fund simulation
    result = run_hedge_fund(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        portfolio=portfolio,
        show_reasoning=False,
        selected_analysts=selected_analysts,
        model_name=model_name,
        model_provider=model_provider,
    )
    
    # Display backtest summary
    console.print("[bold green]Backtest Complete![/bold green]")
    console.print()
    
    # Show decisions
    decisions = result.get("decisions", {})
    if decisions:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Ticker", style="cyan")
        table.add_column("Action", style="green")
        table.add_column("Confidence", style="blue")
        
        for ticker, decision in decisions.items():
            if isinstance(decision, dict):
                table.add_row(
                    ticker,
                    decision.get("action", "HOLD"),
                    str(decision.get("confidence", "N/A"))
                )
        
        console.print(table)
    
    return result


def main():
    """Main entry point for backtester."""
    parser = argparse.ArgumentParser(
        description="KTB Fund Manager - Backtest Trading Strategies"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        required=True,
        help="Comma-separated list of stock tickers (e.g., AAPL,MSFT,NVDA)",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=(datetime.now() - relativedelta(years=1)).strftime("%Y-%m-%d"),
        help="Start date for backtest (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date for backtest (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--initial-cash",
        type=float,
        default=100000.0,
        help="Initial cash position (default: 100000)",
    )
    parser.add_argument(
        "--analysts",
        type=str,
        default=None,
        help="Comma-separated list of analysts to use",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="Model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="OpenAI",
        choices=["OpenAI", "Anthropic"],
        help="Model provider (default: OpenAI)",
    )
    
    args = parser.parse_args()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Parse analysts
    selected_analysts = None
    if args.analysts:
        selected_analysts = [a.strip() for a in args.analysts.split(",")]
    
    print(f"\n{Fore.CYAN}KTB Fund Manager - Backtest{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Initial Cash: ${args.initial_cash:,.2f}\n")
    
    # Run backtest
    run_backtest(
        tickers=tickers,
        start_date=args.start_date,
        end_date=args.end_date,
        initial_cash=args.initial_cash,
        selected_analysts=selected_analysts,
        model_name=args.model,
        model_provider=args.provider,
    )
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
