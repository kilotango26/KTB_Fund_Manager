"""
Display utilities for KTB Fund Manager.

Handles output formatting and visualization of trading results.
"""

from typing import Dict, Any
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


def print_trading_output(result: Dict[str, Any]):
    """
    Print the trading output in a formatted way.
    
    Args:
        result: Dictionary containing decisions and analyst_signals
    """
    decisions = result.get("decisions", {})
    analyst_signals = result.get("analyst_signals", {})
    
    console.print()
    console.print(Panel.fit(
        "[bold cyan]KTB Fund Manager - Trading Decisions[/bold cyan]",
        box=box.DOUBLE
    ))
    console.print()
    
    # Print decisions for each ticker
    if decisions and isinstance(decisions, dict):
        for ticker, decision in decisions.items():
            if isinstance(decision, dict):
                _print_ticker_decision(ticker, decision)
    else:
        console.print("[yellow]No trading decisions generated.[/yellow]")
    
    # Print analyst signals summary
    if analyst_signals:
        _print_analyst_signals_summary(analyst_signals)


def _print_ticker_decision(ticker: str, decision: Dict[str, Any]):
    """Print the decision for a single ticker."""
    action = decision.get("action", "HOLD").upper()
    quantity = decision.get("quantity", 0)
    price = decision.get("price", "N/A")
    confidence = decision.get("confidence", "N/A")
    reasoning = decision.get("reasoning", "")
    
    # Color coding based on action
    action_color = {
        "BUY": "green",
        "SELL": "red",
        "HOLD": "yellow",
        "SHORT": "red",
        "COVER": "green",
    }.get(action, "white")
    
    console.print(Panel(
        f"[bold]{ticker}[/bold]\n"
        f"Action: [{action_color}]{action}[/{action_color}]\n"
        f"Quantity: {quantity}\n"
        f"Price: {price}\n"
        f"Confidence: {confidence}",
        title=f"[bold]{ticker}[/bold]",
        border_style=action_color
    ))
    
    if reasoning:
        console.print(f"[dim]Reasoning:[/dim] {reasoning}")
    console.print()


def _print_analyst_signals_summary(signals: Dict[str, Any]):
    """Print a summary of analyst signals."""
    if not signals:
        return
    
    console.print(Panel.fit(
        "[bold cyan]Analyst Signals Summary[/bold cyan]",
        box=box.SIMPLE
    ))
    console.print()
    
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    table.add_column("Analyst", style="cyan")
    table.add_column("Ticker", style="yellow")
    table.add_column("Signal", style="green")
    table.add_column("Confidence", style="blue")
    
    for analyst, ticker_signals in signals.items():
        if isinstance(ticker_signals, dict):
            for ticker, signal_data in ticker_signals.items():
                if isinstance(signal_data, dict):
                    table.add_row(
                        analyst.replace("_", " ").title(),
                        ticker,
                        signal_data.get("signal", "N/A"),
                        str(signal_data.get("confidence", "N/A"))
                    )
    
    console.print(table)
    console.print()
