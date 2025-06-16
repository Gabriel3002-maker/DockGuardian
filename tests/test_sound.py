import streamlit as st

st.title("Prueba de sonido")

audio_url = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"

st.audio(audio_url)
