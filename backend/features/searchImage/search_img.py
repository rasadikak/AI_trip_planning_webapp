# img_based_search.py
# FastAPI router — loads saved index and handles image search requests

from fastapi import APIRouter, File, UploadFile, HTTPException
import torch
import clip
import faiss
import os
from PIL import Image
import io
from backend.logger import logger

# ─────────────────────────────────────────────────────────────
# CONFIG — must match dataprocessing.py
# ─────────────────────────────────────────────────────────────
CLIP_MODEL    = "ViT-L/14"   # ← same as dataprocessing.py
EMBEDDING_DIM = 768          # ← 768 for ViT-L/14, 512 for ViT-B/32
TOP_K         = 3

# ─────────────────────────────────────────────────────────────
# Device
# ─────────────────────────────────────────────────────────────
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Image search using device: {device}")

# ─────────────────────────────────────────────────────────────
# Load CLIP model
# ─────────────────────────────────────────────────────────────
try:
    model, preprocess = clip.load(CLIP_MODEL, device=device)
    model.eval()
    logger.info(f"CLIP model loaded: {CLIP_MODEL}")
except Exception as e:
    logger.critical(f"Failed to load CLIP model: {e}")
    raise

# ─────────────────────────────────────────────────────────────
# Load FAISS index
# ─────────────────────────────────────────────────────────────
try:
    index_path = os.path.join(os.path.dirname(__file__), "image_index.faiss")
    index = faiss.read_index(index_path)
    logger.info(f"FAISS index loaded: {index.ntotal} vectors from {index_path}")
except Exception as e:
    logger.critical(f"Failed to load FAISS index: {e}")
    raise

# ─────────────────────────────────────────────────────────────
# Load labels
# ─────────────────────────────────────────────────────────────
try:
    labels_path = os.path.join(os.path.dirname(__file__), "image_labels.pt")
    all_labels = torch.load(labels_path)
    if isinstance(all_labels, torch.Tensor):
        all_labels = all_labels.tolist()
    logger.info(f"Labels loaded: {len(all_labels)} labels")
except Exception as e:
    logger.critical(f"Failed to load labels: {e}")
    raise

# ─────────────────────────────────────────────────────────────
# Collect file paths (for returning image URLs)
# ─────────────────────────────────────────────────────────────
paths_path = os.path.join(os.path.dirname(__file__), "image_paths.pt")

try:
    file_paths = torch.load(paths_path)

    # convert to relative path for API (IMPORTANT)
    dataset_folder = "backend/features/searchImage/dataset"
    file_paths = [
        os.path.relpath(p, dataset_folder).replace("\\", "/")
        for p in file_paths
    ]

    logger.info(f"Paths loaded: {len(file_paths)}")
except Exception as e:
    logger.critical(f"Failed to load paths: {e}")
    raise
logger.info(f"Dataset loaded: {len(file_paths)} images found")

# ─────────────────────────────────────────────────────────────
# Sanity check — catch mismatches before any request hits
# ─────────────────────────────────────────────────────────────
if index.ntotal != len(all_labels):
    logger.critical(
        f"Mismatch: FAISS has {index.ntotal} vectors but labels has {len(all_labels)}"
    )
    raise RuntimeError("FAISS index and labels are out of sync. Re-run dataprocessing.py.")

# ─────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────
router = APIRouter(prefix="/img_based_search", tags=["img_based_search"])


@router.post("/")
async def img_based_search(img: UploadFile = File(...)):
    logger.info(f"Image search requested — file: {img.filename}")
    try:
        # Read uploaded bytes → PIL image
        img_bytes = await img.read()
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Preprocess → CLIP embedding
        image_input = preprocess(pil_img).unsqueeze(0).to(device)
        with torch.no_grad():
            embedding = model.encode_image(image_input)
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)

        # Convert to float32 numpy — required by FAISS
        embedding_np = embedding.cpu().numpy().astype("float32")

        # Search
        D, I = index.search(embedding_np, k=TOP_K)

        # Build results
        results = []
        for dist, idx in zip(D[0], I[0]):
            similarity_percent = round(float(dist) * 100, 1)  # cosine score → percentage
            #print("💡Similarity:", similarity_percent)
            results.append({
                "label":            all_labels[idx],
                "image_url":        f"/dataset/{file_paths[idx]}",
                "similarity":       similarity_percent         
            })

        logger.info(f"Image search completed — {len(results)} results for {img.filename}")
        return {"results": results}

    except Image.UnidentifiedImageError:
        logger.warning(f"Invalid image uploaded: {img.filename}")
        raise HTTPException(
            status_code=400,
            detail="Invalid image file. Please upload a valid JPG or PNG."
        )

    except IndexError as e:
        logger.error(f"Index out of range: {e}")
        raise HTTPException(
            status_code=500,
            detail="Search index error. Please try again."
        )

    except Exception as e:
        logger.critical(f"Image search crashed: {e} — file: {img.filename}")
        raise HTTPException(
            status_code=500,
            detail="Image search failed. Please try again."
        )