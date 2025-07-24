from sqlalchemy.orm import Session
from app.models.database import Product
from app.models.schemas import ProductCreate
from typing import List

def create_product(db: Session, product_in: ProductCreate, owner_id: int, image_url: str):
    product = Product(
        name=product_in.name,
        description=product_in.description,
        image_url=image_url,
        expiry_date=product_in.expiry_date,
        batch_number=product_in.batch_number,
        owner_id=owner_id,
        status="pending",
        confidence_score=0.0
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def list_flagged_products(db: Session) -> List[Product]:
    return db.query(Product).filter(Product.status == "flagged").all() 