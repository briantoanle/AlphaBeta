from typing import List, Dict

class RecommendationEngine:
    def generate_recommendations(self, macro_score: float, regime: str, exposure: Dict[str, float], risk_tolerance: float) -> List[Dict]:
        recommendations = []

        # 1. High Stress (Risk-off) Recommendations
        if regime == "Risk-off":
            if exposure["equity"] > 0.5:
                recommendations.append({
                    "action": "Reduce Risk",
                    "type": "Defensive",
                    "title": "Reduce High-Beta Equity Exposure",
                    "reason": f"Macro stress is high ({macro_score:.1f}). Your equity exposure ({exposure['equity']:.2f}) is elevated for a Risk-off regime.",
                    "impact": "Lowers potential drawdown by 15-20% in crash scenarios.",
                    "options": {
                        "conservative": "Move 20% of equity to Cash/Short-term Bonds.",
                        "balanced": "Move 10% of equity to defensive sectors (XLP/XLV).",
                        "aggressive": "Purchase SPY put options as a tail-hedge."
                    },
                    "risks": "Potential underperformance if macro stress dissipates rapidly."
                })

            if exposure["vol"] < -0.3: # short vol exposure
                recommendations.append({
                    "action": "Hedge",
                    "type": "Volatility",
                    "title": "Close Short Volatility Positions",
                    "reason": "Rising macro stress often leads to volatility spikes. Your portfolio is currently short volatility.",
                    "impact": "Protects against rapid margin expansion and liquidity shocks.",
                    "options": {
                        "conservative": "Exit all short-vol positions.",
                        "balanced": "Reduce short-vol size by 50%.",
                        "aggressive": "Buy VIX calls to offset short-vol delta."
                    },
                    "risks": "Cost of hedging (theta decay) if markets remain calm."
                })

        # 2. Low Stress (Risk-on) Recommendations
        elif regime == "Risk-on":
            if exposure["equity"] < 0.4 and risk_tolerance > 5:
                recommendations.append({
                    "action": "Increase Exposure",
                    "type": "Growth",
                    "title": "Deploy Excess Cash",
                    "reason": f"Macro conditions are favorable ({macro_score:.1f}). You have low equity exposure relative to your risk tolerance.",
                    "impact": "Captures upside momentum in a stable economic environment.",
                    "options": {
                        "conservative": "Gradually scale into SPY (2% per week).",
                        "balanced": "Allocate 10% cash to QQQ or high-growth sectors.",
                        "aggressive": "Use 1.2x leverage on broad index core."
                    },
                    "risks": "Late-cycle entry risk if regime shifts abruptly."
                })

        # 3. Always include a rebalance check
        if any(abs(v) > 0.8 for v in exposure.values()):
            recommendations.append({
                "action": "Rebalance",
                "type": "Structural",
                "title": "Extreme Factor Concentration",
                "reason": "One or more of your factor exposures is exceeding institutional safety limits (>0.8 beta).",
                "impact": "Reduces idiosyncratic risk and restores diversification.",
                "options": {
                    "standard": "Rebalance portfolio to target weights."
                },
                "risks": "Transaction costs and tax implications."
            })

        # Fallback if no specific recommendations
        if not recommendations:
            recommendations.append({
                "action": "Hold",
                "type": "Neutral",
                "title": "Maintain Current Allocation",
                "reason": "Macro signals are neutral and portfolio alignment is within healthy bounds.",
                "impact": "Minimizes turnover and tax drag.",
                "options": {"standard": "No immediate action required."},
                "risks": "Requires continued monitoring of labor and behavioral signals."
            })

        return recommendations
