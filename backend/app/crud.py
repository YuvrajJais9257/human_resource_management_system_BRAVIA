from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from typing import Optional, List
from . import models, schemas


# ================= EMPLOYEES =================

def create_employee(db: Session, employee_in: schemas.EmployeeCreate) -> Optional[models.Employee]:
    """
    Create a new employee in the database.

    Args:
        db (Session): SQLAlchemy database session.
        employee_in (EmployeeCreate): Pydantic schema containing employee details.

    Returns:
        Employee | None:
            - Employee object if creation successful.
            - None if employee violates unique constraints (e.g., duplicate email/employee_id).
    """
    db_employee = models.Employee(**employee_in.model_dump())
    db.add(db_employee)

    try:
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        return None


def get_employee_by_id(db: Session, emp_id: int) -> Optional[models.Employee]:
    """
    Retrieve a single employee by primary key ID.

    Args:
        db (Session): Database session.
        emp_id (int): Employee database ID.

    Returns:
        Employee | None: Employee object if found, else None.
    """
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[models.Employee]:
    """
    Retrieve a paginated list of employees.

    Args:
        db (Session): Database session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return.

    Returns:
        List[Employee]: List of employee records.
    """
    return db.query(models.Employee).offset(skip).limit(limit).all()


def delete_employee(db: Session, emp_id: int) -> bool:
    """
    Delete an employee by ID.

    Args:
        db (Session): Database session.
        emp_id (int): Employee database ID.

    Returns:
        bool:
            - True if employee deleted successfully.
            - False if employee not found.
    """
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if not emp:
        return False

    db.delete(emp)
    db.commit()
    return True


# ================= ATTENDANCE =================

def create_attendance(
    db: Session,
    attendance_in: schemas.AttendanceCreate
) -> Optional[models.Attendance]:
    """
    Create a new attendance record for an employee.

    Ensures only one attendance entry per employee per date.

    Args:
        db (Session): Database session.
        attendance_in (AttendanceCreate): Attendance input schema.

    Returns:
        Attendance | None:
            - Attendance object if creation successful.
            - None if duplicate attendance exists or constraint fails.
    """

    # Check duplicate attendance
    existing = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance_in.employee_id,
        models.Attendance.date == attendance_in.date
    ).first()

    if existing:
        return None

    db_record = models.Attendance(**attendance_in.model_dump())
    db.add(db_record)

    try:
        db.commit()
        db.refresh(db_record)
        return db_record
    except IntegrityError:
        db.rollback()
        return None


def get_employee_attendance(
    db: Session,
    emp_id: int,
    attendance_date: Optional[date] = None
) -> List[models.Attendance]:
    """
    Retrieve attendance records for a specific employee.

    Optionally filter by a specific date.

    Args:
        db (Session): Database session.
        emp_id (int): Employee ID.
        attendance_date (date, optional): Specific date to filter attendance.

    Returns:
        List[Attendance]: List of attendance records ordered by most recent date.
    """

    query = db.query(models.Attendance).filter(
        models.Attendance.employee_id == emp_id
    )

    if attendance_date:
        query = query.filter(models.Attendance.date == attendance_date)

    return query.order_by(models.Attendance.date.desc()).all()
