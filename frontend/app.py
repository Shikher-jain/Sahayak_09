# frontend/app.py

import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))
import components.upload as upload
import components.ask as ask
import components.search as search
import components.recommend as recommend
import components.advanced_ui as advanced_ui

# Use image.png as app icon
st.set_page_config(
    page_title="Sahayak - Multimodal AI Assistant",
    layout="wide",
    page_icon="image.png"  # Make sure image.png is in the same directory or provide full path
)

# Ultra-Beautiful Custom CSS for Sahayak
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f3f3fe 60%, #e0f7fa 100%);
    }
    .main-title {
        color: #6C63FF;
        font-size: 3.2em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.1em;
        letter-spacing: 2.5px;
        /* text-shadow removed for no glow */
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        animation: fadeInDown 1.2s;
    }
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-40px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .subtitle {
        color: #009688;
        font-size: 1.4em;
        text-align: center;
        margin-bottom: 1.2em;
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        animation: fadeInUp 1.2s;
    }
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(40px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f3f3fe 60%, #e0f7fa 100%);
        border-radius: 16px;
        box-shadow: 0 2px 12px #e0e0e0;
        padding: 1em 0.5em;
    }
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 0.7em;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6C63FF 60%, #009688 100%);
        color: white;
        font-weight: bold;
        border-radius: 16px;
        font-size: 1.15em;
        box-shadow: 0 2px 12px #bdbdbd;
        transition: background 0.3s, box-shadow 0.3s;
        padding: 0.5em 2em;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #009688 60%, #6C63FF 100%);
        box-shadow: 0 4px 24px #6C63FF;
    }
    .stSidebarNav {
        font-size: 1.15em;
        color: #6C63FF;
    }
    .stSidebarNav > div {
        margin-bottom: 1em;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 1.1em;
        margin-top: 2em;
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        letter-spacing: 1px;
    }
    .emoji {
        font-size: 1.7em;
        vertical-align: middle;
        animation: bounce 1.5s infinite alternate;
    }
    @keyframes bounce {
        0% { transform: translateY(0); }
        100% { transform: translateY(-10px); }
    }
    .stSidebar > div:first-child {
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 Sahayak AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your all-in-one smart assistant for documents, images, audio, and more!<br><span class="emoji"></span></div>', unsafe_allow_html=True)

# Sidebar navigation with icons and future features
tabs = ["📤 Upload", "💬 Ask", "🔍 Search", "✨ Recommend", "⚡ Advanced", "🚀 Future Features"]
selected_tab = st.sidebar.radio("🚀 Navigation", tabs)

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="footer">Made with ❤️ by <b>Shikher Jain</b></div>', unsafe_allow_html=True)

if selected_tab.startswith("📤"):
    upload.show_upload_ui()
elif selected_tab.startswith("💬"):
    ask.show_ask_ui()
elif selected_tab.startswith("🔍"):
    search.show_search_ui()
elif selected_tab.startswith("✨"):
    recommend.show_recommend_ui()
elif selected_tab.startswith("⚡"):
    advanced_ui.show_advanced_ui()
elif selected_tab.startswith("🚀"):
    st.header("Future Features Coming Soon!")
    st.info("Stay tuned for upcoming enhancements and new capabilities in Sahayak.")
