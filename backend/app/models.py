"""
Database models for Employee and Attendance.

This module defines SQLAlchemy ORM models used to represent
employees and their daily attendance records in the database.

The ORM layer abstracts raw SQL queries and allows interaction
with the database using Python objects.
"""

from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import date
from .db import Base
import enum


# ================= ENUM =================

class StatusEnum(str, enum.Enum):
    """Enumeration for employee attendance status."""
    Present = "Present"
    Absent = "Absent"


# ================= EMPLOYEE =================

class Employee(Base):
    """
    Employee database model.

    Stores employee identity and department information.
    One employee can have multiple attendance records.
    """

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), nullable=False)   # Removed unique (names can repeat)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(50), nullable=False)

    created_at = Column(Date, default=date.today, nullable=False)

    # Relationship → One employee → Many attendance records
    attendance = relationship(
        "Attendance",
        back_populates="employee",
        cascade="all, delete-orphan"
    )


# ================= ATTENDANCE =================

class Attendance(Base):
    """
    Attendance database model.

    Stores daily attendance status for employees.
    Ensures only one record per employee per date.
    """

    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="uix_employee_date"),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False
    )

    date = Column(Date, nullable=False)

    status = Column(
        Enum(StatusEnum),
        nullable=False
    )

    # Relationship → Many attendance → One employee
    employee = relationship(
        "Employee",
        back_populates="attendance"
    )
