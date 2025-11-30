# frontend/app.py

import streamlit as st
from frontend.components import upload, ask, search, recommend, advanced_ui

st.set_page_config(page_title="Sahayak - Multimodal AI Assistant", layout="wide")

st.title("Sahayak 🌟 - Multimodal AI Assistant")

# Sidebar navigation
tabs = ["Upload", "Ask", "Search", "Recommend", "Advanced"]
selected_tab = st.sidebar.radio("Navigation", tabs)

if selected_tab == "Upload":
    upload.show_upload_ui()
elif selected_tab == "Ask":
    ask.show_ask_ui()
elif selected_tab == "Search":
    search.show_search_ui()
elif selected_tab == "Recommend":
    recommend.show_recommend_ui()
elif selected_tab == "Advanced":
    advanced_ui.show_advanced_ui()
