from PIL import Image
import imagehash
import os

HASH_DB = {}

# Compute perceptual hash for an image

def compute_image_hash(image_path: str):
    with Image.open(image_path) as img:
        return str(imagehash.phash(img))

# Check if hash is in DB (placeholder, in-memory)
def is_duplicate_hash(image_path: str):
    img_hash = compute_image_hash(image_path)
    for existing_hash in HASH_DB.values():
        if imagehash.hex_to_hash(img_hash) - imagehash.hex_to_hash(existing_hash) < 5:
            return True
    return False 