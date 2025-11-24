---
description: Provision complete cloud infrastructure using Terraform for Google Cloud, including VPC, GKE, databases, and supporting services
---

Provision production-ready cloud infrastructure using Infrastructure as Code (Terraform) with best practices for security, scalability, and maintainability.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand infrastructure needs and constraints
   - Identify required GCP services (Compute, GKE, Cloud SQL, Storage)
   - Determine network architecture (VPC, subnets, firewall rules)
   - Review compliance and security requirements
   - Understand environment requirements (dev, staging, production)
   - Check for existing infrastructure to import
   - Determine resource sizing and scaling needs

2. **Launch Terraform Expert**: Use the `terraform-expert` agent to:
   - Design Terraform module structure
   - Create reusable, composable modules
   - Set up remote state backend (GCS)
   - Define all infrastructure resources
   - Configure variables and outputs
   - Set up workspaces for environments
   - Implement security best practices
   - Plan for state management and locking

3. **Launch GCloud Expert**: Use the `gcloud-expert` agent to:
   - Validate GCP service requirements
   - Review IAM permissions needed
   - Verify network architecture design
   - Ensure security best practices
   - Optimize for cost and performance
   - Review compliance requirements

4. **Launch Kubernetes Expert** (if provisioning GKE): Use the `kubernetes-expert` agent to:
   - Design GKE cluster configuration
   - Plan node pool strategies
   - Configure networking (VPC-native, network policies)
   - Set up workload identity
   - Plan for monitoring and logging

5. **Implement Infrastructure Code**: Create Terraform configuration
   - Organize modules by service or layer
   - Implement proper variable validation
   - Set up remote state and locking
   - Create environment-specific configurations
   - Implement lifecycle policies
   - Add proper tagging and labeling

6. **Testing & Validation**: Validate infrastructure code
   - Run terraform validate and fmt
   - Execute terraform plan for each environment
   - Review security policies (Sentinel, OPA)
   - Test in dev environment first
   - Document any manual steps required

## Output

Present a comprehensive Terraform infrastructure including:

### Terraform Modules

**VPC Module** (`modules/vpc-network/`)
- VPC network with custom subnets
- Firewall rules and security policies
- Cloud NAT for outbound connectivity
- VPC peering if needed
- Private Service Connect

**GKE Module** (`modules/gke-cluster/`)
- GKE cluster with multiple node pools
- Workload Identity configuration
- Private cluster setup
- Auto-scaling configuration
- Monitoring and logging integration

**Cloud SQL Module** (`modules/cloud-sql/`)
- Cloud SQL instance with HA
- Private IP configuration
- Backup configuration
- Read replicas if needed
- Connection security

**Cloud Storage Module** (`modules/cloud-storage/`)
- Storage buckets with lifecycle policies
- IAM bindings
- Encryption configuration
- Versioning and retention

**IAM Module** (`modules/iam/`)
- Service accounts
- IAM role bindings
- Custom roles if needed
- Organization policies

### Environment Configurations

**Development Environment** (`environments/dev/`)
```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state-dev"
    prefix = "infrastructure/dev"
  }
}

module "vpc" {
  source = "../../modules/vpc-network"
  # ... configuration
}

module "gke" {
  source = "../../modules/gke-cluster"
  # ... configuration
}
```

**Staging Environment** (`environments/staging/`)
- Similar structure with staging-specific values

**Production Environment** (`environments/production/`)
- Production-grade configuration
- Enhanced security settings
- High availability setup
- Disaster recovery configuration

### State Management
- Remote backend configuration (GCS)
- State locking with Cloud Storage
- State file encryption
- Separate states per environment

### Variable Definitions
- Input variables with validation
- Output values for integration
- Sensitive variable handling
- Default values for common settings

### Documentation
- README with prerequisites
- Module documentation with examples
- Deployment instructions
- Troubleshooting guide
- Architecture diagrams
- Cost estimates

### CI/CD Integration
- Terraform plan in pull requests
- Automated apply on merge
- Drift detection
- State backup automation
- Atlantis configuration (optional)

### Security Configuration
- IAM least privilege
- VPC Service Controls
- Secret Manager integration
- Encryption at rest and in transit
- Security scanning (checkov, tfsec)

## Examples

### Provision Complete Three-Tier Infrastructure
```
/provision-infrastructure

Create production infrastructure on GCP including:
- VPC with public and private subnets across 3 zones
- GKE cluster with 3 node pools (system, apps, data)
- Cloud SQL PostgreSQL with read replicas
- Cloud Storage buckets for static assets and backups
- Cloud Memorystore Redis for caching
- IAM service accounts with Workload Identity
```

### Provision Multi-Region Infrastructure
```
/provision-infrastructure

Set up multi-region infrastructure with:
- VPC in us-central1 and europe-west1
- GKE clusters in both regions with Anthos Config Management
- Cloud SQL with cross-region replication
- Global HTTP(S) Load Balancer
- Cloud CDN for static content
```

### Provision Serverless Infrastructure
```
/provision-infrastructure

Create serverless infrastructure with:
- VPC with Cloud Run connector
- Cloud Run services for APIs
- Cloud Functions for event processing
- Firestore for NoSQL database
- Pub/Sub topics and subscriptions
- Cloud Storage with lifecycle policies
```

## Terraform Workflow

```bash
# Initialize Terraform
cd environments/production
terraform init

# Validate configuration
terraform validate
terraform fmt -recursive

# Plan changes
terraform plan -out=tfplan

# Review plan carefully
# Apply changes
terraform apply tfplan

# View outputs
terraform output

# Show current state
terraform show
```

## Best Practices Applied

- **Modular Design**: Reusable, composable modules
- **State Management**: Remote state with locking
- **Security**: Least privilege IAM, encryption, secrets management
- **Version Control**: All code in Git with proper branching
- **Documentation**: Comprehensive README and inline comments
- **Testing**: Validation, planning, and terratest
- **Cost Optimization**: Right-sized resources, auto-scaling
- **Disaster Recovery**: Backup strategies, multi-region support
- **Change Management**: CI/CD integration, approval workflows
- **Compliance**: Organization policies, security scanning

Provide production-ready Terraform code that can be applied immediately to provision infrastructure following GCP and Terraform best practices.
