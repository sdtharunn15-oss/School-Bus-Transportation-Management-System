from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.dependencies import transport_manager_or_admin

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


@router.post(
    "",
    response_model=schemas.BusResponse,
    status_code=status.HTTP_201_CREATED
)
def create_bus(
    bus: schemas.BusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    existing_bus = (
        db.query(models.Bus)
        .filter(models.Bus.bus_number == bus.bus_number)
        .first()
    )

    if existing_bus:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bus number already exists."
        )

    new_bus = models.Bus(**bus.model_dump())

    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)

    return new_bus


@router.get(
    "",
    response_model=list[schemas.BusResponse]
)
def get_buses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    route_name: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    query = db.query(models.Bus)

    if route_name:
        query = query.filter(models.Bus.route_name.ilike(f"%{route_name}%"))

    if status_filter:
        query = query.filter(models.Bus.status == status_filter)

    buses = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return buses


@router.get(
    "/{bus_id}",
    response_model=schemas.BusResponse
)
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()

    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    return bus


@router.put(
    "/{bus_id}",
    response_model=schemas.BusResponse
)
def update_bus(
    bus_id: int,
    bus: schemas.BusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    existing_bus = db.query(models.Bus).filter(models.Bus.id == bus_id)

    db_bus = existing_bus.first()

    if not db_bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    duplicate = (
        db.query(models.Bus)
        .filter(
            models.Bus.bus_number == bus.bus_number,
            models.Bus.id != bus_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bus number already exists."
        )

    existing_bus.update(bus.model_dump(), synchronize_session=False)

    db.commit()

    return existing_bus.first()


@router.delete(
    "/{bus_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(transport_manager_or_admin)
):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id)

    if not bus.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bus not found."
        )

    bus.delete(synchronize_session=False)
    db.commit()

    return