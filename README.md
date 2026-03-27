# KTB Fund Manager

An AI-powered hedge fund simulation system for educational purposes. 

**Now powered by OpenRouter free models** - zero cost to start, no API key required!

## Overview

KTB Fund Manager employs a team of AI agents, each embodying different investment philosophies and analytical approaches. This implementation uses **free/open-source models** via OpenRouter - no paid API keys required to get started.

## Why OpenRouter?

| Provider | Cost | Free Tier | Best For |
|----------|------|-----------|----------|
| **OpenRouter** | **$0** | 15+ free models | Multi-model access, no card needed |
| Groq | $0 | 14.4K req/day | Fast inference |
| Together AI | $0 with limits | Various | Open-source models |
| OpenAI/Anthropic | $$$ | None | Proprietary models |

**Key Benefits:**
- No credit card required
- Access to 15+ free models including Llama 3.3 70B, gpt-oss-120b, NVIDIA Nemotron
- Single API for multiple providers
- Easily switch between models

## Recommended Free Models

### For Financial Analysis:
1. **NVIDIA Nemotron 3 Super** (`nvidia/nemotron-3-super-120b-a12b:free`)
   - 120B parameters, 262K context
   - Ranked #24 in Finance benchmarks
   - Best for: Complex financial reasoning

2. **Llama 3.3 70B** (`meta-llama/llama-3.3-70b-instruct:free`)
   - 70B parameters, 66K context  
   - Strong general reasoning
   - Best for: Balanced performance

3. **Arcee Trinity** (`arcee-ai/trinity-large-preview:free`)
   - 400B MoE parameters, 131K context
   - Ranked #27 in Finance benchmarks
   - Best for: Agent-specific tasks

### For Agent Tasks:
4. **Qwen3 Coder** (`qwen/qwen3-coder:free`)
   - 480B MoE parameters, 35B active, 262K context
   - Best for: JSON generation, structured outputs

5. **gpt-oss-120b** (`openai/gpt-oss-120b:free`)
   - 117B parameters, 131K context
   - Best for: Configurable reasoning depth

## Investment Strategy Agents

### Legendary Investor Agents
- **Warren Buffett Agent** - Value investing
- **Charlie Munger Agent** - Mental models  
- **Ben Graham Agent** - Deep value investing
- **Peter Lynch Agent** - Growth investing
- **Cathie Wood Agent** - Disruptive innovation
- **Michael Burry Agent** - Contrarian deep value
- **Stanley Druckenmiller Agent** - Macro investing

### Analysis Agents
- **Fundamentals Agent** - Financial statement analysis
- **Technical Agent** - Price action and indicators
- **Sentiment Agent** - Market sentiment
- **Valuation Agent** - Intrinsic value calculations

### Management Agents
- **Risk Manager** - Position sizing and risk control
- **Portfolio Manager** - Final trading decisions

## Installation

### Prerequisites
- Python 3.11+
- Poetry

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kilotango26/KTB_Fund_Manager.git
cd KTB_Fund_Manager
```

2. Install dependencies:
```bash
poetry install
```

3. (Optional) Set up OpenRouter API key:
```bash
cp .env.example .env
# Edit .env and add your OpenRouter key (free at openrouter.ai/keys)
```

**Note:** Free models work WITHOUT an API key! Adding one increases rate limits.

## Usage

### Quick Start (No API Key Required)

```bash
poetry run python src/main.py --ticker AAPL,MSFT,NVDA
```

### Select a Model

```bash
DEFAULT_MODEL=llama poetry run python src/main.py --ticker AAPL
```

## Configuration

### Environment Variables (.env)

```bash
# Optional: OpenRouter API key for higher limits
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Default model
DEFAULT_MODEL=nemotron
```

## Model Selection Guide

| Use Case | Model | Why |
|----------|-------|-----|
| General analysis | nemotron | #24 in Finance |
| Complex reasoning | gpt_oss | OpenAI's model |
| JSON generation | qwen | Optimized for code |
| Long documents | trinity | 512K context |
| Fast inference | llama | Well-balanced |

## Disclaimer

**This project is for educational and research purposes only.**

- Not intended for real trading
- No warranties or guarantees
- Past performance does not predict future results

## Acknowledgments

- Inspired by ai-hedge-fund by virattt
- Powered by OpenRouter for free model access
- Built with LangGraph for agent workflows
