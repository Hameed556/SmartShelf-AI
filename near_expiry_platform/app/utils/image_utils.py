from PIL import Image

def check_image_integrity(image_path: str) -> bool:
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def resize_image(image_path: str, size=(256, 256)) -> str:
    with Image.open(image_path) as img:
        img = img.resize(size)
        img.save(image_path)
    return image_path 