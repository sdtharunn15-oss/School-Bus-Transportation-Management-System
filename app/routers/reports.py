from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.dependencies import authenticated_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/students/search")
def search_students(
    name: Optional[str] = None,
    admission_number: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    query = db.query(models.Student)

    if current_user.role == "Parent":
        query = query.filter(
            models.Student.parent_id == current_user.id
        )

    if name:
        query = query.filter(
            models.Student.student_name.ilike(f"%{name}%")
        )

    if admission_number:
        query = query.filter(
            models.Student.admission_number == admission_number
        )

    total = query.count()

    students = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": students
    }


@router.get("/buses/filter")
def filter_buses(
    route_name: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    query = db.query(models.Bus)

    if route_name:
        query = query.filter(
            models.Bus.route_name.ilike(f"%{route_name}%")
        )

    if status:
        query = query.filter(
            models.Bus.status == status
        )

    total = query.count()

    buses = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": buses
    }


@router.get("/attendance/daily")
def daily_attendance_report(
    travel_date: date,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    query = (
        db.query(models.Attendance)
        .filter(models.Attendance.travel_date == travel_date)
    )

    if current_user.role == "Parent":
        student_ids = (
            db.query(models.Student.id)
            .filter(models.Student.parent_id == current_user.id)
            .subquery()
        )

        query = query.filter(
            models.Attendance.student_id.in_(student_ids)
        )

    total = query.count()

    attendance = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": attendance
    }