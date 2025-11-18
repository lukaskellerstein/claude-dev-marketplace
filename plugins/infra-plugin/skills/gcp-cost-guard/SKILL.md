---
name: gcp-cost-guard
description: Master GCP cost optimization. Use when creating/modifying GCP Terraform, designing GKE clusters, setting up compute instances, configuring storage, planning databases, or implementing cost controls.
allowed-tools: Read, Edit, Grep
---

# GCP Cost Guard Skill

Master GCP cost optimization strategies to automatically identify savings opportunities, implement best practices, and reduce cloud spending while maintaining performance.

## When to Use This Skill

Use this skill when:

1. Creating or modifying GCP Terraform configurations
2. Designing GKE cluster specifications
3. Setting up compute instances
4. Configuring storage resources
5. Planning database deployments
6. Reviewing cloud cost reports
7. Implementing budget controls and alerts
8. Optimizing existing infrastructure
9. Migrating workloads to GCP
10. Designing multi-region architectures
11. Implementing disaster recovery
12. Setting up development/staging environments
13. Planning capacity for new projects
14. Auditing resource utilization
15. Preparing cost forecasts and budgets

## Quick Start

This skill automatically suggests cost optimizations as you configure resources:

```hcl
# You write:
resource "google_compute_instance" "app" {
  machine_type = "n1-standard-16"
}

# Skill analyzes and suggests:
💰 Cost Optimization Opportunity Detected!

Current configuration:
- Machine type: n1-standard-16
- Est. monthly cost: $584

Recommendations:
1. Switch to e2-standard-16 → Save $175/month (30%)
2. Use preemptible instance → Save $409/month (70%)
3. Right-size to n1-standard-8 → Save $292/month (50%)

Auto-applying recommendation #1...
✅ Switched to e2-standard-16
📊 Monthly savings: $175
```

## Purpose
This skill automatically activates when working with GCP resources to ensure cost optimization best practices are followed and to identify potential savings opportunities.

## Auto-Invocation Context

This skill triggers when:
- Creating or modifying GCP Terraform configurations
- Designing GKE cluster specifications
- Setting up compute instances
- Configuring storage resources
- Planning database deployments

## Cost Optimization Actions

### 1. Compute Instance Optimization

#### Preemptible VMs
Automatically suggest for appropriate workloads:
```hcl
# Before
resource "google_compute_instance" "worker" {
  machine_type = "n1-standard-4"
}

# After optimization (70% savings)
resource "google_compute_instance" "worker" {
  machine_type = "e2-standard-4"  # Better price/performance

  scheduling {
    preemptible         = true
    automatic_restart   = false
    on_host_maintenance = "TERMINATE"
  }

  # Add metadata for preemptible handling
  metadata = {
    shutdown-script = file("${path.module}/scripts/graceful-shutdown.sh")
  }
}
```

#### Right-Sizing Recommendations
```hcl
# Detected: Over-provisioned instance
# Current: n1-standard-16 (16 vCPU, 60GB RAM)
# Usage: 25% CPU, 30% memory
# Recommended: n1-standard-4 (4 vCPU, 15GB RAM)
# Monthly savings: $400

resource "google_compute_instance" "app" {
  # Changed from n1-standard-16
  machine_type = "n1-standard-4"

  # Add monitoring to track actual usage
  metadata = {
    enable-osconfig = "TRUE"
    enable-guest-attributes = "TRUE"
  }
}
```

#### Committed Use Discounts
```hcl
# Suggest commitment for stable workloads
resource "google_compute_reservation" "commitment" {
  name = "one-year-reservation"
  zone = "us-central1-a"

  specific_reservation {
    count = 10
    instance_properties {
      machine_type = "n1-standard-4"
    }
  }

  # 37% savings with 1-year commitment
  # 57% savings with 3-year commitment
}
```

### 2. GKE Cost Optimization

#### Node Pool Configuration
```yaml
# Before
nodeConfig:
  machineType: n1-standard-8
  diskSizeGb: 100

# After optimization
nodeConfig:
  machineType: e2-standard-4  # Better price/performance
  diskSizeGb: 50  # Right-sized disk
  preemptible: true  # For non-critical workloads

  # Enable workload identity for cost tracking
  workloadMetadataConfig:
    mode: GKE_METADATA

  # Add labels for cost allocation
  labels:
    environment: "dev"
    team: "backend"
    cost-center: "engineering"
```

