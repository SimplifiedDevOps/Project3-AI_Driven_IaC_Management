# scripts/integration_test.py
from scripts.iac_template_generation import generate_terraform_template, initialize_openai
from scripts.validate_templates import validate_template
from scripts.deployment_workflow import apply_template_step, monitor_status_step
from scripts.feedback_collection import collect_feedback

def run_integration_test():
    # Initialize OpenAI model
    llm = initialize_openai()
    
    # Step 1: Template Generation
    resource_type = "EC2"
    config = {
        "instance_type": "t2.micro",
        "ami": "ami-0abcdef1234567890",
        "region": "us-west-2"
    }
    generated_template = generate_terraform_template(resource_type, llm, **config)
    print("Template Generation Test Passed" if generated_template else "Template Generation Test Failed")
    
    # Step 2: Template Validation
    documentation_texts = ["Your relevant IaC documentation here"]
    validation_result = validate_template(generated_template, documentation_texts)
    print("Template Validation Test Passed" if "No issues" in validation_result else "Template Validation Test Failed")
    
    # Step 3: Apply Template
    template_path = "../data/terraform_templates/generated_template.tf"
    apply_result = apply_template_step(template_path)
    print("Apply Template Test Passed" if "Apply complete" in apply_result else "Apply Template Test Failed")

    # Step 4: Monitor Status
    instance_id = "i-0abcd1234efgh5678"  # Placeholder; replace with actual ID
    monitor_result = monitor_status_step(instance_id)
    print("Monitor Status Test Passed" if "running" in monitor_result else "Monitor Status Test Failed")
    
    # Step 5: Collect Feedback
    deployment_id = "DEPLOY12345"
    collect_feedback(deployment_id)
    print("Feedback Collection Test Completed")

if __name__ == "__main__":
    run_integration_test()
