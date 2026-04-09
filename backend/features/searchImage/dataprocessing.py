# dataprocessing.py
# Full CLIP + FAISS data processing pipeline
# Run once: python dataprocessing.py

# ─────────────────────────────────────────────────────────────
# Install dependencies (run once in terminal):
# pip install torch torchvision
# pip install git+https://github.com/openai/CLIP.git
# pip install faiss-cpu
# pip install opencv-python imagehash Pillow tqdm
# ─────────────────────────────────────────────────────────────

import os
import cv2
import torch
import clip
import faiss
import hashlib
import numpy as np
import imagehash
from PIL import Image
from tqdm import tqdm
from torchvision import transforms

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
DATASET_DIR        = "./dataset"
EMBEDDINGS_PATH    = "image_embeddings.pt"
LABELS_PATH        = "image_labels.pt"
FAISS_INDEX_PATH   = "image_index.faiss"
CLIP_MODEL         = "ViT-L/14"      # ← 768-dim embeddings
EMBEDDING_DIM      = 768             # ← must match ViT-L/14
N_AUGMENTS         = 3
BLUR_THRESHOLD     = 80
DARK_THRESHOLD     = 30
BRIGHT_THRESHOLD   = 220
HASH_THRESHOLD     = 5
SEMANTIC_THRESHOLD = 0.97
PATHS_PATH = "image_paths.pt"


# ═════════════════════════════════════════════════════════════
# PHASE 1 — Setup
# ═════════════════════════════════════════════════════════════
def setup():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    model, preprocess = clip.load(CLIP_MODEL, device=device)
    model.eval()
    print(f"CLIP model loaded: {CLIP_MODEL}")
    return model, preprocess, device


# ═════════════════════════════════════════════════════════════
# PHASE 2 — Collect image paths
# Expected structure:
#   dataset/
#     category/
#       location_name/
#         image.jpg
# ═════════════════════════════════════════════════════════════
def collect_image_paths(dataset_dir):
    image_paths = []
    labels = []

    for category in os.listdir(dataset_dir):
        category_path = os.path.join(dataset_dir, category)
        if not os.path.isdir(category_path):
            continue
        for dest in os.listdir(category_path):
            dest_path = os.path.join(category_path, dest)
            if not os.path.isdir(dest_path):
                continue
            for img_file in os.listdir(dest_path):
                if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_paths.append(os.path.join(dest_path, img_file))
                    labels.append(dest)

    print(f"Total images found: {len(image_paths)}")
    print(f"Unique labels: {set(labels)}")
    return image_paths, labels


# ═════════════════════════════════════════════════════════════
# PHASE 3 — Dataset cleaning
# ═════════════════════════════════════════════════════════════
def is_valid_image(path):
    try:
        img = Image.open(path)
        img.verify()
        img = Image.open(path).convert("RGB")
        if img.size[0] < 224 or img.size[1] < 224:
            return False
        return True
    except:
        return False


def is_blurry(path, threshold=BLUR_THRESHOLD):
    img = cv2.imread(path)
    if img is None:
        return True
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return score < threshold


def is_bad_exposure(path, dark_thresh=DARK_THRESHOLD, bright_thresh=BRIGHT_THRESHOLD):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return True
    mean_brightness = img.mean()
    return mean_brightness < dark_thresh or mean_brightness > bright_thresh


