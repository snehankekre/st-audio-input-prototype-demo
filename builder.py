import streamlit as st
from openai import OpenAI
from transformers import pipeline

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.caption("Ask the AI to build a Streamlit app for you. Currently only supports Streamlit, its dependencies, Matplotlib, and Plotly.")
st.caption("Create a line chart with Streamlit's built-in line chart command and use random data. Now do the same thing with Plotly.")
audio = st.audio_input(label="Record some audio to transcribe")
pipe = pipeline("automatic-speech-recognition", "openai/whisper-tiny")

if "history" not in st.session_state:
    st.session_state.history = []


if audio:
    transcription = pipe(audio.getvalue())
    st.write(transcription)

    history = '\n'.join([f"{i['role']}: {i['content']}" for i in st.session_state.history])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is a Streamlit expert. You are helping a user with a Streamlit app. Respond with raw, valid, Python Streamlit code. DO NOT include any discussion or explanation. Just the code. Do not format as markdown."},
            {"role": "assistant", "content": history},
            {"role": "user", "content": transcription["text"]},
        ],
    )


    code = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": transcription["text"]})

    with st.expander("View generated code", icon=":material/terminal:"):
        st.code(code)
        # Use st.download_button to download the code as a .py file
        st.download_button("Download code", code, "generated_code.py", "text/plain")

    exec(code)
