
from sentence_transformers import SentenceTransformer

from langchain.embeddings import HuggingFaceBgeEmbeddings

def emb_model():
    model_name = "BAAI/bge-base-en"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs,
        cache_folder = '/tmp'
    )

    return model_norm





