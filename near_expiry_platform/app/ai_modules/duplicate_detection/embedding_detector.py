import torch
import numpy as np
import faiss
from PIL import Image
import clip

# Load CLIP model
clip_model, preprocess = clip.load("ViT-B/32", device="cpu")

# In-memory FAISS index (for demo)
EMBEDDING_DIM = 512
faiss_index = faiss.IndexFlatL2(EMBEDDING_DIM)
embedding_db = []  # To map index to image paths (for demo)


def compute_clip_embedding(image_path: str):
    image = preprocess(Image.open(image_path)).unsqueeze(0)
    with torch.no_grad():
        embedding = clip_model.encode_image(image).cpu().numpy().astype(np.float32)
    return embedding / np.linalg.norm(embedding)


def is_duplicate_embedding(image_path: str, threshold: float = 0.95):
    embedding = compute_clip_embedding(image_path)
    if faiss_index.ntotal == 0:
        faiss_index.add(embedding)
        embedding_db.append(image_path)
        return False
    D, I = faiss_index.search(embedding, k=1)
    similarity = 1 - D[0][0] / 2  # L2 to cosine similarity approx
    if similarity > threshold:
        return True
    faiss_index.add(embedding)
    embedding_db.append(image_path)
    return False 