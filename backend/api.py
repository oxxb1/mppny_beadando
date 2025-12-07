from fastapi import APIRouter, HTTPException, BackgroundTasks
from . import services
from .schemas import WeatherCreate, WeatherRead, Stats
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api")

@router.get('/weather', response_model=List[WeatherRead])
def api_list_weather(limit: int = 100, city: Optional[str] = None):
    return services.list_weather(limit=limit, city=city)

@router.get('/weather/{wid}', response_model=WeatherRead)
def api_get_weather(wid: int):
    w = services.get_weather(wid)
    if not w:
        raise HTTPException(status_code=404, detail='Not found')
    return w

@router.post('/weather', response_model=WeatherRead, status_code=201)
def api_create_weather(payload: WeatherCreate):
    return services.create_weather(payload)

@router.get('/stats', response_model=Stats)
def api_stats():
    s = services.stats()
    return Stats(count=s['count'], avg_temperature=s['avg_temperature'], min_temperature=s['min_temperature'], max_temperature=s['max_temperature'])

class RefreshResponse(BaseModel):
    message: str

@router.post('/refresh', response_model=RefreshResponse)
def api_refresh(background_tasks: BackgroundTasks):
    from .background import import_current_weather
    background_tasks.add_task(import_current_weather)
    return {'message': 'Import started'}
