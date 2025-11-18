---
description: Generate Terraform modules for cloud providers
---

# Generate Terraform Module

## Parse Arguments
```bash
PROVIDER="${ARGUMENTS[0]}"    # gcp|aws|azure
RESOURCE="${ARGUMENTS[1]}"    # compute|network|storage|iam|kubernetes|database
ENVIRONMENT="${ARGUMENTS[2]}" # dev|staging|prod
```

## Validate Input
Ensure all required arguments are provided:
- Provider: gcp, aws, or azure
- Resource: compute, network, storage, iam, kubernetes, database
- Environment: dev, staging, or prod

## Invoke Terraform Expert
Invoke the `terraform-expert` agent with:
- Cloud provider: $PROVIDER
- Resource type: $RESOURCE
- Target environment: $ENVIRONMENT
- Project context

The agent will generate:
1. Module structure (main.tf, variables.tf, outputs.tf)
2. Provider configurations
3. Resource definitions with best practices
4. Variable definitions with descriptions
5. Output values for cross-module references
6. Environment-specific tfvars files
7. Remote backend configuration
8. Cost optimization settings

## Provider-Specific Features
### GCP
- Project and folder organization
- VPC and subnet configurations
- GKE cluster definitions
- IAM bindings and service accounts

### AWS
- VPC and subnet layouts
- EKS cluster configurations
- IAM roles and policies
- S3 bucket configurations

### Azure
- Resource group organization
- AKS cluster setups
- Virtual networks
- Storage accounts

## Output
Display generated Terraform files and provide:
- Module usage instructions
- Terraform commands (init, plan, apply)
- State management guidance
- Cost estimates
- Variable customization guide

## Example Usage
```
/terraform gcp kubernetes production
/terraform aws compute staging
/terraform azure storage dev
/terraform gcp network production
/terraform aws database staging
```