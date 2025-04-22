import streamlit as st
from utils.gpt_scraper import EnterpriseScraper
import pandas as pd
import plotly.express as px

def display_radar_chart(analysis: dict):
    """Interactive radar visualization"""
    df = pd.DataFrame({
        'Metric': ['Reputation', 'Sentiment', 'Engagement', 'Crisis', 'Growth'],
        'Score': [
            analysis['overall_score'],
            analysis['by_source']['average'],
            len(analysis['strengths']),
            10 - len(analysis['crisis_alerts']),
            analysis['by_source'].get('news', 5)
        ]
    })
    fig = px.line_polar(df, r='Score', theta='Metric', line_close=True)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(layout="wide")
    st.title("🚀 Enterprise Intelligence Dashboard")
    
    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name", "Secureonix")
    with col2:
        depth = st.select_slider("Analysis Depth", ["Basic", "Standard", "Deep"])
    
    # Initialize scraper
    scraper = EnterpriseScraper()
    
    if st.button("🔍 Run Comprehensive Scan"):
        with st.spinner(f"Scanning {company} across 50+ sources..."):
            try:
                # Data collection
                data = scraper.scrape_enterprise_data(company)
                analysis = scraper.analyze_sentiment(data)
                
                # Session state
                st.session_state.data = pd.DataFrame(data)
                st.session_state.analysis = analysis
                
                # Display
                st.success(f"Found {len(data)} quality mentions")
                
                with st.expander("📊 Data Overview"):
                    display_radar_chart(analysis)
                    
                with st.expander("🔍 Top Findings"):
                    st.json(analysis, expanded=False)
                    
            except Exception as e:
                st.error(f"Scan failed: {str(e)}")

    # Historical comparison
    if 'analysis' in st.session_state:
        st.divider()
        st.subheader("📈 Trend Analysis")
        
        if st.button("🔄 Compare with Previous Scan"):
            # Implement comparison logic
            st.warning("Historical comparison coming in v2.0")

if __name__ == "__main__":
    main()