from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# -------------------- AUTH --------------------


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


# -------------------- BUS --------------------


class BusBase(BaseModel):
    bus_number: str
    driver_name: str
    route_name: str
    total_seats: int = Field(..., gt=0)
    status: str


class BusCreate(BusBase):
    pass


class BusUpdate(BusBase):
    pass


class BusResponse(BusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------- STUDENT --------------------


class StudentBase(BaseModel):
    student_name: str
    admission_number: str
    class_name: str
    pickup_location: str
    bus_id: int
    parent_id: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------- ATTENDANCE --------------------


class AttendanceBase(BaseModel):
    student_id: int
    bus_id: int
    travel_date: date
    pickup_status: str
    drop_status: str


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)