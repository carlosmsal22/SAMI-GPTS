
import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot
from utils.gpt_helpers import run_gpt_prompt

st.title("🧠 Scrape + Analyze Brand Reputation")

keyword = st.text_input("Enter a brand (e.g. Secureonix)")
num = st.slider("How many posts/reviews?", 5, 50, 10)

if st.button("Scrape the Web"):
    reddit_df = scrape_reddit(keyword, max_posts=num)
    trust_df = scrape_trustpilot(keyword, max_reviews=num)
    full_df = pd.concat([reddit_df, trust_df])
    st.session_state.scraped_data = full_df
    st.success("Scraping complete! Here's a preview:")
    st.dataframe(full_df)

if "scraped_data" in st.session_state and st.button("Analyze with GPT"):
    prompt = f"Based on the following user comments about '{keyword}', summarize sentiment and brand reputation:\n\n"
    for comment in st.session_state.scraped_data['comment'].head(10):
        prompt += f"- {comment}\n"

    st.markdown("### ✅ Prompt Sent to GPT")
    st.code(prompt)

    response = run_gpt_prompt(prompt, module="brand_reputation")
    st.markdown("### 🧠 GPT Response")
    st.write(response)
