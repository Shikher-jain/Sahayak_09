# backend/rag/search.py

from backend.cosdata_client import CosDataClient

class RAGSearcher:
    def __init__(self):
        self.cos_client = CosDataClient()
        self.top_k = 5  # Default number of results to retrieve

    def query(self, query_text=None, query_image_path=None, top_k=None):
        """
        Perform semantic search using Cosdata
        - query_text: string query
        - query_image_path: path to query image
        - top_k: number of results
        Returns: list of matching chunks with metadata
        """
        top_k = top_k or self.top_k
        results = self.cos_client.query_vectors(
            query_text=query_text,
            query_image_path=query_image_path,
            top_k=top_k
        )
        # Extract text and metadata
        hits = []
        for item in results:
            hits.append({
                "text": item.get("text", ""),
                "metadata": item.get("metadata", {})
            })
        return hits
