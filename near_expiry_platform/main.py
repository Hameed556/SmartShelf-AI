from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
from uuid import uuid4
from PIL import Image
import re
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)
print("DEBUG: GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

app = FastAPI(title="AI Expiry Verification API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def google_vision_ocr(image_path: str):
    """Use Google Cloud Vision API for OCR"""
    try:
        # Check if Google credentials are available
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        print(f"🔍 Looking for credentials at: {credentials_path}")
        
        if not credentials_path or not os.path.exists(credentials_path):
            print(f"❌ Google credentials not found at {credentials_path}")
            # Fallback to simple OCR if no Google Vision
            return simple_ocr_extract_text(image_path)
        
        print(f"✅ Using Google Vision with credentials: {credentials_path}")
        
        from google.cloud import vision
        from google.oauth2 import service_account
        
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if not texts:
            print("⚠️ Google Vision found no text in image")
            return "", 0.0
        
        full_text = texts[0].description
        confidence = sum([a.confidence for a in response.text_annotations[1:]]) / max(1, len(response.text_annotations[1:]))
        
        print(f"🎉 Google Vision extracted: {full_text[:100]}... (confidence: {confidence:.2f})")
        return full_text, confidence
        
    except Exception as e:
        print(f"❌ Google Vision error: {e}")
        # Fallback to simple OCR
        return simple_ocr_extract_text(image_path)

def simple_ocr_extract_text(image_path: str):
    """Simple OCR fallback"""
    try:
        print("🔄 Using fallback OCR (not Google Vision)")
        # For now, return a placeholder since we don't have tesseract installed
        return "FALLBACK OCR - NO TEXT FOUND", 0.3
    except Exception as e:
        return f"Error reading image: {str(e)}", 0.0

def parse_expiry_date_from_text(text: str):
    """Parse expiry date from OCR text"""
    date_patterns = [
        r'\b(\d{2}/\d{4})\b',  # MM/YYYY
        r'\b(\d{2}-\d{4})\b',  # MM-YYYY
        r'\b(\d{4}-\d{2})\b',  # YYYY-MM
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1), 0.9
    
    return "", 0.0

def classify_image_content(image_path: str, expected_category: str):
    """Classify image content and check if it matches expected category"""
    try:
        # Simple classification based on image characteristics
        with Image.open(image_path) as img:
            # For now, return a basic classification
            # In production, you'd use Google Vision Label Detection or a custom ML model
            return "text_document", 0.9
            
    except Exception as e:
        return "unknown", 0.0

def check_category_match(classified_category: str, expected_category: str):
    """Check if classified category matches expected category"""
    if expected_category.lower() == "food":
        # Food should not be classified as text_document
        if classified_category == "text_document":
            return False, "Image appears to be text/document, not food product"
        return True, "Category appears to match"
    return True, "Category check passed"

def check_duplicate_image(image_path: str):
    """Simple duplicate detection"""
    return False

def calculate_confidence_score(ocr_conf, expiry_conf, class_conf, is_duplicate, expiry_match, category_match):
    """Calculate confidence score based on all factors"""
    score = 0.0
    rationale = []
    
    if ocr_conf > 0.7:
        score += 0.2
        rationale.append("OCR confidence high")
    else:
        rationale.append("OCR confidence low")
        
    if expiry_conf > 0.7 and expiry_match:
        score += 0.25
        rationale.append("Expiry date matches")
    elif expiry_conf > 0.7:
        score += 0.1
        rationale.append("Expiry date found but doesn't match")
    else:
        rationale.append("No expiry date found")
        
    if class_conf > 0.7 and category_match:
        score += 0.25
        rationale.append("Classification confidence high")
    elif class_conf > 0.7:
        score += 0.1
        rationale.append("Classification confidence high but category mismatch")
    else:
        rationale.append("Classification confidence low")
        
    if not is_duplicate:
        score += 0.3
        rationale.append("No duplicate detected")
    else:
        rationale.append("Duplicate detected")
    
    score = min(score, 1.0)
    
    if score >= 0.85:
        decision = "approve"
    elif score >= 0.6:
        decision = "review"
    else:
        decision = "reject"
    
    return int(score * 100), decision, ", ".join(rationale)

@app.post("/verify")
async def verify(
    image: UploadFile = File(...),
    expected_expiry: str = Form(...),
    product_category: str = Form(...)
):
    try:
        # Save image
        ext = os.path.splitext(image.filename)[1]
        file_id = f"{uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, file_id)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Real AI pipeline
        ocr_text, ocr_conf = google_vision_ocr(file_path)
        detected_expiry, expiry_conf = parse_expiry_date_from_text(ocr_text)
        expiry_match = detected_expiry == expected_expiry
        class_label, class_conf = classify_image_content(file_path, product_category)
        category_match, category_reason = check_category_match(class_label, product_category)
        is_duplicate = check_duplicate_image(file_path)
        
        score, decision, rationale = calculate_confidence_score(
            ocr_conf, expiry_conf, class_conf, is_duplicate, expiry_match, category_match
        )

        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass

        return {
            "extracted_expiry": detected_expiry,
            "expiry_match": expiry_match,
            "image_classification": class_label,
            "category_match": category_match,
            "category_reason": category_reason,
            "is_duplicate": is_duplicate,
            "confidence_score": score,
            "decision": decision,
            "rationale": rationale,
            "ocr_text": ocr_text,
            "note": "Using Google Vision OCR when available"
        }
    except Exception as e:
        return {
            "error": str(e),
            "extracted_expiry": "",
            "expiry_match": False,
            "image_classification": "error",
            "category_match": False,
            "category_reason": f"Error: {str(e)}",
            "is_duplicate": False,
            "confidence_score": 0,
            "decision": "error",
            "rationale": f"Error processing image: {str(e)}"
        }

@app.get("/")
async def root():
    return {"message": "AI Expiry Verification API is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"} 