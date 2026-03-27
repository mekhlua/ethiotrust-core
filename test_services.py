# test_services.py
import httpx
import asyncio

async def test_services():
    """Test all EthioTrust Core services"""
    
    services = {
        "Identity Service": "http://localhost:8000/health",
        "AI Verification": "http://localhost:8001/health",
        "Card Service": "http://localhost:8002/health",
        "Auth Service": "http://localhost:8003/health",
        "Security Service": "http://localhost:8004/health",
        "API Gateway": "http://localhost/health"
    }
    
    print("=" * 50)
    print("EthioTrust Core - Service Health Check")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        for name, url in services.items():
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ {name}: OK - {url}")
                else:
                    print(f"⚠️  {name}: Status {response.status_code} - {url}")
            except Exception as e:
                print(f"❌ {name}: FAILED - {url}")
                print(f"   Error: {str(e)}")
    
    print("=" * 50)
    
    # Test card issuance workflow
    print("\n📱 Testing Card Issuance Workflow:")
    try:
        # Issue a card
        card_response = await client.post(
            "http://localhost:8002/api/v1/cards/issue",
            json={
                "user_id": "test@example.com",
                "identity_verified": True,
                "biometric_template": "test_biometric_hash"
            }
        )
        
        if card_response.status_code == 200:
            card_data = card_response.json()
            print(f"✅ Card Issued: Token={card_data['card_token'][:8]}...")
            
            # Test transaction
            tx_response = await client.post(
                "http://localhost:8002/api/v1/cards/authorize",
                json={
                    "card_token": card_data['card_token'],
                    "amount": 1000,
                    "merchant_id": "test_merchant"
                }
            )
            
            if tx_response.status_code == 200:
                tx_data = tx_response.json()
                print(f"✅ Transaction Approved: {tx_data['transaction_id'][:8]}...")
            else:
                print(f"⚠️  Transaction failed: {tx_response.status_code}")
        else:
            print(f"⚠️  Card issuance failed: {card_response.status_code}")
            
    except Exception as e:
        print(f"❌ Workflow test failed: {str(e)}")
    
    print("\n📊 AI Metrics Dashboard:")
    try:
        metrics_response = await client.get("http://localhost:8001/api/v1/ai/metrics/dashboard")
        if metrics_response.status_code == 200:
            metrics = metrics_response.json()
            print(f"✅ Face Recognition Accuracy: {metrics['face_recognition']['accuracy']}%")
            print(f"✅ Liveness Detection: {metrics['liveness_detection']['true_positive_rate']}%")
        else:
            print(f"⚠️  Metrics unavailable: {metrics_response.status_code}")
    except Exception as e:
        print(f"❌ Metrics test failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_services())