#### Cluster Autoscaling
```hcl
resource "google_container_node_pool" "primary" {
  cluster = google_container_cluster.main.name

  # Optimize autoscaling
  autoscaling {
    min_node_count = 1  # Scale to zero when possible
    max_node_count = 10
  }

  # Enable cluster autoscaler
  management {
    auto_repair  = true
    auto_upgrade = true
  }

  # Use spot instances for 70% savings
  node_config {
    spot         = true
    machine_type = "e2-medium"
  }
}
```

### 3. Storage Optimization

#### Lifecycle Policies
```hcl
resource "google_storage_bucket" "data" {
  name     = "company-data-bucket"
  location = "US-CENTRAL1"  # Regional instead of multi-regional

  # Automatic storage class transitions
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"  # 50% cheaper
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"  # 70% cheaper
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"  # 90% cheaper
    }
  }

  # Delete old versions
  lifecycle_rule {
    condition {
      num_newer_versions = 3
    }
    action {
      type = "Delete"
    }
  }
}
```

### 4. Database Optimization

#### Cloud SQL Right-Sizing
```hcl
resource "google_sql_database_instance" "main" {
  # Changed from db-n1-standard-4 to custom machine type
  settings {
    tier = "db-custom-2-7680"  # Custom 2 vCPU, 7.5GB RAM

    # Optimize for cost
    pricing_plan = "PER_USE"

    # Enable automatic storage increase only when needed
    disk_autoresize       = true
    disk_autoresize_limit = 100  # Set reasonable limit

    # Use HDD for non-performance critical
    disk_type = "PD_HDD"  # 50% cheaper than SSD

    # Backup optimization
    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      transaction_log_retention_days = 3  # Reduced from 7
      backup_retention_settings {
        retained_backups = 7  # Reduced from 30
      }
    }
  }

  # For dev/test environments
  deletion_protection = false
}
```

### 5. Network Optimization

#### Egress Cost Reduction
```hcl
# Use Cloud CDN to reduce egress
resource "google_compute_backend_service" "default" {
  name = "backend-service"

  cdn_policy {
    cache_mode = "CACHE_ALL_STATIC"
    default_ttl = 3600
    max_ttl     = 86400

    # Cache static content
    cache_key_policy {
      include_host         = true
      include_protocol     = true
      include_query_string = false
    }
  }

  # Use Cloud Armor for DDoS protection
  security_policy = google_compute_security_policy.policy.id
}

# Use Private Google Access
resource "google_compute_subnetwork" "subnet" {
  private_ip_google_access = true  # Avoid egress charges
}
```

### 6. BigQuery Optimization

```sql
-- Partition tables to reduce scan costs
CREATE TABLE dataset.partitioned_table
PARTITION BY DATE(timestamp_column)
CLUSTER BY user_id, event_type
AS SELECT * FROM dataset.source_table;

-- Use materialized views for repeated queries
CREATE MATERIALIZED VIEW dataset.mv_daily_stats AS
SELECT
  DATE(timestamp) as date,
  COUNT(*) as events,
  COUNT(DISTINCT user_id) as users
FROM dataset.events
GROUP BY date;

-- Set dataset expiration for temporary data
ALTER SCHEMA temp_dataset
SET OPTIONS(
  default_table_expiration_days=7
);
```

### 7. Cost Allocation

#### Resource Labeling
```hcl
# Enforce labels for cost tracking
locals {
  common_labels = {
    environment  = var.environment
    team        = var.team
    cost-center = var.cost_center
    project     = var.project_name
    managed-by  = "terraform"
    auto-delete = var.environment == "dev" ? "true" : "false"
  }
}

# Apply to all resources
resource "google_compute_instance" "app" {
  labels = local.common_labels
}
```

### 8. Budget Alerts

```hcl
resource "google_billing_budget" "budget" {
  billing_account = var.billing_account
  display_name    = "Monthly Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units        = "1000"
    }
  }

  threshold_rules {
    threshold_percent = 0.5
  }
  threshold_rules {
    threshold_percent = 0.75
  }
  threshold_rules {
    threshold_percent = 0.9
  }
  threshold_rules {
    threshold_percent = 1.0
  }
}
```

## Cost Analysis Report

Generate cost optimization summary:
```
GCP Cost Optimization Report
============================
Current Monthly Cost: $10,000
Optimized Cost: $6,000
Total Savings: $4,000 (40%)

Breakdown by Service:
- Compute Engine: -$2,000 (Preemptible VMs)
- GKE: -$1,000 (Node pool optimization)
- Cloud Storage: -$500 (Lifecycle policies)
- Cloud SQL: -$300 (Right-sizing)
- Network: -$200 (CDN implementation)

Recommendations:
1. Purchase 1-year commitments: Additional 37% savings
2. Implement spot instances: Up to 70% savings
3. Enable cluster autoscaling: Dynamic cost optimization
4. Archive old data: 90% storage cost reduction

Implementation Priority:
- High Impact: Preemptible VMs, Commitments
- Medium Impact: Storage lifecycle, Right-sizing
- Low Impact: Network optimization, Labels
```

