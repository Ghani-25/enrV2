import numpy as np
import pandas as pd
import pickle
import gdown
import torch
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("Ghani-25/LF_enrich_sim", device='cpu')
url = "https://huggingface.co/datasets/Ghani-25/Embeddings_full_Enrichments/resolve/main/Embeddings_full"
output = "Embeddings_full"
gdown.download(url, output, quiet=False)
with open("./Embeddings_full", "rb") as fp:
  Embeddings = pickle.load(fp)
url = "https://drive.google.com/uc?export=download&id=1TyATJx0l5J3eVQ7PXx9zsZop4x1M1Ux6"
OccClean = "occupationClean.csv"
gdown.download(url, OccClean, quiet=False)
occPd = pd.read_csv('./occupationClean.csv', lineterminator='\n', on_bad_lines='skip', header=0, encoding='UTF-8')
def enrichir(tab, count):
    #Compute cosine-similarities with all embeddings
    query = '. '.join(tab)
    query_embedd = model.encode(query)
    cosine_scores = util.pytorch_cos_sim(query_embedd, Embeddings)
    Similarities = torch.sort(cosine_scores,descending=True)
    print('Les taux de similarités sont :', Similarities)
    top_matches = torch.argsort(cosine_scores, dim=-1, descending=True).tolist()[0][0:count]
    print(top_matches)
    results=[]
    for index in top_matches:
      results.append(occPd.iloc[index,1])
    return results
