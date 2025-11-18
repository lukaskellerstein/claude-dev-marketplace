---
name: iac-compliance
description: Master Infrastructure as Code compliance with security frameworks (CIS Benchmarks, PCI DSS, HIPAA, SOC2, GDPR). Use when writing Terraform/CloudFormation, defining security policies, implementing compliance controls, auditing infrastructure, ensuring regulatory adherence, or when discussing compliance requirements, security standards, regulatory frameworks, infrastructure security, encryption at rest, encryption in transit, access controls, audit logging, or compliance validation.
allowed-tools: Read, Grep
---

# Infrastructure as Code Compliance Skill

Master infrastructure compliance standards and automatically validate IaC against security frameworks including CIS Benchmarks, PCI DSS, HIPAA, SOC2, and GDPR requirements.

## When to Use This Skill

Use this skill when:

1. Writing or editing Terraform configurations
2. Creating CloudFormation templates
3. Defining infrastructure security policies
4. Implementing compliance controls
5. Auditing existing infrastructure code
6. Preparing for compliance audits
7. Implementing cloud security best practices
8. Setting up new cloud environments
9. Migrating workloads to the cloud
10. Reviewing infrastructure pull requests
11. Implementing zero-trust architecture
12. Configuring encryption and access controls
13. Setting up logging and monitoring
14. Implementing data residency requirements
15. Documenting compliance posture

## Quick Start

This skill automatically validates IaC for compliance as you write:

```hcl
# You write:
resource "google_compute_firewall" "web" {
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]  # Too permissive
  }
  source_ranges = ["0.0.0.0/0"]  # Public access
}

# Skill alerts:
❌ CIS 3.6: Firewall rule too permissive
❌ PCI DSS 1.2.1: Unrestricted inbound access
✓  Suggested fix: Restrict to specific ports and IPs

# Auto-suggested compliant version:
resource "google_compute_firewall" "web" {
  allow {
    protocol = "tcp"
    ports    = ["443"]  # HTTPS only
  }
  source_ranges = ["10.0.0.0/8"]  # Internal only
}
```

## Purpose
This skill automatically validates infrastructure code against security standards and compliance requirements, ensuring adherence to industry best practices and regulatory frameworks.

## Auto-Invocation Context

This skill triggers when:
- Writing or editing Terraform configurations
- Creating CloudFormation templates
- Defining infrastructure security policies
- Working with any IaC files

## Compliance Standards Checked

### 1. CIS Benchmarks

#### CIS Google Cloud Platform Foundation
```hcl
# CHECK: Enable VPC Flow Logs
resource "google_compute_subnetwork" "subnet" {
  # COMPLIANT: Flow logs enabled
  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling       = 1.0
    metadata           = "INCLUDE_ALL_METADATA"
  }
}

# CHECK: Enable Cloud Audit Logging
resource "google_project_iam_audit_config" "audit" {
  # COMPLIANT: All services audited
  service = "allServices"
  audit_log_config {
    log_type = "ADMIN_READ"
  }
  audit_log_config {
    log_type = "DATA_READ"
  }
  audit_log_config {
    log_type = "DATA_WRITE"
  }
}

# CHECK: Ensure no default network
resource "google_compute_network" "vpc" {
  # COMPLIANT: Custom network, not default
  name                    = "custom-vpc"
  auto_create_subnetworks = false
}
```

#### CIS AWS Foundations
```hcl
# CHECK: Enable MFA for root account
resource "aws_iam_account_password_policy" "strict" {
  # COMPLIANT: Strong password policy
  minimum_password_length        = 14
  require_lowercase_characters   = true
  require_numbers               = true
  require_uppercase_characters   = true
  require_symbols               = true
  allow_users_to_change_password = true
  max_password_age              = 90
  password_reuse_prevention     = 24
}

# CHECK: Enable CloudTrail logging
resource "aws_cloudtrail" "main" {
  # COMPLIANT: Multi-region trail with encryption
  name                          = "audit-trail"
  s3_bucket_name               = aws_s3_bucket.trail.id
  is_multi_region_trail        = true
  enable_log_file_validation   = true
  kms_key_id                   = aws_kms_key.trail.arn

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3:::*/*"]
    }
  }
}
```

