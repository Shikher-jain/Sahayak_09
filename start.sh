#!/bin/bash

echo "Starting CosData…"
docker run -d -p 8443:8443 cosdata/cosdata:latest

echo "Starting Backend…"
cd backend
uvicorn main:app --port 8000 &

echo "Starting Frontend…"
cd ../frontend
streamlit run app.py
