import streamlit as st
import feedparser
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Great Experiment Watch", layout="wide")

# --- News Feeds ---
RSS_FEEDS = {
    "Reuters": "http://feeds.reuters.com/reuters/worldNews",
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Associated Press": "https://apnews.com/rss",
    "NPR": "https://www.npr.org/rss/rss.php?id=1004",
    "Freedom House": "https://freedomhouse.org/rss/press-releases",
    "Amnesty International": "https://www.amnesty.org/en/feed/",
    "Human Rights Watch": "https://www.hrw.org/rss/news",
}

KEYWORDS = [
    "authoritarian", "censorship", "election interference", "surveillance",
    "judicial capture", "freedom of speech", "political arrest", "democracy",
    "human rights", "military coup", "opposition", "media suppression", "martial law"
]

# --- Sidebar ---
st.sidebar.title("🌐 Sources")
selected_sources = st.sidebar.multiselect("Select news sources:", list(RSS_FEEDS.keys()), default=list(RSS_FEEDS.keys()))
search_term = st.sidebar.text_input("🔍 Search keywords")

# --- Fetch & Filter ---
def fetch_articles():
    articles = []
    for source in selected_sources:
        feed = feedparser.parse(RSS_FEEDS[source])
        for entry in feed.entries:
            content = f"{entry.title} {entry.get('summary', '')}".lower()
            if any(kw.lower() in content for kw in KEYWORDS) or (search_term.lower() in content if search_term else False):
                articles.append({
                    "title": entry.title,
                    "summary": entry.get("summary", "No summary available.").replace("<p>", "").replace("</p>", ""),
                    "link": entry.link,
                    "source": source,
                    "published": entry.get("published", "No date"),
                })
    return articles

articles = fetch_articles()

# --- Emergency Alert Filtering ---
emergency_terms = ["military coup", "martial law"]
emergencies = [a for a in articles if any(term in a['summary'].lower() for term in emergency_terms)]
non_emergencies = [a for a in articles if a not in emergencies]

if emergencies:
    st.error("🚨 EMERGENCY ALERT: Potential authoritarian escalation detected.")
    st.markdown("### 🚨 Emergency Incidents")
    for article in emergencies:
        st.markdown(f"#### [{article['title']}]({article['link']})", unsafe_allow_html=True)
        st.caption(f"{article['source']} — {article['published']}")
        st.write(article['summary'])
        st.markdown("---")

# --- Main Dashboard ---
st.title("🛡️ Great Experiment Watch")
st.markdown("Monitoring global threats to democracy in real time.")

st.write(f"### {len(articles)} articles matched")

for article in non_emergencies:
    st.markdown(f"#### [{article['title']}]({article['link']})", unsafe_allow_html=True)
    st.caption(f"{article['source']} — {article['published']}")
    st.write(article['summary'])
    st.markdown("---")

# --- Democracy Lifespan Monitor ---
st.sidebar.markdown("---")
st.sidebar.subheader("📉 Democracy Lifespan Monitor")
lifespan_pct = st.sidebar.slider("Estimated % of Democracy Remaining", 0, 100, 68)
st.sidebar.progress(lifespan_pct / 100)

# --- Plan to Leave Section ---
with st.expander("📦 View / Edit Your Emergency Relocation Plan"):
    st.markdown("""
    - **Passport:** ✅ Ready  
    - **Digital Security:** [Update device encryption, 2FA, password manager]  
    - **Relocation Country Shortlist:** Spain 🇪🇸, Portugal 🇵🇹, Ireland 🇮🇪  
    - **Money Moved Offshore:** [in progress]  
    - **Citizenship by Descent:** [father: Cuba 🇨🇺 → Spain path]  
    """)

# --- Export PDF ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Great Experiment Watch — Weekly Brief", ln=True, align="C")
    pdf.ln(10)

    for a in data:
        pdf.set_font("Arial", 'B', size=12)
        pdf.multi_cell(0, 10, f"{a['title']}")
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, f"{a['summary']}")
        pdf.set_text_color(0, 0, 255)
        pdf.cell(0, 10, a['link'], ln=True, link=a['link'])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

    filename = f"great_experiment_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

if st.button("📄 Export Intelligence Brief (PDF)"):
    if articles:
        filename = generate_pdf(articles)
        st.success(f"PDF generated: {filename}")
        with open(filename, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=filename)
    else:
        st.warning("No articles to include in the brief.")
