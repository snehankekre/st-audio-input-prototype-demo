import streamlit as st

st.caption("This page lets you record audio and play it back.")
audio = st.audio_input(label="todo")

if audio:
    st.audio(audio)
