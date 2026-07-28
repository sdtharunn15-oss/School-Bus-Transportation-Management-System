import uuid

from .conftest import client


def create_parent(db):
    email = f"parent_{uuid.uuid4().hex[:6]}@gmail.com"

    client.post(
        "/auth/register",
        json={
            "username": f"parent_{uuid.uuid4().hex[:4]}",
            "email": email,
            "password": "parent123",
            "role": "Parent"
        }
    )

    from app.models import User

    parent = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    return parent.id


def create_bus(admin_token):
    bus_number = f"BUS{uuid.uuid4().hex[:6].upper()}"

    response = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": bus_number,
            "driver_name": "Driver",
            "route_name": "Route A",
            "total_seats": 5,
            "status": "Active"
        }
    )

    assert response.status_code == 201, response.json()

    return response.json()["id"]


def create_student(admin_token, db):
    parent_id = create_parent(db)
    bus_id = create_bus(admin_token)

    admission = f"ADM{uuid.uuid4().hex[:6]}"

    response = client.post(
        "/students",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_name": "Rahul",
            "admission_number": admission,
            "class_name": "5A",
            "pickup_location": "Anna Nagar",
            "bus_id": bus_id,
            "parent_id": parent_id
        }
    )

    assert response.status_code == 201, response.json()

    return response.json()


def test_create_student(admin_token, db):
    response = create_student(admin_token, db)

    assert response["student_name"] == "Rahul"


def test_duplicate_admission_number(admin_token, db):
    parent_id = create_parent(db)

    bus1 = create_bus(admin_token)
    bus2 = create_bus(admin_token)

    admission = f"ADM{uuid.uuid4().hex[:6]}"

    first = client.post(
        "/students",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_name": "Student1",
            "admission_number": admission,
            "class_name": "6A",
            "pickup_location": "Velachery",
            "bus_id": bus1,
            "parent_id": parent_id
        }
    )

    assert first.status_code == 201, first.json()

    second = client.post(
        "/students",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_name": "Student2",
            "admission_number": admission,
            "class_name": "6B",
            "pickup_location": "Tambaram",
            "bus_id": bus2,
            "parent_id": parent_id
        }
    )

    assert second.status_code == 400


def test_get_students(admin_token):
    response = client.get(
        "/students",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_get_student_by_id(admin_token, db):
    student = create_student(admin_token, db)

    response = client.get(
        f"/students/{student['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_update_student(admin_token, db):
    student = create_student(admin_token, db)

    new_parent = create_parent(db)
    new_bus = create_bus(admin_token)

    response = client.put(
        f"/students/{student['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "student_name": "Updated Student",
            "admission_number": f"ADM{uuid.uuid4().hex[:6]}",
            "class_name": "7A",
            "pickup_location": "Mogappair",
            "bus_id": new_bus,
            "parent_id": new_parent
        }
    )

    assert response.status_code == 200
    assert response.json()["student_name"] == "Updated Student"


def test_search_student_by_name(admin_token):
    response = client.get(
        "/students?name=Rahul",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_search_student_by_admission(admin_token):
    response = client.get(
        "/students?admission_number=ADM001",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200


def test_student_pagination(admin_token):
    response = client.get(
        "/students?page=1&limit=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200