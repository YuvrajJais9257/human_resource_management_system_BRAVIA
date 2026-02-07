from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional
from .models import StatusEnum
class AttendanceBase(BaseModel):
    date: date
    status: StatusEnum

class AttendanceCreate(AttendanceBase):
    employee_id: int

class AttendanceOut(AttendanceBase):
    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    employee_id: str = Field(..., min_length=1)
    name: str
    email: EmailStr
    department: str

class EmployeeCreate(EmployeeBase):
    pass
class EmployeeOut(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True
