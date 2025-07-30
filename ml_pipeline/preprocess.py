import os
import re
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = 'ml_pipeline/data/rawresumes.csv'
PROCESSED_DATA_PATH = 'ml_pipeline/data/resumes.csv'

def clean_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess():
    print(" Looking for file at:", os.path.abspath(RAW_DATA_PATH))
    
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f" {RAW_DATA_PATH} not found. Please provide the raw resumes CSV.")

    df = pd.read_csv(RAW_DATA_PATH)

    # Check required column
    if 'resume_text' not in df.columns:
        raise ValueError(" 'resume_text' column is missing in the dataset.")

    # Handle missing job_role (e.g., if you're simulating or embedding later)
    if 'job_role' not in df.columns:
        print(" 'job_role' column not found. Generating dummy labels...")
        dummy_roles = ["Data Scientist", "Web Developer", "AI Engineer", "Backend Developer", "ML Engineer"]
        df['job_role'] = df['resume_id'].apply(lambda x: dummy_roles[x % len(dummy_roles)] if 'resume_id' in df.columns else "Unknown")

    # Clean the text
    df['resume_text'] = df['resume_text'].apply(clean_text)

    # Drop empty texts after cleaning
    df = df[df['resume_text'].str.strip() != ""]

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f" Preprocessing complete. Cleaned data saved to: {PROCESSED_DATA_PATH}")
    print(f" {len(df)} entries processed.")

if __name__ == '__main__':
    preprocess()
