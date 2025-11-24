# Security Plugin

Comprehensive security toolkit for vulnerability scanning, OWASP Top 10 compliance, secure coding practices, and security audits.

## Features

### Agents

- **security-auditor**: Expert in comprehensive security audits covering OWASP Top 10, vulnerability assessment, secure architecture review, and compliance verification
- **vulnerability-scanner**: Expert in automated vulnerability scanning for dependencies, secrets detection, container security, and infrastructure vulnerabilities
- **secure-code-expert**: Expert in secure coding practices, code injection prevention, input validation, authentication implementation, and security pattern implementation

### Commands

- `/security-audit`: Perform comprehensive security audit covering OWASP Top 10, vulnerabilities, and compliance
- `/scan-vulnerabilities`: Scan for dependency vulnerabilities, secrets, container security issues, and run automated security checks
- `/fix-vulnerability`: Fix specific security vulnerabilities with secure code implementations and automated patches

### Skills

- **input-validation**: Auto-invoked when processing user input to ensure proper validation, sanitization, and injection prevention
- **secure-authentication**: Auto-invoked when implementing authentication, password handling, session management, or authorization to ensure secure practices

## Usage

### Comprehensive Security Audit

```
/security-audit

Perform comprehensive security audit of the web application
including OWASP Top 10, dependency vulnerabilities, and
infrastructure security
```

**What it does:**
- Analyzes entire codebase for OWASP Top 10 vulnerabilities
- Reviews authentication and authorization implementation
- Checks cryptographic implementations
- Identifies security misconfigurations
- Assesses compliance with security standards
- Provides prioritized remediation roadmap

### Vulnerability Scanning

```
/scan-vulnerabilities

Scan all dependencies, check for exposed secrets, and analyze
container security for the entire application
```

**What it does:**
- Scans npm/pip/maven/cargo dependencies for known CVEs
- Detects hardcoded secrets (API keys, passwords, tokens)
- Analyzes Docker images for vulnerabilities
- Checks for infrastructure misconfigurations
- Provides upgrade paths and remediation steps

### Fix Security Vulnerabilities

```
/fix-vulnerability

Fix SQL injection vulnerability in user search endpoint
(src/api/users.js:45) using parameterized queries
```

**What it does:**
- Implements secure code replacements
- Adds input validation and sanitization
- Implements proper authentication/authorization
- Includes security tests
- Provides complete before/after code examples

### Use Agents Directly

Invoke specialized agents for focused work:

- "Use security-auditor to perform OWASP Top 10 assessment"
- "Use vulnerability-scanner to scan for exposed AWS credentials"
- "Use secure-code-expert to implement JWT authentication securely"

## Security Coverage

### OWASP Top 10 (2021)

1. **A01: Broken Access Control**
   - IDOR (Insecure Direct Object Reference) prevention
   - Authorization bypass detection
   - Privilege escalation prevention
   - Missing function level access control

2. **A02: Cryptographic Failures**
   - Weak encryption detection
   - Insecure password storage
   - Missing encryption at rest/transit
   - Weak random number generation

3. **A03: Injection**
   - SQL injection prevention
   - NoSQL injection prevention
   - Command injection prevention
   - LDAP injection prevention
   - XSS (Cross-Site Scripting) prevention

4. **A04: Insecure Design**
   - Threat modeling
   - Secure design patterns
   - Business logic vulnerabilities

5. **A05: Security Misconfiguration**
   - Default credentials
   - Unnecessary features enabled
   - Missing security headers
   - Verbose error messages

6. **A06: Vulnerable Components**
   - Outdated dependencies
   - Known CVE detection
   - Supply chain security
   - Dependency scanning

7. **A07: Authentication Failures**
   - Weak password policies
   - Missing MFA
   - Session management issues
   - Credential stuffing prevention

8. **A08: Software and Data Integrity Failures**
   - Insecure deserialization
   - CI/CD pipeline security
   - Unsigned/unverified code

9. **A09: Security Logging and Monitoring Failures**
   - Missing security logging
   - Insufficient monitoring
   - No incident response

10. **A10: Server-Side Request Forgery (SSRF)**
    - SSRF detection and prevention
    - URL validation

### Vulnerability Categories

**Dependency Vulnerabilities**
- NPM package vulnerabilities (npm audit)
- Python package vulnerabilities (pip-audit, safety)
- Java/Maven vulnerabilities (OWASP Dependency-Check)
- Go module vulnerabilities (govulncheck)
- Ruby gem vulnerabilities (bundler-audit)
- Container image vulnerabilities (Trivy, Grype)

