# scripts/deployment_workflow.py
import subprocess
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from scripts.validate_templates import validate_template
from scripts.iac_template_generation import generate_terraform_template, initialize_openai

# Step 1: Validate the Terraform Template
def validate_template_step(template, documentation_texts):
    return validate_template(template, documentation_texts)

# Step 2: Apply the Terraform Template
def apply_template_step(template_path):
    # Assuming the template is saved at template_path
    apply_command = f"terraform apply -auto-approve {template_path}"
    try:
        result = subprocess.run(apply_command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Deployment failed: {e.stderr}"

# Step 3: Monitor Deployment Status
def monitor_status_step(resource_id):
    # Placeholder for monitoring logic, could be enhanced with specific cloud monitoring commands
    monitor_command = f"aws ec2 describe-instances --instance-ids {resource_id}"
    try:
        result = subprocess.run(monitor_command, shell=True, check=True, capture_output=True, text=True)
        return f"Resource status: {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Monitoring failed: {e.stderr}"

# Main function to run the deployment workflow
def deployment_workflow(resource_type, config, documentation_texts, template_path):
    # Initialize OpenAI and generate template
    llm = initialize_openai()
    generated_template = generate_terraform_template(resource_type, llm, **config)

    # Step 1: Validate the generated template
    validation_result = validate_template_step(generated_template, documentation_texts)
    print("Validation Result:\n", validation_result)

    # Step 2: Apply the validated template
    print("Applying the Terraform Template...")
    apply_result = apply_template_step(template_path)
    print("Apply Result:\n", apply_result)

    # Step 3: Monitor the deployment status
    print("Monitoring the Deployment Status...")
    # Here, replace `resource_id` with the actual ID obtained from the apply result, if available
    monitor_result = monitor_status_step("resource_id_placeholder")
    print("Monitor Result:\n", monitor_result)

if __name__ == "__main__":
    # Example configuration
    resource_type = "EC2"
    config = {
        "instance_type": "t2.micro",
        "ami": "ami-0abcdef1234567890",
        "region": "us-west-2"
    }
    documentation_texts = ["Your relevant IaC documentation here"]
    template_path = "../data/terraform_templates/generated_template.tf"

    # Run the deployment workflow
    deployment_workflow(resource_type, config, documentation_texts, template_path)
