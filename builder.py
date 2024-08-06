import streamlit as st
from openai import OpenAI
from transformers import pipeline

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

audio = st.audio_input(label="Record some audio to transcribe")
pipe = pipeline("automatic-speech-recognition", "openai/whisper-tiny")

if "history" not in st.session_state:
    st.session_state.history = []


if audio:
    transcription = pipe(audio.getvalue())
    st.write(transcription)

    # join the history and feed it to the content
    history = '\n'.join([f"{i['role']}: {i['content']}" for i in st.session_state.history])
    st.write(history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is a Streamlit expert. You are helping a user with a Streamlit app. Respond with raw, valid, Python Streamlit code. DO NOT include any discussion or explanation. Just the code. Do not format as markdown."},
            #join the history and feed it to the content
            {"role": "assistant", "content": history},
            {"role": "user", "content": transcription["text"]},
        ],
    )


    code = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": transcription["text"]})

    with st.expander("View generated code", icon=":material/terminal:"):
        st.code(code)

    exec(code)
