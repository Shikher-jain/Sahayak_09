# frontend/components/advanced_ui.py

import streamlit as st
from backend.processing.timeline import TimelineExtractor
from backend.rag.duplicate import DuplicateDetector
from backend.analytics import Analytics

def show_advanced_ui():
    st.header("⚡ Advanced Features")

    feature = st.selectbox("Choose feature", ["Timeline Extraction", "Duplicate Detection", "Analytics Dashboard"])

    if feature == "Timeline Extraction":
        text_input = st.text_area("Enter text or paste document content:")
        if st.button("Generate Timeline") and text_input:
            extractor = TimelineExtractor()
            timeline = extractor.build_timeline([text_input])
            if not timeline:
                st.warning("No dates or events detected.")
            else:
                st.success("Timeline:")
                for date, events in timeline.items():
                    st.markdown(f"**{date.date()}:**")
                    for event in events:
                        st.markdown(f"- {event}")

    elif feature == "Duplicate Detection":
        text_input = st.text_area("Enter text to check duplicates:")
        if st.button("Check Duplicates") and text_input:
            detector = DuplicateDetector()
            duplicates = detector.check_duplicates(text_input)
            if not duplicates:
                st.success("No duplicates found.")
            else:
                st.warning(f"{len(duplicates)} duplicates found:")
                for dup in duplicates:
                    st.markdown(f"- **Text:** {dup['text']}")
                    st.markdown(f"  **Similarity:** {dup['similarity']:.2f}")
                    st.markdown(f"  **Metadata:** {dup['metadata']}")

    elif feature == "Analytics Dashboard":
        analytics = Analytics()
        events = analytics.get_events()
        if not events:
            st.info("No analytics data yet.")
        else:
            st.success(f"Total events logged: {len(events)}")
            st.dataframe(events)
