# backend/rag/duplicate.py

from backend.cosdata_client import CosDataClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class DuplicateDetector:
    def __init__(self, threshold=0.85):
        """
        threshold: cosine similarity above which two chunks are considered duplicates
        """
        self.cos_client = CosDataClient()
        self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.threshold = threshold

    def check_duplicates(self, new_text):
        """
        Check if new_text is a duplicate of any existing vector in Cosdata
        Returns: list of duplicate items
        """
        collection_vectors = self.cos_client.collection.get_all_vectors()  # placeholder
        if not collection_vectors:
            return []

        new_vec = self.embedding_model.encode([new_text])[0]
        duplicates = []

        for item in collection_vectors:
            existing_vec = item['dense_values']
            sim = cosine_similarity([new_vec], [existing_vec])[0][0]
            if sim >= self.threshold:
                duplicates.append({
                    "text": item.get("text", ""),
                    "metadata": item.get("metadata", {}),
                    "similarity": sim
                })
        return duplicates
