import os
import joblib
import torch
from transformers import AutoTokenizer, AutoModel


# Set model paths

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.normpath(os.path.join(BASE_DIR, '../../ml_pipeline/models/bert_model.pkl'))
EMBEDDER_PATH = os.path.normpath(os.path.join(BASE_DIR, '../../ml_pipeline/models/bert_embedder.pkl'))


# Load model and embedder

try:
    model = joblib.load(MODEL_PATH)
    tokenizer, bert_model = joblib.load(EMBEDDER_PATH)
    bert_model.eval()
    print(" Models loaded successfully.")
except Exception as e:
    raise RuntimeError(f" Failed to load model or embedder: {e}")


# Embedding function

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0].squeeze().numpy()

# Predict function

def predict_job_role(text):
    text = text.lower().strip()
    embedding = get_embedding(text)
    prediction = model.predict([embedding])[0]
    return prediction

