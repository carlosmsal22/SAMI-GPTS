import streamlit as st
import pandas as pd
import plotly.express as px
import json  # Critical missing import
from datetime import datetime
from utils.gpt_scraper import EnterpriseScraper

def display_radar_chart(analysis: dict):
    """Visualize multi-dimensional scores"""
    if not analysis:
        return
        
    metrics = {
        'Reputation': analysis.get('overall_score', 0),
        'Sentiment': analysis.get('sentiment_score', 0),
        'Engagement': len(analysis.get('top_strengths', [])),
        'Stability': 10 - len(analysis.get('crisis_alerts', [])),
        'Growth': analysis.get('growth_potential', 0)
    }
    
    fig = px.line_polar(
        pd.DataFrame({
            'Metric': list(metrics.keys()),
            'Score': list(metrics.values())
        }), 
        r='Score', 
        theta='Metric',
        line_close=True,
        range_r=[0,10]
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(layout="wide", page_title="EnterpriseIQ")
    st.title("🚀 Enterprise Intelligence Dashboard")
    
    # Configuration
    company = st.text_input("Company Name", "Apple")
    analysis_depth = st.radio(
        "Analysis Depth",
        ["Basic", "Standard", "Deep"],
        horizontal=True,
        index=1
    )
    
    if st.button("🔍 Run Comprehensive Scan", type="primary"):
        with st.spinner(f"Scanning {company} (this may take 2-3 minutes)..."):
            try:
                # Initialize and run scraper
                scraper = EnterpriseScraper()
                
                # Data collection
                data = scraper.scrape_enterprise_data(company)
                if not data:
                    st.error("No valid data found. Try adjusting search terms.")
                    return
                
                # Convert to DataFrame for display
                df = pd.DataFrame(data)
                
                # Analysis
                analysis = scraper.analyze_sentiment(data)
                if 'error' in analysis:
                    st.error(f"Analysis failed: {analysis['error']}")
                    return
                
                # Store results
                st.session_state.data = df
                st.session_state.analysis = analysis
                
                # Display success
                st.success(f"✅ Collected {len(df)} mentions from {df['source'].nunique()} sources")
                
                # Show analysis
                display_radar_chart(analysis)
                
                # Data explorer
                with st.expander("📊 View Raw Data"):
                    st.dataframe(df[['content', 'source', 'date']])
                
                # Export options
                with st.expander("💾 Export Results"):
                    st.download_button(
                        "Download as JSON",
                        data=json.dumps({
                            "company": company,
                            "data": data,
                            "analysis": analysis
                        }, indent=2),
                        file_name=f"{company}_analysis.json"
                    )
                    
            except Exception as e:
                st.error(f"Scan failed: {str(e)}")
                if st.button("Show Technical Details"):
                    st.exception(e)

if __name__ == "__main__":
    main()
