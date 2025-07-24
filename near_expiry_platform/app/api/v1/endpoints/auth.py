from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/login")
def login():
    # TODO: Implement login (JWT)
    return {"access_token": "fake-token", "token_type": "bearer"}

@router.post("/register")
def register():
    # TODO: Implement user registration
    return {"message": "User registered (placeholder)"} 