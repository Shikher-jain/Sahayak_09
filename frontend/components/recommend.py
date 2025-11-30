# frontend/components/recommend.py

import streamlit as st
from backend.rag.recommend import Recommender

def show_recommend_ui():
    st.header("✨ Recommendations")

    query_text = st.text_input("Enter text to get recommendations:")
    top_k = st.slider("Number of recommendations", min_value=1, max_value=10, value=5)

    if st.button("Get Recommendations") and query_text:
        st.info("Fetching recommendations...")
        recommender = Recommender()
        results = recommender.recommend(query_text=query_text, top_k=top_k)
        if not results:
            st.warning("No recommendations found!")
            return
        st.success(f"Top {len(results)} recommendations:")
        for idx, item in enumerate(results):
            st.markdown(f"**Recommendation {idx+1}:** {item['text']}")
            st.markdown(f"**Metadata:** {item['metadata']}")
            st.markdown("---")
