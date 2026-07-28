from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import authenticated_user, transport_manager_or_admin

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post(
    "",
    response_model=schemas.AttendanceResponse,
    status_code=status.HTTP_201_CREATED
)
def mark_attendance(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    student = (
        db.query(models.Student)
        .filter(models.Student.id == attendance.student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    bus = (
        db.query(models.Bus)
        .filter(models.Bus.id == attendance.bus_id)
        .first()
    )

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    if student.bus_id != attendance.bus_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not assigned to this bus."
        )

    existing = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.student_id == attendance.student_id,
            models.Attendance.travel_date == attendance.travel_date
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this student today."
        )

    new_attendance = models.Attendance(**attendance.model_dump())

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@router.get(
    "",
    response_model=list[schemas.AttendanceResponse]
)
def get_attendance(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    query = db.query(models.Attendance)

    if current_user.role == "Parent":
        student_ids = (
            db.query(models.Student.id)
            .filter(models.Student.parent_id == current_user.id)
            .subquery()
        )

        query = query.filter(
            models.Attendance.student_id.in_(student_ids)
        )

    attendance = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return attendance


@router.get(
    "/{attendance_id}",
    response_model=schemas.AttendanceResponse
)
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    attendance = (
        db.query(models.Attendance)
        .filter(models.Attendance.id == attendance_id)
        .first()
    )

    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found."
        )

    if current_user.role == "Parent":
        student = (
            db.query(models.Student)
            .filter(models.Student.id == attendance.student_id)
            .first()
        )

        if student.parent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied."
            )

    return attendance