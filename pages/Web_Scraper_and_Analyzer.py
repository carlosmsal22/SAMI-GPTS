
# pages/Web_Scraper_and_Analyzer.py
import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot, scrape_google_reviews
from utils.gpt_helpers import run_gpt_prompt

st.title("🌐 Web Scraper + Brand Analyzer")
st.markdown("Scrape Reddit, Trustpilot, and Google reviews for brand sentiment.")

keyword = st.text_input("Enter a brand name or keyword (e.g., Secureonix)")
num_posts = st.slider("Number of reviews/posts per platform", 5, 50, 20)

# Initialize session state for memory
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None

if "gpt_chain" not in st.session_state:
    st.session_state.gpt_chain = []

if st.button("Scrape & Analyze"):
    st.info(f"Scraping platforms for: {keyword}")

    with st.spinner("Scraping Reddit..."):
        reddit_df = scrape_reddit(keyword, num_posts)
    with st.spinner("Scraping Trustpilot..."):
        trustpilot_df = scrape_trustpilot(keyword, num_posts)
    with st.spinner("Scraping Google Reviews..."):
        google_df = scrape_google_reviews(keyword, num_posts)

    full_df = pd.concat([reddit_df, trustpilot_df, google_df], ignore_index=True)
    st.session_state.scraped_data = full_df

    st.success("Scraping complete. Preview below:")
    st.dataframe(full_df)

    csv = full_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"{keyword}_reviews.csv", mime="text/csv")

if st.session_state.scraped_data is not None:
    st.markdown("### 🧠 GPT Brand Reputation Analysis")

    if st.button("Run Initial GPT Analysis"):
        prompt = f"Based on the following user feedback about '{keyword}', provide a sentiment summary, emotion breakdown, and brand reputation insights:\n\n"
        for row in st.session_state.scraped_data['comment'].head(10):
            prompt += f"- {row}\n"

        gpt_response = run_gpt_prompt(prompt)
        st.session_state.gpt_chain.append({"user": prompt, "assistant": gpt_response})

    for i, turn in enumerate(st.session_state.gpt_chain):
        st.markdown(f"**🧠 GPT Analysis #{i+1}:**")
        st.markdown(turn["assistant"])

    follow_up = st.text_area("Ask a follow-up question based on the above analysis:")
    if st.button("Send Follow-up to GPT") and follow_up.strip() != "":
        conversation = [{"role": "system", "content": "You are a brand strategy and sentiment expert."}]
        for turn in st.session_state.gpt_chain:
            conversation.append({"role": "user", "content": turn["user"]})
            conversation.append({"role": "assistant", "content": turn["assistant"]})
        conversation.append({"role": "user", "content": follow_up})

        try:
            response = run_gpt_prompt(follow_up)
            st.session_state.gpt_chain.append({"user": follow_up, "assistant": response})
        except Exception as e:
            st.error(f"GPT Error: {e}")
