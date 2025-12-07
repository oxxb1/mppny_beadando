from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'weather.db'}")

print(f"📊 Database URL: {DATABASE_URL}")

CITY_NAME = os.getenv("CITY_NAME", "Eger")
CITY_LAT = float(os.getenv("CITY_LAT", "47.9026"))
CITY_LON = float(os.getenv("CITY_LON", "20.3770"))
REFRESH_INTERVAL_SECONDS = int(os.getenv("REFRESH_INTERVAL_SECONDS", "300"))
