---
name: security-validation
description: Automatically validate agent security, prevent prompt injection, and protect sensitive data
allowed-tools: Read, Write, Bash
---

# Security Validation Skill

This skill automatically validates agent security, protects against attacks, and ensures safe operation.

## When This Activates

This skill activates when:
- Creating new agents
- Deploying to production
- Handling user input
- Processing sensitive data
- Running security tests

## What It Does

### 1. Input Validation

Protects against attacks:
- Prompt injection detection
- SQL injection prevention
- XSS prevention
- Command injection blocking

### 2. Output Sanitization

Prevents data leaks:
- PII redaction
- Sensitive data filtering
- Safe output formatting
- Credential protection

### 3. Access Control

Enforces security:
- Tool permission checking
- Rate limiting
- Authentication validation
- Authorization enforcement

## Implementation

```python
import re
from typing import List, Dict, Any

class SecurityValidator:
    def __init__(self):
        self.pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
        }

        self.injection_patterns = [
            r"ignore\s+previous\s+instructions",
            r"system:\s*you\s+are\s+now",
            r"<\s*script",
            r"javascript:",
            r"on\w+\s*=",
            r"DROP\s+TABLE",
            r"UNION\s+SELECT",
            r"\|\s*rm\s+-rf",
            r"&&\s*cat\s+/etc/passwd",
        ]

    def validate_input(self, user_input: str) -> Dict[str, Any]:
        """Validate user input for security issues"""

        issues = []

        # Check for prompt injection
        if self._detect_prompt_injection(user_input):
            issues.append({
                "type": "prompt_injection",
                "severity": "high",
                "message": "Potential prompt injection detected"
            })

        # Check for SQL injection
        if self._detect_sql_injection(user_input):
            issues.append({
                "type": "sql_injection",
                "severity": "high",
                "message": "Potential SQL injection detected"
            })

        # Check for XSS
        if self._detect_xss(user_input):
            issues.append({
                "type": "xss",
                "severity": "medium",
                "message": "Potential XSS attack detected"
            })

        return {
            "is_safe": len(issues) == 0,
            "issues": issues
        }

    def _detect_prompt_injection(self, text: str) -> bool:
        """Detect prompt injection attempts"""
        text_lower = text.lower()

        for pattern in self.injection_patterns[:4]:  # Prompt-specific
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        return False

    def _detect_sql_injection(self, text: str) -> bool:
        """Detect SQL injection attempts"""
        text_lower = text.lower()

        sql_patterns = self.injection_patterns[5:7]
        for pattern in sql_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True

        return False

    def _detect_xss(self, text: str) -> bool:
        """Detect XSS attempts"""
        xss_patterns = self.injection_patterns[2:5]

        for pattern in xss_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def sanitize_output(self, output: str) -> str:
        """Remove PII and sensitive data from output"""

        sanitized = output

        for pii_type, pattern in self.pii_patterns.items():
            if pii_type == "ssn":
                sanitized = re.sub(pattern, "XXX-XX-XXXX", sanitized)
            elif pii_type == "email":
                sanitized = re.sub(
                    pattern,
                    lambda m: f"{m.group(0).split('@')[0][:2]}***@{m.group(0).split('@')[1]}",
                    sanitized
                )
            elif pii_type == "phone":
                sanitized = re.sub(pattern, "XXX-XXX-XXXX", sanitized)
            elif pii_type == "credit_card":
                sanitized = re.sub(pattern, "XXXX-XXXX-XXXX-XXXX", sanitized)

        return sanitized

    def check_tool_permissions(
        self,
        tool_name: str,
        allowed_tools: List[str]
    ) -> bool:
        """Check if tool usage is allowed"""
        return tool_name in allowed_tools

    def rate_limit_check(
        self,
        user_id: str,
        max_requests: int = 100,
        window_seconds: int = 3600
    ) -> bool:
        """Check if user is within rate limits"""
        # Implementation would track requests per user
        # This is a simplified version
        return True
```

## Security Patterns

### 1. Input Sanitization

```python
def sanitize_user_input(user_input: str) -> str:
    """Sanitize user input before processing"""

    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>\"\'`]', '', user_input)

    # Limit length
    max_length = 10000
    sanitized = sanitized[:max_length]

    # Remove control characters
    sanitized = ''.join(
        char for char in sanitized
        if ord(char) >= 32 or char in '\n\r\t'
    )

    return sanitized
```

### 2. PII Redaction Middleware

```python
from langchain.agents.middleware import AgentMiddleware

