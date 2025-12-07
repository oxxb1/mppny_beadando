import sys
import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.services import create_weather, list_weather, get_weather
from backend.schemas import WeatherCreate
from backend.db import Base, engine, SessionLocal
import pytest

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_weather():
    item = WeatherCreate(
        city="Eger",
        temperature=10.5,
        windspeed=5.2,
        weathercode=3,
        source="test"
    )
    w = create_weather(item)

    assert w.id is not None
    assert w.city == "Eger"
    assert w.temperature == 10.5


def test_list_weather():
    create_weather(WeatherCreate(city="Eger", temperature=10))
    create_weather(WeatherCreate(city="Eger", temperature=12))

    items = list_weather()
    assert len(items) == 2
    assert items[0].temperature in (10, 12)


def test_get_weather():
    w = create_weather(WeatherCreate(city="Eger", temperature=15))
    fetched = get_weather(w.id)
    assert fetched.id == w.id
    assert fetched.temperature == 15