### 2. PCI DSS Requirements

```hcl
# Requirement 2.2: Develop configuration standards
resource "google_compute_firewall" "secure" {
  # COMPLIANT: Restrictive firewall rules
  name    = "secure-firewall"
  network = google_compute_network.vpc.name

  deny {
    protocol = "all"
  }

  # Only allow specific required ports
  allow {
    protocol = "tcp"
    ports    = ["443"]  # Only HTTPS
  }

  source_ranges = ["10.0.0.0/8"]  # Internal only
  target_tags   = ["web-server"]
}

# Requirement 3.4: Encrypt PAN
resource "google_kms_crypto_key" "payment" {
  # COMPLIANT: Encryption for payment data
  name     = "payment-data-key"
  key_ring = google_kms_key_ring.payment.id

  rotation_period = "7776000s"  # 90 days

  version_template {
    algorithm        = "GOOGLE_SYMMETRIC_ENCRYPTION"
    protection_level = "HSM"
  }
}

# Requirement 8.2: Multi-factor authentication
resource "google_organization_iam_policy" "org" {
  # COMPLIANT: Enforce MFA
  org_id = var.org_id

  policy_data = jsonencode({
    bindings = [
      {
        role = "roles/owner"
        members = []  # No direct owner access
        condition = {
          title       = "Require MFA"
          description = "Require multi-factor authentication"
          expression  = "request.auth.claims.mfa == true"
        }
      }
    ]
  })
}
```

### 3. HIPAA Controls

```hcl
# §164.312(a)(1): Access control
resource "aws_iam_role" "hipaa_compliant" {
  # COMPLIANT: Unique user identification
  name = "hipaa-role-${var.user_id}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${var.account_id}:saml-provider/ADFS"
        }
        Action = "sts:AssumeRoleWithSAML"
        Condition = {
          StringEquals = {
            "SAML:aud" = "https://signin.aws.amazon.com/saml"
          }
        }
      }
    ]
  })
}

# §164.312(a)(2)(iv): Encryption and decryption
resource "aws_s3_bucket_server_side_encryption_configuration" "hipaa" {
  # COMPLIANT: Encryption at rest
  bucket = aws_s3_bucket.phi_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.hipaa.arn
    }
  }
}

# §164.312(b): Audit controls
resource "aws_s3_bucket_logging" "audit" {
  # COMPLIANT: Access logging
  bucket = aws_s3_bucket.phi_data.id

  target_bucket = aws_s3_bucket.audit_logs.id
  target_prefix = "phi-access-logs/"
}
```

### 4. SOC2 Standards

```hcl
# CC6.1: Logical and physical access controls
resource "google_compute_firewall" "soc2_compliant" {
  # COMPLIANT: Network segmentation
  priority = 1000

  source_service_accounts = [
    google_service_account.authorized.email
  ]

  # Deny by default
  deny {
    protocol = "all"
  }

  # Log all connections
  log_config {
    metadata = "INCLUDE_ALL_METADATA"
  }
}

# CC7.2: System monitoring
resource "google_monitoring_alert_policy" "soc2" {
  # COMPLIANT: Security monitoring
  display_name = "Unauthorized Access Attempt"

  conditions {
    display_name = "Failed authentication"
    condition_threshold {
      filter = "resource.type=\"gce_instance\" AND log.severity=\"ERROR\""
      comparison = "COMPARISON_GT"
      threshold_value = 5
      duration = "60s"
    }
  }

  notification_channels = [
    google_monitoring_notification_channel.security_team.name
  ]
}
```

### 5. GDPR Requirements

