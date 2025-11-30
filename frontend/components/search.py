# frontend/components/search.py

import streamlit as st
import requests

BACKEND_URL = "https://sahayak-09.onrender.com"

def show_search_ui():
    st.header("🔍 Semantic Search")

    search_type = st.selectbox("Search using", ["Text Query", "Image Query"])
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

    if search_type == "Text Query":
        query_text = st.text_input("Enter search text:")
        if st.button("Search") and query_text:
            st.info("Searching...")
            try:
                resp = requests.post(f"{BACKEND_URL}/search", json={"query": query_text, "top_k": top_k}, timeout=20)
                if not resp.ok:
                    st.error("Search failed on backend")
                    return
                results = resp.json().get("results", [])
            except Exception as e:
                st.error(f"Search error: {e}")
                return

            if not results:
                st.warning("No results found!")
                return
            st.success(f"Top {len(results)} results:")
            for idx, item in enumerate(results):
                st.markdown(f"**Result {idx+1}:** {item.get('text','')}")
                st.markdown(f"**Metadata:** {item.get('metadata',{})}")
                st.markdown("---")

    elif search_type == "Image Query":
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if uploaded_file and st.button("Search Image"):
            st.info("Image search is not enabled in this lightweight deployment.\nUse text search or add a backend image-search endpoint.")
