if (!(Test-Path "venv")) {
    python -m venv venv
}

venv\Scripts\activate

pip install -r requirements.txt

Start-Process powershell -ArgumentList "uvicorn backend.main:app --reload"

streamlit run frontend/app.py
