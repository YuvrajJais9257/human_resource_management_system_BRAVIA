"""
Schemas for Employee and Attendance data models.

This module defines Pydantic schemas used for:
- Creating employee records
- Returning employee data from the database
- Creating attendance entries
- Returning attendance records

These schemas act as a validation and serialization layer
between the API and database models.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional
from .models import StatusEnum


# ================= Attendance =================

class AttendanceBase(BaseModel):
    """Base schema for attendance containing common fields."""
    date: date
    status: StatusEnum


class AttendanceCreate(AttendanceBase):
    """Schema used when creating a new attendance record."""
    employee_id: int


class AttendanceOut(AttendanceBase):
    """Schema used when returning attendance data from the database."""

    class Config:
        from_attributes = True


# ================= Employee =================

class EmployeeBase(BaseModel):
    """Base schema for employee containing shared attributes."""
    employee_id: str = Field(..., min_length=1)
    name: str
    email: EmailStr
    department: str


class EmployeeCreate(EmployeeBase):
    """Schema used for creating a new employee."""
    pass


class EmployeeOut(EmployeeBase):
    """Schema used when returning employee data from the database."""
    id: int

    class Config:
        from_attributes = True
