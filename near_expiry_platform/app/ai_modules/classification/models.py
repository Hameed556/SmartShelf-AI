import torch
from torchvision import models, transforms
from PIL import Image

# Load a pretrained MobileNetV2 model
_model = None

IMAGENET_LABELS = [
    'background', 'tench', 'goldfish', 'great white shark', 'tiger shark', 'hammerhead', 'electric ray', 'stingray',
    # ... (truncated for brevity, you can download full ImageNet labels if needed)
    'toilet tissue'
]

def load_model():
    global _model
    if _model is None:
        _model = models.mobilenet_v2(pretrained=True)
        _model.eval()
    return _model

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return transform(img).unsqueeze(0) 