---
name: iac-compliance
description: Ensure infrastructure code compliance with security standards
allowed-tools: Read, Grep
---

# Infrastructure as Code Compliance Skill

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

This skill ensures infrastructure code meets all relevant compliance standards and security best practices, reducing risk and ensuring regulatory adherence.