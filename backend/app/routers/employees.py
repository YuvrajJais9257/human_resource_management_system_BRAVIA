"""
Employee API routes.

This module defines REST endpoints for managing employees:
- Create employee
- List employees
- Delete employee
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import schemas, crud


router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"]
)


# ================= CREATE EMPLOYEE =================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.EmployeeOut
)
def create_employee(
    data: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new employee.

    Args:
        data (EmployeeCreate): Employee details.
        db (Session): Database session.

    Returns:
        EmployeeOut: Created employee object.

    Raises:
        HTTPException 409: If employee with same ID or email already exists.
    """
    emp = crud.create_employee(db, data)

    if not emp:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with this ID or email already exists"
        )

    return emp


# ================= LIST EMPLOYEES =================

@router.get(
    "",
    response_model=List[schemas.EmployeeOut]
)
def list_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of employees with optional pagination.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum records to return.
        db (Session): Database session.

    Returns:
        List[EmployeeOut]: List of employee records.
    """
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


# ================= DELETE EMPLOYEE =================

@router.delete(
    "/{emp_id}",
    status_code=status.HTTP_200_OK
)
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an employee by ID.

    Args:
        emp_id (int): Employee database ID.
        db (Session): Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException 404: If employee not found.
    """
    success = crud.delete_employee(db, emp_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return {"message": f"Employee {emp_id} deleted successfully"}
