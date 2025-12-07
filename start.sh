python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload &
streamlit run frontend/app.py
