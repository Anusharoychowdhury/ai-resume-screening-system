import csv
import os
from resume_parser import extract_text_from_pdf, clean_text
from job_matching import calculate_similarity

# Job description
job_text = """
We are looking for a Python developer with experience in machine learning,
data analysis, pandas, SQL, and communication skills.
"""

job_text = clean_text(job_text)

resume_folder = "data/resumes"
results = []

for file in os.listdir(resume_folder):
    if file.endswith(".pdf"):
        file_path = os.path.join(resume_folder, file)

        resume_text = extract_text_from_pdf(file_path)
        resume_text = clean_text(resume_text)

        score = calculate_similarity(resume_text, job_text)

        results.append((file, score))

# Sort by highest score
#results.sort(key=lambda x: x[1], reverse=True)
# Sort results by score (highest first)
results = sorted(results, key=lambda x: x[1], reverse=True)

print("\nTop 3 Candidates:\n")

for i, (filename, score) in enumerate(results[:3], start=1):
    print(f"{i}. {filename} -> {round(score * 100, 2)}%")


print("\nResume Ranking:\n")
for rank, (file, score) in enumerate(results, start=1):
    print(f"{rank}. {file} → {score}%")

# Save all results to CSV
with open("ranking_results.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Resume", "Score (%)"])

    for filename, score in results:
        writer.writerow([filename, round(score * 100, 2)])

print("\nResults saved to ranking_results.csv")