## Real-World Applications

### Startup Scaling Cost Optimization

**Scenario:** Rapidly growing startup needing to control cloud costs

```hcl
# Development environment - Maximum cost savings
resource "google_compute_instance" "dev" {
  machine_type = "e2-medium"  # Cost-effective machine type

  scheduling {
    preemptible       = true  # 70% savings
    automatic_restart = false
  }

  # Auto-shutdown during off-hours
  metadata = {
    shutdown-script = <<-EOT
      #!/bin/bash
      # Save state before shutdown
      systemctl stop myapp
    EOT
  }

  labels = {
    environment = "dev"
    auto-delete = "true"  # Delete if unused for 7 days
  }
}

# Production environment - Balanced cost and reliability
resource "google_compute_instance" "prod" {
  machine_type = "e2-standard-4"  # 30% cheaper than n1

  # Use committed use discounts
  lifecycle {
    ignore_changes = [machine_type]  # Managed by reservation
  }

  # Production requires reliability
  scheduling {
    preemptible       = false
    automatic_restart = true
  }
}

# 1-year commitment for predictable workloads
resource "google_compute_reservation" "prod_commitment" {
  name = "prod-reservation"
  zone = "us-central1-a"

  specific_reservation {
    count = 5  # Number of instances
    instance_properties {
      machine_type = "e2-standard-4"
    }
  }

  # 37% savings with 1-year commitment
}
```

### E-commerce Platform Cost Optimization

**Scenario:** E-commerce site with variable traffic patterns

```hcl
# GKE cluster with aggressive cost optimization
resource "google_container_cluster" "ecommerce" {
  name     = "ecommerce-cluster"
  location = "us-central1"

  # Optimize cluster for cost
  cluster_autoscaling {
    enabled = true
    auto_provisioning_defaults {
      # Use most cost-effective machine family
      machine_type = "e2-standard-2"

      # Enable disk autoscaling
      disk_size = 50
      disk_type = "pd-standard"  # Cheaper than SSD
    }

    resource_limits {
      resource_type = "cpu"
      minimum       = 4
      maximum       = 64  # Scale based on traffic
    }

    resource_limits {
      resource_type = "memory"
      minimum       = 16
      maximum       = 256
    }
  }
}

# Node pool for batch processing - use spot instances
resource "google_container_node_pool" "batch" {
  cluster = google_container_cluster.ecommerce.name

  autoscaling {
    min_node_count = 0  # Scale to zero when idle
    max_node_count = 10
  }

  node_config {
    spot = true  # 70% cheaper for batch jobs

    machine_type = "e2-standard-4"

    labels = {
      workload = "batch"
      cost-optimized = "true"
    }
  }
}
```

### Data Analytics Platform

**Scenario:** Big data processing with smart storage tiering

```hcl
# Hot data - frequently accessed
resource "google_storage_bucket" "analytics_hot" {
  name     = "analytics-hot-data"
  location = "US-CENTRAL1"  # Regional cheaper than multi-regional

  storage_class = "STANDARD"

  # Transition to cheaper storage after 7 days
  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"  # 50% cheaper
    }
  }
}

# Archive data - rarely accessed
resource "google_storage_bucket" "analytics_archive" {
  name     = "analytics-archive"
  location = "US-CENTRAL1"

  storage_class = "ARCHIVE"  # 90% cheaper than STANDARD

  # Auto-delete after retention period
  lifecycle_rule {
    condition {
      age = 2555  # 7 years
    }
    action {
      type = "Delete"
    }
  }
}

# BigQuery with cost controls
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "analytics"
  location   = "US"

  # Partition tables to reduce scan costs
  default_table_expiration_ms = 2592000000  # 30 days

  # Set reasonable limits
  max_time_travel_hours = 168  # 7 days (vs 7 days default)
}
```

## Best Practices

### Right-Sizing Strategy
- Start with smallest instance type that meets requirements
- Monitor actual usage for 2-4 weeks before scaling up
- Use committed use discounts for predictable workloads
- Reserve instances for steady-state workloads (save 57%)

