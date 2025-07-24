# Near-Expiry Product Discount Platform

This is a production-grade FastAPI backend for an AI-powered platform enabling vendors to sell nearly-expired goods at discounts. The system verifies product authenticity and expiry via image analysis and OCR, flags suspicious items, and manages workflow via a modular backend architecture.

## Features
- Product image upload and expiry verification
- Google Vision OCR integration for expiry/batch extraction
- Image content classification (valid product detection)
- Duplicate/fake image detection (perceptual hash & deep embedding)
- AI confidence scoring and workflow automation
- Admin review endpoints for flagged items
- Modular, extensible AI pipeline (LangChain-powered)
- JWT authentication and user management
- Dockerized for production

## Project Structure
```
near_expiry_platform/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Environment-based configuration
│   │   └── database.py         # Database connection setup
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Authentication & authorization
│   │   ├── exceptions.py       # Custom exception handlers
│   │   └── middleware.py       # Custom middleware
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py      # Main API router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── products.py    # Product verification endpoints
│   │           ├── admin.py       # Admin endpoints
│   │           ├── auth.py        # Authentication endpoints
│   │           └── health.py      # Health check endpoints
│   ├── ai_modules/
│   │   ├── __init__.py
│   │   ├── base.py            # Base AI module interface
│   │   ├── ocr/
│   │   │   ├── __init__.py
│   │   │   ├── extractor.py   # OCR text extraction
│   │   │   └── date_parser.py # Date parsing logic
│   │   ├── classification/
│   │   │   ├── __init__.py
│   │   │   ├── content_classifier.py  # Image content validation
│   │   │   └── models.py      # ML model loading/inference
│   │   ├── duplicate_detection/
│   │   │   ├── __init__.py
│   │   │   ├── hash_detector.py       # Perceptual hashing
│   │   │   └── embedding_detector.py  # Deep embedding comparison
│   │   └── scoring/
│   │       ├── __init__.py
│   │       └── confidence_scorer.py   # Confidence aggregation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py     # Product business logic
│   │   ├── ai_pipeline_service.py # AI processing orchestration
│   │   ├── file_service.py        # File upload/storage handling
│   │   └── notification_service.py # Email/SMS notifications
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py        # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   └── enums.py          # Enumerations
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py           # Base CRUD operations
│   │   ├── product.py        # Product CRUD
│   │   └── user.py           # User CRUD
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py    # Image processing utilities
│   │   ├── date_utils.py     # Date parsing utilities
│   │   └── logging.py        # Logging configuration
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py       # Pytest configuration
│       ├── test_api/
│       ├── test_ai_modules/
│       └── test_services/
├── migrations/               # Alembic database migrations
├── scripts/
│   ├── init_db.py           # Database initialization
│   └── deploy.py            # Deployment scripts
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── docker-compose.prod.yml
├── requirements/
│   ├── base.txt             # Base dependencies
│   ├── dev.txt              # Development dependencies
│   └── prod.txt             # Production dependencies
├── .env.example
├── .gitignore
├── README.md
└── pyproject.toml
```

## Tech Stack
- FastAPI, Pydantic, SQLAlchemy
- Google Vision API (OCR)
- PyTorch/TensorFlow (image classification)
- ImageHash, CLIP/FAISS (duplicate detection)
- LangChain (AI pipeline orchestration)
- Docker, Alembic, Pytest

---

## Setup
1. Clone the repo
2. Install dependencies from `requirements/`
3. Configure environment variables (`.env`)
4. Run database migrations
5. Start the FastAPI app

---

## License
MIT 