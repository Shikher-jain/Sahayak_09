# backend/rag/search.py

from backend.cosdata_client import search

class RAGSearcher:
    def __init__(self):
        self.top_k = 5  # Default number of results to retrieve

    def query(self, query_text=None, query_image_path=None, top_k=None):
        """
        Perform semantic search using CosData
        - query_text: string query
        - query_image_path: path to query image (not supported yet)
        - top_k: number of results
        Returns: list of matching chunks with metadata
        """
        if not query_text:
            return []
        
        top_k = top_k or self.top_k
        results = search(query_text)
        
        # Extract text and metadata from CosData results
        hits = []
        for item in results:
            hits.append({
                "text": item.get("content", ""),
                "metadata": item.get("metadata", {})
            })
        return hits
