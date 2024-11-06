# scripts/setup_vector_db.py
import pinecone
import faiss
import os

def initialize_pinecone(api_key, environment, index_name="IaC-templates", dimension=512):
    pinecone.init(api_key=api_key, environment=environment)
    index = pinecone.Index(index_name)
    return index

def initialize_faiss(dimension=512):
    index = faiss.IndexFlatL2(dimension)
    return index

if __name__ == "__main__":
    # Choose between Pinecone or Faiss
    # Example for Pinecone
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_environment = os.getenv("PINECONE_ENV")
    pinecone_index = initialize_pinecone(pinecone_api_key, pinecone_environment)

    # Example for Faiss
    faiss_index = initialize_faiss()
