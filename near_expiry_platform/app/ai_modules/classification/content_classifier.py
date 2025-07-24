from .models import load_model, preprocess_image, IMAGENET_LABELS
import torch
import torch.nn.functional as F

def classify_image(image_path: str):
    model = load_model()
    input_tensor = preprocess_image(image_path)
    with torch.no_grad():
        output = model(input_tensor)
        probs = F.softmax(output[0], dim=0)
        conf, idx = torch.max(probs, 0)
        label = IMAGENET_LABELS[idx] if idx < len(IMAGENET_LABELS) else str(idx.item())
        return label, float(conf) 