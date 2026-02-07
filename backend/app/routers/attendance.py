"""
Attendance API routes.

This module provides endpoints to:
- Mark attendance for an employee
- Retrieve attendance records (optionally filtered by date)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from ..db import get_db
from .. import schemas, crud, models


router = APIRouter(
    prefix="/api/v1/attendance",
    tags=["Attendance"]
)


# ================= MARK ATTENDANCE =================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def mark_attendance(
    data: schemas.AttendanceCreate,
    db: Session = Depends(get_db)
):
    """
    Mark attendance for an employee on a specific date.

    Args:
        data (AttendanceCreate): Attendance input data.
        db (Session): Database session.

    Returns:
        dict: Success message with created record ID.

    Raises:
        HTTPException 404: If employee does not exist.
        HTTPException 409: If attendance already marked for that date.
    """

    # Check employee exists
    emp = db.query(models.Employee).filter(
        models.Employee.id == data.employee_id
    ).first()

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee does not exist"
        )

    record = crud.create_attendance(db, data)

    if not record:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Attendance already marked for employee {data.employee_id} on {data.date}"
        )

    return {
        "message": "Attendance marked successfully",
        "record_id": record.id
    }


# ================= GET ATTENDANCE =================

@router.get(
    "/{emp_id}",
    response_model=List[schemas.AttendanceOut]
)
def get_attendance(
    emp_id: int,
    attendance_date: Optional[date] = Query(None, description="Filter by specific date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve attendance records for a specific employee.

    Optionally filter by a specific date.

    Args:
        emp_id (int): Employee ID.
        attendance_date (date, optional): Filter by date.
        db (Session): Database session.

    Returns:
        List[AttendanceOut]: Attendance records sorted by most recent date.

    Raises:
        HTTPException 404: If employee does not exist.
    """

    emp = db.query(models.Employee).filter(
        models.Employee.id == emp_id
    ).first()

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    records = crud.get_employee_attendance(db, emp_id, attendance_date)
    return records
