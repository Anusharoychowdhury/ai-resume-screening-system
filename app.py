import streamlit as st
import os
import pandas as pd

from resume_parser import extract_text_from_pdf, clean_text
from job_matching import calculate_similarity

# ------------------ PAGE TITLE ------------------
st.set_page_config(page_title="AI Resume Screening System")
st.title("🤖 AI Resume Screening System")

# ------------------ INPUTS ------------------
job_text = st.text_area("Paste Job Description Here")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type="pdf",
    accept_multiple_files=True
)

# ------------------ MAIN BUTTON ------------------
if st.button("Rank Resumes"):

    if job_text and uploaded_files:

        job_text = clean_text(job_text)
        results = []

        # ---------- PROCESS EACH RESUME ----------
        for uploaded_file in uploaded_files:
            try:
                # Save uploaded file temporarily
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Extract text
                resume_text = extract_text_from_pdf(uploaded_file.name)
                resume_text = clean_text(resume_text)

                # Calculate similarity
                score = calculate_similarity(job_text, resume_text)
                results.append((uploaded_file.name, score))

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

        # ---------- SORT RESULTS ----------
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # ---------- DISPLAY TABLE ----------
        df = pd.DataFrame(results, columns=["Resume", "Match Score"])

        st.subheader("🏆 Ranked Resumes")
        st.dataframe(df)
        # ---------- PROGRESS BARS ----------
        st.subheader("📊 Match Visualization")

        for filename, score in results:
         st.write(f"**{filename}**")
         st.progress(min(int(score), 100))

        # ---------- BEST MATCH ----------
        if len(results) > 0:
            top_resume, top_score = results[0]
            st.success(f"⭐ Best Match: {top_resume} ({top_score:.2f}%)")

        # ---------- DOWNLOAD BUTTON ----------
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="resume_ranking.csv",
            mime="text/csv",
        )

    else:
        st.warning("⚠️ Please provide job description and upload resumes.")