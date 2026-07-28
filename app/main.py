from fastapi import FastAPI

from app.database import Base, engine
from app.routers import (
    attendance,
    auth,
    buses,
    reports,
    students,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Bus Transportation Management System",
    version="1.0.0",
    description="Backend API for managing school buses, students, attendance, authentication, and reports."
)

app.include_router(auth.router)
app.include_router(buses.router)
app.include_router(students.router)
app.include_router(attendance.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {
        "message": "School Bus Transportation Management System API is running."
    }