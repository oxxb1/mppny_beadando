import pytest
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from backend.main import app
from backend.db import Base, engine
from backend.schemas import WeatherCreate

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_weather_post_and_get():
    payload = {
        "city": "Eger",
        "temperature": 11.2,
        "windspeed": 3.5,
        "weathercode": 2,
        "source": "test"
    }

    r = client.post("/api/weather", json=payload)
    assert r.status_code == 201
    data = r.json()
    wid = data["id"]

    r2 = client.get(f"/api/weather/{wid}")
    assert r2.status_code == 200
    assert r2.json()["temperature"] == 11.2


def test_weather_list_empty():
    r = client.get("/api/weather")
    assert r.status_code == 200
    assert r.json() == []
