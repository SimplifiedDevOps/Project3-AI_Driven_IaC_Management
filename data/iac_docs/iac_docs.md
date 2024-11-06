# iac_docs Directory

These files provide documentation and references for validating and generating templates:

---

## Best_Practices.md

**Content**: Guidelines for naming conventions, security practices, tagging standards, and recommended configurations.

**Example**:

```markdown
# Best Practices for IaC
- **Naming Convention**: Use lowercase, hyphen-separated names (e.g., `web-server-prod`).
- **Tagging**: Include `environment`, `project`, `owner`, and `cost_center` tags.
- **Security**: Avoid hardcoding credentials; use AWS IAM roles for access.

# EC2 Instance Setup Guide
- **AMI**: Use official Amazon Linux AMI.
- **Instance Type**: Recommended type for general workloads is `t2.micro`.
- **Security Groups**: Allow SSH (port 22) for management, HTTPS/HTTP for web services.

# Common Issues with IaC Deployments
- **Error**: `IAM Role not found`
  - **Solution**: Ensure the correct IAM role is referenced in your configuration file.

# RAG Reference Guide
- **Purpose**: To improve accuracy of generated templates by retrieving relevant configuration data.
- **Usage**: Use specific keywords to retrieve modules or templates.

# Terraform Module Standards
- **File Structure**: Each module should include `main.tf`, `variables.tf`, and `outputs.tf`.
- **Versioning**: Follow Semantic Versioning (e.g., `v1.0.0`).

