# scripts/feedback_based_learning.py
import csv
import pandas as pd
from scripts.iac_template_generation import create_prompt_template
from scripts.preprocess_and_store import generate_embeddings
from scripts.setup_vector_db import initialize_pinecone

# File path for feedback responses
feedback_file_path = "../feedback/feedback_responses.csv"

# Load feedback data
def load_feedback_data():
    return pd.read_csv(feedback_file_path)

# Analyze feedback data to adjust prompt templates and validation checks
def analyze_feedback_and_adjust():
    feedback_data = load_feedback_data()
    avg_rating = feedback_data["Rating"].mean()
    common_issues = feedback_data["Comments"].value_counts().head(3)

    # Example adjustment: modify prompt template based on common issues
    if avg_rating < 3:
        print("Average rating is low. Adjusting templates or validation checks may be needed.")
        print("Top 3 common issues based on feedback:\n", common_issues)
        # Modify prompt templates or validation checks as needed based on common issues
        # This can involve refining prompt wording, validation logic, or configuration parameters

# Update vector store with new configurations based on feedback
def update_vector_store_with_feedback(new_configuration_text):
    # Generate embedding for the new configuration
    embedding = generate_embeddings([new_configuration_text])[0]
    
    # Initialize Pinecone and update vector store
    pinecone_api_key = "your_pinecone_api_key"
    pinecone_env = "your_pinecone_environment"
    pinecone_index_name = "IaC-templates"
    pinecone_index = initialize_pinecone(pinecone_api_key, pinecone_env, pinecone_index_name)
    
    # Add the new embedding to the vector store
    pinecone_index.upsert([(str(hash(new_configuration_text)), embedding.tolist())])
    print("Updated vector store with new configuration.")

if __name__ == "__main__":
    # Analyze feedback data and adjust configurations or templates
    analyze_feedback_and_adjust()

    # Example new configuration text from feedback
    new_configuration_text = "Example updated Terraform configuration for AWS EC2 instance with enhanced settings based on feedback."
    update_vector_store_with_feedback(new_configuration_text)
