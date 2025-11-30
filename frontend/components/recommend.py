# frontend/components/recommend.py

import streamlit as st
import requests

BACKEND_URL = "https://sahayak-09.onrender.com"

def show_recommend_ui():
    st.header("✨ Recommendations")

    query_text = st.text_input("Enter text to get recommendations:")
    top_k = st.slider("Number of recommendations", min_value=1, max_value=10, value=5)

    if st.button("Get Recommendations") and query_text:
        st.info("Fetching recommendations...")
        try:
            resp = requests.post(f"{BACKEND_URL}/recommend", json={"query": query_text, "top_k": top_k}, timeout=20)
            if not resp.ok:
                st.error("Recommendation failed on backend")
                return
            results = resp.json().get("results", [])
        except Exception as e:
            st.error(f"Recommendation error: {e}")
            return

        if not results:
            st.warning("No recommendations found!")
            return
        st.success(f"Top {len(results)} recommendations:")
        for idx, item in enumerate(results):
            st.markdown(f"**Recommendation {idx+1}:** {item.get('text','')}")
            st.markdown(f"**Metadata:** {item.get('metadata',{})}")
            st.markdown("---")
