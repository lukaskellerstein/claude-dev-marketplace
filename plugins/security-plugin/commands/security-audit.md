---
description: Perform comprehensive security audit covering OWASP Top 10, vulnerabilities, secure architecture, and compliance
---

Conduct a thorough security audit of the application to identify vulnerabilities and security weaknesses.

## Process

Follow these steps:

1. **Initial Assessment**: Understand the application
   - Identify tech stack and frameworks
   - Map application architecture and components
   - Identify entry points and attack surface
   - Review authentication and authorization mechanisms
   - Check for existing security documentation

2. **Launch Security Auditor**: Use the `security-plugin:security-auditor` agent to:
   - Perform OWASP Top 10 vulnerability assessment
   - Review authentication and authorization implementation
   - Analyze data handling and encryption
   - Check for security misconfigurations
   - Review error handling and logging
   - Assess API security
   - Evaluate infrastructure security
   - Check compliance with security standards

3. **Code Review**: Deep dive into security-critical code
   - Input validation and sanitization
   - Output encoding and escaping
   - SQL/NoSQL query construction
   - Authentication logic
   - Authorization checks
   - Cryptographic implementations
   - Session management
   - File upload handling
   - Error handling

4. **Configuration Review**: Check all security configurations
   - Security headers (CSP, HSTS, etc.)
   - CORS settings
   - TLS/SSL configuration
   - Secrets management
   - Database security settings
   - Cloud resource configurations
   - Container security settings

5. **Threat Modeling**: Identify potential attack vectors
   - Data flow diagrams
   - Trust boundaries
   - Attack surface analysis
   - Threat scenarios
   - Security control assessment

## Output

Present a comprehensive security audit report with:

### Executive Summary
- Overall security posture rating (Critical/High Risk/Moderate/Good)
- Total vulnerabilities found by severity
- Critical findings requiring immediate action
- Compliance assessment (OWASP, GDPR, PCI DSS, etc.)
- Recommended next steps

### Critical Findings
For each critical vulnerability:
- **Severity**: Critical with CVSS score
- **Category**: OWASP Top 10 category, CWE ID
- **Location**: Exact file path and line numbers
- **Description**: What the vulnerability is and why it's dangerous
- **Exploit Scenario**: How an attacker could exploit this
- **Impact**: Data breach, unauthorized access, DoS, etc.
- **Proof of Concept**: Demonstration of the vulnerability
- **Remediation**: Step-by-step fix with code examples
- **Timeline**: Recommended fix within 24-48 hours

### High Priority Findings
Similar format to critical, fix within 1-2 weeks

### Medium/Low Priority Findings
Grouped by category with summary remediation guidance

### Secure Architecture Review
- Architecture diagram with security boundaries
- Trust zones and data flow
- Security controls assessment
- Single points of failure
- Defense in depth evaluation
- Recommendations for architectural improvements

### Compliance Assessment
- **OWASP Top 10**: Coverage for each category
  - A01: Broken Access Control - Status and findings
  - A02: Cryptographic Failures - Status and findings
  - (Continue for all 10 categories)
- **GDPR** (if applicable): Data protection assessment
- **PCI DSS** (if handling payments): Payment security assessment
- **HIPAA** (if handling health data): PHI protection assessment
- **Industry Standards**: SOC 2, ISO 27001 readiness

### Risk Matrix
Prioritized list of vulnerabilities:
```
|   Severity   | Exploitability | Business Impact | Priority |
|--------------|----------------|-----------------|----------|
| Critical     | High           | Critical        | P0       |
| High         | High           | High            | P1       |
| High         | Medium         | High            | P1       |
| Medium       | High           | Medium          | P2       |
```

### Remediation Roadmap

**Immediate Actions (0-48 hours)**
- Critical vulnerabilities requiring immediate patching
- Emergency security measures

**Short Term (1-4 weeks)**
- High priority vulnerabilities
- Security configuration improvements
- Quick wins (easy to fix, high impact)

**Medium Term (1-3 months)**
- Medium priority vulnerabilities
- Security tool implementation
- Training and process improvements

**Long Term (3-12 months)**
- Low priority findings
- Strategic security initiatives
- Security architecture improvements
- Compliance certification

### Testing Recommendations
- Penetration testing scope
- Automated security testing setup
- Code review processes
- Security regression testing

### Monitoring & Detection
- Security logging requirements
- Intrusion detection recommendations
- Anomaly detection setup
- Incident response preparation

## Examples

### Full Application Audit
```
/security-audit

Perform comprehensive security audit of the web application
including OWASP Top 10, dependency vulnerabilities, and
infrastructure security
```

### API Security Audit
```
/security-audit

Focus on API security: authentication, authorization, rate
limiting, input validation, and API-specific vulnerabilities
```

### Compliance Audit
```
/security-audit

Perform GDPR compliance audit focusing on data protection,
consent management, data retention, and user rights
```

### Post-Incident Audit
```
/security-audit

Perform security audit after security incident to identify
root cause, related vulnerabilities, and prevention measures
```

## Best Practices Applied

- **Risk-Based Approach**: Prioritize by business impact and exploitability
- **Defense in Depth**: Multiple layers of security controls
- **Least Privilege**: Minimal permissions for users and services
- **Secure by Default**: Secure configurations out of the box
- **Fail Securely**: Failures don't compromise security
- **Complete Mediation**: All access requests are checked
- **Open Design**: Security doesn't rely on obscurity
- **Separation of Duties**: No single person has complete control
- **Least Common Mechanism**: Minimize shared resources
- **Psychological Acceptability**: Security is usable

## Integration with Other Commands

- Run `/security-audit` first to identify issues
- Follow with `/scan-vulnerabilities` for dependency analysis
- Use `/fix-vulnerability` to remediate specific findings
- Implement fixes with `security-plugin:secure-code-expert` agent

Provide actionable, prioritized security audit reports that enable immediate remediation of critical vulnerabilities.
