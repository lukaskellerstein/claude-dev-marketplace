---
description: Audit infrastructure configuration for security, cost, and compliance
allowed-tools: Read, Grep, Glob
---

# Infrastructure Audit

## Parse Arguments
```bash
SCOPE="${ARGUMENTS[0]:-all}"  # docker|kubernetes|terraform|security|cost|all
```

## Validate Input
Check audit scope:
- docker: Docker configurations and Dockerfiles
- kubernetes: K8s manifests and configurations
- terraform: Terraform modules and state
- security: Security-focused audit
- cost: Cost optimization audit
- all: Comprehensive audit (default)

## Invoke Infrastructure Expert
Invoke the `infrastructure-expert` agent with:
- Audit scope: $SCOPE
- Current directory context
- Infrastructure files found

The agent will perform:

1. **Security Audit**
   - Check for exposed secrets
   - Validate IAM permissions
   - Review network exposure
   - Check encryption settings
   - Validate authentication methods
   - Scan for vulnerabilities

2. **Cost Analysis**
   - Identify over-provisioned resources
   - Find unused resources
   - Suggest right-sizing
   - Recommend reserved instances
   - Calculate potential savings

3. **Compliance Check**
   - CIS benchmark validation
   - PCI DSS compliance
   - HIPAA requirements
   - SOC2 standards
   - GDPR compliance

4. **Best Practices**
   - Resource naming conventions
   - Tagging strategies
   - Backup configurations
   - Monitoring coverage
   - Documentation completeness

5. **Performance Review**
   - Identify bottlenecks
   - Check scaling configurations
   - Review caching strategies
   - Validate load balancing

## Report Generation
Generate comprehensive report including:
- Executive summary
- Critical issues (requiring immediate action)
- High priority recommendations
- Medium priority improvements
- Cost saving opportunities
- Compliance gaps
- Remediation playbook

## Output Format
```
=== Infrastructure Audit Report ===
Scope: [SCOPE]
Date: [TIMESTAMP]

CRITICAL ISSUES: [count]
- [Issue description and remediation]

HIGH PRIORITY: [count]
- [Recommendation and impact]

COST SAVINGS: $[amount]/month
- [Optimization opportunities]

COMPLIANCE: [percentage]%
- [Standards and gaps]

NEXT STEPS:
1. [Prioritized action items]
```

## Example Usage
```
/infra-audit all
/infra-audit security
/infra-audit cost
/infra-audit kubernetes
/infra-audit terraform
```