from fastapi import FastAPI, APIRouter, File, UploadFile
import torch
import clip
import faiss
from data_preprocess import index

device= 'cuda' if torch.cuda.is_available() else 'cpu'
model,preprocess= clip.load('ViT-B/32', device=device)
model.eval()






router= APIRouter(prefix='/img_based_search')

router.post('/')
def img_based_search(img:UploadFile= File()):
     
    pass



def search_embeddings(img):
    image_input= preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding= model.encode_image(image_input)
        embedding= embedding/embedding.norm(dim=-1, keepdim=True)
    embedding= torch.cat(embedding, dim=0)
    output= index.search(embedding, k=3)
    print(output)

