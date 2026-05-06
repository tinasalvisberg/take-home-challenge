from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

reference_sentences = {
    "low_concern": [
        "I feel well today.",
        "I slept badly but otherwise feel fine.",
        "I have mild tiredness but no other symptoms."
    ],
    "needs_follow_up": [
        "I have been feeling dizzy for several days.",
        "I feel unusually tired and it is not improving.",
        "My symptoms are not severe but I am worried."
    ],
    "urgent_review": [
        "I have chest pain and shortness of breath.",
        "I feel faint and have difficulty breathing.",
        "I have sudden weakness on one side of my body."
    ]
}

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
reference_embeddings = {
    label: model.encode(phrases)
    for label, phrases in reference_sentences.items()
}


def classify(text: str) -> dict:
    input_vec = model.encode([text])
    scores = {}
    for label, ref_vecs in reference_embeddings.items():
        similarities = cosine_similarity(input_vec, ref_vecs)
        scores[label] = float(np.mean(similarities))

    best_label = max(scores, key=scores.get)
    return {"label": best_label, "confidence": round(scores[best_label], 2)}