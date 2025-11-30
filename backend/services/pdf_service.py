import pdfplumber

def ingest_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    # Here you would call vector DB API or external ML API
    # For demo, just print
    print(f"Ingested PDF: {pdf_path}, length: {len(text)}")
