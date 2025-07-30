import os
import joblib
from django.conf import settings
from ml_pipeline.ollama_client import generate_response
from ml_pipeline.utils.resume_parser import parse_resume

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_pipeline', 'models', 'model.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Trained model not found at {MODEL_PATH}. Please train it first.")
    return joblib.load(MODEL_PATH)

def extract_resume_text_components(resume_text: str) -> str:
    """
    Parse and flatten resume components to use as input for both ML and LLM.
    """
    parsed = parse_resume(resume_text)
    combined = " ".join([
        parsed.get('name', ''),
        parsed.get('email', ''),
        parsed.get('phone', ''),
        " ".join(parsed.get('skills', [])),
        " ".join(parsed.get('education', [])),
        " ".join(parsed.get('experience', [])),
    ])
    return combined.strip()

def get_ml_recommendations(resume_text: str, top_n: int = 3) -> list:
    """
    Use the trained ML model to recommend job roles based on resume text.
    """
    model = load_model()
    processed_input = [resume_text]  # Already preprocessed text
    predicted_role = model.predict(processed_input)[0]
    
    return [{
        'title': predicted_role,
        'description': f"This role matches your resume based on the trained ML model.",
        'match_percent': 95,
        'matched_skills': [],
        'unmatched_skills': []
    }]

def get_llm_recommendations(resume_text: str) -> list:
    """
    Use LLM to generate contextual job recommendations based on resume content.
    """
    prompt = (
        "Based on the following resume content, suggest 3 suitable job roles with short descriptions.\n\n"
        f"Resume Content:\n{resume_text}\n\n"
        "Provide the response in the following JSON format:\n"
        "[\n"
        "  {\"title\": \"Job Title\", \"description\": \"Brief job description\"},\n"
        "  ...\n"
        "]"
    )

    llm_output = generate_response(prompt)
    
    try:
        recommendations = eval(llm_output.strip())
        return [
            {
                'title': rec.get('title', 'Unknown'),
                'description': rec.get('description', ''),
                'match_percent': 80,
                'matched_skills': [],
                'unmatched_skills': []
            }
            for rec in recommendations if isinstance(rec, dict)
        ]
    except Exception as e:
        return [{
            'title': 'LLM Recommendation Error',
            'description': f'Error parsing LLM response: {str(e)}',
            'match_percent': 0,
            'matched_skills': [],
            'unmatched_skills': []
        }]

def suggest_recommendations(resume_text: str, method: str = 'ml') -> list:
    """
    Unified interface to generate job recommendations using either ML or LLM.
    
    Args:
        resume_text (str): Full resume plain text.
        method (str): 'ml', 'llm', or 'hybrid'

    Returns:
        list: List of recommendation dictionaries.
    """
    parsed_text = extract_resume_text_components(resume_text)

    if method == 'ml':
        return get_ml_recommendations(parsed_text)
    elif method == 'llm':
        return get_llm_recommendations(parsed_text)
    elif method == 'hybrid':
        return get_ml_recommendations(parsed_text) + get_llm_recommendations(parsed_text)
    else:
        return [{
            'title': 'Invalid Method',
            'description': 'Supported methods: ml, llm, hybrid.',
            'match_percent': 0,
            'matched_skills': [],
            'unmatched_skills': []
        }]
