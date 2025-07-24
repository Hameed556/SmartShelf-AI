from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import verify_api_key

router = APIRouter()

@router.get("/flagged", dependencies=[Depends(verify_api_key)])
def list_flagged_products(db: Session = Depends(get_db)):
    # TODO: List flagged products for admin review
    return []

@router.post("/review/{product_id}", dependencies=[Depends(verify_api_key)])
def review_product(product_id: int, decision: str, db: Session = Depends(get_db)):
    # TODO: Approve or reject product
    return {"product_id": product_id, "decision": decision} 