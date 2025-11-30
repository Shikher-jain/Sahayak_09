# backend/auth.py

from fastapi import Header, HTTPException

# Simple API key store (in production, use secure DB)
API_KEYS = {
    "demo-key-123": "user1",
    "hackathon-key": "team_cosdata"
}

def api_key_auth(x_api_key: str = Header(...)):
    """
    Simple API key authentication for FastAPI endpoints
    """
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return API_KEYS[x_api_key]
