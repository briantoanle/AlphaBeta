import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

# Use connect_args={"check_same_thread": False} only for SQLite
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Use an environment variable for the database URL with a sensible default
# The default uses the SQLite database in the monorepo structure
DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "../../packages/database/dev.db")
SQLALCHEMY_DATABASE_URL = os.getenv(
    "AURORA_DATABASE_URL",
    f"sqlite:///{DEFAULT_DB_PATH}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # check_same_thread is only needed for SQLite
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
