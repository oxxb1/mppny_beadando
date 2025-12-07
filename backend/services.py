from .db import SessionLocal
from .models import Weather
from .schemas import WeatherCreate
from sqlalchemy import func
from typing import List, Optional

def create_weather(item: WeatherCreate) -> Weather:
    db = SessionLocal()
    try:
        w = Weather(city=item.city, temperature=item.temperature, windspeed=item.windspeed, weathercode=item.weathercode, source=item.source)
        db.add(w)
        db.commit()
        db.refresh(w)
        return w
    finally:
        db.close()

def list_weather(limit: int = 100, city: Optional[str] = None) -> List[Weather]:
    db = SessionLocal()
    try:
        q = db.query(Weather)
        if city:
            q = q.filter(Weather.city.contains(city))
        return q.order_by(Weather.created_at.desc()).limit(limit).all()
    finally:
        db.close()

def get_weather(wid: int):
    db = SessionLocal()
    try:
        return db.query(Weather).filter(Weather.id == wid).first()
    finally:
        db.close()

def stats():
    db = SessionLocal()
    try:
        total = db.query(func.count(Weather.id)).scalar() or 0
        avg_t = db.query(func.avg(Weather.temperature)).scalar() or 0.0
        min_t = db.query(func.min(Weather.temperature)).scalar() or 0.0
        max_t = db.query(func.max(Weather.temperature)).scalar() or 0.0
        return {"count": total, "avg_temperature": float(avg_t), "min_temperature": float(min_t), "max_temperature": float(max_t)}
    finally:
        db.close()
