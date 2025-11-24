---
description: Scan for dependency vulnerabilities, secrets, container security issues, and run automated security checks
---

Run automated security scans to detect vulnerabilities in dependencies, exposed secrets, and security misconfigurations.

## Process

Follow these steps:

1. **Environment Detection**: Identify scanning targets
   - Detect package managers (npm, pip, maven, go, cargo, etc.)
   - Identify container images (Docker, OCI)
   - Find configuration files
   - Check for secrets in code and git history
   - Map cloud resources if applicable

2. **Launch Vulnerability Scanner**: Use the `vulnerability-scanner` agent to:
   - Run dependency vulnerability scans
   - Detect hardcoded secrets and credentials
   - Scan container images for vulnerabilities
   - Check for infrastructure misconfigurations
   - Search for dangerous code patterns
   - Analyze security configurations
   - Generate comprehensive vulnerability report

3. **Dependency Analysis**: Scan all dependencies
   - Direct dependencies vulnerabilities
   - Transitive dependencies risks
   - CVE lookup and CVSS scoring
   - Exploitability assessment
   - Available patches and upgrade paths
   - Breaking changes in security updates

4. **Secrets Detection**: Scan for exposed secrets
   - API keys and tokens
   - Database credentials
   - Cloud provider keys (AWS, GCP, Azure)
   - Private keys and certificates
   - OAuth tokens
   - High-entropy strings
   - Check git history for leaked secrets

5. **Container Security**: If containers are present
   - Base image vulnerabilities
   - Package vulnerabilities in image
   - Dockerfile security issues
   - Container configuration weaknesses
   - Exposed secrets in image layers

6. **Prioritization & Reporting**: Create actionable report
   - Severity-based prioritization
   - Exploitability assessment
   - False positive filtering
   - Upgrade recommendations
   - Quick fix identification

## Output

Present a comprehensive vulnerability scan report with:

### Scan Summary
```
Total Vulnerabilities: 47
├─ Critical: 5 (Immediate action required)
├─ High: 15 (Fix within 1 week)
├─ Medium: 20 (Fix within 1 month)
└─ Low: 7 (Fix when possible)

Secrets Found: 3 (CRITICAL - Revoke immediately)
Container Issues: 12
Configuration Issues: 8
```

### Critical Vulnerabilities

For each critical vulnerability:
```markdown
## CVE-2023-12345 - Prototype Pollution in lodash

**Severity**: CRITICAL (CVSS 9.8)
**Package**: lodash@4.17.19
**Fixed In**: lodash@4.17.21
**Exploit**: Public exploit available, actively exploited in the wild

### Description
Prototype pollution vulnerability allows attackers to inject properties
into Object.prototype, leading to potential remote code execution.

### Location
- package.json (line 15)
- Used in: src/utils/helpers.js (line 45)
- Used in: src/api/users.js (line 67)

### Impact
- Remote code execution possible
- Application crash/DoS
- Data manipulation

### Exploitation
Attackers can send malicious payloads through API endpoints that process
user input using vulnerable lodash functions.

### Remediation
**IMMEDIATE ACTION REQUIRED**

1. Update lodash to 4.17.21 or later:
   ```bash
   npm install lodash@4.17.21
   # or
   npm update lodash
   ```

2. If update not possible immediately, add input validation:
   ```javascript
   // Add to all user input processing
   function sanitizeObject(obj) {
     if (obj.__proto__ || obj.constructor || obj.prototype) {
       throw new Error('Invalid object properties');
     }
     return obj;
   }
   ```

3. Test after update:
   ```bash
   npm test
   npm audit
   ```

### References
- https://nvd.nist.gov/vuln/detail/CVE-2023-12345
- https://github.com/advisories/GHSA-xxxx-xxxx-xxxx
- https://snyk.io/vuln/SNYK-JS-LODASH-1234567
```

### Exposed Secrets

```markdown
## CRITICAL: AWS Access Keys Exposed

**Location**: config/aws.js:12
**Type**: AWS Access Key
**Pattern Match**: AKIAIOSFODNN7EXAMPLE

### Risk
- Full AWS account access
- Potential data breach
- Unauthorized resource usage
- Financial impact from resource abuse

### Immediate Actions Required

1. **REVOKE IMMEDIATELY** in AWS Console:
   - Go to IAM > Users > Security Credentials
   - Delete the exposed access key
   - Create new access key

2. **Rotate Secret**:
   ```bash
   aws iam delete-access-key --access-key-id AKIAIOSFODNN7EXAMPLE
   aws iam create-access-key --user-name your-user
   ```

3. **Move to Environment Variables**:
   ```javascript
   // BEFORE (INSECURE)
   const AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE';

   // AFTER (SECURE)
   const AWS_ACCESS_KEY = process.env.AWS_ACCESS_KEY_ID;
   ```

4. **Use AWS Secrets Manager** (Recommended):
   ```javascript
   const AWS = require('aws-sdk');
   const client = new AWS.SecretsManager();

   async function getSecret() {
     const data = await client.getSecretValue({
       SecretId: 'prod/aws/credentials'
     }).promise();
     return JSON.parse(data.SecretString);
   }
   ```

5. **Check CloudTrail** for unauthorized usage

6. **Add to .gitignore**:
   ```
   .env
   .env.local
   config/secrets.js
   credentials.json
   ```

7. **Scan Git History** and remove:
   ```bash
   # BFG Repo-Cleaner (recommended)
   bfg --replace-text passwords.txt repo.git

   # Or git filter-branch
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch config/aws.js' \
     --prune-empty --tag-name-filter cat -- --all
   ```
```

### Dependency Vulnerabilities by Package

Organized by package for easy remediation:

