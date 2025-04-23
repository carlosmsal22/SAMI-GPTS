import streamlit as st
from utils.sami_integration import SAMIAnalyzer
from utils.Web_Scraper import hybrid_scrape  # From previous implementation
import json

def display_sami_report(report: Dict):
    """Render SAMI-style interactive report"""
    st.header(f"🔮 {report['title']}")
    st.caption(f"Generated at {report['timestamp']}")
    
    # Strategic Overview
    with st.container(border=True):
        st.subheader("🎯 Strategic Overview")
        st.write(report['analysis']['overview'])
        
        cols = st.columns(3)
        cols[0].metric("Positive", f"{report['analysis']['sentiment_breakdown']['positive']}%")
        cols[1].metric("Negative", f"{report['analysis']['sentiment_breakdown']['negative']}%")
        cols[2].metric("Neutral", f"{report['analysis']['sentiment_breakdown']['neutral']}%")
    
    # Emotional Analysis
    st.subheader("🧠 Emotional Pulse")
    emotions = pd.DataFrame(report['analysis']['emotional_analysis'])
    st.bar_chart(emotions.set_index('emotion'))
    
    # Competitive Benchmark
    with st.expander("🏆 Competitive Benchmarking"):
        st.write(report['analysis']['competitive_benchmark'])
    
    # Recommendations
    st.subheader("💡 Strategic Recommendations")
    for rec in report['analysis']['strategic_recommendations']:
        st.markdown(f"- {rec}")

def main():
    st.set_page_config(layout="wide", page_title="SAMI Enterprise")
    
    # SAMI Configuration
    analysis_types = [
        "Sentiment and Emotion Analysis",
        "Split Emotion Analysis",
        "Brand Reputation Report",
        "Custom Analysis"
    ]
    
    # UI Layout
    col1, col2 = st.columns([3, 1])
    with col1:
        company = st.text_input("Company Name", "Secureonix")
    with col2:
        analysis_type = st.selectbox("Report Type", analysis_types)
    
    if st.button("✨ Generate SAMI Report"):
        with st.spinner("Conducting deep reputation analysis..."):
            try:
                # Step 1: Data Collection
                data = hybrid_scrape(company)
                
                # Step 2: SAMI Analysis
                analyzer = SAMIAnalyzer()
                report = analyzer.generate_report(data, analysis_type)
                
                # Display results
                st.session_state.sami_report = report
                display_sami_report(report)
                
                # Export
                st.download_button(
                    "📥 Download Full Report",
                    data=json.dumps(report, indent=2),
                    file_name=f"SAMI_{company}_{datetime.now().strftime('%Y%m%d')}.json"
                )
                
            except Exception as e:
                st.error(f"SAMI Analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
