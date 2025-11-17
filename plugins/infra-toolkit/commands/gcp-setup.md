---
description: Initialize GCP project with best practices and required services
allowed-tools: Bash, Write, Read, Edit
---

# GCP Project Setup

## Parse Arguments
```bash
PROJECT_ID="${ARGUMENTS[0]}"  # GCP project ID
REGION="${ARGUMENTS[1]}"      # Deployment region (e.g., us-central1)
SERVICES="${ARGUMENTS[2]}"    # Comma-separated services
```

## Validate Input
Ensure required arguments:
- PROJECT_ID: Valid GCP project ID format
- REGION: Valid GCP region
- SERVICES: Optional, defaults to "compute,storage"

Parse services:
- compute: Compute Engine API
- storage: Cloud Storage
- kubernetes: Google Kubernetes Engine
- cloud-build: Cloud Build for CI/CD
- firestore: Firestore database
- bigquery: BigQuery analytics
- pubsub: Pub/Sub messaging

## Invoke GCP Expert
Invoke the `gcp-expert` agent to:

1. **Project Initialization**
   - Set default project and region
   - Enable billing if needed
   - Configure project metadata

2. **API Enablement**
   - Enable required Google Cloud APIs
   - Set up API quotas
   - Configure rate limiting

3. **IAM Setup**
   - Create service accounts
   - Assign appropriate roles
   - Set up workload identity
   - Configure organization policies

4. **Networking**
   - Create VPC network
   - Configure subnets
   - Set up Cloud NAT
   - Configure firewall rules
   - Enable Private Google Access

5. **Storage Setup**
   - Create storage buckets
   - Set lifecycle policies
   - Configure access controls
   - Enable versioning

6. **GKE Cluster** (if kubernetes service)
   - Create GKE cluster
   - Configure node pools
   - Set up autoscaling
   - Enable workload identity
   - Configure Binary Authorization

7. **Monitoring**
   - Enable Cloud Monitoring
   - Set up logging
   - Configure alerts
   - Create dashboards

## Output
Generate and display:
- Terraform configurations
- gcloud CLI scripts
- Setup documentation
- Cost estimates
- Next steps guide

## Example Usage
```
/gcp-setup my-project-123 us-central1 compute,storage,kubernetes
/gcp-setup prod-app europe-west1 cloud-build,firestore
/gcp-setup dev-env us-east1 compute,bigquery,pubsub
```