from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import datetime
from typing import List
from sqlalchemy.orm import Session

from database import get_db, engine
from models import db as db_models
from models.schemas import PortfolioBase, HoldingBase, MacroScoreResponse
from services.auth import get_current_user
from services.connectors.fred import FredConnector
from services.connectors.market import MarketConnector
from services.connectors.behavioral import BehavioralConnector
from services.engines.macro_engine import MacroStressEngine
from services.engines.portfolio_engine import PortfolioRiskEngine
from services.engines.recommendation_engine import RecommendationEngine

# Create tables if they don't exist (though Prisma should have done it)
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AURORA Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singletons
macro_engine = MacroStressEngine()
portfolio_engine = PortfolioRiskEngine()
rec_engine = RecommendationEngine()

fred = FredConnector()
market = MarketConnector()
behavioral = BehavioralConnector()

# Seed a demo user if not exists
def seed_demo_user(db: Session):
    user = db.query(db_models.User).filter(db_models.User.email == "demo@aurora.ai").first()
    if not user:
        user = db_models.User(id="demo-user-id", email="demo@aurora.ai", name="Demo User", riskLevel="Intermediate")
        db.add(user)
        db.commit()
        db.refresh(user)
        # Add a default portfolio
        portfolio = db_models.Portfolio(id="demo-portfolio-id", userId=user.id, name="Demo Portfolio", riskTolerance=5.0)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        # Add holdings
        h1 = db_models.Holding(id="h1", portfolioId=portfolio.id, symbol="SPY", weight=0.6)
        h2 = db_models.Holding(id="h2", portfolioId=portfolio.id, symbol="TLT", weight=0.3)
        h3 = db_models.Holding(id="h3", portfolioId=portfolio.id, symbol="GLD", weight=0.1)
        db.add_all([h1, h2, h3])
        db.commit()
    return user

@app.on_event("startup")
def startup_event():
    db_gen = get_db()
    db = next(db_gen)
    try:
        seed_demo_user(db)
    finally:
        db_gen.close()

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "aurora-engine"}

@app.get("/api/data/freshness")
def get_freshness(db: Session = Depends(get_db)):
    # In real app, check timestamps of raw data in DB
    return {
        "fred": (datetime.datetime.utcnow() - datetime.timedelta(hours=2)).isoformat(),
        "yfinance": datetime.datetime.utcnow().isoformat(),
        "pytrends": (datetime.datetime.utcnow() - datetime.timedelta(minutes=45)).isoformat()
    }

@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db), user: db_models.User = Depends(get_current_user)):
    macro = get_macro_score(db)
    summary = get_portfolio_summary_internal(db, user)

    alerts = []
    if macro["score"] > 60:
        alerts.append({
            "id": "1",
            "type": "MACRO_STRESS",
            "severity": "High",
            "message": f"Macro Stress Score is elevated ({macro['score']}). Consider hedging.",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

    if summary["fragility"] > 50:
        alerts.append({
            "id": "2",
            "type": "PORTFOLIO_FRAGILITY",
            "severity": "Medium",
            "message": "Portfolio fragility is above threshold. High concentration detected.",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })

    return alerts

@app.get("/api/macro/score", response_model=MacroScoreResponse)
def get_macro_score(db: Session = Depends(get_db)):
    # Try to get latest score from DB
    latest_db_score = db.query(db_models.MacroScore).order_by(db_models.MacroScore.timestamp.desc()).first()

    # If no score or older than 4 hours, recompute
    if not latest_db_score or (datetime.datetime.utcnow() - latest_db_score.timestamp).total_seconds() > 14400:
        signals = {
            "VIX": market.fetch_data("^VIX", start_date="2024-01-01"),
            "ICSA": fred.fetch_data("ICSA"),
            "recession_trends": behavioral.fetch_data("recession", start_date="2024-01-01"),
            "HYG": market.fetch_data("HYG", start_date="2024-01-01")
        }

        signal_categories = {
            "VIX": "market", "ICSA": "labor", "recession_trends": "behavioral", "HYG": "credit"
        }

        normalized = macro_engine.normalize_signals(signals)
        scores = macro_engine.compute_stress_score(normalized, signal_categories)

        if not scores.empty:
            latest_val = float(scores["score"].iloc[-1])
            regime = macro_engine.detect_regime(latest_val)
            attribution = macro_engine.get_attribution(normalized.iloc[-1], signal_categories)

            new_score = db_models.MacroScore(
                score=round(latest_val, 2),
                regime=regime,
                drivers=attribution,
                confidence="High"
            )
            db.add(new_score)
            db.commit()
            db.refresh(new_score)
            latest_db_score = new_score

    if not latest_db_score:
        return {
            "score": 50.0, "regime": "Neutral", "drivers": [],
            "timestamp": datetime.datetime.now().isoformat()
        }

    return {
        "score": latest_db_score.score,
        "regime": latest_db_score.regime,
        "drivers": latest_db_score.drivers,
        "timestamp": latest_db_score.timestamp.isoformat()
    }

@app.post("/api/portfolio/import")
def import_portfolio(portfolio_data: PortfolioBase, db: Session = Depends(get_db), user: db_models.User = Depends(get_current_user)):

    # Create new portfolio for user
    new_portfolio = db_models.Portfolio(
        userId=user.id,
        name=portfolio_data.name,
        riskTolerance=portfolio_data.riskTolerance,
        horizon=portfolio_data.horizon
    )
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    for h in portfolio_data.holdings:
        holding = db_models.Holding(
            portfolioId=new_portfolio.id,
            symbol=h.symbol,
            weight=h.weight
        )
        db.add(holding)

    db.commit()
    return {"status": "success", "portfolioId": new_portfolio.id}

def get_portfolio_summary_internal(db: Session, user: db_models.User):
    # Get latest portfolio
    portfolio = db.query(db_models.Portfolio).filter(db_models.Portfolio.userId == user.id).order_by(db_models.Portfolio.createdAt.desc()).first()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    holdings = [{"symbol": h.symbol, "weight": h.weight} for h in portfolio.holdings]
    exposure = portfolio_engine.compute_exposure(holdings)
    fragility = portfolio_engine.compute_fragility_score(holdings)

    stress_tests = [
        portfolio_engine.run_stress_test(holdings, "recession"),
        portfolio_engine.run_stress_test(holdings, "vol_spike"),
        portfolio_engine.run_stress_test(holdings, "rates_spike")
    ]

    mc = portfolio_engine.monte_carlo_drawdown(holdings, iterations=100)

    return {
        "id": portfolio.id,
        "name": portfolio.name,
        "holdings": holdings,
        "exposure": exposure,
        "fragility": fragility,
        "stress_tests": stress_tests,
        "monte_carlo": mc
    }

@app.get("/api/portfolio/summary")
def get_portfolio_summary(db: Session = Depends(get_db), user: db_models.User = Depends(get_current_user)):
    return get_portfolio_summary_internal(db, user)

@app.get("/api/recommendations")
def get_recommendations(db: Session = Depends(get_db), user: db_models.User = Depends(get_current_user)):
    macro = get_macro_score(db)
    summary = get_portfolio_summary_internal(db, user)

    recs = rec_engine.generate_recommendations(
        macro_score=macro["score"],
        regime=macro["regime"],
        exposure=summary["exposure"],
        risk_tolerance=user.riskLevel # Simplified
    )

    return {"recommendations": recs}
