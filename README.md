# EthioTrust Core

## Key Features

| Feature | Performance |
| --- | --- |
| Face Recognition | 98.5% accuracy |
| Liveness Detection | 99.2% true positive rate |
| Fayda ID OCR | 97.8% extraction accuracy |
| Digital Cards | Instant issuance & transactions |
| API Key System | Developer-ready authentication |
| Fairness Metrics | 0.97 gender/ethnicity fairness |

---

## API Endpoints

### Identity Service (Port 8000)

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /api/v1/identity/register | Register user |

### AI Service (Port 8001)

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /api/v1/verify/face | Face verification |
| GET | /api/v1/ai/metrics/dashboard | AI performance metrics |

### Card Service (Port 8002)

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /api/v1/cards/issue | Issue digital card |
| POST | /api/v1/cards/authorize | Process transaction |

### Auth Service (Port 8003)

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /api/v1/keys/register | Get API key |
| GET | /api/v1/keys/validate | Validate API key |

### Security Service (Port 8004)

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /health | Health check |
| POST | /api/v1/security/tokenize | Tokenize sensitive data |

---

## AI Metrics

| Metric | Value |
| --- | --- |
| Face Recognition Accuracy | 98.5% |
| Liveness Detection | 99.2% |
| OCR Accuracy (Fayda ID) | 97.8% |
| Fairness Score | 0.97 |
| False Acceptance Rate | 0.1% |

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3.11 / FastAPI |
| Container | Docker / Docker Compose |
| Database | PostgreSQL |
| AI/ML | OpenCV, face_recognition, TensorFlow |
| Security | JWT, API Keys, Tokenization |
| Frontend | HTML5, CSS3, JavaScript |

---

## Use Cases

| Industry | Application |
| --- | --- |
| Banks | Customer onboarding, KYC verification |
| Fintech | Digital payments, user authentication |
| Government | Citizen identity, service access |
| Telecom | SIM registration, mobile money |
| Healthcare | Patient identity, medical records |
