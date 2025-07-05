import streamlit as st
import feedparser
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Great Experiment Watch", layout="wide")

# --- News Feeds ---
RSS_FEEDS = {
    "Reuters": ("http://feeds.reuters.com/reuters/worldNews", "International"),
    "BBC": ("http://feeds.bbci.co.uk/news/world/rss.xml", "International"),
    "The Guardian": ("https://www.theguardian.com/world/rss", "International"),
    "Al Jazeera": ("https://www.aljazeera.com/xml/rss/all.xml", "International"),
    "Associated Press": ("https://apnews.com/rss", "US"),
    "NPR": ("https://www.npr.org/rss/rss.php?id=1004", "US"),
    "Freedom House": ("https://freedomhouse.org/rss/press-releases", "US"),
    "Amnesty International": ("https://www.amnesty.org/en/feed/", "International"),
    "Human Rights Watch": ("https://www.hrw.org/rss/news", "International"),
}

KEYWORDS = [
    "authoritarian", "censorship", "election interference", "surveillance",
    "judicial capture", "freedom of speech", "political arrest", "democracy",
    "human rights", "military coup", "opposition", "media suppression", "martial law"
]

# --- Sidebar ---
st.sidebar.title("🌐 Sources")
selected_sources = st.sidebar.multiselect(
    "Select news sources:",
    list(RSS_FEEDS.keys()),
    default=list(RSS_FEEDS.keys())
)

search_term = st.sidebar.text_input("🔍 Search keywords")

# --- Democracy Monitor ---
st.sidebar.markdown("### 🧭 Democracy Lifespan Monitor")
st.sidebar.markdown("Estimated % of Democracy Remaining")
st.sidebar.progress(0.68)  # placeholder static value for now

# --- Fetch & Filter ---
def fetch_articles():
    us_articles = []
    intl_articles = []
    for source in selected_sources:
        feed_url, region = RSS_FEEDS[source]
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            content = f"{entry.title} {entry.get('summary', '')}".lower()
            if any(kw.lower() in content for kw in KEYWORDS) or (search_term.lower() in content if search_term else False):
                article = {
                    "title": entry.title,
                    "summary": entry.get("summary", "No summary available."),
                    "link": entry.link,
                    "source": source,
                    "published": entry.get("published", "No date"),
                    "rendered_html": f"""
                        <h4><a href="{entry.link}" target="_blank">{entry.title}</a></h4>
                        <small><i>{source} — {entry.get("published", "No date")}</i></small>
                        <p>{entry.get("summary", "No summary available.")}</p>
                        <hr>
                    """
                }
                if region == "US":
                    us_articles.append(article)
                else:
                    intl_articles.append(article)
    return us_articles, intl_articles

us_articles, intl_articles = fetch_articles()
all_articles = us_articles + intl_articles

# --- Emergency Alert ---
alert_triggered = any(
    "military coup" in a['summary'].lower() or "martial law" in a['summary'].lower()
    for a in all_articles
)

if alert_triggered:
    st.error("🚨 EMERGENCY ALERT: Potential authoritarian escalation detected.")

# --- Emergency Incident Section ---
if alert_triggered:
    st.markdown("## 🧨 Emergency Incidents")
    for a in all_articles:
        if "military coup" in a['summary'].lower() or "martial law" in a['summary'].lower():
            st.markdown(a['rendered_html'], unsafe_allow_html=True)

# --- Main Dashboard ---
st.markdown("## 🛡️ Great Experiment Watch")
st.markdown("Monitoring global threats to democracy in real time.")

st.write(f"### {len(all_articles)} articles matched")

# --- Grouped Articles ---
if us_articles:
    st.markdown("## 🇺🇸 U.S. Articles")
    for a in us_articles:
        st.markdown(a['rendered_html'], unsafe_allow_html=True)

if intl_articles:
    st.markdown("## 🌍 International Articles")
    for a in intl_articles:
        st.markdown(a['rendered_html'], unsafe_allow_html=True)

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
    if all_articles:
        filename = generate_pdf(all_articles)
        st.success(f"PDF generated: {filename}")
        with open(filename, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=filename)
    else:
        st.warning("No articles to include in the brief.")
