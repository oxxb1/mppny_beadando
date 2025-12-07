import threading, time, requests, logging
from .config import CITY_LAT, CITY_LON, CITY_NAME, REFRESH_INTERVAL_SECONDS
from .services import create_weather
from .schemas import WeatherCreate

logger = logging.getLogger(__name__)

def fetch_current_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.exception("Failed to fetch weather: %s", e)
        return None

def import_current_weather(lat=CITY_LAT, lon=CITY_LON, city=CITY_NAME):
    payload = fetch_current_weather(lat, lon)
    if not payload:
        return
    cw = payload.get('current_weather', {})
    temp = cw.get('temperature')
    wind = cw.get('windspeed')
    code = cw.get('weathercode')
    if temp is None:
        return
    try:
        create_weather(WeatherCreate(city=city, temperature=float(temp), windspeed=float(wind) if wind is not None else None, weathercode=int(code) if code is not None else None, source='open-meteo'))
        logger.info("Imported weather for %s: %s C", city, temp)
    except Exception:
        logger.exception("Failed to save weather")
def start_periodic_import(stop_event: threading.Event):
    def loop():
        while not stop_event.is_set():
            try:
                import_current_weather()
            except Exception:
                logger.exception("Background import failed")
            stop_event.wait(REFRESH_INTERVAL_SECONDS)
        logger.info("Background importer exiting.")
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    return t
