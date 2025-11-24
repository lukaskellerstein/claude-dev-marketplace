---
name: terraform-patterns
description: Auto-invoked when writing Terraform code to ensure Infrastructure as Code best practices, proper module structure, and maintainability
allowed-tools: Read, Grep, Glob
---

# Terraform Patterns and Best Practices

This skill provides guidance on Terraform best practices for Infrastructure as Code.

## When Active

This skill activates when you:
- Write or modify Terraform configurations (.tf files)
- Design Terraform modules
- Review infrastructure code
- Set up remote state
- Plan infrastructure changes
- Debug Terraform issues

## Project Structure Best Practices

### Recommended Directory Structure

```
infrastructure/
├── modules/                    # Reusable modules
│   ├── vpc-network/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── versions.tf
│   │   └── README.md
│   ├── gke-cluster/
│   ├── cloud-sql/
│   └── cloud-storage/
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── backend.tf
│   │   ├── terraform.tfvars
│   │   └── README.md
│   ├── staging/
│   └── production/
├── .terraform.lock.hcl        # Provider version locks
└── README.md
```

### Module Structure

Each module should have:
- `main.tf` - Primary resource definitions
- `variables.tf` - Input variable declarations
- `outputs.tf` - Output value definitions
- `versions.tf` - Terraform and provider version constraints
- `README.md` - Module documentation with examples

## Terraform Version Management

### Always Specify Versions

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5"  # Minimum Terraform version

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"  # Compatible with 5.x
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}
```

**Version Constraint Operators**:
- `= 1.5.0` - Exact version (too restrictive)
- `!= 1.5.0` - Exclude specific version
- `>= 1.5` - Minimum version
- `<= 1.5` - Maximum version
- `~> 1.5` - Pessimistic constraint (1.5.x, but not 1.6)
- `>= 1.5, < 2.0` - Range

**Best Practice**: Use `~>` for providers to get patch updates but avoid breaking changes.

## Variable Best Practices

### 1. Always Add Descriptions and Types

```hcl
# variables.tf
variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
}

variable "region" {
  description = "The GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "node_count" {
  description = "The number of nodes per zone in the GKE node pool"
  type        = number
  default     = 1

  validation {
    condition     = var.node_count >= 1 && var.node_count <= 100
    error_message = "Node count must be between 1 and 100."
  }
}

