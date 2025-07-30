import os
import pandas as pd
import joblib
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics import accuracy_score, classification_report
from tqdm import tqdm

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'resumes.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'bert_model.pkl')
EMBEDDER_PATH = os.path.join(BASE_DIR, 'models', 'bert_embedder.pkl')

def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0].squeeze().numpy()

def evaluate_model():
    print(" Checking model and data availability...")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f" Trained model not found at {MODEL_PATH}. Train the model first.")

    if not os.path.exists(EMBEDDER_PATH):
        raise FileNotFoundError(f" Tokenizer and model not found at {EMBEDDER_PATH}. Run train_model.py first.")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f" Processed data not found at {DATA_PATH}. Run preprocess.py first.")

    df = pd.read_csv(DATA_PATH)

    if 'resume_text' not in df.columns or 'job_role' not in df.columns:
        raise ValueError(" CSV must contain 'resume_text' and 'job_role' columns.")

    X_text = df['resume_text']
    y_true = df['job_role']

    # Load tokenizer + model
    tokenizer, embedder = joblib.load(EMBEDDER_PATH)
    embedder.eval()

    # Convert resumes to embeddings
    print(" Generating embeddings for evaluation...")
    X_embed = np.array([get_embedding(text, tokenizer, embedder) for text in tqdm(X_text)])

    # Load trained classifier
    clf = joblib.load(MODEL_PATH)

    # Predict
    y_pred = clf.predict(X_embed)

    # Evaluate
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred)

    print(f"\n Model evaluation completed.")
    print(f" Accuracy on entire dataset: {accuracy:.2f}")
    print(f"\n Classification Report:\n{report}")

if __name__ == '__main__':
    evaluate_model()
# This script evaluates the trained model on the processed resume dataset.
# It loads the embeddings and classifier, makes predictions, and prints accuracy and classification report.