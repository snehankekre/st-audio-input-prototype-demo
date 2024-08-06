import tempfile

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


st.caption("Translate audio to English using OpenAI")
audio = st.audio_input(label="Record some audio to translate")


# st.help(audio.getvalue())

if audio:

    # name the file audio.wav
    with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as f:
        f.write(audio.getvalue())
        i = f.name

        # open and translate the file
        audio_file = open(i, "rb")


        translation = client.audio.translations.create(
        model="whisper-1", 
        file=audio_file,
        prompt="Translate the following audio to English. First determine the language of the audio and then translate it to English.",
        )
        st.write(translation.text)

        f.close()