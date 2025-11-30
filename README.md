# Sahayak 🌟 - Multimodal AI Assistant

Sahayak is a **production-ready multimodal AI assistant** built for handling **PDFs, images, audio, video, and URLs**.  
It provides **semantic search, summarization, RAG-based question answering, recommendations, timeline extraction, duplicate detection, and analytics**.

---

## Features

- **File Ingestion**: Upload PDFs, images, audio, video, or URLs.
- **Semantic Search**: Search across all ingested content using text or image queries.
- **RAG-based QA**: Ask questions and get answers from ingested content with summaries.
- **Recommendations**: Suggest similar documents or content based on semantic similarity.
- **Advanced Features**:
  - Timeline extraction from text/documents
  - Duplicate detection using embeddings
  - Analytics dashboard for usage tracking
- **Multimodal Embeddings**: Supports text, images, and audio/video embeddings using HuggingFace models.
- **Modular & Scalable**: Easily extendable for future integrations like LLMs, multilingual support, or new ingestion types.

---

## Installation

```bash
git clone https://github.com/Shikher-jain/Sahayak_09
cd Sahayak_09
pip install -r requirements.txt
````

---

## Usage

```bash
streamlit run frontend/app.py
```

* Navigate using sidebar tabs:

  * **Upload**: Ingest content
  * **Ask**: Question answering
  * **Search**: Semantic search
  * **Recommend**: Content recommendations
  * **Advanced**: Timeline, duplicates, analytics

---

## Backend Architecture

* **Ingestion**: Handles PDFs, images, audio, video, and URLs
* **Processing**: Embeddings, summarization, tagging, timeline
* **RAG**: Search, query rewriting, recommendation, duplicate detection
* **Analytics**: Tracks uploads, queries, recommendations
* **Auth**: API key-based authentication

---

## Tech Stack

* **Frontend**: Streamlit
* **Backend**: FastAPI, Cosdata SDK
* **ML Models**: HuggingFace Transformers, Sentence-Transformers
* **Media Handling**: MoviePy, PDFPlumber, Pillow, OpenCV

---

## Future Improvements

* LLM-based query generation & summarization
* Multilingual support for ingestion and QA
* Real-time collaboration dashboard
* Cloud deployment (AWS, GCP)

---

## Author

**Shikher Jain**
