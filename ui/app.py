import streamlit as st
import os
import requests
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

@st.cache_data(ttl=10)
def fetch_containers():
    try:
        response = requests.get(f"{API_URL}/containers")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return []

def main():
    # Auto refrescar cada 10 segundos
    st_autorefresh(interval=10 * 1000, limit=None, key="refresh")

    st.title("Monitor de Contenedores Docker")

    if 'alerts' not in st.session_state:
        st.session_state['alerts'] = [] 

    containers = fetch_containers()

    exited = [c for c in containers if c['status'].lower() == 'exited']

    for c in exited:
        if not any(alert['id'] == c['id'] for alert in st.session_state['alerts']):
            st.session_state['alerts'].append({
                'id': c['id'],
                'name': c['name'],
                'status': c['status'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    active_alerts = [a for a in st.session_state['alerts'] if any(c['id'] == a['id'] for c in exited)]

    if active_alerts:
        st.warning("⚠️ ¡Hay contenedores detenidos!")
        st.markdown("""
            <audio autoplay>
                <source src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg" type="audio/ogg">
                Tu navegador no soporta audio.
            </audio>
        """, unsafe_allow_html=True)

        st.subheader("Alertas activas")
        for a in active_alerts:
            st.write(f"**{a['name']}** ({a['id']}) detenido desde: {a['timestamp']}")

    # Mostrar historial completo
    if st.session_state['alerts']:
        st.subheader("Historial de alertas")
        for a in st.session_state['alerts']:
            st.write(f"**{a['name']}** ({a['id']}) estado: {a['status']} desde: {a['timestamp']}")

    st.header("Todos los contenedores")
    if containers:
        for c in containers:
            st.write(f"**{c['name']}** ({c['id']}) - Estado: {c['status']} - Imagen: {c.get('image', 'desconocida')}")
    else:
        st.info("No hay contenedores para mostrar.")

if __name__ == "__main__":
    main()
