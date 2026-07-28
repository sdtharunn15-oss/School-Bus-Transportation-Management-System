School Bus Transportation Management System

Project Overview

The School Bus Transportation Management System is a RESTful backend application developed using FastAPI. It helps schools efficiently manage buses, student allocations, daily attendance, and transportation operations. The system includes secure JWT authentication, role-based authorization, business validations, reporting, search functionality, pagination, and database persistence.

Tech Stack

Python 3.9+
FastAPI
SQLAlchemy
Pydantic
SQLite
JWT Authentication
Passlib
Uvicorn
Pytest

Project Structure

school_bus_transportation_management_system/

app/
    main.py
    database.py
    models.py
    schemas.py
    oauth2.py
    utils.py
    dependencies.py

    routers/
        auth.py
        buses.py
        students.py
        attendance.py
        reports.py

tests/
    conftest.py
    test_auth.py
    test_buses.py
    test_students.py
    test_attendance.py
    test_reports.py

requirements.txt
README.md

Features

JWT Authentication

User Registration

User Login

Role-Based Authorization

Bus Management

Student Allocation

Route Attendance Management

Attendance Reports

Student Search

Bus Filtering

Pagination

Business Rule Validation

Database Persistence

Swagger API Documentation

User Roles

Admin

Can manage all modules.

Transport Manager

Can manage buses and attendance.

Parent

Can view only their child's bus and attendance information.

Authentication

The application uses JWT Authentication.

After successful login, an access token is generated.

All protected APIs require the Authorization header.

Authorization: Bearer <access_token>

Bus Management

Create Bus

Update Bus

Delete Bus

View Bus

List All Buses

Filter by Route

Filter by Status

Student Management

Create Student

Update Student

View Student

List Students

Search by Student Name

Search by Admission Number

Attendance Management

Create Attendance

View Attendance

View Attendance by ID

Daily Attendance Report

Reports

Search Students

Filter Buses

Daily Attendance Report

Pagination Support

Business Rules

Bus number must be unique.

Admission number must be unique.

Students can only be assigned to active buses.

Students cannot be assigned if bus capacity is full.

One bus can contain multiple students.

Attendance can be marked only once per student per day.

Only valid parent accounts can be assigned to students.

Only Admin can manage students.

Only Admin and Transport Manager can manage transportation operations.

Parents can access only their own child's information.

Validation Rules

Bus number is mandatory.

Driver name is mandatory.

Route name is mandatory.

Total seats must be greater than zero.

Student name is mandatory.

Admission number must be unique.

Parent ID must exist.

Bus ID must exist.

Travel date is required.

Pickup status is required.

Drop status is required.

API Endpoints

Authentication

POST /auth/register

POST /auth/login

Bus Management

POST /buses

GET /buses

GET /buses/{bus_id}

PUT /buses/{bus_id}

DELETE /buses/{bus_id}

Student Management

POST /students

GET /students

GET /students/{student_id}

PUT /students/{student_id}

Attendance

POST /attendance

GET /attendance

GET /attendance/{attendance_id}

Reports

GET /reports/students/search

GET /reports/buses/filter

GET /reports/attendance/daily

Installation

Clone the repository.

git clone <repository_url>

Open the project directory.

cd school_bus_transportation_management_system

Create a virtual environment.

python -m venv venv

Activate the virtual environment.

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

Install dependencies.

pip install -r requirements.txt

Run the application.

uvicorn app.main:app --reload

Open Swagger Documentation.

http://127.0.0.1:8000/docs

Run Tests

pytest -v

Database

Database Engine

SQLite

Database File

school_bus.db

Testing

Testing Framework

Pytest

The project contains automated test cases for:

Authentication

Bus APIs

Student APIs

Attendance APIs

Reports APIs

Role-Based Authorization

Business Rule Validation

Expected Test Result

39 Passed

API Documentation

Swagger UI

http://127.0.0.1:8000/docs

ReDoc

http://127.0.0.1:8000/redoc

Security

JWT Authentication

Password Hashing

Role-Based Authorization

Protected Routes

Business Rule Validation

Future Enhancements

GPS Tracking

Live Bus Location

Parent Notifications

SMS Alerts

Email Notifications

Driver Mobile Application

Student QR Code Attendance

Dashboard Analytics

Export Reports to Excel and PDF

Author
Tharun