```hcl
# Article 32: Security of processing
resource "google_compute_backend_service" "gdpr" {
  # COMPLIANT: Encryption in transit
  protocol = "HTTPS"

  backend {
    group = google_compute_instance_group_manager.app.instance_group
  }

  # Data locality for GDPR
  backend {
    group = google_compute_instance_group_manager.eu.instance_group
    balancing_mode = "RATE"
    max_rate = 100

    # Keep EU traffic in EU
    description = "EU-only backend for GDPR compliance"
  }
}

# Article 25: Data protection by design
resource "google_bigquery_dataset" "gdpr" {
  # COMPLIANT: Privacy by design
  dataset_id = "user_data"
  location   = "EU"  # Data residency

  default_encryption_configuration {
    kms_key_name = google_kms_crypto_key.eu_key.id
  }

  default_table_expiration_ms = 7776000000  # 90 days auto-deletion
}
```

## Security Validations

### Encryption at Rest
```hcl
# CHECK: All storage encrypted
resource "google_compute_disk" "encrypted" {
  # COMPLIANT
  disk_encryption_key {
    kms_key_self_link = google_kms_crypto_key.disk.id
  }
}
```

### TLS/SSL Configuration
```hcl
# CHECK: Enforce TLS 1.2+
resource "google_compute_ssl_policy" "modern" {
  # COMPLIANT
  name            = "modern-ssl-policy"
  profile         = "MODERN"
  min_tls_version = "TLS_1_2"
}
```

### IAM Least Privilege
```hcl
# CHECK: No wildcard permissions
resource "google_project_iam_member" "least_privilege" {
  # COMPLIANT: Specific role, not owner/editor
  role   = "roles/compute.viewer"
  member = "serviceAccount:${google_service_account.app.email}"
}
```

### Network Segmentation
```hcl
# CHECK: Private subnets for databases
resource "google_compute_subnetwork" "database" {
  # COMPLIANT: No external IP
  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "database"
    ip_cidr_range = "192.168.0.0/24"
  }
}
```

### Logging and Monitoring
```hcl
# CHECK: Audit logging enabled
resource "google_logging_project_sink" "audit" {
  # COMPLIANT: Centralized logging
  name        = "audit-sink"
  destination = "storage.googleapis.com/${google_storage_bucket.audit.name}"

  filter = "severity >= WARNING"

  unique_writer_identity = true
}
```

### Backup Configuration
```hcl
# CHECK: Automated backups
resource "google_sql_database_instance" "compliant" {
  settings {
    backup_configuration {
      # COMPLIANT: Daily backups with PITR
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = 30
        retention_unit   = "COUNT"
      }
    }
  }
}
```

## Compliance Report

Generate compliance assessment:
```
Infrastructure Compliance Report
================================
Date: 2024-01-15
Scope: Production Infrastructure

Standards Compliance:
- CIS Benchmarks: 92% compliant (138/150 controls)
- PCI DSS: 88% compliant (11/12.4 requirements)
- HIPAA: 85% compliant (45/53 controls)
- SOC2: 90% compliant (Trust principles met)
- GDPR: 95% compliant (Data protection verified)

Critical Findings:
1. [CIS 2.1.1] Default network still exists
2. [PCI 8.2] MFA not enforced for all admin access
3. [HIPAA §164.312] Encryption missing on 3 buckets

High Priority Remediation:
- Enable MFA for all administrative access
- Encrypt remaining storage buckets
- Delete default VPC network
- Enable flow logs on all subnets

Compliance Score: B+ (87%)
Next Audit: 30 days
```

## Real-World Applications

### Healthcare Provider (HIPAA Compliance)

**Scenario:** Hospital deploying patient records system on GCP

