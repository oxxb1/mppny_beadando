# **Mikroszerviz – Időjárás Egerben (Python, FastAPI, Streamlit)**

Ez a projekt egy mikroszerviz jellegű Python-rendszer, amely az Open-Meteo API segítségével 
Eger aktuális időjárási adatait gyűjti, az adatokat SQLite adatbázisban tárolja, majd egy 
Streamlit alapú webes felületen jeleníti meg táblázat és grafikon formájában.

A rendszer célja bemutatni a:
- procedurális,
- funkcionális és
- objektumorientált programozási paradigmák,
valamint a modern Python eszközök (FastAPI, SQLAlchemy, Streamlit) használatát egy 
mikroszerviz-szerű architektúrában.

---

## **Architektúra áttekintése**

A projekt négy fő komponensből áll:

### **1. Backend – FastAPI**
- REST API végpontok (`/api/weather`, `/api/stats`, `/api/refresh`)
- SQLAlchemy ORM modell (`Weather`)
- Pydantic sémák (input/output)
- Időzített vagy manuális import Open-Meteo API-ból
- Háttérfolyamat külön threadben (5 percenkénti frissítés)

### **2. Adatbázis – SQLite**
- ORM alapú táblastruktúra
- Automatikus inicializálás startupkor (`init_db()`)

### **3. Frontend – Streamlit**
- Adatok megjelenítése HTML táblában
- Időbeli hőmérséklet-változás grafikon (matplotlib)
- Statisztikai nézet
- Manuális frissítés indítása

### **4. Konfiguráció**
- `.env` fájl (adatbázis URL, koordináták, frissítési intervallum)
- `.env.example` minta a konfigurációhoz

---

## **Mappa struktúra**

- backend/
   - api.py
   - background.py
   - config.py
   - db.py
   - main.py
   - models.py
   - schemas.py
   - services.py
- frontend/
   - app.py
- start.sh
- requirements.txt
- README.md
- weather.db


---
### Projekt indítása:

- Windows PowerShell: `start.ps1`
- Linux / Mac: `start.sh`
---

## **Futtatás lokálisan**

### **1. Virtuális környezet létrehozása és aktiválása**
```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
```
### **2. Függőségek telepítése**
```bash
pip install -r requirements.txt
```
### **3. Backend indítása**
```bash
uvicorn backend.main:app --reload
```
### **4. Frontend indítása**
```bash
streamlit run frontend/app.py
```



