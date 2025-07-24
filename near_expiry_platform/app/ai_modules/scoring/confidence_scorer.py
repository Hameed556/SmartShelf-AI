def aggregate_confidence(ocr_conf, expiry_conf, class_conf, is_duplicate_hash, is_duplicate_embed, expiry_match):
    score = 0.0
    rationale = []
    if ocr_conf > 0.7:
        score += 0.25
        rationale.append("OCR confidence high")
    if expiry_conf > 0.7 and expiry_match:
        score += 0.25
        rationale.append("Expiry date matches")
    if class_conf > 0.7:
        score += 0.25
        rationale.append("Classification confidence high")
    if not is_duplicate_hash and not is_duplicate_embed:
        score += 0.25
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