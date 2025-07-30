import re
import spacy
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Define a curated set of known tech and soft skills
KNOWN_SKILLS = {
    "python", "java", "c++", "django", "nlp", "spark", "aws",
    "kubernetes", "docker", "react", "flask", "angular",
    "model deployment", "scrum", "pytorch", "tensorflow", 
    "computer vision", "mysql", "html", "css", "javascript",
    "agile", "system design", "linux", "git", "jira", "typescript",
    "mongodb", "rest api", "sql", "graphql", "data analysis"
}


def extract_skills(text):
    text = text.lower()
    doc = nlp(text)
    skills = set()

    # Token-level skill matching
    for token in doc:
        word = token.text.strip().lower()
        if word in KNOWN_SKILLS and word not in ENGLISH_STOP_WORDS:
            skills.add(word)

    # Phrase-level matching
    for phrase in KNOWN_SKILLS:
        if phrase in text:
            skills.add(phrase)

    return list(skills)
