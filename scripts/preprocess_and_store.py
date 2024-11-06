# scripts/preprocess_and_store.py
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import pinecone
import faiss

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load IaC documents and templates
def load_data(folder_path):
    data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            data.append(content)
    return data

# Embed data
def generate_embeddings(text_data):
    return model.encode(text_data)

# Store embeddings in Pinecone
def store_in_pinecone(index, embeddings):
    index.upsert([(str(i), embedding.tolist()) for i, embedding in enumerate(embeddings)])

# Store embeddings in Faiss
def store_in_faiss(index, embeddings):
    index.add(np.array(embeddings))

if __name__ == "__main__":
    # Set up Pinecone or Faiss
    use_pinecone = True  # Set to False if using Faiss

    # Load IaC data
    iac_data = load_data("../data/iac_docs") + load_data("../data/terraform_templates")

    # Generate embeddings
    embeddings = generate_embeddings(iac_data)

    if use_pinecone:
        # Pinecone setup
        pinecone_api_key = os.getenv("PINECONE_API_KEY")
        pinecone_environment = os.getenv("PINECONE_ENV")
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
        index = pinecone.Index("IaC-templates")
        store_in_pinecone(index, embeddings)
    else:
        # Faiss setup
        dimension = 512  # Set according to embedding size
        faiss_index = faiss.IndexFlatL2(dimension)
        store_in_faiss(faiss_index, embeddings)

        # Save the Faiss index
        faiss.write_index(faiss_index, "../embeddings/faiss_index.bin")
