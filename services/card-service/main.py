from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uuid
import os

app = FastAPI(title="Card Service")

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
    return {"status": "healthy", "service": "card-service"}

@app.post("/api/v1/cards/issue")
async def issue_card(x_api_key: str = Header(...), user_id: str = "", identity_verified: bool = True):
    await validate_api_key(x_api_key)
    card_token = f"card_{uuid.uuid4().hex[:8]}"
    return {"card_token": card_token, "card_number_masked": "****-****-****-1234", "expires_at": "2027-12-31", "is_biometric_bound": True}

@app.post("/api/v1/cards/authorize")
async def authorize_transaction(x_api_key: str = Header(...), card_token: str = "", amount: float = 0, merchant_id: str = ""):
    await validate_api_key(x_api_key)
    return {"transaction_id": f"tx_{uuid.uuid4().hex[:8]}", "status": "approved", "amount": amount, "remaining_balance": 8500.00}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)