from fpdf import FPDF

def export_pdf(news_articles):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Great Experiment Watch Report", ln=True, align="C")

    for article in news_articles:
        pdf.ln(10)
        pdf.multi_cell(0, 10, f"{article['title']}\n{article['summary']}\n{article['url']}")

    output_path = "report.pdf"
    pdf.output(output_path)
    return output_path
