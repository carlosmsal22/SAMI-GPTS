import pandas as pd
from fpdf import FPDF
import streamlit as st
from io import BytesIO
import re

def clean_text(text):
    # Remove non-ASCII characters (e.g., emojis) that FPDF cannot encode
    return re.sub(r'[^\x00-\x7F]+', '', text)

def export_csv(df, filename="output.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name=filename, mime='text/csv')

def export_pdf(summary_text, filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    safe_text = clean_text(summary_text)
    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf_output = pdf.output(dest="S").encode("latin-1")
    buffer = BytesIO(pdf_output)

    st.download_button("Download PDF", buffer, file_name=filename, mime="application/pdf")
