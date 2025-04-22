
# SAMI GPT Suite

This Streamlit-based application is designed to host modular GPT-powered tools for market research, including:

- SAMI Brand Reputation
- SAMI VoC AI
- SAMI Pricing AI
- SAMI Segmentation AI

## 🚀 How to Run Locally

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the app:
```
streamlit run app.py
```

3. Explore each module via the left-hand sidebar.

## 📁 Directory Structure

- `app.py` – Main entry point
- `/pages/` – Individual GPT modules
- `/utils/` – Helper functions (prompt loading, OpenAI API calls)

## 🔧 Requirements

- Python 3.9+
- OpenAI API Key (set as environment variable `OPENAI_API_KEY`)
