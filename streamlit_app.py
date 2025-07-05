import streamlit as st
from news_fetcher import fetch_top_news
from pdf_exporter import export_pdf

st.set_page_config(page_title="Great Experiment Watch", layout="wide")

# === Header ===
st.title("🛡️ Great Experiment Watch")
st.markdown(
    """
    **Real-time tracker for authoritarian drift and democracy health indicators.**  
    Pulls headlines from verified sources and allows you to export intelligence-style reports.
    """
)

# === News Section ===
st.subheader("📰 Authoritarian Risk Headlines")
news = fetch_top_news()

if not news:
    st.warning("No news articles were fetched. Check your internet connection or news_fetcher logic.")
else:
    for article in news:
        st.markdown(f"""
        ### {article['title']}
        **Source:** [{article['source']}]({article['url']})  
        {article['summary']}
        ---
        """)

# === Export Section ===
st.subheader("📄 Export Intelligence Brief")

if st.button("Export PDF Report"):
    pdf_path = export_pdf(news)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            file_name="GreatExperimentWatch_Report.pdf",
            mime="application/pdf"
        )