```hcl
# terraform/hipaa-compliant-storage.tf
resource "google_storage_bucket" "patient_records" {
  name     = "hospital-patient-records"
  location = "US"

  # HIPAA: Encryption at rest
  encryption {
    default_kms_key_name = google_kms_crypto_key.hipaa.id
  }

  # HIPAA: Access logging
  logging {
    log_bucket = google_storage_bucket.audit_logs.name
  }

  # HIPAA: Versioning for data integrity
  versioning {
    enabled = true
  }

  # HIPAA: Lifecycle policies
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 2555  # 7 years retention
    }
  }

  # Block public access
  uniform_bucket_level_access = true
}

# Audit logging
resource "google_storage_bucket" "audit_logs" {
  name     = "hospital-audit-logs"
  location = "US"

  retention_policy {
    retention_period = 220752000  # 7 years in seconds
    is_locked        = true
  }
}
```

### Financial Institution (PCI DSS Compliance)

**Scenario:** Payment processing service requiring PCI DSS compliance

```hcl
# terraform/pci-dss-network.tf
resource "google_compute_network" "payment_vpc" {
  name                    = "payment-processing"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "payment_subnet" {
  name          = "payment-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = "us-central1"
  network       = google_compute_network.payment_vpc.id

  # PCI DSS: Enable flow logs
  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 1.0
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# PCI DSS: Network segmentation
resource "google_compute_firewall" "deny_all_ingress" {
  name    = "deny-all-ingress"
  network = google_compute_network.payment_vpc.name

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  priority      = 65535
}

resource "google_compute_firewall" "allow_payment_api" {
  name    = "allow-payment-api"
  network = google_compute_network.payment_vpc.name

  allow {
    protocol = "tcp"
    ports    = ["443"]  # Only HTTPS
  }

  source_ranges = ["10.0.0.0/8"]
  target_tags   = ["payment-api"]
  priority      = 1000
}
```

### SaaS Company (SOC 2 Type II Compliance)

**Scenario:** Multi-tenant SaaS application requiring SOC 2

```hcl
# terraform/soc2-compliant-infrastructure.tf
module "soc2_compliant_gke" {
  source = "./modules/compliant-gke"

  cluster_name = "production-cluster"
  region       = "us-central1"

  # SOC 2: Enable audit logging
  logging_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }

  # SOC 2: Enable monitoring
  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS"]
    managed_prometheus {
      enabled = true
    }
  }

  # SOC 2: Binary authorization
  binary_authorization {
    evaluation_mode = "PROJECT_SINGLETON_POLICY_ENFORCE"
  }

  # SOC 2: Network policies
  network_policy {
    enabled  = true
    provider = "CALICO"
  }

  # SOC 2: Pod security policies
  pod_security_policy_config {
    enabled = true
  }

  # SOC 2: Workload identity
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}
```

## Best Practices

### Policy as Code
- Store compliance policies in version control
- Use tools like OPA, Checkov, tfsec for automated validation
- Integrate compliance checks in CI/CD pipelines
- Version and document all policy changes

### Separation of Concerns
- Separate production and development environments
- Use different projects/accounts per environment
- Implement least privilege access
- Enforce network segmentation

### Audit and Monitoring
- Enable comprehensive audit logging
- Monitor compliance drift continuously
- Set up alerts for compliance violations
- Maintain audit logs for required retention periods

### Encryption
- Encrypt data at rest with customer-managed keys
- Encrypt data in transit (TLS 1.2+)
- Rotate encryption keys regularly
- Store keys separately from data

### Access Control
- Implement MFA for all privileged access
- Use service accounts with minimal permissions
- Regularly review and revoke unused access
- Maintain access logs for auditing

### Documentation
- Document compliance mappings (controls → resources)
- Maintain runbooks for compliance procedures
- Keep evidence of compliance activities
- Update documentation with infrastructure changes

## Common Pitfalls

### ❌ Hardcoded Secrets in IaC

**Problem:**
```hcl
resource "google_sql_database_instance" "main" {
  name = "production-db"

  settings {
    user_name     = "admin"
    user_password = "hardcoded_password_123"  # CRITICAL VIOLATION!
  }
}
```

**Solution:** Use secret management
```hcl
resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"

  replication {
    automatic = true
  }
}

resource "google_sql_database_instance" "main" {
  name = "production-db"
  # Password retrieved from Secret Manager at runtime
}
```

