from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fetch_weather():
    response = client.get("/weather/fetch/bangalore")
    assert response.status_code == 200


def test_history():
    response = client.get("/weather/history/bangalore")
    assert response.status_code in [200, 404]