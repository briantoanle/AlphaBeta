import pandas as pd
from typing import Dict, List, Tuple

class MacroStressEngine:
    def __init__(self, weights: Dict[str, float] = None):
        # Default weights for categories
        self.weights = weights or {
            "behavioral": 0.2,
            "labor": 0.25,
            "market": 0.35,
            "credit": 0.2
        }

    def normalize_signals(self, signals: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Applies z-score normalization to each signal."""
        normalized_df = pd.DataFrame()

        for name, df in signals.items():
            if df.empty:
                continue

            # Use rolling z-score to avoid lookahead bias and handle non-stationarity
            # Window of 90 days for normalization
            series = df["value"]
            mean = series.rolling(window=90, min_periods=10).mean()
            std = series.rolling(window=90, min_periods=10).std()
            z_score = (series - mean) / (std + 1e-6)

            # Clip outliers
            z_score = z_score.clip(-3, 3)
            normalized_df[name] = z_score

        return normalized_df.ffill().dropna()

    def compute_stress_score(self, normalized_df: pd.DataFrame, signal_categories: Dict[str, str]) -> pd.DataFrame:
        """
        Computes the composite Macro Stress Score (0-100).
        signal_categories: maps signal name to category (behavioral, labor, market, credit)
        """
        if normalized_df.empty:
            return pd.DataFrame()

        # Group signals by category and compute category scores
        category_scores = pd.DataFrame(index=normalized_df.index)

        for category, weight in self.weights.items():
            cat_signals = [s for s, c in signal_categories.items() if c == category and s in normalized_df.columns]
            if cat_signals:
                # Average z-scores in category, then map to 0-1
                # A z-score of 0 is "normal" (50), +2 is "high stress" (100), -2 is "low stress" (0)
                cat_avg = normalized_df[cat_signals].mean(axis=1)
                category_scores[category] = cat_avg
            else:
                category_scores[category] = 0.0

        # Weighted sum of category z-scores
        composite_z = sum(category_scores[cat] * self.weights[cat] for cat in self.weights)

        # Map z-score to 0-100 scale using sigmoid-like function or linear mapping
        # Let's use a simple linear map: z=-2 -> 0, z=0 -> 50, z=2 -> 100
        stress_score = (composite_z * 25) + 50
        stress_score = stress_score.clip(0, 100)

        res = pd.DataFrame({"score": stress_score}, index=normalized_df.index)

        # Add category contributions for attribution
        for cat in self.weights:
            res[f"contrib_{cat}"] = category_scores[cat]

        return res

    def detect_regime(self, score: float) -> str:
        """
        Categorizes the stress score into Risk-off, Risk-on, or Neutral regimes.

        Thresholds:
        - > 70: Risk-off (High Stress)
        - < 40: Risk-on (Low Stress)
        - 40-70: Neutral
        """
        if score > 70:
            return "Risk-off"
        elif score < 40:
            return "Risk-on"
        return "Neutral"

    def get_attribution(self, normalized_row: pd.Series, signal_categories: Dict[str, str]) -> List[Dict]:
        """Returns top drivers of the stress score for a given point in time."""
        drivers = []
        for signal, z_val in normalized_row.items():
            category = signal_categories.get(signal, "unknown")
            impact = z_val * self.weights.get(category, 0.1)
            drivers.append({
                "signal": signal,
                "category": category,
                "z_score": round(float(z_val), 2),
                "impact": round(float(impact), 2)
            })

        # Sort by absolute impact
        drivers.sort(key=lambda x: abs(x["impact"]), reverse=True)
        return drivers[:5]
