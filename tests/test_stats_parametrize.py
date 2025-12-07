import sys
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from backend.services import create_weather, stats
from backend.schemas import WeatherCreate
from backend.db import Base, engine

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.mark.parametrize(
    "temps, expected_avg",
    [
        ([10, 20, 30], 20.0),
        ([5, 5, 5], 5.0),
        ([0, 10], 5.0)
    ]
)
def test_stats_average(temps, expected_avg):
    for t in temps:
        create_weather(WeatherCreate(city="Eger", temperature=t))

    s = stats()
    assert s["avg_temperature"] == expected_avg
