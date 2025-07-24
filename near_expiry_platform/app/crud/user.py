from sqlalchemy.orm import Session
from app.models.database import User
from app.models.schemas import UserCreate
from app.core.security import hash_password

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 