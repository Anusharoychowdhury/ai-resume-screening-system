import pdfplumber
import re
from collections import Counter
import re

def extract_top_skills(text, top_n=10):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    common = Counter(words).most_common(top_n)
    return [word for word, _ in common]
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text
