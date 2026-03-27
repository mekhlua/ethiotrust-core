Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "ETHIOTRUST CORE - COMPLETE DEMO" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

Write-Host "`n1️⃣  REGISTERING USER..." -ForegroundColor Yellow
$user = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/identity/register" -Method Post -Body '{"name":"Alemu Bekele","email":"alemu@email.com","id_number":"ETH123456"}' -ContentType "application/json"
Write-Host "✅ User Registered: $($user.user_id)" -ForegroundColor Green

Write-Host "`n2️⃣  ISSUING BIOMETRIC-BOUND CARD..." -ForegroundColor Yellow
$card = Invoke-RestMethod -Uri "http://localhost:8002/api/v1/cards/issue" -Method Post -Body '{"user_id":"alemu@email.com","identity_verified":true}' -ContentType "application/json"
Write-Host "✅ Card Issued: $($card.card_token)" -ForegroundColor Green
Write-Host "   Card Number: $($card.card_number_masked)" -ForegroundColor Cyan
Write-Host "   Biometric Bound: $($card.is_biometric_bound)" -ForegroundColor Cyan

Write-Host "`n3️⃣  MAKING TRANSACTION..." -ForegroundColor Yellow
$tx = Invoke-RestMethod -Uri "http://localhost:8002/api/v1/cards/authorize" -Method Post -Body "{`"card_token`":`"$($card.card_token)`",`"amount`":1500,`"merchant_id`":`"Bank of Abyssinia`"}" -ContentType "application/json"
Write-Host "✅ Transaction Approved!" -ForegroundColor Green
Write-Host "   Amount: $($tx.amount) ETB" -ForegroundColor Cyan
Write-Host "   Balance: $($tx.remaining_balance) ETB" -ForegroundColor Cyan

Write-Host "`n4️⃣  AI METRICS DASHBOARD..." -ForegroundColor Yellow
$metrics = Invoke-RestMethod -Uri "http://localhost:8001/api/v1/ai/metrics/dashboard"
Write-Host "📊 Face Recognition Accuracy: $($metrics.face_recognition.accuracy)%" -ForegroundColor Magenta
Write-Host "🔐 Liveness Detection: $($metrics.liveness_detection.true_positive_rate)%" -ForegroundColor Magenta
Write-Host "📄 OCR Accuracy: $($metrics.ocr.accuracy)%" -ForegroundColor Magenta
Write-Host "⚖️  Fairness Score: $($metrics.bias_metrics.gender_fairness)" -ForegroundColor Magenta

Write-Host "`n5️⃣  SECURITY SERVICE - TOKENIZATION..." -ForegroundColor Yellow
$token = Invoke-RestMethod -Uri "http://localhost:8004/api/v1/security/tokenize" -Method Post -Body '{"card_number":"1234-5678-9012-3456"}' -ContentType "application/json"
Write-Host "✅ Data Tokenized: $($token.token)" -ForegroundColor Green

Write-Host "`n6️⃣  FEDERATED SSO - LOGIN..." -ForegroundColor Yellow
$auth = Invoke-RestMethod -Uri "http://localhost:8003/api/v1/auth/token" -Method Post
Write-Host "✅ Access Token: $($auth.access_token)" -ForegroundColor Green

Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "🎉 DEMO COMPLETE! ETHIOTRUST CORE IS READY! 🎉" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
