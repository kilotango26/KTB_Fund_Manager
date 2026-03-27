# KTB Fund Manager - Three Novel Feature Proposals

## Current State
- ✅ 8 AI agents (Buffett, Graham, Munger, Lynch + technicals, fundamentals, sentiment, valuation)
- ✅ Alpha Vantage integration for real market data
- ✅ Zo.space UI for web-based backtesting
- ✅ OpenRouter free LLM models (Nemotron, Llama 3.3, etc.)
- ✅ Vote-based portfolio aggregation

---

## 🚀 FEATURE 1: Agent Consensus & Confidence Scoring

### The Problem
Currently agents vote independently. There's no insight into **why** agents disagree or how confident the collective decision is.

### The Solution
Implement a "Wisdom of the Crowds" algorithm:

```python
class ConsensusEngine:
    """
    Calculates:
    - Divergence score (how much agents disagree)
    - Confidence interval (statistical bounds)
    - Conviction weight (high-confidence agents get more say)
    - Confidence decay (older signals matter less)
    """
    
    def calculate(self, signals):
        # Agent types have different weightings
        value_weight = 0.4   # Buffett, Graham, Munger
        growth_weight = 0.2  # Lynch
        quant_weight = 0.2   # Technicals, Fundamentals, Valuation
        sentiment_weight = 0.2  # Sentiment
        
        # Weighted voting ensemble
        weighted_vote = sum(s.confidence * s.weight for s in signals)
        
        # Divergence: std dev of confidence across agents
        divergence = np.std([s.confidence for s in signals])
        
        # If divergence > 30, flag for human review
        if divergence > 30:
            return Flag.FOR_REVIEW
        
        return weighted_vote
```

### Implementation
- Add `ConfidenceAnalyzer` class to aggregate
- UI shows "Divergence Warning" when agents strongly disagree
- Generate PDF report explaining consensus logic

### Value
- Reduces blind spot errors
- Surfaces edge cases worth human attention
- Explains **why** the fund is making a decision

---

## 🚀 FEATURE 2: Live Paper Trading Execution

### The Problem
Backtests are hypothetical. The real value is seeing if your "AI fund" can actually make money.

### The Solution
Integrate with Alpaca Markets (free paper trading API) to execute trades:

```python
class PaperTradingManager:
    """
    Paper trading via Alpaca Markets:
    - Free account, zero real money
    - Execute BUY/SELL/HOLD decisions automatically
    - Track PnL in real-time
    - Compare AI fund vs S&P 500 benchmark
    """
    
    def execute_portfolio_rebalance(self, decisions):
        # Get current positions
        positions = alpaca.list_positions()
        
        # Calculate new allocations
        for ticker, decision in decisions.items():
            if decision.action == "BUY":
                target = portfolio_value * decision.position_size / 100
                current = positions.get(ticker, 0).market_value
                delta = target - current
                if delta > 0:
                    alpaca.submit_order(
                        symbol=ticker,
                        notional=delta,
                        side="buy",
                        time_in_force="day"
                    )
            elif decision.action == "SELL":
                # Close position
                alpaca.close_position(ticker)
```

### Implementation
1. Add `src/broker/alpaca.py` integration
2. Run scheduled rebalancing (daily/weekly)
3. Real-time dashboard showing:
   - Current PnL
   - Alpha vs S&P 500
   - Position attribution (which agents contributed most gain)

### Value
- **Real validation** - does it actually work?
- Track which agents perform best *live*
- Build track record before risking real capital

---

## 🚀 FEATURE 3: Adversarial Agent System ("Red Team")

### The Problem
Confirmation bias. All agents tend to look for bullish signals in stocks you've selected. No one challenges the thesis.

### The Solution
Deploy **contrarian agents** specifically designed to poke holes in the bull case:

```python
class AdversarialAgent:
    """
    The "Bear Case Builder":
    - Mandated to find reasons NOT to buy
    - Uses inversion: "How could this investment fail?"
    - Searches for: accounting red flags, industry headwinds, competition, regulatory risks
    
    Agents:
    1. ShortSellerBot - Identifies weakness catalysts
    2. CompetitionAnalyzer - Maps competitive threats  
    3. MacroRiskBot - Exposes sector/business model vulnerabilities
    4. ValuationSkeptic - Stress-tests optimistic growth assumptions
    """
    
    def generate_bear_case(self, ticker, bullish_signals):
        """
        Given all the reasons other agents are bullish,
        build the strongest possible bear case.
        """
        prompt = f"""
        The following {num_bullish_agents} investing experts recommend BUYING {ticker}:
        {bullish_signals}
        
        Your job is to play devil's advocate.  
        Identify:
        1. What could turn these positives into negatives?
        2. What aren't the bulls seeing?
        3. What are the 3 most likely failure scenarios?
        4. What valuation/assumptions are baked in that might be wrong?
        
        Be ruthless. Your credibility depends on finding real risks.
        """
        
        return llm.analyze(prompt)
```

### Implementation
- Add 4 adversarial agents to the mix
- Require "bull confidence" - "bear concerns" = final conviction
theta = 1.5  # More weight to bear concerns
- UI shows "Bear Case" alongside "Bull Case" for each ticker

### Value
- Prevents groupthink
- Surface risks before they become losses  
- Mimics how top hedge funds operate (always have someone arguing the opposite)
- Builds intellectual honesty in the system

---

## Implementation Priority

1. **Alpha Vantage + All Agents** ✅ DONE
2. **Consensus Engine** - 2 weeks
3. **Paper Trading** - 3 weeks  
4. **Adversarial System** - 3 weeks

## Expected Impact

- **Feature 1**: ~15-20% reduction in false-positive BUY signals
- **Feature 2**: Real track record + learning from live data
- **Feature 3**: ~30% improvement in identifying major loss cases early

Combined: Fundamentally changes this from a "backtest toy" to a professional-grade decision support system.
