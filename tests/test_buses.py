from .conftest import client


import uuid


def create_bus(admin_token):
    bus_number = f"BUS{uuid.uuid4().hex[:6].upper()}"

    response = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": bus_number,
            "driver_name": "Driver",
            "route_name": "Route A",
            "total_seats": 2,
            "status": "Active"
        }
    )

    assert response.status_code == 201, response.json()

    return response.json()["id"]

def test_duplicate_bus_number(admin_token):
    client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS102",
            "driver_name": "Driver1",
            "route_name": "Route B",
            "total_seats": 45,
            "status": "Active"
        }
    )

    response = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS102",
            "driver_name": "Driver2",
            "route_name": "Route C",
            "total_seats": 50,
            "status": "Active"
        }
    )

    assert response.status_code == 400


def test_get_all_buses(manager_token):
    response = client.get(
        "/buses",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_bus_by_id(manager_token, admin_token):
    create = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS103",
            "driver_name": "Alex",
            "route_name": "Route D",
            "total_seats": 35,
            "status": "Active"
        }
    )

    bus_id = create.json()["id"]

    response = client.get(
        f"/buses/{bus_id}",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == bus_id


def test_update_bus(admin_token):
    create = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS104",
            "driver_name": "David",
            "route_name": "Route E",
            "total_seats": 42,
            "status": "Active"
        }
    )

    bus_id = create.json()["id"]

    response = client.put(
        f"/buses/{bus_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS104",
            "driver_name": "Updated Driver",
            "route_name": "Updated Route",
            "total_seats": 45,
            "status": "Maintenance"
        }
    )

    assert response.status_code == 200
    assert response.json()["driver_name"] == "Updated Driver"


def test_delete_bus(admin_token):
    create = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "bus_number": "BUS105",
            "driver_name": "Delete Driver",
            "route_name": "Delete Route",
            "total_seats": 30,
            "status": "Active"
        }
    )

    bus_id = create.json()["id"]

    response = client.delete(
        f"/buses/{bus_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 204


def test_filter_by_route(manager_token):
    response = client.get(
        "/buses?route_name=Route",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200


def test_filter_by_status(manager_token):
    response = client.get(
        "/buses?status=Active",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200


def test_pagination(manager_token):
    response = client.get(
        "/buses?page=1&limit=5",
        headers={"Authorization": f"Bearer {manager_token}"}
    )

    assert response.status_code == 200


def test_parent_cannot_create_bus(parent_token):
    response = client.post(
        "/buses",
        headers={"Authorization": f"Bearer {parent_token}"},
        json={
            "bus_number": "BUS999",
            "driver_name": "Parent",
            "route_name": "Route X",
            "total_seats": 40,
            "status": "Active"
        }
    )

    assert response.status_code == 403