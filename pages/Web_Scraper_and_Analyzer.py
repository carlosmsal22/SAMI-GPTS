
# pages/Web_Scraper_and_Analyzer.py
import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot, scrape_google_reviews

st.title("🌐 Web Scraper + Brand Analyzer")
st.markdown("Scrape Reddit, Trustpilot, and Google reviews for brand sentiment.")

keyword = st.text_input("Enter a brand name or keyword (e.g., Secureonix)")
num_posts = st.slider("Number of reviews/posts per platform", 5, 50, 20)

if st.button("Scrape & Analyze"):
    st.info(f"Scraping platforms for: {keyword}")

    with st.spinner("Scraping Reddit..."):
        reddit_df = scrape_reddit(keyword, num_posts)
    with st.spinner("Scraping Trustpilot..."):
        trustpilot_df = scrape_trustpilot(keyword, num_posts)
    with st.spinner("Scraping Google Reviews..."):
        google_df = scrape_google_reviews(keyword, num_posts)

    full_df = pd.concat([reddit_df, trustpilot_df, google_df], ignore_index=True)
    st.success("Scraping complete. Preview below:")
    st.dataframe(full_df)

    csv = full_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"{keyword}_reviews.csv", mime="text/csv")

    st.markdown("### 🤖 Suggested GPT Prompt")
    st.code(f"Analyze sentiment and brand perception for '{keyword}' using the scraped review data.")
