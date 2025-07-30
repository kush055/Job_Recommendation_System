import os
import pandas as pd
import joblib
import numpy as np
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from transformers import AutoTokenizer, AutoModel
import torch

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'resumes.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'bert_model.pkl')
EMBEDDER_PATH = os.path.join(BASE_DIR, 'models', 'bert_embedder.pkl')

# Function to get BERT embeddings from resume text
def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0].squeeze().numpy()

def train_model():
    print(" Checking for dataset at:", PROCESSED_DATA_PATH)

    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f" File not found at {PROCESSED_DATA_PATH}. Please check path or preprocess data.")

    # Load dataset
    df = pd.read_csv(PROCESSED_DATA_PATH)

    if 'resume_text' not in df.columns or 'job_role' not in df.columns:
        raise ValueError(" CSV must contain 'resume_text' and 'job_role' columns.")

    X_texts = df['resume_text']
    y = df['job_role']

    # Load BERT model from Hugging Face
    print(" Loading BERT model: BAAI/bge-m3 ...")
    tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
    model = AutoModel.from_pretrained("BAAI/bge-m3")
    model.eval()

    # Generate embeddings for all resumes
    print(" Generating resume embeddings...")
    embeddings = np.array([get_embedding(text, tokenizer, model) for text in tqdm(X_texts)])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(embeddings, y, test_size=0.2, random_state=42)

    # Train classifier
    print(" Training logistic regression model...")
    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n Model trained successfully with accuracy: {acc:.2f}")
    print("\n Classification Report:\n", classification_report(y_test, y_pred))

    # Save model and embedder
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    joblib.dump((tokenizer, model), EMBEDDER_PATH)

    print(f"\n Trained model saved to: {MODEL_PATH}")
    print(f" Tokenizer and model saved to: {EMBEDDER_PATH}")

# Run if executed directly
if __name__ == '__main__':
    train_model()
