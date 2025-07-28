# AI Expiry Verification Microservice

This is a minimal FastAPI microservice for AI-powered product expiry verification. It exposes a single `/verify` endpoint that:
- Extracts expiry date from product images (OCR)
- Validates image content (classification)
- Detects duplicate/fake images (hashing & embedding)
- Aggregates a confidence score and decision

## Usage

### Endpoint
`POST /verify`

**Form Data:**
- `image`: (file) Product image
- `expected_expiry`: (str) Expected expiry date (e.g., 04/2025)
- `product_category`: (str) Product category (e.g., food)

**Response:**
```json
{
  "extracted_expiry": "04/2025",
  "expiry_match": true,
  "image_classification": "food_product",
  "is_duplicate": false,
  "confidence_score": 91,
  "decision": "approve",
  "rationale": "OCR confidence high, Expiry date matches, Classification confidence high, No duplicate detected"
}
```

## Running Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Docker
```bash
docker build -t ai-expiry-api .
docker run -p 8000:8000 ai-expiry-api
```

## Environment Variables
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Vision service account JSON

## Deployment
- Ready for Railway, Render, or any cloud platform supporting Docker.

---
MIT License 