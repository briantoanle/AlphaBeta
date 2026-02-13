from services.engines.recommendation_engine import RecommendationEngine

def test_recommendation_engine():
    engine = RecommendationEngine()

    # Case 1: High stress, high equity
    recs = engine.generate_recommendations(
        macro_score=85.0,
        regime="Risk-off",
        exposure={"equity": 0.8, "rates": -0.2, "vol": -0.1},
        risk_tolerance=5.0
    )
    assert any(r["action"] == "Reduce Risk" for r in recs)
    print(f"Risk-off recs: {recs[0]['title']}")

    # Case 2: Low stress, low equity
    recs = engine.generate_recommendations(
        macro_score=20.0,
        regime="Risk-on",
        exposure={"equity": 0.2, "rates": 0.0, "vol": 0.0},
        risk_tolerance=8.0
    )
    assert any(r["action"] == "Increase Exposure" for r in recs)
    print(f"Risk-on recs: {recs[0]['title']}")

    print("RecommendationEngine Test OK")

if __name__ == "__main__":
    test_recommendation_engine()
