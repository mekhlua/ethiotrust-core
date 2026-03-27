from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import secrets
import uuid

app = FastAPI(title="Auth Service - API Key Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store API keys (in production, use database)
# Format: {api_key: {name, email, created_at, usage, last_used}}
api_keys = {}

# Also store keys by user for lookup
user_keys = {}  # {email: api_key}

class KeyRegisterRequest(BaseModel):
    name: str
    email: str
    company: str = None

class KeyResponse(BaseModel):
    api_key: str
    name: str
    email: str
    message: str

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "auth-service"}

@app.post("/api/v1/auth/token")
async def login():
    """Demo login - returns JWT token"""
    return {"access_token": "demo_token_123", "token_type": "bearer"}

@app.post("/api/v1/keys/register", response_model=KeyResponse)
async def register_api_key(request: KeyRegisterRequest):
    """
    Register for an API key
    - Returns a unique API key
    - Key must be used in X-API-Key header for all requests
    """
    # Check if email already has a key
    if request.email in user_keys:
        existing_key = user_keys[request.email]
        return {
            "api_key": existing_key,
            "name": api_keys[existing_key]["name"],
            "email": request.email,
            "message": "You already have an API key. Use your existing key."
        }
    
    # Generate unique API key
    # Format: eth_et_ + 32 random hex characters
    api_key = f"eth_et_{secrets.token_hex(16)}"
    
    # Store the key
    api_keys[api_key] = {
        "name": request.name,
        "email": request.email,
        "company": request.company,
        "created_at": datetime.now().isoformat(),
        "usage": 0,
        "last_used": None
    }
    user_keys[request.email] = api_key
    
    return {
        "api_key": api_key,
        "name": request.name,
        "email": request.email,
        "message": "API key created successfully! Use it in X-API-Key header."
    }

@app.get("/api/v1/keys/validate")
async def validate_api_key(x_api_key: str = Header(...)):
    """
    Validate an API key
    Called by other services to check if a key is valid
    """
    if x_api_key not in api_keys:
        return {"valid": False, "message": "Invalid API key"}
    
    # Update usage stats
    api_keys[x_api_key]["usage"] += 1
    api_keys[x_api_key]["last_used"] = datetime.now().isoformat()
    
    return {
        "valid": True,
        "name": api_keys[x_api_key]["name"],
        "email": api_keys[x_api_key]["email"],
        "usage": api_keys[x_api_key]["usage"]
    }

@app.get("/api/v1/keys/info")
async def get_key_info(x_api_key: str = Header(...)):
    """Get information about your API key"""
    if x_api_key not in api_keys:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "valid": True,
        "name": api_keys[x_api_key]["name"],
        "email": api_keys[x_api_key]["email"],
        "created_at": api_keys[x_api_key]["created_at"],
        "usage": api_keys[x_api_key]["usage"],
        "last_used": api_keys[x_api_key]["last_used"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)