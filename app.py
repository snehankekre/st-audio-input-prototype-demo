import streamlit as st

pg = st.navigation([st.Page("basic.py"), st.Page("transcribe.py"), st.Page("translation.py"), st.Page("builder.py"), st.Page("vision.py")])
pg.run()
