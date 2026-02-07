"""
Database configuration and session management.

This module:
- Creates a SQLAlchemy engine for MySQL connection
- Verifies database connectivity at startup
- Provides a database session generator for FastAPI dependency injection
- Defines the Base class for ORM models
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import sys


# ================= LOAD ENV =================

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASS, DB_HOST, DB_NAME]):
    print("❌ Missing database environment variables.")
    sys.exit(1)


# ================= DATABASE URL =================

DB_URL =f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ================= ENGINE =================

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,      # reconnect if connection dropped
    pool_recycle=3600,       # prevent MySQL timeout (1 hour)
    echo=False               # set True only for debugging SQL
)


# ================= TEST CONNECTION =================

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ DB connection successful.")
except Exception as e:
    print("❌ DB connection failed.")
    print(e)
    sys.exit(1)


# ================= SESSION =================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# ================= DEPENDENCY =================

def get_db() -> Session:
    """
    FastAPI dependency that provides a database session.

    Yields:
        Session: SQLAlchemy database session.

    Ensures:
        - Session is automatically closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
