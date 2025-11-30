# frontend/components/ask.py

import streamlit as st
from backend.rag.search import RAGSearcher
from backend.processing.summarization import Summarizer

def show_ask_ui():
    st.header("💬 Ask a Question")

    query = st.text_input("Enter your question here:")
    top_k = st.slider("Number of results to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Get Answer") and query:
        st.info("Fetching relevant context...")
        rag_searcher = RAGSearcher()
        summarizer = Summarizer()

        results = rag_searcher.query(query_text=query, top_k=top_k)
        if not results:
            st.warning("No relevant data found!")
            return

        st.success(f"Top {len(results)} relevant chunks retrieved:")

        for idx, item in enumerate(results):
            st.markdown(f"**Chunk {idx+1}:** {item['text']}")
            summary = summarizer.summarize_text(item['text'])
            st.markdown(f"**Summary:** {summary}")
            st.markdown(f"**Metadata:** {item['metadata']}")
            st.markdown("---")
