
#!/bin/bash

echo "Starting CosData…"
docker run -d -p 8443:8443 cosdata/cosdata:latest
sleep 5

# Check CosData health
COSDATA_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8443/health || echo "000")
if [ "$COSDATA_HEALTH" == "200" ]; then
	echo "CosData is running. Using CosData as vector DB."
	export COSDATA_ENABLED=true
else
	echo "CosData not available. Falling back to ChromaDB."
	export COSDATA_ENABLED=false
fi

echo "Starting Backend…"
cd backend
uvicorn main:app --port 8000 &

echo "Starting Frontend…"
cd ../frontend
streamlit run app.py
