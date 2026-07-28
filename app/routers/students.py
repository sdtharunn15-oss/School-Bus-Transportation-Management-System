from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import admin_only, authenticated_user

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    # Admission number must be unique
    existing_student = (
        db.query(models.Student)
        .filter(
            models.Student.admission_number ==
            student.admission_number
        )
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admission number already exists."
        )

    # Bus must exist
    bus = (
        db.query(models.Bus)
        .filter(models.Bus.id == student.bus_id)
        .first()
    )

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    # Cannot assign to inactive/maintenance bus
    if bus.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Students can only be assigned to active buses."
        )

    # Bus capacity validation
    allocated_students = (
        db.query(models.Student)
        .filter(models.Student.bus_id == bus.id)
        .count()
    )

    if allocated_students >= bus.total_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bus capacity exceeded."
        )

    # Parent must exist
    parent = (
        db.query(models.User)
        .filter(models.User.id == student.parent_id)
        .first()
    )

    if not parent or parent.role != "Parent":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid parent."
        )

    new_student = models.Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get(
    "",
    response_model=list[schemas.StudentResponse]
)
def get_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    name: Optional[str] = None,
    admission_number: Optional[str] = None,
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

    students = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return students


@router.get(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(authenticated_user)
):
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    if (
        current_user.role == "Parent"
        and student.parent_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )

    return student


@router.put(
    "/{student_id}",
    response_model=schemas.StudentResponse
)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    db_student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found."
        )

    duplicate = (
        db.query(models.Student)
        .filter(
            models.Student.admission_number ==
            student.admission_number,
            models.Student.id != student_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admission number already exists."
        )

    bus = (
        db.query(models.Bus)
        .filter(models.Bus.id == student.bus_id)
        .first()
    )

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    if bus.status != "Active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Students can only be assigned to active buses."
        )

    allocated_students = (
        db.query(models.Student)
        .filter(
            models.Student.bus_id == student.bus_id,
            models.Student.id != student_id
        )
        .count()
    )

    if allocated_students >= bus.total_seats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bus capacity exceeded."
        )

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student