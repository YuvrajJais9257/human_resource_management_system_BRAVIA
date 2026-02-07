"""
Docstring for backend.app.models
a models.py python file to define db models using sql alchemy as orm isntead of directly executign the queries
"""
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base
import enum

class StatusEnum(str, enum.Enum):
    Present="Present"
    Absent="Absent"

class Employee(Base):
    __tablename__="employees"
    id=Column(Integer, primary_key=True, index=True)
    employee_id=Column(String(20), unique=True, nullable=False)
    name=Column(String(50), unique=True, nullable=False)
    email=Column(String(100), unique=True, nullable=False)
    department=Column(String(50), nullable=False)
    created_at=Column(Date)
    attendance = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__="attendance"
    __table_args__=(UniqueConstraint("employee_id","date", name="uix_employee_date"))
    id=Column(Integer, primary_key=True, index=True)
    employee_id=Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date=Column(Date, nullable=False)
    status=Column(Enum(StatusEnum), nullable=False)

    employee=relationship("Employee", back_populates="attendance")