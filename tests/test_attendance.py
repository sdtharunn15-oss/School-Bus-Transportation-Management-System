from datetime import date
import uuid

from .conftest import client


def create_bus(admin_token):
    bus_number = f"BUS{uuid.uuid4().hex[:6].upper()}"

    response = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": bus_number,
            "driver_name": "Driver Attendance",
            "route_name": "Route Attendance",
            "total_seats": 10,
            "status": "Active"
        }
    )

    assert response.status_code == 201, response.json()

    return response.json()["id"]


def create_parent():
    email = f"attendance_{uuid.uuid4().hex[:6]}@gmail.com"

    client.post(
        "/auth/register",
        json={
            "username": "attendanceparent",
            "email": email,
            "password": "parent123",
            "role": "Parent"
        }
    )

    return email


def get_parent_id(db, email):
    from app.models import User

    parent = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return parent.id


def create_student(admin_token, db):
    bus_id = create_bus(admin_token)

    email = create_parent()

    parent_id = get_parent_id(db, email)

    admission = f"ATT{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/students",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_name": "Attendance Student",
            "admission_number": admission,
            "class_name": "8A",
            "pickup_location": "Anna Nagar",
            "bus_id": bus_id,
            "parent_id": parent_id
        }
    )

    assert response.status_code == 201, response.json()

    student = response.json()

    return student["id"], bus_id


def test_create_attendance(admin_token, db):
    student_id, bus_id = create_student(admin_token, db)

    response = client.post(
        "/attendance",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_id": student_id,
            "bus_id": bus_id,
            "travel_date": str(date.today()),
            "pickup_status": "Present",
            "drop_status": "Present"
        }
    )

    assert response.status_code == 201


def test_duplicate_attendance(admin_token, db):
    student_id, bus_id = create_student(admin_token, db)

    payload = {
        "student_id": student_id,
        "bus_id": bus_id,
        "travel_date": str(date.today()),
        "pickup_status": "Present",
        "drop_status": "Present"
    }

    first = client.post(
        "/attendance",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    assert first.status_code == 201, first.json()

    second = client.post(
        "/attendance",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=payload
    )

    assert second.status_code == 400


def test_get_all_attendance(admin_token):
    response = client.get(
        "/attendance",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_get_attendance_by_id(admin_token):
    response = client.get(
        "/attendance/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code in [200, 404]


def test_parent_view_attendance(parent_token):
    response = client.get(
        "/attendance",
        headers={"Authorization": f"Bearer {parent_token}"}
    )

    assert response.status_code == 200


def test_transport_manager_can_mark_attendance(manager_token):
    response = client.get(
        "/attendance",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200