def remove_exact_duplicates(image_paths):
    seen_hashes = {}
    unique_paths = []
    duplicates = []
    for path in tqdm(image_paths, desc="Exact dedup"):
        with open(path, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()
        if h in seen_hashes:
            duplicates.append(path)
        else:
            seen_hashes[h] = path
            unique_paths.append(path)
    print(f"  Exact duplicates removed: {len(duplicates)}")
    return unique_paths


def remove_perceptual_duplicates(image_paths, threshold=HASH_THRESHOLD):
    seen_hashes = {}
    unique_paths = []
    duplicates = []
    for path in tqdm(image_paths, desc="Perceptual dedup"):
        try:
            img = Image.open(path).convert("RGB")
            h = imagehash.phash(img)
            is_dup = False
            for existing_path, existing_hash in seen_hashes.items():
                if abs(h - existing_hash) <= threshold:
                    duplicates.append(path)
                    is_dup = True
                    break
            if not is_dup:
                seen_hashes[path] = h
                unique_paths.append(path)
        except Exception as e:
            print(f"  Skipping {path}: {e}")
    print(f"  Perceptual duplicates removed: {len(duplicates)}")
    return unique_paths


def remove_semantic_duplicates(image_paths, model, preprocess, device,
                                threshold=SEMANTIC_THRESHOLD):
    embeddings = []
    valid_paths = []
    for path in tqdm(image_paths, desc="Semantic dedup"):
        try:
            img = Image.open(path).convert("RGB")
            tensor = preprocess(img).unsqueeze(0).to(device)
            with torch.no_grad():
                emb = model.encode_image(tensor)
                emb = emb / emb.norm(dim=-1, keepdim=True)
            embeddings.append(emb.cpu())
            valid_paths.append(path)
        except Exception as e:
            print(f"  Skipping {path}: {e}")

    embeddings = torch.cat(embeddings, dim=0)
    sim_matrix = (embeddings @ embeddings.T).numpy()

    unique_indices = []
    removed = set()
    for i in range(len(valid_paths)):
        if i in removed:
            continue
        unique_indices.append(i)
        for j in range(i + 1, len(valid_paths)):
            if sim_matrix[i][j] >= threshold:
                removed.add(j)

    unique_paths = [valid_paths[i] for i in unique_indices]
    print(f"  Semantic duplicates removed: {len(removed)}")
    return unique_paths


def clean_dataset(image_paths, model, preprocess, device):
    print(f"\nStarting cleaning — {len(image_paths)} images")

    valid = [p for p in tqdm(image_paths, desc="Validity check") if is_valid_image(p)]
    print(f"  Corrupted/too small removed: {len(image_paths) - len(valid)}")

    sharp = [p for p in tqdm(valid, desc="Blur check") if not is_blurry(p)]
    print(f"  Blurry removed: {len(valid) - len(sharp)}")

    exposed = [p for p in tqdm(sharp, desc="Exposure check") if not is_bad_exposure(p)]
    print(f"  Bad exposure removed: {len(sharp) - len(exposed)}")

    unique = remove_exact_duplicates(exposed)
    unique = remove_perceptual_duplicates(unique)
    unique = remove_semantic_duplicates(unique, model, preprocess, device)

    print(f"\nCleaning complete — {len(unique)} clean images remaining")
    return unique


# ═════════════════════════════════════════════════════════════
# PHASE 4 — Augmentation
# ═════════════════════════════════════════════════════════════
safe_augmentation = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1, hue=0.0),
    transforms.RandomRotation(degrees=10),
])


def verify_augmentation_quality(image_paths, model, preprocess, device, n_check=3):
    print("\nVerifying augmentation quality...")
    for path in image_paths[:3]:
        image = Image.open(path).convert("RGB")
        tensor = preprocess(image).unsqueeze(0).to(device)
        with torch.no_grad():
            orig_emb = model.encode_image(tensor)
            orig_emb = orig_emb / orig_emb.norm(dim=-1, keepdim=True)
        for i in range(n_check):
            aug = safe_augmentation(image)
            t = preprocess(aug).unsqueeze(0).to(device)
            with torch.no_grad():
                aug_emb = model.encode_image(t)
                aug_emb = aug_emb / aug_emb.norm(dim=-1, keepdim=True)
            sim = (orig_emb @ aug_emb.T).item()
            status = "GOOD" if sim >= 0.85 else "TOO AGGRESSIVE — reduce augmentation"
            print(f"  {os.path.basename(path)} aug {i+1}: similarity={sim:.4f} [{status}]")


