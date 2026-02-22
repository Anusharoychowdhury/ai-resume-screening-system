from resume_parser import extract_text_from_pdf

text = extract_text_from_pdf("data/resumes/sample.pdf")
print(text[:1000])
