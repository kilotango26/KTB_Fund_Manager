"""
KTB Fund Manager - Main Entry Point

An AI-powered hedge fund simulation system that uses multiple agents
to make trading decisions based on different investment strategies.
"""

import sys
import argparse
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph
from colorama import Fore, Style, init

from src.agents.portfolio_manager import portfolio_management_agent
from src.agents.risk_manager import risk_management_agent
from src.graph.state import AgentState
from src.utils.display import print_trading_output
from src.utils.analysts import ANALYST_ORDER, get_analyst_nodes
from src.utils.progress import progress

# Load environment variables
load_dotenv()
init(autoreset=True)


def parse_hedge_fund_response(response):
    """Parse the hedge fund agent response."""
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}\nResponse: {repr(response)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def create_workflow(selected_analysts=None):
    """Create the workflow with selected analysts."""
    workflow = StateGraph(AgentState)
    
    # Add start node
    workflow.add_node("start_node", lambda state: state)
    
    # Get analyst nodes
    analyst_nodes = get_analyst_nodes()
    
    # Default to all analysts if none selected
    if selected_analysts is None:
        selected_analysts = list(analyst_nodes.keys())
    
    # Add analyst nodes
    for analyst_key in selected_analysts:
        node_name, node_func = analyst_nodes[analyst_key]
        workflow.add_node(node_name, node_func)
        workflow.add_edge("start_node", node_name)
    
    # Add risk and portfolio management
    workflow.add_node("risk_management_agent", risk_management_agent)
    workflow.add_node("portfolio_manager", portfolio_management_agent)
    
    # Connect analysts to risk management
    for analyst_key in selected_analysts:
        node_name = analyst_nodes[analyst_key][0]
        workflow.add_edge(node_name, "risk_management_agent")
    
    workflow.add_edge("risk_management_agent", "portfolio_manager")
    workflow.add_edge("portfolio_manager", END)
    workflow.set_entry_point("start_node")
    
    return workflow


def run_hedge_fund(
    tickers: list[str],
    start_date: str,
    end_date: str,
    portfolio: dict,
    show_reasoning: bool = False,
    selected_analysts: list[str] = None,
    model_name: str = "gpt-4o",
    model_provider: str = "OpenAI",
):
    """Run the hedge fund simulation."""
    progress.start()
    
    try:
        # Build and compile workflow
        workflow = create_workflow(selected_analysts)
        agent = workflow.compile()
        
        # Run the agent
        final_state = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="Make trading decisions based on the provided data.",
                    )
                ],
                "data": {
                    "tickers": tickers,
                    "portfolio": portfolio,
                    "start_date": start_date,
                    "end_date": end_date,
                    "analyst_signals": {},
                },
                "metadata": {
                    "show_reasoning": show_reasoning,
                    "model_name": model_name,
                    "model_provider": model_provider,
                },
            },
        )
        
        return {
            "decisions": parse_hedge_fund_response(final_state["messages"][-1].content),
            "analyst_signals": final_state["data"]["analyst_signals"],
        }
    finally:
        progress.stop()


def parse_cli_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="KTB Fund Manager - AI Hedge Fund Simulation"
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
        default=(datetime.now() - relativedelta(months=3)).strftime("%Y-%m-%d"),
        help="Start date for analysis (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="End date for analysis (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--initial-cash",
        type=float,
        default=100000.0,
        help="Initial cash position (default: 100000)",
    )
    parser.add_argument(
        "--margin-requirement",
        type=float,
        default=0.0,
        help="Margin requirement (default: 0)",
    )
    parser.add_argument(
        "--analysts",
        type=str,
        default=None,
        help="Comma-separated list of analysts to use (default: all)",
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
    parser.add_argument(
        "--show-reasoning",
        action="store_true",
        help="Show reasoning from each analyst",
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_cli_args()
    
    # Parse tickers
    tickers = [t.strip().upper() for t in args.ticker.split(",")]
    
    # Parse analysts
    selected_analysts = None
    if args.analysts:
        selected_analysts = [a.strip() for a in args.analysts.split(",")]
    
    # Create portfolio
    portfolio = {
        "cash": args.initial_cash,
        "margin_requirement": args.margin_requirement,
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
    
    print(f"\n{Fore.CYAN}KTB Fund Manager - AI Hedge Fund Simulation{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Period: {args.start_date} to {args.end_date}")
    print(f"Initial Cash: ${args.initial_cash:,.2f}")
    print(f"Model: {args.model} ({args.provider})\n")
    
    # Run the hedge fund
    result = run_hedge_fund(
        tickers=tickers,
        start_date=args.start_date,
        end_date=args.end_date,
        portfolio=portfolio,
        show_reasoning=args.show_reasoning,
        selected_analysts=selected_analysts,
        model_name=args.model,
        model_provider=args.provider,
    )
    
    # Display results
    print_trading_output(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
