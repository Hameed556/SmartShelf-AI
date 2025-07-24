from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Security
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.security import verify_api_key
from app.services.file_service import save_upload_file
from app.services.ai_pipeline_service import verify_product_image
from app.crud.product import create_product, get_product
from app.models.schemas import ProductCreate, ProductRead

router = APIRouter()

@router.post("/upload", response_model=dict, dependencies=[Depends(verify_api_key)])
def upload_product(
    image: UploadFile = File(...),
    expected_expiry: str = Form(...),
    product_category: str = Form(...),
    owner_id: int = Form(...),  # In production, get from JWT
    db: Session = Depends(get_db)
):
    # 1. Save image
    image_path = save_upload_file(image)
    # 2. Run AI pipeline
    ai_result = verify_product_image(image_path, expected_expiry, product_category)
    # 3. Store product in DB
    product_in = ProductCreate(
        name=product_category,
        description=None,
        image_url=image_path,
        expiry_date=expected_expiry,
        batch_number=None
    )
    product = create_product(db, product_in, owner_id, image_path)
    # 4. Update product with AI result (status, confidence)
    product.status = ai_result["decision"]
    product.confidence_score = ai_result["confidence_score"]
    db.commit()
    db.refresh(product)
    # 5. Return structured response
    return {
        "product_id": product.id,
        **ai_result
    }

@router.get("/status/{product_id}", response_model=ProductRead, dependencies=[Depends(verify_api_key)])
def get_product_status(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product 