# ═════════════════════════════════════════════════════════════
# PHASE 5 — Generate embeddings
# ═════════════════════════════════════════════════════════════
def generate_embeddings(image_paths, labels, model, preprocess, device):
    
    print(f"\nGenerating embeddings ({N_AUGMENTS} augments per image)...")
    
    all_embeddings = []
    all_labels = []
    all_paths = []

    for path, label in tqdm(zip(image_paths, labels), total=len(image_paths)):
        try:
            image = Image.open(path).convert("RGB")

            # ORIGINAL
            tensor = preprocess(image).unsqueeze(0).to(device)
            with torch.no_grad():
                emb = model.encode_image(tensor)
                emb = emb / emb.norm(dim=-1, keepdim=True)

            all_embeddings.append(emb.cpu())
            all_labels.append(label)
            all_paths.append(path)   # ✅ IMPORTANT

            # AUGMENTED
            for _ in range(N_AUGMENTS):
                aug_image = safe_augmentation(image)
                tensor = preprocess(aug_image).unsqueeze(0).to(device)

                with torch.no_grad():
                    emb = model.encode_image(tensor)
                    emb = emb / emb.norm(dim=-1, keepdim=True)

                all_embeddings.append(emb.cpu())
                all_labels.append(label)
                all_paths.append(path)   # ✅ SAME PATH

        except Exception as e:
            print(f"Skipping {path}: {e}")

    all_embeddings = torch.cat(all_embeddings, dim=0)
    return all_embeddings, all_labels, all_paths


# ═════════════════════════════════════════════════════════════
# PHASE 6 — Verify embeddings
# ═════════════════════════════════════════════════════════════
def verify_embeddings(embeddings):
    print("\nVerifying embeddings...")
    print(f"  Shape : {embeddings.shape}")          # should be (N, 768)
    print(f"  Dtype : {embeddings.dtype}")           # should be torch.float32
    print(f"  Norm  : {embeddings[0].norm():.6f}")   # must be 1.000000
    print(f"  Min   : {embeddings.min():.4f}")
    print(f"  Max   : {embeddings.max():.4f}")

    norms = embeddings.norm(dim=-1)
    bad = (norms - 1.0).abs() > 1e-4
    if bad.any():
        print(f"  WARNING: {bad.sum()} embeddings are not properly normalized!")
    else:
        print("  All embeddings correctly normalized.")


# ═════════════════════════════════════════════════════════════
# PHASE 7 — Save embeddings + build FAISS index
# ═════════════════════════════════════════════════════════════
def save_embeddings(embeddings, labels,paths):
    torch.save(embeddings, EMBEDDINGS_PATH)
    torch.save(labels, LABELS_PATH)
    torch.save(paths, PATHS_PATH)   # ✅ NEW
    print(f"\nSaved embeddings to : {EMBEDDINGS_PATH}")
    print(f"Saved labels to     : {LABELS_PATH}")
    print(f"Saved paths to      : {PATHS_PATH}")
    

def build_faiss_index(embeddings):
    print("\nBuilding FAISS index...")
    embeddings_np = embeddings.numpy().astype("float32")

    # IndexFlatIP = cosine similarity on L2-normalized vectors
    # EMBEDDING_DIM = 768 for ViT-L/14
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embeddings_np)

    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"FAISS index built   : {index.ntotal} vectors")
    print(f"Saved index to      : {FAISS_INDEX_PATH}")
    return index


# ═════════════════════════════════════════════════════════════
# PHASE 8 — Test search
# ═════════════════════════════════════════════════════════════
def test_search(image_path, index, labels, model, preprocess, device, k=3):
    print(f"\nTest search using: {image_path}")
    image = Image.open(image_path).convert("RGB")
    tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        query = model.encode_image(tensor)
        query = query / query.norm(dim=-1, keepdim=True)

    query_np = query.cpu().numpy().astype("float32")   # ← float32 required by FAISS
    distances, indices = index.search(query_np, k=k)

    print(f"Top {k} results:")
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        print(f"  {i+1}. {labels[idx]}  (score: {dist:.4f})")


# ═════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":

    model, preprocess, device = setup()

    image_paths, labels = collect_image_paths(DATASET_DIR)

    clean_paths = clean_dataset(image_paths, model, preprocess, device)

    path_to_label = dict(zip(image_paths, labels))
    clean_labels = [path_to_label[p] for p in clean_paths]

    verify_augmentation_quality(clean_paths, model, preprocess, device)

    all_embeddings, all_labels, all_paths = generate_embeddings(
        clean_paths, clean_labels, model, preprocess, device
    )

    verify_embeddings(all_embeddings)

    save_embeddings(all_embeddings, all_labels, all_paths)
    index = build_faiss_index(all_embeddings)

    test_search(clean_paths[0], index, all_labels, model, preprocess, device, k=3)

    print("\nPipeline complete!")