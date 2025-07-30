import re
from fuzzywuzzy import fuzz

# Synonyms and aliases for more flexible matching
skill_aliases = {
    "js": "javascript",
    "py": "python",
    "ml": "machine learning",
    "nlp": "natural language processing",
    "sql": "structured query language",
    "ppt": "powerpoint",
    "c sharp": "c#",
    "ms excel": "microsoft excel"
}

# Expanded skill database
common_skills = [
    'python', 'java', 'javascript', 'django', 'sql', 'structured query language',
    'html', 'css', 'c++', 'c#', 'machine learning', 'deep learning', 'natural language processing',
    'excel', 'microsoft excel', 'git', 'github', 'powerpoint', 'ppt',
    'react', 'nodejs', 'angular', 'mongodb', 'data analysis', 'data science',
    'flask', 'api', 'rest', 'linux', 'oop', 'json', 'typescript'
]

def normalize_text(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())

def map_skill_alias(skill):
    return skill_aliases.get(skill.lower(), skill.lower())

def extract_skills(text):
    normalized_text = normalize_text(text)
    found_skills = set()

    # Direct match
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', normalized_text):
            found_skills.add(skill)

    # Alias match
    words = normalized_text.split()
    for word in words:
        alias = map_skill_alias(word)
        if alias in common_skills:
            found_skills.add(alias)

    # Fuzzy match
    for skill in common_skills:
        for word in words:
            if fuzz.partial_ratio(word, skill) >= 85:
                found_skills.add(skill)

    return list(found_skills)

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        if len(line.split()) >= 2 and line[0].isupper():
            return line.strip()
    return "Unknown"

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "Not found"

def extract_phone_number(text):
    match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?){1,2}\d{4}', text)
    return match.group(0) if match else "Not found"

def extract_education(text):
    education_keywords = ['bachelor', 'master', 'b.tech', 'm.tech', 'b.sc', 'm.sc', 'phd', 'university', 'college']
    education_lines = []
    for line in text.split('\n'):
        if any(keyword in line.lower() for keyword in education_keywords):
            education_lines.append(line.strip())
    return education_lines

def extract_experience(text):
    experience_keywords = ['experience', 'worked at', 'intern', 'project', 'company', 'role', 'position']
    experience_lines = []
    for line in text.split('\n'):
        if any(keyword in line.lower() for keyword in experience_keywords):
            experience_lines.append(line.strip())
    return experience_lines

def extract_keywords(text):
    stopwords = {"and", "or", "the", "with", "in", "on", "for", "to", "a", "an", "of", "is", "by", "as", "at"}
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return list(set(word for word in words if word not in stopwords))

def parse_resume(text):
    """
    Parses text content and returns structured data from the resume.
    """
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone_number(text),
        'skills': extract_skills(text),
        'education': extract_education(text),
        'experience': extract_experience(text),
    }
