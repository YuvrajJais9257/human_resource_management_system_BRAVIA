"""
Docstring for backend.app.db
simple python api to connect to mysql db 
"""
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import sys
from dotenv import load_dotenv

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASS=os.getenv("DB_PASS")
DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")

DB_URL=f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine=create_engine(DB_URL, pool_pre_ping=True)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ DB connection successful.")
except Exception as e:
    print(f"❌ DB Connection failed: {e}")
    sys.exit(1)

SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()