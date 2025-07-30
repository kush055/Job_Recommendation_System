import os
import sys
import pandas as pd

# Setup Django import path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Import your extractor
from resumes.utils.extract_keywords import extract_skills

INPUT_PATH = os.path.join(BASE_DIR, 'ml_pipeline', 'data', 'resumes.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'ml_pipeline', 'data', 'resumes_with_skills.csv')

def add_skills_column():
    df = pd.read_csv(INPUT_PATH)

    if 'resume_text' in df.columns:
        df['job_skills'] = df['resume_text'].apply(lambda x: extract_skills(str(x)))
    elif 'description' in df.columns:
        df['job_skills'] = df['description'].apply(lambda x: extract_skills(str(x)))
    else:
        raise ValueError("CSV must contain either 'resume_text' or 'description'.")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f" File saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    add_skills_column()
# This script adds a 'job_skills' column to the resumes CSV file by extracting skills from the resume text or job description.
# It saves the updated DataFrame to a new CSV file.