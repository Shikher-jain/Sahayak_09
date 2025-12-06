import numpy as np

class Retriever:
    def __init__(self, cosdata_client):
        self.cosdata_client = cosdata_client

    def search_vectors(self, query_vector, top_k=5):
        vectors = self.cosdata_client.get_all_vectors()
        scores = []
        for v in vectors:
            score = self.cosine_similarity(query_vector, v["vector"])
            scores.append((score, v))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [item[1] for item in scores[:top_k]]

    @staticmethod
    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
