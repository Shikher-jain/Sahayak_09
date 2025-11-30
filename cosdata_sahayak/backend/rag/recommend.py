# backend/rag/recommend.py

from backend.cosdata_client import CosDataClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Recommender:
    def __init__(self):
        self.cos_client = CosDataClient()
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def recommend(self, query_text, top_k=5):
        """
        Recommend similar documents based on query_text
        Returns: list of recommended items with text + metadata
        """
        # Get all items from Cosdata
        # For large datasets, you may implement batch retrieval
        collection_vectors = self.cos_client.collection.get_all_vectors()  # placeholder method
        if not collection_vectors:
            return []

        # Compute embeddings
        query_vec = self.embedding_model.encode([query_text])[0]
        candidate_vecs = [item['dense_values'] for item in collection_vectors]

        # Compute similarity
        sims = cosine_similarity([query_vec], candidate_vecs)[0]
        top_indices = sims.argsort()[::-1][:top_k]

        recommendations = []
        for idx in top_indices:
            recommendations.append({
                "text": collection_vectors[idx].get("text", ""),
                "metadata": collection_vectors[idx].get("metadata", {})
            })
        return recommendations
