# scripts/iac_template_generation.py
import openai
from langchain.prompts import PromptTemplate
from langchain import OpenAI

# Initialize OpenAI with API Key
def initialize_openai():
    llm = OpenAI(api_key="your_openai_api_key")
    return llm

# Define a prompt template for Terraform configuration generation
def create_prompt_template(resource_type, **kwargs):
    templates = {
        "EC2": "Generate a Terraform configuration for an AWS EC2 instance with the following specifications: instance type is {instance_type}, AMI is {ami}, region is {region}.",
        "S3": "Generate a Terraform configuration for an AWS S3 bucket with the following specifications: bucket name is {bucket_name}, region is {region}, and versioning is {versioning}.",
        # Add more templates for other resources as needed
    }
    template = templates.get(resource_type)
    if template:
        return PromptTemplate.from_template(template).format(**kwargs)
    else:
        raise ValueError(f"No prompt template available for resource type: {resource_type}")

# Generate Terraform configuration
def generate_terraform_template(resource_type, llm, **kwargs):
    prompt = create_prompt_template(resource_type, **kwargs)
    response = llm(prompt)
    return response

if __name__ == "__main__":
    # Initialize OpenAI model
    llm = initialize_openai()

    # Example use case: Generate EC2 Terraform template
    resource_type = "EC2"
    config = {
        "instance_type": "t2.micro",
        "ami": "ami-0abcdef1234567890",
        "region": "us-west-2"
    }
    terraform_template = generate_terraform_template(resource_type, llm, **config)
    print("Generated Terraform Template:\n", terraform_template)
