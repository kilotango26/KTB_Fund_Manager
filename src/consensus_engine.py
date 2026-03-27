
"""
Consensus Engine - Feature 1 Implementation
"""
import math
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class ConsensusResult:
    action: str
    confidence: int
    position_size: int
    buy_votes: int
    hold_votes: int  
    sell_votes: int
    divergence_score: float
    requires_review: bool
    explanation: str

class ConsensusEngine:
    """Weighted ensemble with divergence detection."""
    
    weights = {
        "warren_buffett": 0.18,
        "charlie_munger": 0.12,
        "ben_graham": 0.10,
        "peter_lynch": 0.12,
        "fundamentals": 0.15,
        "valuation": 0.12,
        "technicals": 0.08,
        "sentiment": 0.08
    }
    
    def calculate(self, signals: Dict[str, Any]) -> ConsensusResult:
        signal_map = {"BUY": 1, "HOLD": 0, "SELL": -1}
        
        buy_votes = sum(1 for s in signals.values() if s.get("signal") == "BUY")
        sell_votes = sum(1 for s in signals.values() if s.get("signal") == "SELL")
        hold_votes = len(signals) - buy_votes - sell_votes
        
        # Weighted score
        weighted = 0.0
        total_weight = 0.0
        confidences = []
        for agent, sig in signals.items():
            w = self.weights.get(agent, 0.08)
            v = signal_map.get(sig.get("signal", "HOLD"), 0)
            c = sig.get("confidence", 50)
            weighted += v * w * (c/100)
            total_weight += w * (c/100)
            confidences.append(c)
        
        score = weighted / total_weight if total_weight else 0
        
        # Action
        if score > 0.15:
            action = "BUY"
            position = int(5 + score * 40)
        elif score < -0.15:
            action = "SELL"
            position = 0
        else:
            action = "HOLD"
            position = int(5 + abs(score) * 20)
        
        # Confidence & divergence
        avg_conf = sum(confidences) // len(confidences) if confidences else 50
        if len(confidences) > 1:
            mean = sum(confidences) / len(confidences)
            var = sum((c-mean)**2 for c in confidences) / len(confidences)
            divergence = math.sqrt(var)
        else:
            divergence = 0
        
        requires_review = divergence > 25
        
        exp = f"{action}: {buy_votes}B/{hold_votes}H/{sell_votes}S, div={divergence:.0f}"
        
        return ConsensusResult(action, min(98, avg_conf), min(25, position), 
                               buy_votes, hold_votes, sell_votes, 
                               round(divergence, 1), requires_review, exp)
