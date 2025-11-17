---
description: Manage GCP IAM policies and service accounts
allowed-tools: Write, Read, Bash
---

# GCP IAM Management

## Parse Arguments
```bash
ACTION="${ARGUMENTS[0]}"    # create|update|audit
RESOURCE="${ARGUMENTS[1]}"  # service-account|role|policy
```

## Validate Input
Ensure valid action and resource:
- Actions: create, update, audit
- Resources: service-account, role, policy

## Invoke GCP Expert
Invoke the `gcp-expert` agent based on action and resource:

### Create Service Account
Generate:
- Service account with appropriate naming
- Key generation (if needed)
- Initial IAM bindings
- Workload identity setup
- Terraform configuration

### Create Custom Role
Generate:
- Custom role definition
- Permission assignments
- Role description
- Terraform configuration
- Usage examples

### Create Policy
Generate:
- Organization policies
- Resource hierarchy policies
- Conditional IAM policies
- Terraform configurations

### Update Operations
Modify existing:
- Add/remove permissions
- Update role bindings
- Rotate service account keys
- Modify policy conditions

### Audit Operations
Review and report:
- Overly permissive roles
- Unused service accounts
- Policy violations
- Best practice deviations
- Security recommendations

## Output
Based on action, provide:
- Generated configurations
- gcloud commands
- Terraform code
- Security analysis
- Compliance report
- Remediation steps

## Example Usage
```
/gcp-iam create service-account
/gcp-iam update role
/gcp-iam audit policy
/gcp-iam create role
/gcp-iam update service-account
```