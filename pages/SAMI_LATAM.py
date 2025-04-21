
import streamlit as st

st.title("📊 SAMI.AI INSIGHTS LATAM")
st.write("Multilingual market insights assistant for Latin America.")

uploaded_file = st.file_uploader("Upload survey data or open-ended responses", type=["csv", "xlsx", "txt"])
if uploaded_file:
    st.success("File uploaded! (Processing functionality coming soon.)")
