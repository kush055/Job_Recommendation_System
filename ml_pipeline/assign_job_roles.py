import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

# File paths
RAW_RESUME_PATH = 'ml_pipeline/data/rawresumes.csv'
JOB_DB_PATH = 'ml_pipeline/data/job_database.csv'
OUTPUT_PATH = 'ml_pipeline/data/resumes.csv'

# Load data
print(" Loading data...")
resumes_df = pd.read_csv(RAW_RESUME_PATH)
jobs_df = pd.read_csv(JOB_DB_PATH)

if 'resume_text' not in resumes_df.columns or 'job_description' not in jobs_df.columns:
    raise ValueError(" Missing required columns in input files.")

# Load embedding model
print(" Loading BERT model...")
model = SentenceTransformer("BAAI/bge-m3")

# Generate embeddings
print(" Generating job description embeddings...")
job_descriptions = jobs_df['job_description'].tolist()
job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

print(" Generating resume embeddings...")
resume_texts = resumes_df['resume_text'].tolist()
resume_embeddings = model.encode(resume_texts, convert_to_tensor=True)

# Match each resume to closest job
print(" Matching resumes to job roles...")
assigned_roles = []
for i in tqdm(range(len(resume_embeddings))):
    scores = util.cos_sim(resume_embeddings[i], job_embeddings)
    best_match_idx = scores.argmax().item()
    matched_role = jobs_df.iloc[best_match_idx]['job_role']
    assigned_roles.append(matched_role)

# Assign and save
resumes_df['job_role'] = assigned_roles
resumes_df.to_csv(OUTPUT_PATH, index=False)

print(f"\n Job roles assigned and saved to {OUTPUT_PATH}")
