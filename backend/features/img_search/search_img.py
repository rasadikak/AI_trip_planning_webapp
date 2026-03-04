from fastapi import FastAPI, APIRouter, File, UploadFile
import torch
import clip
import faiss


from PIL import Image  #python imaging library, used for open img, resize img preprocess etc
import io   #It is used to convert raw bytes into something PIL can read.

device= 'cuda' if torch.cuda.is_available() else 'cpu'
model,preprocess= clip.load('ViT-B/32', device=device)
model.eval()


index= faiss.read_index("image_index.faiss")



all_labels = torch.load("backend/features/img_search/img_labels.pt")
all_labels = all_labels.tolist()  # convert to Python list
print(all_labels)

#clip is a pytorch based model

router= APIRouter(prefix='/img_based_search')

router.post('/')
async def img_based_search(img:UploadFile= File()):
    img_bytes= await img.read()
    PIL_img= Image.open(io.BytesIO(img_bytes)).convert('RGB')
    #Image.open() expects a file-like object. BytesIO?It converts raw bytes into a fake in-memory file.
    image_input= preprocess(PIL_img).unsqueeze(0).to(device)# WE SHOULD GIVE A PIL IMAGE TO PREPROCESS 
    with torch.no_grad(): # we are not training a model, so torch.no grad, (only output, no  training the model)
        embedding= model.encode_image(image_input)  #That operation is using PyTorch tensors.
        embedding= embedding/embedding.norm(dim=-1, keepdim=True)
    embedding= embedding.cpu().numpy()
    D,I= index.search(embedding, k=3)


    indices= I.to_list()
    img_id=indices.find('image_embeddings.pt')
    photos =img_id.find('image_labels.pt')
    
    
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