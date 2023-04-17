import numpy as np
import pandas as pd
import torch
import pinecone
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("Ghani-25/LF_enrich_sim", device='cpu')
pinecone.init(api_key='16146b33-2d76-4f3a-b03b-92fb81d42a42', environment='us-east4-gcp')
index = pinecone.Index('aiprospects')
#url = "https://drive.google.com/uc?export=download&id=1rQc3XpyzW3a2l1m6ewqq_iBvot2sS4aY"
#OccClean = "occupationClean5m.csv"
#gdown.download(url, OccClean, quiet=False)
#occupation = pd.read_csv('./occupationClean5m.csv', sep=',', lineterminator='\n', on_bad_lines='skip', header=0, encoding='UTF-8')
def enrichir(query):
    xq = modell.encode([query]).tolist()
    result = index.query(xq, top_k=30, includeMetadata=False)
    res = result.to_dict() #conversion to dict
    lis = list(res.values())[0]
    #Liste_enrichie = pd.DataFrame(lis)
    #Liste_enrichie = Liste_enrichie.rename(columns={"id": "linkedinId"})
    #Liste_enrichie['linkedinId'] = Liste_enrichie['linkedinId'].astype(float)
    #merged_df = pd.merge(Liste_enrichie, occupation, on='linkedinId', how='inner')
    #merged_df.drop_duplicates(subset='linkedinId', keep='first', inplace=True)
    return lis
