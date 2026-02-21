import numpy as np
from typing import List, Dict

class PortfolioRiskEngine:
    def __init__(self):
        # Basic factor sensitivities (beta to proxies)
        # In a real app, these would be derived from regression
        self.factor_betas = {
            "SPY": {"equity": 1.0, "rates": -0.2, "vol": -0.5},
            "TLT": {"equity": -0.1, "rates": -1.0, "vol": 0.2},
            "GLD": {"equity": 0.1, "rates": -0.1, "vol": 0.3},
            "USO": {"equity": 0.4, "rates": 0.2, "vol": -0.1},
            "HYG": {"equity": 0.6, "rates": -0.4, "vol": -0.3},
            "CASH": {"equity": 0.0, "rates": 0.0, "vol": 0.0}
        }

    def compute_exposure(self, holdings: List[Dict]) -> Dict[str, float]:
        """
        holdings: [{"symbol": "SPY", "weight": 0.6}, ...]
        """
        exposure = {"equity": 0.0, "rates": 0.0, "vol": 0.0}

        for holding in holdings:
            symbol = holding["symbol"]
            weight = holding["weight"]

            betas = self.factor_betas.get(symbol, self.factor_betas["SPY"]) # default to SPY beta
            for factor, beta in betas.items():
                exposure[factor] += beta * weight

        return exposure

    def run_stress_test(self, holdings: List[Dict], scenario: str) -> Dict:
        """
        scenario: 'rates_spike', 'oil_shock', 'vol_spike', 'recession'
        """
        scenarios = {
            "rates_spike": {"equity": -0.1, "rates": -0.15, "vol": 0.05},
            "oil_shock": {"equity": -0.05, "rates": 0.02, "vol": 0.1},
            "vol_spike": {"equity": -0.15, "rates": 0.05, "vol": -0.2}, # vol factor is short-vol usually
            "recession": {"equity": -0.25, "rates": 0.1, "vol": 0.2}
        }

        shocks = scenarios.get(scenario, {"equity": 0, "rates": 0, "vol": 0})
        exposure = self.compute_exposure(holdings)

        expected_loss = sum(exposure[f] * shocks[f] for f in shocks)

        return {
            "scenario": scenario,
            "expected_return": round(expected_loss, 4),
            "impact": "High" if expected_loss < -0.1 else "Medium" if expected_loss < -0.05 else "Low"
        }

    def compute_fragility_score(self, holdings: List[Dict]) -> float:
        """Computes a 0-100 fragility score based on concentration and exposure."""
        if not holdings: return 0.0

        # 1. Concentration (HHI)
        weights = [h["weight"] for h in holdings]
        hhi = sum(w**2 for w in weights) # 0 to 1

        # 2. Beta exposure
        exposure = self.compute_exposure(holdings)
        avg_beta = abs(exposure["equity"]) + abs(exposure["rates"]) + abs(exposure["vol"])

        # Composite score
        score = (hhi * 50) + (min(avg_beta, 2.0) / 2.0 * 50)
        return min(round(score, 2), 100.0)

    def monte_carlo_drawdown(self, holdings: List[Dict], iterations: int = 1000) -> Dict:
        """Simplified Monte Carlo for drawdown distribution."""
        exposure = self.compute_exposure(holdings)
        # Assumed daily vol for factors
        factor_vols = {"equity": 0.012, "rates": 0.008, "vol": 0.02}

        # Combined portfolio vol (simplified, ignoring correlation)
        port_vol = np.sqrt(sum((exposure[f] * factor_vols[f])**2 for f in factor_vols))

        # Simulate 252 days
        drawdowns = []
        for _ in range(iterations):
            returns = np.random.normal(0, port_vol, 252)
            cum_returns = np.cumsum(returns)
            peak = np.maximum.accumulate(cum_returns)
            drawdown = (cum_returns - peak).min()
            drawdowns.append(drawdown)

        return {
            "expected_annual_vol": round(port_vol * np.sqrt(252), 4),
            "worst_case_drawdown": round(float(np.percentile(drawdowns, 5)), 4),
            "median_drawdown": round(float(np.median(drawdowns)), 4)
        }
