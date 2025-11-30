# frontend/components/ask.py



import streamlit as st
import requests

BACKEND_URL = "https://sahayak-09.onrender.com"

def show_ask_ui():
    st.header("💬 Ask a Question")

    query = st.text_input("Enter your question here:")
    top_k = st.slider("Number of results to retrieve", min_value=1, max_value=10, value=5)

    if st.button("Get Answer") and query:
        st.info("Fetching relevant context...")
        try:
            response = requests.post(f"{BACKEND_URL}/rag/search", json={"query": query, "top_k": top_k})
            if not response.ok:
                st.error("RAG search failed!")
                return
            results = response.json().get("results", [])
        except Exception as e:
            st.error(f"Error: {e}")
            return

        if not results:
            st.warning("No relevant data found!")
            return

        st.success(f"Top {len(results)} relevant chunks retrieved:")

        for idx, item in enumerate(results):
            st.markdown(f"**Chunk {idx+1}:** {item.get('text', '')}")
            # Summarize via backend API
            try:
                sum_resp = requests.post(f"{BACKEND_URL}/summarize", json={"text": item.get('text', '')})
                summary = sum_resp.json().get("summary", "") if sum_resp.ok else "(summary failed)"
            except Exception:
                summary = "(summary failed)"
            st.markdown(f"**Summary:** {summary}")
            st.markdown(f"**Metadata:** {item.get('metadata', {})}")
            st.markdown("---")
