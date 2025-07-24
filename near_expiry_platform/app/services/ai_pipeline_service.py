from app.ai_modules.ocr.extractor import extract_text_from_image
from app.ai_modules.ocr.date_parser import parse_expiry_date
from app.ai_modules.classification.content_classifier import classify_image
from app.ai_modules.duplicate_detection.hash_detector import is_duplicate_hash
from app.ai_modules.duplicate_detection.embedding_detector import is_duplicate_embedding
from app.ai_modules.scoring.confidence_scorer import aggregate_confidence

# LangChain is used for modular chaining, but here we show a simple pipeline

def verify_product_image(image_path: str, expected_expiry: str, product_category: str):
    # Step 1: OCR
    ocr_text, ocr_conf = extract_text_from_image(image_path)
    # Step 2: Expiry date parsing
    detected_expiry, expiry_conf = parse_expiry_date(ocr_text)
    expiry_match = detected_expiry == expected_expiry
    # Step 3: Classification
    class_label, class_conf = classify_image(image_path)
    # Step 4: Duplicate detection
    duplicate_hash = is_duplicate_hash(image_path)
    duplicate_embed = is_duplicate_embedding(image_path)
    # Step 5: Confidence scoring
    score, decision, rationale = aggregate_confidence(
        ocr_conf, expiry_conf, class_conf, duplicate_hash, duplicate_embed, expiry_match
    )
    return {
        "extracted_expiry": detected_expiry,
        "expiry_match": expiry_match,
        "image_classification": class_label,
        "is_duplicate": duplicate_hash or duplicate_embed,
        "confidence_score": score,
        "decision": decision,
        "rationale": rationale
    } 