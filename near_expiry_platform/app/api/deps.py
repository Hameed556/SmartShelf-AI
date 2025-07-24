from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Placeholder for current user dependency (to be implemented with JWT)
def get_current_user():
    # TODO: Implement JWT-based user extraction
    return None 