import streamlit as st
from openai import OpenAI
from transformers import pipeline

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

audio = st.audio_input(label="Test")
pipe = pipeline("automatic-speech-recognition", "openai/whisper-tiny")

image_url = st.text_input("Enter image URL", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg")

if image_url:
    st.image(image_url)

if audio and image_url:
    transcription = pipe(audio.getvalue())
    st.write(transcription)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": transcription["text"]},
                {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "low"
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )

    text = response.choices[0].message.content

    st.caption(text)

    tts = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    tts.stream_to_file("audio1.mp3")

    st.caption("AI response")
    st.audio("audio1.mp3", autoplay=True)