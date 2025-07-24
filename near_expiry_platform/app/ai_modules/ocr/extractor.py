import os
from google.cloud import vision
from google.oauth2 import service_account

def extract_text_from_image(image_path: str):
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if not texts:
        return "", 0.0
    full_text = texts[0].description
    confidence = sum([a.confidence for a in response.text_annotations[1:]]) / max(1, len(response.text_annotations[1:]))
    return full_text, confidence 