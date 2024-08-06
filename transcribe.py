import streamlit as st
from openai import OpenAI
from transformers import pipeline

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.caption("Record some audio and it will be transcribed.")
audio = st.audio_input(label="Record some audio to transcribe")
pipe = pipeline("automatic-speech-recognition", "openai/whisper-tiny")


if audio:
    transcription = pipe(audio.getvalue())
    st.write(transcription)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=transcription["text"],
    )

    response.stream_to_file("audio.mp3")

    st.caption("Transcribed audio fed into OpenAI's text-to-speech model")
    st.audio("audio.mp3", autoplay=True)




