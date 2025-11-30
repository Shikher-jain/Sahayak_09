
# frontend/components/advanced_ui.py
import streamlit as st
import requests

BACKEND_URL = "https://sahayak-09.onrender.com"

def show_advanced_ui():
    st.header("⚡ Advanced Features")

    feature = st.selectbox("Choose feature", ["Timeline Extraction", "Duplicate Detection", "Analytics Dashboard"])

    if feature == "Timeline Extraction":
        text_input = st.text_area("Enter text or paste document content:")
        if st.button("Generate Timeline") and text_input:
            try:
                resp = requests.post(f"{BACKEND_URL}/timeline", json={"text": text_input}, timeout=20)
                if not resp.ok:
                    st.error("Timeline extraction failed on backend")
                    return
                timeline = resp.json().get("timeline", {})
            except Exception as e:
                st.error(f"Timeline extraction error: {e}")
                return
            if not timeline:
                st.warning("No dates or events detected.")
            else:
                st.success("Timeline:")
                for date, events in timeline.items():
                    st.markdown(f"**{date}:**")
                    for event in events:
                        st.markdown(f"- {event}")

    elif feature == "Duplicate Detection":
        text_input = st.text_area("Enter text to check duplicates:")
        if st.button("Check Duplicates") and text_input:
            try:
                resp = requests.post(f"{BACKEND_URL}/duplicate", json={"text": text_input}, timeout=20)
                if not resp.ok:
                    st.error("Duplicate detection failed on backend")
                    return
                duplicates = resp.json().get("duplicates", [])
            except Exception as e:
                st.error(f"Duplicate detection error: {e}")
                return
            if not duplicates:
                st.success("No duplicates found.")
            else:
                st.warning(f"{len(duplicates)} duplicates found:")
                for dup in duplicates:
                    st.markdown(f"- **Text:** {dup.get('text','')}")
                    st.markdown(f"  **Similarity:** {dup.get('similarity',0):.2f}")
                    st.markdown(f"  **Metadata:** {dup.get('metadata',{})}")

    elif feature == "Analytics Dashboard":
        try:
            resp = requests.get(f"{BACKEND_URL}/analytics", timeout=20)
            if not resp.ok:
                st.info("No analytics data yet.")
                return
            events = resp.json().get("events", [])
        except Exception as e:
            st.error(f"Analytics error: {e}")
            return
        if not events:
            st.info("No analytics data yet.")
        else:
            st.success(f"Total events logged: {len(events)}")
            st.dataframe(events)
