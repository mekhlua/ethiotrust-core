from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="Identity Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8003")

async def validate_api_key(x_api_key: str = Header(...)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{AUTH_SERVICE_URL}/api/v1/keys/validate",
                headers={"X-API-Key": x_api_key},
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return data
            raise HTTPException(status_code=401, detail="Invalid API key")
    except Exception as e:
        raise HTTPException(status_code=401, detail="API key validation failed")

@app.get("/health")
async def health(x_api_key: str = Header(...)):
    await validate_api_key(x_api_key)
    return {"status": "healthy", "service": "identity-service"}

@app.post("/api/v1/identity/register")
async def register_user(x_api_key: str = Header(...), name: str = "", email: str = "", id_number: str = ""):
    await validate_api_key(x_api_key)
    return {"user_id": "user_123", "status": "registered", "verified": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)