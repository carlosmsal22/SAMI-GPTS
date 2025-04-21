
import streamlit as st

st.set_page_config(layout="wide")

st.title("🎯 SAMI Category & Target AI")
st.write("Upload a dataset or paste a prompt to begin using 🎯 SAMI Category & Target AI.")

uploaded_file = st.file_uploader("Upload file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])
if uploaded_file:
    st.success("File uploaded successfully!")
    st.info("Processing and GPT integration coming next...")

st.text_area("Or enter your prompt here:", height=200)
