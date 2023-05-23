import pinecone
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("Ghani-25/LF_enrich_sim", device='cpu')
pinecone.init(api_key='55f76c4b-d5e7-43f8-9ea4-60209aad21b4', environment='northamerica-northeast1-gcp')
index = pinecone.Index('ai-find')

def enrichir(query, count):
    xq = model.encode(query).tolist()
    result = index.query(xq, top_k=count, includeMetadata=False)
    res = result.to_dict() #conversion to dict
    lis = list(res.values())[0]
    return lis
