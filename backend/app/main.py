"""
Main application entry point for HRMS Lite API.

This module:
- Initializes FastAPI app
- Configures CORS middleware
- Registers API routers
- Creates database tables (if not existing)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app.routers import employees, attendance


# ================= CREATE TABLES =================
# NOTE: In production, use Alembic migrations instead of create_all()
Base.metadata.create_all(bind=engine)


# ================= FASTAPI APP =================

app = FastAPI(
    title="HRMS Lite API",
    version="1.0",
    description="A simple API for managing Employee Attendance",
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc"         # ReDoc UI
)


# ================= CORS =================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= ROUTERS =================

app.include_router(employees.router)
app.include_router(attendance.router)


# ================= ROOT =================

@app.get("/")
def root():
    """
    Health check endpoint.

    Returns:
        dict: API status and documentation links.
    """
    return {
        "status": "online",
        "docs": "/docs",
        "redoc": "/redoc",
        "message": "Welcome to HRMS Lite API"
    }
