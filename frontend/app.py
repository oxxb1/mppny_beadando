import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
from datetime import datetime

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/api')

st.set_page_config(page_title='Időjárás - Eger', layout='wide')

st.markdown("""
    <style>
        table {
            width: 100%;
        }
        table th, table td {
            text-align: center !important;
            vertical-align: middle !important;
            padding: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title('Eger időjárása - Mikroszerviz bemutató')

def format_datetime(iso_string):
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime("%Y.%m.%d %H:%M:%S")
    except:
        return iso_string


resp = requests.get(f"{BACKEND_URL}/weather", params={'limit': 100})
if resp.status_code == 200:
    data = resp.json()
    if data:
        df = pd.DataFrame(data)

        if 'created_at' in df.columns:
            df['created_at'] = df['created_at'].apply(format_datetime)

        df = df.rename(columns={
            'city': 'Város',
            'temperature': 'Hőmérséklet (°C)',
            'windspeed': 'Szélsebesség (km/h)',
            'weathercode': 'Időjárás kód',
            'id': 'Azonosító',
            'created_at': 'Mérés ideje',
            'source': 'Forrás'
        })

        display_cols = ['Mérés ideje', 'Város', 'Hőmérséklet (°C)', 
                        'Szélsebesség (km/h)', 'Időjárás kód', 'Forrás']
        display_cols = [c for c in display_cols if c in df.columns]

        st.subheader('Gyűjtött időjárási adatok')

        st.markdown(df[display_cols].to_html(index=False, justify='center'), unsafe_allow_html=True)

        if not df.empty:
            chart_df = pd.DataFrame(data)
            chart_df['created_at'] = pd.to_datetime(chart_df['created_at'])
            recent = chart_df.head(20).sort_values('created_at')

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(recent['created_at'], recent['temperature'], marker='o', linewidth=2, markersize=6)
            ax.set_xlabel('Időpont', fontsize=12)
            ax.set_ylabel('Hőmérséklet (°C)', fontsize=12)
            ax.set_title('Hőmérséklet változása', fontsize=14)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

    else:
        st.info('Nincsenek még rögzített időjárási adatok.')
else:
    st.error('Nem sikerült lekérni az időjárási adatokat a backendből.')


r = requests.get(f"{BACKEND_URL}/stats")
if r.status_code == 200:
    s = r.json()
    st.subheader('Statisztikák')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Darabszám', s.get('count', 0))
    col2.metric('Átlag (°C)', f"{s.get('avg_temperature', 0.0):.1f}")
    col3.metric('Minimum (°C)', f"{s.get('min_temperature', 0.0):.1f}")
    col4.metric('Maximum (°C)', f"{s.get('max_temperature', 0.0):.1f}")
else:
    st.warning('Statisztika nem elérhető.')

col1, col2 = st.columns([1, 3])
with col1:
    if st.button('🔄 Frissítés (kézi)', type='primary'):
        with st.spinner('Adatok frissítése...'):
            try:
                rr = requests.post(f"{BACKEND_URL}/refresh")
                if rr.status_code == 200:
                    st.success('Adatok frissítve! Az oldal újratöltődik.')
                    st.rerun()
                else:
                    st.error('Nem sikerült elindítani az importot.')
            except Exception as e:
                st.error(f'Hiba: {e}')

with col2:
    st.info("Az automatikus frissítés 5 percenként fut. A 'Frissítés' gombbal azonnal hívhatod a külső API-t.")

st.divider()
st.caption(f"Backend URL: {BACKEND_URL} | Utolsó frissítés: {datetime.now().strftime('%Y.%m.%d %H:%M:%S')}")
