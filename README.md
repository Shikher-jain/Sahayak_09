# 📘 Multilingual AI Teaching Assistant

### *YouTube + PDF + Images + Audio + Text → Notes • Answers • Summaries (Multilingual)*

### *Built with RAG + Embeddings + CosData Local Vector DB*

---

# 🚀 Features

* Upload **YouTube videos, PDFs, images, audio, or text**
* Automatic **OCR, speech-to-text, keyframe extraction**
* Multilingual support (all HuggingFace-supported languages)
* Embedding + similarity search using **CosData local vector DB**
* Streamlit UI
* Fully local, **no API keys required**
* Fully open-source and offline-capable

---

# 🏁 Quick Start (Anyone Can Use)

> Works on any system: Windows, macOS, Linux.
> No signup, no API keys, no paid services — 100% local.

---

## **1️⃣ Install Docker (Required)**

Download from:
[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

---

## **2️⃣ Start CosData Vector DB (Local Mode)**

Run this in terminal:

```bash
docker run -p 8443:8443 cosdata/cosdata:latest
```

CosData will start at:

```
http://localhost:8443
```

⚠ **Do NOT close this terminal.**
The database must keep running.

---

## **3️⃣ Clone This Repository**

```bash
git clone https://github.com/<your-repo>/sahayak_09.git
cd sahayak_09
```

---

## **4️⃣ Create Python Environment (Python 3.9–3.11)**

```bash
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

---

## **5️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **6️⃣ Set Up Environment Variables**

Create **.env** in root:

```bash
COSDATA_HOST=http://localhost:8443
COSDATA_USER=admin
COSDATA_PASS=admin
```

This works for every user.
No key ███████, no third-party billing.

---

## **7️⃣ Start Backend API**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

---

## **8️⃣ Start Frontend (Streamlit)**

```bash
cd frontend
streamlit run app.py
```

---

# 🧠 Project Architecture

```
sahayak_09/
│
├── backend/
│   ├── main.py
│   ├── ingestion/
│   │   ├── text.py
│   │   ├── pdf.py
│   │   ├── audio.py
│   │   ├── image.py
│   │   └── video.py
│   ├── cosdata_client.py
│   └── utils/
│
├── frontend/
│   ├── app.py
│   └── components/
│       ├── upload.py
│       ├── chat.py
│       └── preview.py
│
└── README.md
```

---

# 🔧 Technologies Used

### **Backend**

* FastAPI
* HuggingFace Transformers
* Sentence-Transformers
* Whisper / OCR
* OpenCV
* CosData Vector DB
* ffmpeg

### **Frontend**

* Streamlit
* Minimal UI, highly extensible

---

# 🧩 Why CosData Local Mode?

* No cloud dependency
* No API key
* No rate limits
* Perfect for open-source apps
* Runs offline
* Faster than Pinecone, Qdrant, Weaviate in local pipelines

Your users only need Docker — nothing else.

---

# 🧪 Testing

Run unit tests:

```bash
pytest
```

---

# 🐛 Troubleshooting

### ❌ **CosData not reachable**

Error:

```
CosData server not reachable at http://localhost:8443
```

Fix → Run CosData:

```bash
docker run -p 8443:8443 cosdata/cosdata:latest
```

---

### ❌ **CV2 import error**

Install OpenCV manually:

```bash
pip install opencv-python-headless
```

---

### ❌ PermissionError on Windows

Run PowerShell as **Administrator**.

---

# 📄 License

MIT — free for academic + commercial use.

---

# 🙌 Contributing

Pull requests welcome.

