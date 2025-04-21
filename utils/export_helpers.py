
import pandas as pd
from fpdf import FPDF
import streamlit as st

def export_csv(df, filename="output.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name=filename, mime='text/csv')

def export_pdf(summary_text, filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    with open(filename, "wb") as f:
        pdf.output(f)
    with open(filename, "rb") as f:
        st.download_button("Download PDF", f.read(), file_name=filename, mime="application/pdf")
