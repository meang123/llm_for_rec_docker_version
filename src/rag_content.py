from langchain.document_loaders.directory import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.document_loaders import PyPDFDirectoryLoader
from bge_embedding import emb_model
from langchain.vectorstores import FAISS
import os
import shutil
import sys
def rag_advice():

    os.environ['TRANSFORMERS_CACHE'] = '/tmp'

    loader = PyPDFDirectoryLoader('/tmp/data/', glob="./*.pdf")
    #PyPDFLoader
    documents = loader.load()

    #splitting the text into
    pdf_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    texts = pdf_text_splitter.split_documents(documents)

    # cromdb 생성 및 임베딩 사용
    persist_directory = '/tmp/db'

    ## Here is the nmew embeddings being used
    embedding = emb_model()



    vectordb = FAISS.from_documents(documents=texts,embedding=embedding)
    #FAISS.save_local(folder_path =persist_directory)

    #vectordb = FAISS.load_local(folder_path=persist_directory,embeddings=embedding)

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})  # default

    return retriever



