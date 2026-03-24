from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
import torch
import clip
import faiss
import os
from PIL import Image  #python imaging library, used for open img, resize img preprocess etc
import io   #It is used to convert raw bytes into something PIL can read.
from backend.logger import logger

device= 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f"Image search using device: {device}")

try:
    model, preprocess = clip.load('ViT-B/32', device=device)
    model.eval()
    logger.info("CLIP model loaded successfully")
except Exception as e:
    logger.critical(f"Failed to load CLIP model: {e}")
    raise

try:
    index_path = os.path.join(os.path.dirname(__file__), "image_index.faiss")
    index = faiss.read_index(index_path)
    logger.info(f"FAISS index loaded: {index_path}")
except Exception as e:
    logger.critical(f"Failed to load FAISS index: {e}")
    raise

dataset_folder = "backend/features/searchImage/dataset"
file_paths=[]
for root, dirs, files in os.walk(dataset_folder):
    dirs.sort()
    files.sort()
    for file in files:
        if file.endswith(("jpg","jpeg","png")):
            rel_path= os.path.relpath(os.path.join(root, file), dataset_folder).replace("\\","/")
            file_paths.append(rel_path)
#print(file_paths[2])
logger.info(f"Dataset loaded: {len(file_paths)} images found")

try:
    all_labels=os.path.join(os.path.dirname(__file__), "image_labels.pt")
    all_labels = torch.load(all_labels)
    if isinstance(all_labels, torch.Tensor):
        all_labels= all_labels.tolist() 
    logger.info(f"Labels loaded: {len(all_labels)} labels")
except Exception as e:
    logger.critical(f"Failed to load image labels: {e}")
    raise

#print(all_labels)
#clip is a pytorch based model
router= APIRouter(prefix='/img_based_search',tags=['img_based_search'])

@router.post('/')
async def img_based_search(img:UploadFile= File(...)):
    logger.info(f"Image search requested — file:{img.filename}")
    try:
        #print("hiii")
        img_bytes= await img.read()
        #print("hi 2")
        PIL_img= Image.open(io.BytesIO(img_bytes)).convert('RGB')
        #print("hi 3")
        #Image.open() expects a file-like object. BytesIO?It converts raw bytes into a fake in-memory file.
        image_input= preprocess(PIL_img).unsqueeze(0).to(device)# WE SHOULD GIVE A PIL IMAGE TO PREPROCESS 
        #print("hi 4")
        with torch.no_grad(): # we are not training a model, so torch.no grad, (only output, no  training the model)
            embedding= model.encode_image(image_input) 
            #print("hi 5") #That operation is using PyTorch tensors.
            embedding= embedding/embedding.norm(dim=-1, keepdim=True)
        #print("hi 6")
        embedding= embedding.cpu().numpy()
        #print("hi 7")
        D,I= index.search(embedding, k=3)
        #print("hi 8")
        results=[]
        for idx in I[0]:
            #if idx < len(file_paths):
               #print("hi 9")
               results.append({
                "label": all_labels[idx],
                "image_url": f"/dataset/{file_paths[idx]}"  # use relative path
            })
        #print("hi 10")
        #print(results)
        logger.info(f"Image search completed — results:{len(results)} file:{img.filename}")
        return {"results":results}

    except Image.UnidentifiedImageError:
        logger.warning(f"Invalid image file uploaded: {img.filename}")
        raise HTTPException(status_code=400, detail="Invalid image file. Please upload a valid JPG or PNG.")

    except IndexError as e:
        logger.error(f"Index out of range in image search: {e}")
        raise HTTPException(status_code=500, detail="Search index error. Please try again.")

    except Exception as e:
        logger.critical(f"Image search crashed: {e} — file:{img.filename}")
        raise HTTPException(status_code=500, detail="Image search failed. Please try again.")

    
    
    # .pt files are PyTorch tensors — not FAISS index. so we use .faiss file
    #in notebook, we use torch.cat because fasii does not accept list of tensors, it accepts single 2D array:
#(num_images, embedding_dimension), think we have (1,512), (1,512),.. so on. fasii doesnt accept them all, so using toch.concat we combine them then,m we feed 
#(2, 512) to faiss. in the fast api code we  only have one image, so no need of concat
# clip outputs pytorch tensors
#FAISS does NOT understand torch tensors. faiss accepts numpy arrays
#FAISS wants: NumPy array ,dtype = float32, shape = (num_vectors, dimension)
#before adding to FAISS you must do:
#embeddings = embeddings.numpy().astype("float32")
#FAISS returns TWO numpy arrays: I,D
#D = distances
#Shape:(1, k)
#These are similarity scores (L2 distances if using IndexFlatL2).
#I = indices
#Shape:(1, k)
#These are positions of the most similar images.
#Example:
#I = [[25, 100, 7]]
#That means:Most similar image = image 25, Second = image 100, Third = image 7




#pip install git+https://github.com/openai/CLIP.git