**Secrets Detection**
- AWS access keys and secrets
- GCP service account keys
- Azure connection strings
- Database credentials
- API keys (Stripe, GitHub, Slack, etc.)
- Private keys (SSH, RSA, PGP)
- OAuth tokens and JWT secrets
- High-entropy strings

**Container Security**
- Base image vulnerabilities
- Outdated packages in containers
- Insecure Dockerfile patterns
- Root user usage
- Exposed secrets in layers
- Excessive privileges

**Infrastructure Security**
- Open ports and services
- Cloud misconfigurations
- S3 bucket permissions
- IAM policy weaknesses
- Security group rules
- Unencrypted resources
- SSL/TLS configuration

## Secure Coding Patterns

### SQL Injection Prevention

```javascript
// VULNERABLE
const query = `SELECT * FROM users WHERE id = ${userId}`;

// SECURE - Parameterized Query
const query = 'SELECT * FROM users WHERE id = ?';
const result = await db.query(query, [userId]);

// SECURE - ORM
const user = await User.findOne({ where: { id: userId } });
```

### XSS Prevention

```javascript
// VULNERABLE
element.innerHTML = userInput;

// SECURE
element.textContent = userInput;

// SECURE - Sanitized
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Authentication

```javascript
const bcrypt = require('bcrypt');

// Hash password
async function hashPassword(password) {
  const saltRounds = 12;
  return await bcrypt.hash(password, saltRounds);
}

// Verify password
async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}
```

### Authorization

```javascript
// Check ownership before allowing access
app.get('/orders/:id', authenticateToken, async (req, res) => {
  const order = await Order.findById(req.params.id);

  if (!order) {
    return res.status(404).json({ error: 'Not found' });
  }

  // IDOR Prevention - verify ownership
  if (order.userId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json(order);
});
```

### Input Validation

```javascript
const { body, validationResult } = require('express-validator');

const validateUser = [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }).matches(/^(?=.*[A-Za-z])(?=.*\d)/),
  body('name').trim().isLength({ min: 2, max: 50 }).escape(),
];

app.post('/users', validateUser, (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  // Process valid input
});
```

### CSRF Protection

```javascript
const csrf = require('csurf');
const csrfProtection = csrf({ cookie: true });

app.get('/form', csrfProtection, (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit', csrfProtection, (req, res) => {
  // CSRF token validated automatically
});
```

### Rate Limiting

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later'
});

app.use('/api/', limiter);
```

## Example Workflows

### Securing a New Application

1. **Initial Security Audit**
   ```
   /security-audit

   Perform initial security assessment of the new application
   to identify baseline security posture and critical issues
   ```

2. **Scan for Vulnerabilities**
   ```
   /scan-vulnerabilities

   Scan dependencies and check for exposed secrets in the
   new application codebase
   ```

3. **Fix Critical Issues**
   ```
   /fix-vulnerability

   Fix critical SQL injection in login endpoint identified
   in the security audit
   ```

4. **Implement Security Controls**
   - Use `secure-code-expert` to implement authentication
   - Add input validation with `input-validation` skill
   - Set up rate limiting and security headers

### Pre-Production Security Review

1. **Comprehensive Audit**
   ```
   /security-audit

   Perform final security audit before production deployment
   including OWASP Top 10, compliance, and infrastructure
   ```

2. **Dependency Check**
   ```
   /scan-vulnerabilities

   Final dependency vulnerability scan and secret detection
   before production release
   ```

3. **Fix Remaining Issues**
   ```
   /fix-vulnerability

   Address all high and critical vulnerabilities identified
   in pre-production audit
   ```

### Responding to Security Incident

1. **Vulnerability Analysis**
   ```
   /security-audit

   Perform targeted audit focusing on the vulnerability type
   that was exploited to find similar issues
   ```

2. **Scan for Exposure**
   ```
   /scan-vulnerabilities

   Scan for exposed credentials and secrets that may have
   been compromised during the incident
   ```

3. **Implement Fixes**
   ```
   /fix-vulnerability

   Implement secure fixes for all identified vulnerabilities
   related to the security incident
   ```

### Regular Security Maintenance

1. **Weekly Dependency Scan**
   ```
   /scan-vulnerabilities

   Weekly automated scan for new dependency vulnerabilities
   and security updates
   ```

2. **Monthly Security Audit**
   ```
   /security-audit

   Monthly comprehensive security audit to identify new
   vulnerabilities and ensure compliance
   ```

3. **Continuous Improvement**
   - Review security logs
   - Update security policies
   - Train team on secure coding
   - Improve security tooling

## Integration with Development Workflow

