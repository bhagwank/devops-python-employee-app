import pytest
import app as employee_app


@pytest.fixture
def client(tmp_path, monkeypatch):

    # Use a separate temporary database for testing
    test_db = tmp_path / "test.db"

    monkeypatch.setattr(
        employee_app,
        "DATABASE",
        str(test_db)
    )

    employee_app.initialize_database()

    with employee_app.app.test_client() as client:
        yield client


def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_employees(client):

    response = client.get("/employees")

    assert response.status_code == 200
    assert response.json == []


def test_add_employee(client):

    response = client.post(
        "/employees",
        json={
            "name": "John",
            "department": "DevOps"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Employee added successfully"


def test_add_employee_missing_data(client):

    response = client.post(
        "/employees",
        json={"name": "John"}
    )

    assert response.status_code == 400
