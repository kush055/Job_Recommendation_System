import os
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from .parser_utils import parse_resume, map_skill_alias, common_skills
from django.conf import settings

# Load and preprocess the dataset
csv_path = os.path.join(settings.BASE_DIR, 'ml_pipeline', 'data', 'resumes_with_skills.csv')
job_df = pd.read_csv(csv_path)
job_df.rename(columns={'resume_text': 'description', 'job_role': 'title'}, inplace=True)
job_df['job_skills'] = job_df['job_skills'].apply(ast.literal_eval)

# Fuzzy skill matching function
def match_skills(resume_skills, job_skills):
    matched = []
    unmatched = []

    for job_skill in job_skills:
        found = False
        for res_skill in resume_skills:
            if fuzz.partial_ratio(res_skill.lower(), job_skill.lower()) >= 85:
                matched.append(job_skill)
                found = True
                break
        if not found:
            unmatched.append(job_skill)

    return matched, unmatched

# Main recommendation generator
def generate_recommendations(resume_text, top_n=5):
    if not resume_text or not resume_text.strip():
        return [], []

    try:
        # Step 1: Parse resume
        resume_data = parse_resume(resume_text)

        # Step 2: Create vectorable text for TF-IDF
        resume_vector_text = " ".join([
            resume_data.get('name', ''),
            resume_data.get('email', ''),
            resume_data.get('phone', ''),
            " ".join(resume_data.get('skills', [])),
            " ".join(resume_data.get('education', [])),
            " ".join(resume_data.get('experience', [])),
        ])

        # Step 3: Vectorize using TF-IDF
        job_texts = job_df['description'].astype(str).tolist()
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_vector_text] + job_texts)
        similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        # Step 4: Normalize resume skills
        resume_skills = set([map_skill_alias(skill.lower()) for skill in resume_data.get('skills', [])])

        top_indices = similarities.argsort()[::-1]
        unique_titles = set()
        recommendations = []

        for idx in top_indices:
            row = job_df.iloc[idx]
            job_title = row['title']
            if job_title in unique_titles:
                continue

            job_desc = row['description']
            job_skills_raw = row['job_skills']
            job_skills = set([skill.lower() for skill in job_skills_raw])

            matched, unmatched = match_skills(resume_skills, job_skills)
            match_percent = int((len(matched) / len(job_skills) * 100)) if job_skills else 0

            recommendations.append({
                'title': job_title,
                'description': job_desc,
                'match_percent': match_percent,
                'matched_skills': matched,
                'unmatched_skills': unmatched,
                'matched_count': len(matched),
                'similarity_score': round(similarities[idx] * 100, 2)
            })

            unique_titles.add(job_title)
            if len(recommendations) >= top_n:
                break

        # Sort by match percent, then skill count
        recommendations.sort(key=lambda x: (x['match_percent'], x['matched_count'], x['similarity_score']), reverse=True)

        # Get unmatched resume skills (resume ones not found in any job)
        all_known_job_skills = set().union(*[set(js) for js in job_df['job_skills']])
        unmatched_resume_skills = list(resume_skills - all_known_job_skills)

        return recommendations, unmatched_resume_skills

    except Exception as e:
        print("Error in generate_recommendations:", e)
        return [], []
