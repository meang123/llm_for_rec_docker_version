from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

import shutil
from recommend import llm

from langchain.retrievers.document_compressors import CohereRerank
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.document_transformers import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain.retrievers import ContextualCompressionRetriever
from langchain.vectorstores import FAISS

from bge_embedding import emb_model
from langchain.chains import RetrievalQA
import re


class CustomCohereRerank(CohereRerank):

    class Config(CohereRerank.Config):
        arbitrary_types_allowed = True






def contextual_compression_pipeline():


    loader_mentee = TextLoader("/tmp/data/mentee_info.txt")
    data_mentee = loader_mentee.load()
    mentee_text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=20)
    mentee_texts = mentee_text_splitter.split_documents(data_mentee)
    persist_directory_review = '/tmp/review_db'

    review_embedding = emb_model()


    review_vectordb = FAISS.from_documents(documents=mentee_texts,embedding=review_embedding)


    #base retrival : review
    retriever_review = review_vectordb.as_retriever(search_kwargs={"k": 4}) # default

    CustomCohereRerank.update_forward_refs()

    compressor = CustomCohereRerank(top_n=3,user_agent='langchain')
    redundant_filter = EmbeddingsRedundantFilter(embeddings=review_embedding)
    relevant_filter = EmbeddingsFilter(embeddings=review_embedding,similarity_threshold=0.60)

    pipeline_compressor = DocumentCompressorPipeline(
        transformers=[compressor,redundant_filter,relevant_filter]
    )



    compression_retriever = ContextualCompressionRetriever(base_compressor=pipeline_compressor, base_retriever=retriever_review)

    return compression_retriever



def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs['source_documents']])



#list return
def review_chain(retrival_mentee_obj):


    compression_retriever = contextual_compression_pipeline()
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type="stuff",
                                           retriever=compression_retriever,
                                           return_source_documents=True)

    doc = qa_chain(f"I'm looking to find someone with a similar personality or traits as {retrival_mentee_obj}")
    result = format_docs(doc)

    #names = re.findall(r'# (\w+)', s)

    print("review chain result ",result)
    names = re.findall(r'# (\w+)', result)

    return names

