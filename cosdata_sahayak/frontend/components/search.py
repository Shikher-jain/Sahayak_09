# frontend/components/search.py

import streamlit as st
from backend.rag.search import RAGSearcher

def show_search_ui():
    st.header("🔍 Semantic Search")

    search_type = st.selectbox("Search using", ["Text Query", "Image Query"])
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

    if search_type == "Text Query":
        query_text = st.text_input("Enter search text:")
        if st.button("Search") and query_text:
            st.info("Searching...")
            searcher = RAGSearcher()
            results = searcher.query(query_text=query_text, top_k=top_k)
            if not results:
                st.warning("No results found!")
                return
            st.success(f"Top {len(results)} results:")
            for idx, item in enumerate(results):
                st.markdown(f"**Result {idx+1}:** {item['text']}")
                st.markdown(f"**Metadata:** {item['metadata']}")
                st.markdown("---")

    elif search_type == "Image Query":
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file and st.button("Search Image"):
            st.info("Searching using image...")
            searcher = RAGSearcher()
            results = searcher.query(query_image_path=uploaded_file, top_k=top_k)
            if not results:
                st.warning("No results found!")
                return
            st.success(f"Top {len(results)} results:")
            for idx, item in enumerate(results):
                st.markdown(f"**Result {idx+1}:** {item['text']}")
                st.markdown(f"**Metadata:** {item['metadata']}")
                st.markdown("---")
