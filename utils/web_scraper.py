import streamlit as st
import pandas as pd
from utils.web_scraper import scrape_reddit, scrape_trustpilot, scrape_google_reviews
from utils.gpt_helpers import run_gpt_prompt

st.title("🌐 Web Scraper + Brand Analyzer")
st.markdown("Scrape Reddit, Trustpilot, and Google reviews for brand sentiment.")

keyword = st.text_input("Enter a brand name or keyword (e.g., Secureonix)")
num_posts = st.slider("Number of reviews/posts per platform", 5, 50, 20)

# Session memory
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None

if "gpt_chain" not in st.session_state:
    st.session_state.gpt_chain = []

if st.button("Scrape & Analyze"):
    with st.spinner("Scraping data..."):
        reddit_df = scrape_reddit(keyword, num_posts)
        trustpilot_df = scrape_trustpilot(keyword, num_posts)
        google_df = scrape_google_reviews(keyword, num_posts)

        full_df = pd.concat([reddit_df, trustpilot_df, google_df], ignore_index=True)
        st.session_state.scraped_data = full_df

    st.success("Scraping complete. Preview below:")
    st.dataframe(full_df)

    csv = full_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, f"{keyword}_scraped_data.csv")

# GPT prompt & response
if st.session_state.scraped_data is not None:
    st.markdown("### 🧠 GPT Brand Reputation Analysis")

    if st.button("Run Initial GPT Analysis"):
        prompt = f"Based on the following real user comments about '{keyword}', analyze the brand sentiment, reputation drivers, and emotional tone:\n\n"
        for row in st.session_state.scraped_data['comment'].head(10):
            prompt += f"- {row}\n"

        st.markdown("### 📤 Prompt Sent to GPT")
        st.code(prompt)

        gpt_response = run_gpt_prompt(prompt, module="brand_reputation")
        st.session_state.gpt_chain.append({"user": prompt, "assistant": gpt_response})

        st.markdown("### 🤖 GPT Response")
        st.write(gpt_response)

    # Show full GPT chat history
    for i, turn in enumerate(st.session_state.gpt_chain):
        st.markdown(f"**🧠 GPT Analysis #{i+1}:**")
        st.markdown(turn["assistant"])

    # Follow-up prompt
    follow_up = st.text_area("Ask a follow-up question based on GPT insights:")
    if st.button("Send Follow-up to GPT") and follow_up.strip():
        conversation = [{"role": "system", "content": "You are a brand strategy and sentiment expert."}]
        for turn in st.session_state.gpt_chain:
            conversation.append({"role": "user", "content": turn["user"]})
            conversation.append({"role": "assistant", "content": turn["assistant"]})
        conversation.append({"role": "user", "content": follow_up})

        followup_response = run_gpt_prompt(follow_up, module="brand_reputation")
        st.session_state.gpt_chain.append({"user": follow_up, "assistant": followup_response})

        st.markdown("### 🧠 GPT Follow-Up Response")
        st.write(followup_response)
