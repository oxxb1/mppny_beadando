from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherBase(BaseModel):
    city: str
    temperature: float
    windspeed: Optional[float] = None
    weathercode: Optional[int] = None
    source: Optional[str] = None

class WeatherCreate(WeatherBase):
    pass

class WeatherRead(WeatherBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Stats(BaseModel):
    count: int
    avg_temperature: float
    min_temperature: float
    max_temperature: float
