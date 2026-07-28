from datetime import date

from .conftest import client


def test_search_students_by_name(admin_token):
    response = client.get(
        "/reports/students/search?name=Rahul",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_search_students_by_admission_number(admin_token):
    response = client.get(
        "/reports/students/search?admission_number=ADM001",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_student_search_pagination(admin_token):
    response = client.get(
        "/reports/students/search?page=1&limit=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_filter_buses_by_route(admin_token):
    response = client.get(
        "/reports/buses/filter?route_name=Route",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_filter_buses_by_status(admin_token):
    response = client.get(
        "/reports/buses/filter?status=Active",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_bus_filter_pagination(admin_token):
    response = client.get(
        "/reports/buses/filter?page=1&limit=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_daily_attendance_report(admin_token):
    response = client.get(
        f"/reports/attendance/daily?travel_date={date.today()}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_daily_attendance_pagination(admin_token):
    response = client.get(
        f"/reports/attendance/daily?travel_date={date.today()}&page=1&limit=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["page"] == 1


def test_parent_can_view_reports(parent_token):
    response = client.get(
        f"/reports/attendance/daily?travel_date={date.today()}",
        headers={"Authorization": f"Bearer {parent_token}"}
    )

    assert response.status_code == 200