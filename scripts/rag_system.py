# scripts/rag_system.py
import openai
import pinecone
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone or Faiss
def init_pinecone(api_key, environment, index_name="IaC-templates"):
    pinecone.init(api_key=api_key, environment=environment)
    return pinecone.Index(index_name)

def init_faiss(dimension=512, index_file="../embeddings/faiss_index.bin"):
    index = faiss.read_index(index_file)
    return index

# Generate embeddings for a user prompt
def get_embedding(text):
    return model.encode([text])

# RAG retrieval function using Pinecone
def retrieve_from_pinecone(index, query_embedding, top_k=3):
    results = index.query(query_embedding.tolist(), top_k=top_k, include_metadata=True)
    return results["matches"]

# RAG retrieval function using Faiss
def retrieve_from_faiss(index, query_embedding, data, top_k=3):
    query_embedding = np.array(query_embedding).astype("float32")
    _, indices = index.search(query_embedding, top_k)
    return [data[idx] for idx in indices[0]]

# Fetch documentation based on the prompt
def fetch_documentation(prompt, use_pinecone=True):
    embedding = get_embedding(prompt)
    if use_pinecone:
        pinecone_api_key = "your_pinecone_api_key"
        pinecone_env = "your_pinecone_environment"
        index = init_pinecone(pinecone_api_key, pinecone_env)
        results = retrieve_from_pinecone(index, embedding)
    else:
        dimension = 512  # embedding dimension
        index = init_faiss(dimension)
        iac_data = load_data("../data/iac_docs") + load_data("../data/terraform_templates")
        results = retrieve_from_faiss(index, embedding, iac_data)
    
    return results

# Function to interact with OpenAI API
def generate_response(prompt, documents):
    context = " ".join([doc["metadata"]["text"] if "metadata" in doc else doc for doc in documents])
    full_prompt = f"{context}\n\n{prompt}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=150
    )
    return response["choices"][0]["text"].strip()

if __name__ == "__main__":
    prompt = "Create a Terraform template for an EC2 instance"
    documents = fetch_documentation(prompt)
    answer = generate_response(prompt, documents)
    print("Generated Response:", answer)
