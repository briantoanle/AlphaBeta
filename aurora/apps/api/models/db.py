from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
import datetime
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "User"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    riskLevel = Column(String, default="Intermediate")
    portfolios = relationship("Portfolio", back_populates="user")
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Portfolio(Base):
    __tablename__ = "Portfolio"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    userId = Column(String, ForeignKey("User.id"))
    name = Column(String)
    riskTolerance = Column(Float, default=5.0)
    horizon = Column(Integer, default=10)
    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio")
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Holding(Base):
    __tablename__ = "Holding"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    portfolioId = Column(String, ForeignKey("Portfolio.id"))
    symbol = Column(String)
    weight = Column(Float)
    portfolio = relationship("Portfolio", back_populates="holdings")

class MacroScore(Base):
    __tablename__ = "MacroScore"
    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    score = Column(Float)
    regime = Column(String)
    drivers = Column(JSON)
    confidence = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
