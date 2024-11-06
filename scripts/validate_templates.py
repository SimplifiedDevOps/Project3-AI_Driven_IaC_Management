# scripts/validate_templates.py
import openai
from scripts.rag_system import fetch_documentation
from scripts.iac_template_generation import generate_terraform_template, initialize_openai

# Function to validate the generated Terraform template
def validate_template(template_text, documentation_texts):
    # Formulate a prompt to check for inconsistencies
    validation_prompt = f"Review the following Terraform template:\n\n{template_text}\n\nCompare it with the relevant IaC documentation below and identify any errors or inconsistencies. Suggest corrections if needed.\n\nDocumentation:\n"
    for doc in documentation_texts:
        validation_prompt += f"\n- {doc}"

    # Use OpenAI to validate and suggest corrections
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=validation_prompt,
        max_tokens=200
    )
    return response["choices"][0]["text"].strip()

if __name__ == "__main__":
    # Initialize OpenAI model
    llm = initialize_openai()

    # Example: Generate a Terraform template for EC2 instance
    resource_type = "EC2"
    config = {
        "instance_type": "t2.micro",
        "ami": "ami-0abcdef1234567890",
        "region": "us-west-2"
    }
    generated_template = generate_terraform_template(resource_type, llm, **config)

    # Retrieve relevant documentation using RAG
    documentation_texts = fetch_documentation("Terraform configuration for an AWS EC2 instance")

    # Validate the generated template
    validation_result = validate_template(generated_template, documentation_texts)
    print("Validation Result:\n", validation_result)
