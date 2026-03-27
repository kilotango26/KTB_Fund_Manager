# KTB Fund Manager

An AI-powered hedge fund simulation system for educational purposes. This project explores the use of AI agents to make trading decisions based on multiple investment strategies.

## Overview

KTB Fund Manager employs a team of AI agents, each embodying different investment philosophies and analytical approaches:

### Investment Strategy Agents
- **Warren Buffett Agent** - Value investing: wonderful companies at fair prices
- **Charlie Munger Agent** - Mental models and wonderful businesses
- **Ben Graham Agent** - Deep value investing with margin of safety
- **Peter Lynch Agent** - Growth investing in understandable businesses
- **Cathie Wood Agent** - Disruptive innovation and high-growth themes
- **Michael Burry Agent** - Contrarian deep value opportunities
- **Stanley Druckenmiller Agent** - Macro-driven asymmetric opportunities

### Analysis Agents
- **Fundamentals Agent** - Financial statement analysis
- **Technical Agent** - Price action and technical indicators
- **Sentiment Agent** - Market sentiment and news analysis
- **Valuation Agent** - Intrinsic value calculations

### Management Agents
- **Risk Manager** - Position sizing and risk control
- **Portfolio Manager** - Final trading decisions and execution

## Disclaimer

**This project is for educational and research purposes only.**

- Not intended for real trading or investment
- No investment advice or guarantees provided
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions
- Past performance does not indicate future results

## Installation

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kilotango26/KTB_Fund_Manager.git
cd KTB_Fund_Manager
```

2. Install dependencies with Poetry:
```bash
poetry install
```

Or with pip:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Running the Hedge Fund

Basic usage:
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

With date range:
```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA --start-date 2024-01-01 --end-date 2024-03-01
```

Select specific analysts:
```bash
poetry run python src/main.py --ticker AAPL --analysts warren_buffett,ben_graham,technicals
```

### Running the Backtester

```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

## Project Structure

```
KTB_Fund_Manager/
├── src/
│   ├── agents/           # AI agent implementations
│   ├── utils/           # Utility functions
│   ├── data/            # Data fetching and caching
│   ├── graph/           # LangGraph workflow definitions
│   ├── cli/             # Command-line interface
│   ├── backtesting/     # Backtesting framework
│   ├── main.py          # Main entry point
│   └── backtester.py    # Backtesting entry point
├── tests/               # Test suite
├── app/                 # Web application (future)
├── pyproject.toml       # Project dependencies
└── README.md
```

## Configuration

### API Keys Required

1. **OpenAI API Key** - For GPT-4/GPT-4o models
2. **Anthropic API Key** - For Claude models
3. **Financial Datasets API Key** - For market data

Set these in your `.env` file.

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black src/
poetry run isort src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Inspired by the [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) project by virattt.
