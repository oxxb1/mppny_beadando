from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base
import datetime

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    windspeed = Column(Float, nullable=True)
    weathercode = Column(Integer, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