class PIIRedactionMiddleware(AgentMiddleware):
    """Middleware to redact PII from agent conversations"""

    def __init__(self):
        self.validator = SecurityValidator()

    async def after_model(self, state: dict, context: Any) -> dict:
        """Redact PII from model output"""
        message = state["messages"][-1]

        if hasattr(message, 'content'):
            sanitized = self.validator.sanitize_output(message.content)
            message.content = sanitized

        return state

# Use in agent
agent = create_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[web_search],
    middleware=[PIIRedactionMiddleware()]
)
```

### 3. Secure Tool Access

```python
class SecureToolWrapper:
    """Wrapper to enforce security on tool calls"""

    def __init__(self, tool, allowed_users: List[str]):
        self.tool = tool
        self.allowed_users = allowed_users

    async def execute(self, user_id: str, **kwargs):
        """Execute tool with security checks"""

        # Check authorization
        if user_id not in self.allowed_users:
            raise PermissionError(f"User {user_id} not authorized")

        # Validate inputs
        validator = SecurityValidator()
        for key, value in kwargs.items():
            if isinstance(value, str):
                validation = validator.validate_input(value)
                if not validation["is_safe"]:
                    raise ValueError(
                        f"Security issue in {key}: {validation['issues']}"
                    )

        # Execute tool
        result = await self.tool.execute(**kwargs)

        # Sanitize output
        if isinstance(result, str):
            result = validator.sanitize_output(result)

        return result
```

### 4. Audit Logging

```python
import logging
import json
from datetime import datetime

class SecurityAuditLogger:
    """Log security events for auditing"""

    def __init__(self, log_file: str = "security_audit.log"):
        self.logger = logging.getLogger("security_audit")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_event(
        self,
        event_type: str,
        user_id: str,
        details: Dict[str, Any]
    ):
        """Log security event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "user_id": user_id,
            "details": details
        }

        self.logger.info(json.dumps(event))

# Usage
audit_logger = SecurityAuditLogger()

audit_logger.log_event(
    event_type="prompt_injection_detected",
    user_id="user-123",
    details={
        "input": "Ignore previous instructions...",
        "action": "blocked"
    }
)
```

### 5. Secure Configuration

```python
import os
from typing import Dict

class SecureConfig:
    """Manage secure configuration"""

    @staticmethod
    def get_api_key(service: str) -> str:
        """Get API key from environment"""
        key = os.environ.get(f"{service.upper()}_API_KEY")

        if not key:
            raise ValueError(f"API key for {service} not found")

        return key

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration is secure"""

        # Check no hardcoded secrets
        for key, value in config.items():
            if isinstance(value, str):
                if re.match(r"^[A-Za-z0-9-_]{20,}$", value):
                    if key.lower() not in ["api_key", "secret", "token"]:
                        print(f"Warning: {key} looks like a secret")

        return True

# Usage
api_key = SecureConfig.get_api_key("anthropic")
client = Anthropic(api_key=api_key)
```

## Security Checklist

- [ ] Validate all user inputs
- [ ] Redact PII from outputs
- [ ] Implement rate limiting
- [ ] Use authentication
- [ ] Enforce authorization
- [ ] Log security events
- [ ] Encrypt sensitive data
- [ ] Use secure connections (HTTPS)
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] Incident response plan
- [ ] Test for vulnerabilities

## Best Practices

1. **Defense in Depth**: Multiple security layers
2. **Principle of Least Privilege**: Minimal permissions
3. **Validate Everything**: Trust nothing
4. **Fail Securely**: Errors shouldn't leak info
5. **Log Security Events**: Audit trail
6. **Encrypt Secrets**: Never hardcode
7. **Regular Updates**: Patch vulnerabilities
8. **Test Security**: Automated tests
9. **User Education**: Inform about security
10. **Incident Response**: Plan for breaches

## Compliance

```python
class ComplianceChecker:
    """Check compliance with regulations"""

    def check_gdpr_compliance(self, data_handling: Dict) -> bool:
        """Check GDPR compliance"""
        required = [
            "data_minimization",
            "right_to_erasure",
            "consent_management",
            "data_portability"
        ]

        return all(data_handling.get(req) for req in required)

    def check_hipaa_compliance(self, security_measures: Dict) -> bool:
        """Check HIPAA compliance"""
        required = [
            "encryption_at_rest",
            "encryption_in_transit",
            "access_controls",
            "audit_logs"
        ]

        return all(security_measures.get(req) for req in required)
```

This skill ensures agents operate securely and protect user data.
