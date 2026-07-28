from .conftest import client


def test_register_admin():
    response = client.post(
        "/auth/register",
        json={
            "username": "admin2",
            "email": "admin2@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "admin2@gmail.com"


def test_register_transport_manager():
    response = client.post(
        "/auth/register",
        json={
            "username": "manager2",
            "email": "manager2@gmail.com",
            "password": "manager123",
            "role": "Transport Manager"
        }
    )

    assert response.status_code == 201
    assert response.json()["role"] == "Transport Manager"


def test_register_parent():
    response = client.post(
        "/auth/register",
        json={
            "username": "parent2",
            "email": "parent2@gmail.com",
            "password": "parent123",
            "role": "Parent"
        }
    )

    assert response.status_code == 201
    assert response.json()["role"] == "Parent"


def test_duplicate_email():
    client.post(
        "/auth/register",
        json={
            "username": "duplicate",
            "email": "duplicate@gmail.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate2",
            "email": "duplicate@gmail.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    assert response.status_code == 400


def test_login_success():
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "login@gmail.com",
            "password": "password123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        data={
            "username": "login@gmail.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_login_invalid_email():
    response = client.post(
        "/auth/login",
        data={
            "username": "unknown@gmail.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401