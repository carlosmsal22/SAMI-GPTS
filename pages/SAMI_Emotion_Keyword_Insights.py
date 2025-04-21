
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

st.set_page_config(layout="wide")
st.title("🧠 Emotion & Keyword Insight Module")

uploaded_file = st.file_uploader("Upload your feedback file (CSV, XLSX, or TXT)", type=["csv", "xlsx", "txt"])

def extract_keywords(texts):
    text_blob = " ".join(texts).lower()
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text_blob)
    stopwords = set(pd.read_csv("https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt", header=None)[0])
    keywords = [word for word in words if word not in stopwords]
    return Counter(keywords).most_common(20)

def infer_emotion(text):
    # Very simplified keyword-based detection
    joy_words = ["happy", "delight", "love", "great"]
    anger_words = ["angry", "frustrated", "bad", "hate"]
    sadness_words = ["sad", "disappointed", "upset", "cry"]
    trust_words = ["trust", "confident", "secure"]
    
    scores = {"Joy": 0, "Anger": 0, "Sadness": 0, "Trust": 0}
    text = text.lower()
    for word in joy_words:
        if word in text:
            scores["Joy"] += 1
    for word in anger_words:
        if word in text:
            scores["Anger"] += 1
    for word in sadness_words:
        if word in text:
            scores["Sadness"] += 1
    for word in trust_words:
        if word in text:
            scores["Trust"] += 1
    return scores

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            df = pd.read_csv(uploaded_file, delimiter="\t")
        st.success("File loaded!")

        text_col = st.selectbox("Select the column with open-ended feedback:", df.columns)

        # Keyword clustering
        keywords = extract_keywords(df[text_col].astype(str))
        kw_df = pd.DataFrame(keywords, columns=["Keyword", "Frequency"])
        st.markdown("### 📌 Top Keywords")
        st.dataframe(kw_df)
        st.bar_chart(kw_df.set_index("Keyword"))

        # Emotion overlay
        emotion_totals = {"Joy": 0, "Anger": 0, "Sadness": 0, "Trust": 0}
        for feedback in df[text_col].dropna():
            scores = infer_emotion(feedback)
            for emo in emotion_totals:
                emotion_totals[emo] += scores[emo]

        emo_df = pd.DataFrame.from_dict(emotion_totals, orient="index", columns=["Count"]).reset_index()
        emo_df.columns = ["Emotion", "Count"]

        fig = px.pie(emo_df, values="Count", names="Emotion", title="🎨 Emotion Profile")
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Failed to read file: {e}")
else:
    st.info("Please upload a file to begin.")
