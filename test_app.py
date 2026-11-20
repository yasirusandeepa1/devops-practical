from app import app


def test_home_endpoint():
    response = app.test_client().get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["version"] == "v1"


def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}