variable "environment" {
  description = "The environment name (dev, staging, production)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "labels" {
  description = "Labels to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "subnets" {
  description = "List of subnets to create"
  type = list(object({
    subnet_name           = string
    subnet_ip             = string
    subnet_region         = string
    subnet_private_access = bool
  }))
}
```

**Guidelines**:
- Always add description
- Always specify type
- Use validation for constraints
- Provide sensible defaults where appropriate
- Use complex types (object, map, list) for structured data

### 2. Sensitive Variables

```hcl
variable "database_password" {
  description = "PostgreSQL database password"
  type        = string
  sensitive   = true
}
```

**Guidelines**:
- Mark sensitive variables with `sensitive = true`
- Never commit .tfvars files with secrets to Git
- Use secret management tools (Secret Manager, Vault)
- Pass via environment variables: `TF_VAR_database_password`

## Output Best Practices

### 1. Provide Useful Outputs

```hcl
# outputs.tf
output "cluster_name" {
  description = "The name of the GKE cluster"
  value       = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  description = "The endpoint for the GKE cluster"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

output "cluster_ca_certificate" {
  description = "The CA certificate for the GKE cluster"
  value       = google_container_cluster.primary.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "network_id" {
  description = "The ID of the VPC network"
  value       = google_compute_network.vpc.id
}

output "network_name" {
  description = "The name of the VPC network"
  value       = google_compute_network.vpc.name
}

output "subnet_names" {
  description = "List of subnet names"
  value       = [for subnet in google_compute_subnetwork.subnets : subnet.name]
}
```

**Guidelines**:
- Output values needed by other modules or for documentation
- Mark sensitive outputs with `sensitive = true`
- Add descriptions to all outputs
- Use descriptive names

## Resource Naming and Tagging

### 1. Use Consistent Naming Convention

```hcl
locals {
  name_prefix = "${var.environment}-${var.project_name}"

  common_labels = {
    environment = var.environment
    managed-by  = "terraform"
    project     = var.project_name
    terraform   = "true"
  }
}

resource "google_container_cluster" "primary" {
  name     = "${local.name_prefix}-gke-cluster"
  location = var.region

  resource_labels = merge(
    local.common_labels,
    {
      component = "compute"
      service   = "gke"
    },
    var.additional_labels
  )
}
```

**Guidelines**:
- Use consistent naming across all resources
- Include environment in resource names
- Use `local` values for computed names and common configurations
- Tag all resources with labels for cost tracking and organization

## State Management

### 1. Always Use Remote State

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "production/gke"

    # Implicitly enables state locking
  }
}
```

**Guidelines**:
- Never use local state for team projects
- Use GCS backend for GCP (includes automatic locking)
- Separate state files per environment
- Enable versioning on state bucket
- Restrict access to state bucket (contains sensitive data)
- Use different prefixes or buckets for different stacks

### 2. State File Security

```bash
# Enable versioning
gcloud storage buckets update gs://my-terraform-state --versioning

# Restrict access
gcloud storage buckets add-iam-policy-binding gs://my-terraform-state \
  --member="group:infra-team@example.com" \
  --role="roles/storage.objectAdmin"

# Enable encryption
gcloud storage buckets update gs://my-terraform-state \
  --default-encryption-key=projects/PROJECT_ID/locations/LOCATION/keyRings/RING/cryptoKeys/KEY
```

## Resource Organization

### 1. Group Related Resources

```hcl
# network.tf - All networking resources
resource "google_compute_network" "vpc" { }
resource "google_compute_subnetwork" "subnets" { }
resource "google_compute_firewall" "rules" { }

# compute.tf - All compute resources
resource "google_container_cluster" "gke" { }
resource "google_container_node_pool" "pools" { }

# storage.tf - All storage resources
resource "google_storage_bucket" "buckets" { }
resource "google_sql_database_instance" "db" { }

# iam.tf - All IAM resources
resource "google_service_account" "sa" { }
resource "google_project_iam_member" "bindings" { }
```

### 2. Use Descriptive Resource Names

```hcl
# Good
resource "google_container_cluster" "production_gke_cluster" { }
resource "google_compute_firewall" "allow_internal_traffic" { }

# Bad
resource "google_container_cluster" "cluster1" { }
resource "google_compute_firewall" "fw1" { }
```

## Dynamic Blocks and Loops

### 1. Use for_each for Multiple Resources

```hcl
# Good: Use for_each with map
variable "storage_buckets" {
  type = map(object({
    location      = string
    storage_class = string
  }))
  default = {
    "assets" = {
      location      = "us-central1"
      storage_class = "STANDARD"
    }
    "backups" = {
      location      = "us"
      storage_class = "NEARLINE"
    }
  }
}

resource "google_storage_bucket" "buckets" {
  for_each = var.storage_buckets

  name          = "${var.project_id}-${each.key}"
  location      = each.value.location
  storage_class = each.value.storage_class
}

# Access: google_storage_bucket.buckets["assets"].name
```

```hcl
# Alternative: Use count for identical resources
resource "google_compute_instance" "workers" {
  count = var.worker_count

  name         = "worker-${count.index + 1}"
  machine_type = var.machine_type
}
```

**Guidelines**:
- Prefer `for_each` over `count` for resources with unique configurations
- Use `count` only for identical resources
- `for_each` allows removal of specific items without recreating others
- Use maps with meaningful keys for `for_each`

### 2. Dynamic Blocks

```hcl
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  # Dynamic block for master authorized networks
  dynamic "master_authorized_networks_config" {
    for_each = var.master_authorized_networks != null ? [1] : []

    content {
      dynamic "cidr_blocks" {
        for_each = var.master_authorized_networks

        content {
          cidr_block   = cidr_blocks.value.cidr_block
          display_name = cidr_blocks.value.display_name
        }
      }
    }
  }
}
```

## Lifecycle Management

### 1. Use Lifecycle Meta-Arguments

```hcl
resource "google_container_node_pool" "primary" {
  name    = "primary-pool"
  cluster = google_container_cluster.primary.name

  # Lifecycle configuration
  lifecycle {
    create_before_destroy = true  # Create new before deleting old
    prevent_destroy       = false # Prevent accidental deletion
    ignore_changes = [
      initial_node_count,  # Ignore changes to these attributes
      node_config[0].labels,
    ]
  }
}
```

**Use Cases**:
- `create_before_destroy`: For resources that must exist during updates (e.g., node pools)
- `prevent_destroy`: For critical resources (e.g., production databases)
- `ignore_changes`: For attributes managed outside Terraform

## Data Sources

### 1. Use Data Sources for Existing Resources

```hcl
# Fetch existing VPC network
data "google_compute_network" "existing_vpc" {
  name = "existing-network"
}

# Fetch GKE versions
data "google_container_engine_versions" "gke_versions" {
  location = var.region
}

# Use in resources
resource "google_container_cluster" "primary" {
  network    = data.google_compute_network.existing_vpc.id
  min_master_version = data.google_container_engine_versions.gke_versions.latest_master_version
}
```

**Guidelines**:
- Use data sources to reference existing resources
- Use data sources for dynamic values (latest versions, availability zones)
- Cache data source queries in locals if used multiple times

## Module Best Practices

### 1. Create Reusable Modules

```hcl
# modules/gke-cluster/main.tf
resource "google_container_cluster" "cluster" {
  name     = var.cluster_name
  location = var.region
  # ... configuration
}

# modules/gke-cluster/variables.tf
variable "cluster_name" {
  description = "The name of the GKE cluster"
  type        = string
}

variable "region" {
  description = "The region for the GKE cluster"
  type        = string
}

# modules/gke-cluster/outputs.tf
output "cluster_name" {
  description = "The name of the created GKE cluster"
  value       = google_container_cluster.cluster.name
}
```

### 2. Use Modules in Environments

```hcl
# environments/production/main.tf
module "gke_cluster" {
  source = "../../modules/gke-cluster"

  cluster_name = "production-cluster"
  region       = "us-central1"
  node_count   = 5

  # ... other variables
}

# Access module outputs
output "cluster_endpoint" {
  value = module.gke_cluster.cluster_endpoint
}
```

**Guidelines**:
- Keep modules focused and single-purpose
- Document module inputs and outputs
- Version modules for stability
- Use relative paths for local modules
- Use versioned sources for remote modules

## Dependency Management

### 1. Implicit Dependencies

```hcl
# Terraform infers dependency from resource references
resource "google_container_cluster" "primary" {
  network = google_compute_network.vpc.id  # Implicit dependency
}
```

### 2. Explicit Dependencies

```hcl
resource "google_container_node_pool" "primary" {
  cluster = google_container_cluster.primary.name

  # Explicit dependency when no direct reference exists
  depends_on = [
    google_project_iam_member.gke_service_account
  ]
}
```

**Guidelines**:
- Prefer implicit dependencies (via references)
- Use `depends_on` only when necessary (no direct reference)
- Be careful with `depends_on` as it can slow down parallel operations

## Security Best Practices

### 1. Never Commit Secrets

```gitignore
# .gitignore
*.tfvars
*.tfstate
*.tfstate.backup
.terraform/
.terraform.lock.hcl  # Optional, some teams commit this
```

### 2. Use Secret Manager

```hcl
# Fetch secret from Secret Manager
data "google_secret_manager_secret_version" "db_password" {
  secret = "database-password"
}

resource "google_sql_user" "user" {
  name     = "app-user"
  instance = google_sql_database_instance.main.name
  password = data.google_secret_manager_secret_version.db_password.secret_data
}
```

## Common Patterns

### 1. Conditional Resource Creation

```hcl
resource "google_container_node_pool" "spot_pool" {
  count = var.enable_spot_pool ? 1 : 0

  name    = "spot-pool"
  cluster = google_container_cluster.primary.name

  node_config {
    spot = true
  }
}
```

### 2. Resource Defaults with Merge

```hcl
locals {
  default_labels = {
    managed-by  = "terraform"
    environment = var.environment
  }
}

resource "google_container_cluster" "primary" {
  name = var.cluster_name

  resource_labels = merge(
    local.default_labels,
    var.additional_labels
  )
}
```

### 3. Computed Values with Locals

```hcl
locals {
  # Compute node pool name
  node_pool_name = "${var.cluster_name}-${var.environment}-pool"

  # Parse CIDR blocks
  subnet_cidr_blocks = [
    for subnet in var.subnets : subnet.cidr_block
  ]

  # Conditional values
  instance_type = var.environment == "production" ? "n2-standard-4" : "n2-standard-2"
}
```

## Terraform Commands

### Essential Workflow

```bash
# Initialize (download providers)
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy resources
terraform destroy

# Show current state
terraform show

# List resources in state
terraform state list

# Import existing resource
terraform import google_compute_instance.default projects/my-project/zones/us-central1-a/instances/my-instance

# Refresh state
terraform refresh

# Output values
terraform output
terraform output -json
```

## Troubleshooting

### Common Issues

1. **State Lock Error**
```bash
# Force unlock (use carefully!)
terraform force-unlock LOCK_ID
```

2. **Resource Already Exists**
```bash
# Import existing resource
terraform import ADDRESS ID
```

3. **Drift Detection**
```bash
# Check for configuration drift
terraform plan -refresh-only
```

4. **Debug Mode**
```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform plan
```

## Checklist

Before applying Terraform changes:
- [ ] All files formatted with `terraform fmt`
- [ ] Configuration validated with `terraform validate`
- [ ] Remote backend configured
- [ ] Provider versions pinned
- [ ] Variables have types and descriptions
- [ ] Validation rules for critical variables
- [ ] Sensitive variables marked as sensitive
- [ ] Resources have descriptive names
- [ ] All resources properly labeled/tagged
- [ ] Outputs documented with descriptions
- [ ] State lock tested (for new backends)
- [ ] Plan reviewed and approved
- [ ] Secrets not committed to version control
- [ ] Module documentation complete
- [ ] Backup plan for critical resources

Use this guidance to ensure Terraform code is maintainable, secure, and follows Infrastructure as Code best practices.