```markdown
### lodash (4.17.19 → 4.17.21)
- CVE-2023-12345 (Critical): Prototype pollution
- CVE-2023-12346 (High): ReDoS in template
- **Fix**: `npm update lodash` ✅ Non-breaking

### express (4.17.1 → 4.18.2)
- CVE-2022-24999 (High): Open redirect
- **Fix**: `npm install express@4.18.2` ⚠️ May have breaking changes

### jsonwebtoken (8.5.1 → 9.0.0)
- CVE-2022-23529 (High): Algorithm confusion
- CVE-2022-23540 (Medium): Improper verification
- **Fix**: `npm install jsonwebtoken@9.0.0` ⚠️ BREAKING CHANGES
  - Review JWT verification code
  - Update algorithm specifications
  - Test authentication thoroughly
```

### Container Vulnerabilities

```markdown
## Container: myapp:latest

**Base Image**: node:16 (OUTDATED)
**Total Vulnerabilities**: 45
- Critical: 8
- High: 15
- Medium: 18
- Low: 4

### Critical Issues

1. **CVE-2023-XXXXX in openssl** (CVSS 9.8)
   - Remote code execution via crafted certificate
   - Fixed in openssl 3.0.9

2. **Base image end-of-life**
   - Node.js 16 reached EOL on 2023-09-11
   - No security updates

### Remediation

**Update Dockerfile**:
```dockerfile
# BEFORE
FROM node:16

# AFTER
FROM node:20.10-alpine

# Benefits:
# - Latest security patches
# - Smaller image size (alpine)
# - Active LTS support until 2026
```

**Multi-stage build for smaller attack surface**:
```dockerfile
# Build stage
FROM node:20.10 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:20.10-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Rebuild and rescan**:
```bash
docker build -t myapp:latest .
trivy image myapp:latest
```
```

### Quick Wins (Easy to Fix, High Impact)

```markdown
1. ✅ **Update lodash** (5 min, fixes 2 critical vulnerabilities)
   ```bash
   npm update lodash
   ```

2. ✅ **Rotate exposed AWS key** (10 min, prevents account compromise)
   - Revoke in AWS Console
   - Update environment variables

3. ✅ **Update base image** (15 min, fixes 8 critical container CVEs)
   ```bash
   # Update Dockerfile: FROM node:20.10-alpine
   docker build -t myapp:latest .
   ```

4. ✅ **Add security headers** (20 min, prevents XSS/Clickjacking)
   ```bash
   npm install helmet
   # Add app.use(helmet()) in server.js
   ```

5. ✅ **Enable npm audit in CI** (10 min, catch future vulnerabilities)
   ```yaml
   # .github/workflows/security.yml
   - run: npm audit --audit-level=high
   ```
```

### Remediation Timeline

```markdown
## Week 1 (Critical + Quick Wins)
- [ ] Revoke exposed secrets (Day 1)
- [ ] Update lodash, express, axios (Day 1-2)
- [ ] Update container base image (Day 2)
- [ ] Add security headers (Day 3)
- [ ] Setup automated scanning in CI (Day 3-4)

## Week 2-4 (High Priority)
- [ ] Update jsonwebtoken with breaking changes
- [ ] Fix SQL injection vulnerabilities
- [ ] Implement rate limiting
- [ ] Update remaining high severity dependencies
- [ ] Container security hardening

## Month 2-3 (Medium/Low Priority)
- [ ] Update medium severity dependencies
- [ ] Implement additional security controls
- [ ] Security training for team
- [ ] Penetration testing
```

### CI/CD Integration

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for secret scanning

      - name: Dependency Scan
        run: |
          npm audit --audit-level=high
          # Fail if critical or high vulnerabilities found

      - name: Secret Scan
        uses: gitleaks/gitleaks-action@v2

      - name: Container Scan
        run: |
          docker build -t myapp:latest .
          trivy image --severity HIGH,CRITICAL --exit-code 1 myapp:latest

      - name: SAST
        run: |
          npx semgrep --config auto --error
```

## Examples

### Full Vulnerability Scan
```
/scan-vulnerabilities

Scan all dependencies, check for exposed secrets, and analyze
container security for the entire application
```

### Dependency-Only Scan
```
/scan-vulnerabilities

Focus on dependency vulnerabilities in package.json and provide
upgrade path with breaking changes analysis
```

### Secrets Detection
```
/scan-vulnerabilities

Scan codebase and git history for exposed secrets, API keys,
and credentials that need to be rotated
```

### Container Security Scan
```
/scan-vulnerabilities

Scan all Docker images for vulnerabilities and provide
hardened Dockerfile recommendations
```

### Pre-Release Scan
```
/scan-vulnerabilities

Run comprehensive security scan before production release
including dependencies, secrets, and configuration
```

## Best Practices Applied

- **Automated Scanning**: Run scans on every commit and daily
- **Shift Left**: Catch vulnerabilities early in development
- **Risk-Based Prioritization**: Focus on critical and exploitable vulnerabilities
- **Actionable Results**: Provide specific upgrade commands and code fixes
- **Continuous Monitoring**: Setup automated alerts for new vulnerabilities
- **Minimal False Positives**: Filter out noise to focus on real issues
- **Supply Chain Security**: Monitor entire dependency tree
- **Secret Prevention**: Block commits with secrets

## Integration with Other Commands

- Run `/scan-vulnerabilities` regularly (daily/weekly)
- Follow with `/fix-vulnerability` for specific CVEs
- Combine with `/security-audit` for comprehensive assessment
- Use `vulnerability-scanner` agent for deep analysis

Provide actionable vulnerability scan reports with clear remediation steps, severity-based prioritization, and automated fixes where possible.