### ❌ Public Storage Buckets

**Problem:**
```hcl
resource "google_storage_bucket" "data" {
  name     = "company-data"
  location = "US"
  # No access controls - publicly accessible!
}
```

**Solution:** Enforce private access
```hcl
resource "google_storage_bucket" "data" {
  name     = "company-data"
  location = "US"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  iam_binding {
    role    = "roles/storage.objectViewer"
    members = ["serviceAccount:app@project.iam.gserviceaccount.com"]
  }
}
```

### ❌ Missing Encryption

**Problem:**
```hcl
resource "google_compute_disk" "data" {
  name = "application-data"
  # Uses Google-managed encryption - not compliant for some regulations
}
```

**Solution:** Use customer-managed encryption keys
```hcl
resource "google_kms_key_ring" "compliance" {
  name     = "compliance-keys"
  location = "us-central1"
}

resource "google_kms_crypto_key" "data_key" {
  name     = "data-encryption-key"
  key_ring = google_kms_key_ring.compliance.id

  rotation_period = "7776000s"  # 90 days
}

resource "google_compute_disk" "data" {
  name = "application-data"

  disk_encryption_key {
    kms_key_self_link = google_kms_crypto_key.data_key.id
  }
}
```

### ❌ Disabled Audit Logging

**Problem:**
```hcl
# No audit logging configuration
# Fails compliance requirements
```

**Solution:** Enable comprehensive audit logging
```hcl
resource "google_project_iam_audit_config" "project" {
  project = var.project_id
  service = "allServices"

  audit_log_config {
    log_type = "ADMIN_READ"
  }
  audit_log_config {
    log_type = "DATA_READ"
  }
  audit_log_config {
    log_type = "DATA_WRITE"
  }
}
```

### ❌ Overly Permissive Firewall Rules

**Problem:**
```hcl
resource "google_compute_firewall" "allow_all" {
  name    = "allow-all"
  network = google_compute_network.vpc.name

  allow {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]  # CRITICAL: Open to internet!
}
```

**Solution:** Implement least privilege network access
```hcl
resource "google_compute_firewall" "allow_specific" {
  name    = "allow-https-from-lb"
  network = google_compute_network.vpc.name

  allow {
    protocol = "tcp"
    ports    = ["443"]
  }

  source_ranges = ["10.0.0.0/8"]  # Internal only
  target_tags   = ["web-server"]
}
```

### ❌ No Compliance Drift Detection

**Problem:** Infrastructure changes made manually without validation

**Solution:** Implement continuous compliance monitoring
```yaml
# .github/workflows/compliance-check.yml
name: Compliance Check

on:
  push:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run compliance checks
        run: |
          # Check Terraform files
          tfsec .

          # Check for policy violations
          checkov -d . --framework terraform

          # Custom compliance rules
          opa test ./policies/
```

### ❌ Missing Data Retention Policies

**Problem:**
```hcl
resource "google_storage_bucket" "logs" {
  name = "application-logs"
  # No retention policy - might violate compliance
}
```

**Solution:** Implement required retention
```hcl
resource "google_storage_bucket" "logs" {
  name = "application-logs"

  retention_policy {
    retention_period = 220752000  # 7 years for financial data
    is_locked        = true        # Cannot be reduced
  }

  lifecycle_rule {
    action {
      type          = "SetStorageClass"
      storage_class = "ARCHIVE"
    }
    condition {
      age = 90  # Move to archive after 90 days
    }
  }
}
```

## Related Skills

- **helm-validator**: Ensures Kubernetes deployments meet compliance
- **docker-security**: Validates container security compliance
- **gcp-cost-guard**: Optimizes costs while maintaining compliance
- **k8s-optimizer**: Ensures Kubernetes resources follow security best practices

This skill ensures infrastructure code meets all relevant compliance standards and security best practices, reducing risk and ensuring regulatory adherence.