### Storage Optimization
- Use lifecycle policies to transition to cheaper storage classes
- Delete unused persistent disks and snapshots
- Compress data before storing in Cloud Storage
- Use coldline/archive storage for infrequently accessed data

### Network Cost Management
- Keep data transfer within same region when possible
- Use private IPs for internal communication (free)
- Implement Cloud CDN for frequently accessed content
- Monitor egress costs closely

### Monitoring and Alerts
- Set up budget alerts at 50%, 80%, and 100%
- Review cost reports weekly
- Track cost per service/project/team
- Identify and eliminate waste immediately

### Automation
- Use Cloud Scheduler to stop dev/test resources after hours
- Implement auto-scaling based on actual demand
- Delete orphaned resources automatically
- Tag all resources for cost attribution

## Common Pitfalls

### ❌ Over-Provisioned Instances

**Problem:**
```hcl
resource "google_compute_instance" "app" {
  machine_type = "n1-standard-16"  # 16 vCPUs, 60GB RAM
  # App only uses 2 vCPUs and 8GB RAM - wasting 87% of capacity!
}
```

**Solution:** Right-size based on actual usage
```hcl
resource "google_compute_instance" "app" {
  machine_type = "e2-standard-2"  # 2 vCPUs, 8GB RAM
  # Saves ~$400/month while meeting requirements
}
```

### ❌ Not Using Committed Use Discounts

**Problem:** Running steady workloads on on-demand pricing

**Solution:** Commit to 1-year or 3-year contracts
```hcl
# Save 57% for 3-year commitment, 37% for 1-year
resource "google_compute_instance" "production" {
  machine_type = "n2-standard-4"
  # Add commitment via Console or Terraform
}
```

### ❌ Forgetting to Delete Unused Resources

**Problem:**
- Old persistent disks from deleted instances ($0.04/GB/month)
- Unused static IP addresses ($0.01/hour = $7.20/month each)
- Test Cloud SQL instances left running ($50-500/month)

**Solution:** Implement cleanup automation
```bash
# Find unused disks
gcloud compute disks list --filter="users:*" --format="table(name,sizeGb,zone)"

# Find unused IPs
gcloud compute addresses list --filter="status:RESERVED" --format="table(name,address,status)"

# Schedule cleanup
gcloud scheduler jobs create http cleanup-unused \
  --schedule="0 2 * * SUN" \
  --uri="https://cleanup-function-xyz.cloudfunctions.net/cleanup"
```

### ❌ Excessive Data Transfer

**Problem:**
```hcl
# Frontend in us-central1, API in europe-west1
# Every request incurs egress charges ($0.01-0.12/GB)
```

**Solution:** Colocate services in same region
```hcl
# Both in us-central1
# Internal traffic within region is FREE
```

### ❌ Not Using Appropriate Storage Classes

**Problem:**
```hcl
resource "google_storage_bucket" "logs" {
  name     = "app-logs"
  location = "US"
  # Using Standard storage ($0.020/GB/month)
  # Logs accessed once a month - should use Nearline ($0.010/GB/month)
}
```

**Solution:** Use lifecycle policies
```hcl
resource "google_storage_bucket" "logs" {
  name     = "app-logs"
  location = "US"

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"  # 50% savings
    }
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"  # 80% savings
    }
  }
}
```

### ❌ Running Dev/Test 24/7

**Problem:** Development environments running nights and weekends

**Solution:** Schedule startup/shutdown
```hcl
# Cloud Scheduler to stop instances at 6 PM, start at 8 AM
resource "google_cloud_scheduler_job" "stop_dev" {
  name     = "stop-dev-instances"
  schedule = "0 18 * * 1-5"  # 6 PM weekdays

  http_target {
    uri         = "https://compute.googleapis.com/compute/v1/projects/${var.project}/zones/${var.zone}/instances/${var.instance}/stop"
    http_method = "POST"
  }
}

# Save 60% on dev costs (12h weekdays + weekends)
```

### ❌ Ignoring Sustained Use Discounts

**Problem:** Restarting instances daily, preventing sustained use discount eligibility

**Solution:** Keep instances running for full month
- Automatic 30% discount after running 25% of month
- Maximize to reduce per-hour cost

## Related Skills

- **iac-compliance**: Ensures cost optimizations meet compliance requirements
- **k8s-optimizer**: Optimizes Kubernetes resources for cost efficiency
- **helm-validator**: Validates Helm charts have appropriate resource limits
- **terraform-best-practices**: Applies Terraform patterns for cost management

This skill ensures optimal cost efficiency for every GCP resource, potentially saving 20-40% on cloud spending while maintaining performance requirements.