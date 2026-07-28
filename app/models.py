from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    students = relationship("Student", back_populates="parent")


class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False, index=True)
    driver_name = Column(String, nullable=False)
    route_name = Column(String, nullable=False)
    total_seats = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    students = relationship(
        "Student",
        back_populates="bus",
        cascade="all, delete"
    )

    attendance = relationship(
        "Attendance",
        back_populates="bus",
        cascade="all, delete"
    )


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    admission_number = Column(String, unique=True, nullable=False, index=True)
    class_name = Column(String, nullable=False)
    pickup_location = Column(String, nullable=False)

    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    bus = relationship("Bus", back_populates="students")
    parent = relationship("User", back_populates="students")

    attendance = relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete"
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)

    travel_date = Column(Date, nullable=False)
    pickup_status = Column(String, nullable=False)
    drop_status = Column(String, nullable=False)

    student = relationship("Student", back_populates="attendance")
    bus = relationship("Bus", back_populates="attendance")

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "travel_date",
            name="unique_student_attendance"
        ),
    )