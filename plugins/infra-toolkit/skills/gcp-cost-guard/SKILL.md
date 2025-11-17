---
name: gcp-cost-guard
description: Automatically optimize GCP resource costs
allowed-tools: Read, Edit, Grep
---

# GCP Cost Guard Skill

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

This skill ensures optimal cost efficiency for every GCP resource, potentially saving 20-40% on cloud spending while maintaining performance requirements.