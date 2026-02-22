from resume_parser import extract_text_from_pdf, clean_text
from job_matching import calculate_similarity

resume_text = extract_text_from_pdf("data/resumes/sample.pdf")
resume_text = clean_text(resume_text)

job_text = """
We are looking for a Python developer with experience in machine learning,
data analysis, pandas, and SQL. Strong communication skills required.
"""

job_text = clean_text(job_text)

score = calculate_similarity(resume_text, job_text)

print(f"Resume Match Score: {score}%")
