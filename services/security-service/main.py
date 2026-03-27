from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uuid
import os

app = FastAPI(title="Security Service")

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
    return {"status": "healthy", "service": "security-service"}

@app.post("/api/v1/security/tokenize")
async def tokenize(x_api_key: str = Header(...), data: dict = {}):
    await validate_api_key(x_api_key)
    return {"token": f"tok_{uuid.uuid4().hex[:16]}", "message": "Data tokenized"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)