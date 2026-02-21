from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import relationship
import datetime
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    riskLevel = Column(String, default="Intermediate")
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    portfolios = relationship("Portfolio", back_populates="user")
    alerts = relationship("Alert", back_populates="user")

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.id"))
    name = Column(String)
    riskTolerance = Column(Float, default=5.0)
    horizon = Column(Integer, default=10)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio")

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(String, primary_key=True, default=generate_uuid)
    portfolioId = Column(String, ForeignKey("portfolios.id"))
    symbol = Column(String)
    weight = Column(Float)

    portfolio = relationship("Portfolio", back_populates="holdings")

class MacroSignal(Base):
    __tablename__ = "macro_signals"

    id = Column(String, primary_key=True, default=generate_uuid)
    source = Column(String)
    name = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)
    category = Column(String)

class MacroScore(Base):
    __tablename__ = "macro_scores"

    id = Column(String, primary_key=True, default=generate_uuid)
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
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String)
    portfolioId = Column(String)
    action = Column(String)
    content = Column(String)
    options = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=generate_uuid)
    userId = Column(String, ForeignKey("users.id"))
    type = Column(String)
    threshold = Column(Float)
    isActive = Column(Boolean, default=True)

    user = relationship("User", back_populates="alerts")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