### CI/CD Pipeline Integration

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Dependency Scan
        run: npm audit --audit-level=high

      - name: Secret Scan
        uses: gitleaks/gitleaks-action@v2

      - name: SAST
        run: npx semgrep --config auto --error

      - name: Container Scan
        run: |
          docker build -t myapp:latest .
          trivy image --severity HIGH,CRITICAL myapp:latest
```

### Pre-Commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Scan for secrets before commit
gitleaks protect --staged

# Run security linting
npm run lint:security

# Fail if issues found
if [ $? -ne 0 ]; then
  echo "Security issues found. Commit blocked."
  exit 1
fi
```

### Development Best Practices

1. **Security by Design**: Consider security from project inception
2. **Shift Left**: Catch security issues early in development
3. **Defense in Depth**: Multiple layers of security controls
4. **Least Privilege**: Minimal permissions for users and services
5. **Fail Securely**: Failures don't compromise security
6. **Input Validation**: Validate all user input on server side
7. **Output Encoding**: Context-aware encoding for all output
8. **Regular Scanning**: Automated daily/weekly security scans
9. **Security Reviews**: Manual code review for security-critical code
10. **Incident Response**: Plan and practice incident response

## Compliance & Standards

### OWASP Coverage
- ✅ OWASP Top 10 (2021)
- ✅ OWASP ASVS (Application Security Verification Standard)
- ✅ OWASP Testing Guide
- ✅ OWASP Cheat Sheet Series

### Security Frameworks
- **CWE**: Common Weakness Enumeration
- **CVE**: Common Vulnerabilities and Exposures
- **CVSS**: Common Vulnerability Scoring System
- **NIST**: Cybersecurity Framework
- **PCI DSS**: Payment Card Industry Data Security Standard
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act
- **SOC 2**: Service Organization Control 2
- **ISO 27001**: Information Security Management

## Security Tools Integration

### Scanning Tools
- **npm audit**: NPM dependency vulnerabilities
- **pip-audit / safety**: Python package vulnerabilities
- **govulncheck**: Go module vulnerabilities
- **Trivy**: Container and filesystem vulnerabilities
- **Grype**: Vulnerability scanner for containers and filesystems
- **Gitleaks**: Secret detection in git repositories
- **TruffleHog**: Secret scanning with high entropy detection
- **Semgrep**: Static analysis security testing (SAST)
- **Bandit**: Python security linter
- **ESLint security plugins**: JavaScript security linting

### Security Services
- **Snyk**: Dependency vulnerability database
- **GitHub Security Advisories**: Package vulnerabilities
- **NVD**: National Vulnerability Database
- **Have I Been Pwned**: Password breach detection

## Advanced Security Topics

### Threat Modeling
- STRIDE methodology
- Attack tree analysis
- Data flow diagrams
- Trust boundaries
- Risk assessment

### Secure Architecture
- Zero Trust Architecture
- Defense in depth
- Principle of least privilege
- Separation of duties
- Security zones and segmentation

### Cryptography
- Encryption at rest and in transit
- Key management and rotation
- Digital signatures
- Certificate management
- Perfect Forward Secrecy

### Security Monitoring
- Security event logging
- Intrusion detection (IDS)
- Intrusion prevention (IPS)
- SIEM integration
- Anomaly detection

### Incident Response
- Incident detection
- Containment procedures
- Evidence collection
- Root cause analysis
- Post-incident review

## Integration with Other Plugins

- **backend-plugin**: Secure API design and implementation
- **frontend-plugin**: XSS prevention and secure UI patterns
- **database-plugin**: Secure database configuration and queries
- **infra-plugin**: Infrastructure security and secrets management
- **cicd-plugin**: Security scanning in CI/CD pipeline

## Resources & References

### OWASP Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Security Standards
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PCI DSS](https://www.pcisecuritystandards.org/)

### Learning Resources
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Security Training by Google](https://www.google.com/about/appsecurity/learning/index.html)

## Support & Troubleshooting

### Common Issues

**False Positives in Scanning**
- Review and whitelist known safe patterns
- Update scanning rules and configurations
- Document exceptions with justification

**Performance Impact**
- Run expensive scans asynchronously
- Cache scan results
- Optimize scan scope and frequency

**Breaking Changes from Security Updates**
- Review changelog before updating
- Test in staging environment
- Have rollback plan ready

### Getting Help

For security issues:
1. Run `/security-audit` for comprehensive analysis
2. Use `/scan-vulnerabilities` for automated detection
3. Consult OWASP resources for specific vulnerability types
4. Review security logs for patterns
5. Engage security team for complex issues

---

**Security is not a one-time task, it's an ongoing process.** Use this plugin to maintain a strong security posture throughout your application lifecycle.
