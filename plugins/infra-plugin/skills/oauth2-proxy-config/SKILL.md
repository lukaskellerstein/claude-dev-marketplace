---
name: oauth2-proxy-config
description: Generate and validate OAuth2-proxy configurations with security best practices. Use when creating or editing oauth2-proxy config files, ConfigMaps, deployment manifests, or setting up reverse proxy authentication.
---

# OAuth2-Proxy Configuration Skill

Expert guidance for configuring OAuth2-proxy to protect web applications with authentication via OAuth2/OIDC providers.

## When to Use This Skill

Use this skill when:
- Creating new OAuth2-proxy configuration files
- Setting up OAuth2-proxy in Kubernetes with ConfigMaps
- Configuring authentication providers (Keycloak, Google, GitHub, Azure AD)
- Implementing cookie-based session management
- Setting up upstream authentication for applications
- Debugging OAuth2-proxy authentication issues
- Migrating between authentication providers

## Core Configuration Areas

### Provider Configuration

**Keycloak OIDC Provider**
```cfg
provider = "keycloak-oidc"
provider_display_name = "Company SSO"
client_id = "oauth2-proxy"
client_secret = "your-client-secret"
redirect_url = "https://app.example.com/oauth2/callback"
oidc_issuer_url = "https://keycloak.example.com/realms/company"
```

**Generic OIDC Provider**
```cfg
provider = "oidc"
provider_display_name = "Custom OIDC"
client_id = "your-client-id"
client_secret = "your-client-secret"
redirect_url = "https://app.example.com/oauth2/callback"
oidc_issuer_url = "https://provider.example.com"
oidc_jwks_url = "https://provider.example.com/protocol/openid-connect/certs"
login_url = "https://provider.example.com/protocol/openid-connect/auth"
redeem_url = "https://provider.example.com/protocol/openid-connect/token"
```

**Google Provider**
```cfg
provider = "google"
client_id = "your-google-client-id.apps.googleusercontent.com"
client_secret = "your-google-client-secret"
redirect_url = "https://app.example.com/oauth2/callback"
```

**GitHub Provider**
```cfg
provider = "github"
client_id = "your-github-client-id"
client_secret = "your-github-client-secret"
redirect_url = "https://app.example.com/oauth2/callback"
github_org = "your-organization"
github_team = "authorized-team"
```

### Cookie & Session Configuration

**Secure Cookie Settings**
```cfg
cookie_name = "_oauth2_proxy"
cookie_secret = "32-byte-base64-encoded-secret"  # Generate with: openssl rand -base64 32
cookie_domains = [".example.com"]
cookie_expire = "168h"  # 7 days
cookie_refresh = "1h"
cookie_secure = true
cookie_httponly = true
cookie_samesite = "lax"
```

**Session Storage**
```cfg
# Cookie-based (default, simple but limited size)
session_store_type = "cookie"

# Redis-based (recommended for production)
session_store_type = "redis"
redis_connection_url = "redis://redis-master:6379"
redis_password = "your-redis-password"
redis_sentinel_master_name = "mymaster"
redis_sentinel_connection_urls = ["redis://sentinel1:26379", "redis://sentinel2:26379"]
```

### Upstream & Routing Configuration

**Single Upstream**
```cfg
upstreams = ["http://backend-service:8080"]
pass_host_header = true
pass_access_token = true
set_xauthrequest = true
set_authorization_header = true
```

**Multiple Upstreams with Path Routing**
```cfg
upstreams = [
  "http://api.example.com/=/api/",
  "http://web.example.com/=/",
]
```

**Skip Authentication for Specific Paths**
```cfg
skip_auth_routes = [
  "^/health$",
  "^/metrics$",
  "^/public/.*",
]
skip_auth_regex = ["^/api/v1/webhook.*"]
```

### Email & Authorization

**Email Domain Restrictions**
```cfg
email_domains = ["example.com", "partner.com"]
authenticated_emails_file = "/etc/oauth2-proxy/emails.txt"
```

**Group/Role-based Authorization**
```cfg
allowed_groups = ["admins", "developers"]
oidc_groups_claim = "groups"
```

### Security Headers & Features

**Request Headers to Upstream**
```cfg
pass_access_token = true
pass_user_headers = true
set_xauthrequest = true
set_authorization_header = true
skip_jwt_bearer_tokens = true

# Custom headers
inject_request_headers = [
  "X-Auth-Request-User",
  "X-Auth-Request-Email",
  "X-Auth-Request-Groups",
]
```

**Security Hardening**
```cfg
force_https = true
ssl_insecure_skip_verify = false  # Never true in production!
reverse_proxy = true
real_client_ip_header = "X-Forwarded-For"
trusted_ips = ["10.0.0.0/8", "172.16.0.0/12"]
```

## Kubernetes Deployment Patterns

### ConfigMap-based Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: oauth2-proxy-config
  namespace: auth
data:
  oauth2_proxy.cfg: |
    provider = "keycloak-oidc"
    client_id = "oauth2-proxy"
    redirect_url = "https://app.example.com/oauth2/callback"
    oidc_issuer_url = "https://keycloak.example.com/realms/company"

    upstreams = ["http://backend:8080"]

    cookie_name = "_oauth2_proxy"
    cookie_secure = true
    cookie_httponly = true
    cookie_domains = [".example.com"]
    cookie_expire = "168h"
    cookie_refresh = "1h"

    email_domains = ["example.com"]

    pass_access_token = true
    set_xauthrequest = true
    set_authorization_header = true

    session_store_type = "redis"
    redis_connection_url = "redis://redis:6379"
```

### Deployment with Environment Variables

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oauth2-proxy
  namespace: auth
spec:
  replicas: 2
  selector:
    matchLabels:
      app: oauth2-proxy
  template:
    metadata:
      labels:
        app: oauth2-proxy
    spec:
      containers:
      - name: oauth2-proxy
        image: quay.io/oauth2-proxy/oauth2-proxy:v7.5.1
        args:
        - --config=/etc/oauth2-proxy/oauth2_proxy.cfg
        ports:
        - containerPort: 4180
          name: http
          protocol: TCP
        env:
        - name: OAUTH2_PROXY_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: oauth2-proxy-secrets
              key: client-secret
        - name: OAUTH2_PROXY_COOKIE_SECRET
          valueFrom:
            secretKeyRef:
              name: oauth2-proxy-secrets
              key: cookie-secret
        volumeMounts:
        - name: config
          mountPath: /etc/oauth2-proxy
          readOnly: true
        livenessProbe:
          httpGet:
            path: /ping
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ping
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
        securityContext:
          runAsNonRoot: true
          runAsUser: 2000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
          readOnlyRootFilesystem: true
      volumes:
      - name: config
        configMap:
          name: oauth2-proxy-config
```

### Secrets Management

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: oauth2-proxy-secrets
  namespace: auth
type: Opaque
stringData:
  client-secret: "keycloak-client-secret-here"
  cookie-secret: "generate-with-openssl-rand-base64-32"
```

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: oauth2-proxy
  namespace: auth
spec:
  selector:
    app: oauth2-proxy
  ports:
  - name: http
    port: 4180
    targetPort: http
    protocol: TCP
  type: ClusterIP
```

## NGINX Ingress Integration

### Authentication Annotations

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: protected-application
  annotations:
    # OAuth2-proxy authentication
    nginx.ingress.kubernetes.io/auth-url: "https://$host/oauth2/auth"
    nginx.ingress.kubernetes.io/auth-signin: "https://$host/oauth2/start?rd=$escaped_request_uri"
    nginx.ingress.kubernetes.io/auth-response-headers: "X-Auth-Request-User,X-Auth-Request-Email,X-Auth-Request-Groups"

    # Optional: snippets for custom logic
    nginx.ingress.kubernetes.io/configuration-snippet: |
      auth_request_set $user $upstream_http_x_auth_request_user;
      auth_request_set $email $upstream_http_x_auth_request_email;
      proxy_set_header X-User $user;
      proxy_set_header X-Email $email;
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: oauth2-proxy-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /oauth2
        pathType: Prefix
        backend:
          service:
            name: oauth2-proxy
            port:
              number: 4180
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls-cert
```

## Common Configuration Patterns

### Development Environment
```cfg
provider = "oidc"
oidc_issuer_url = "http://keycloak.local/realms/dev"
cookie_secure = false  # Only for local development!
email_domains = ["*"]
skip_provider_button = true
```

### Production Environment
```cfg
provider = "keycloak-oidc"
oidc_issuer_url = "https://keycloak.company.com/realms/production"
cookie_secure = true
cookie_samesite = "strict"
email_domains = ["company.com"]
session_store_type = "redis"
redis_connection_url = "redis://redis-cluster:6379"
force_https = true
```

### API Gateway Pattern
```cfg
skip_jwt_bearer_tokens = true  # Allow JWT tokens to bypass OAuth2-proxy
pass_access_token = true
set_authorization_header = true
extra_jwt_issuers = [
  "https://keycloak.company.com/realms/production=HS256",
]
```

## Validation Checklist

When reviewing OAuth2-proxy configurations, verify:

- [ ] **Cookie secret** is at least 32 bytes and properly encoded
- [ ] **Client secret** is stored in Kubernetes Secret, not ConfigMap
- [ ] **cookie_secure** is `true` for production (HTTPS)
- [ ] **cookie_httponly** is `true` to prevent XSS
- [ ] **cookie_samesite** is set (`lax` or `strict`)
- [ ] **Redirect URL** matches exactly what's configured in the provider
- [ ] **OIDC issuer URL** is correct and accessible
- [ ] **Email domains** are properly restricted (not `["*"]` in production)
- [ ] **Session storage** uses Redis for multi-replica deployments
- [ ] **Skip auth routes** are minimal and necessary only
- [ ] **HTTPS is enforced** with `force_https = true`
- [ ] **Resource limits** are set on the deployment
- [ ] **Health checks** (liveness/readiness) are configured
- [ ] **Logging level** is appropriate (not debug in production)
- [ ] **Token passing** headers are correctly configured for upstream

## Troubleshooting

### Issue: Redirect Loop
**Causes:**
- Incorrect `cookie_domains` setting
- Upstream returning 401/403
- Missing skip-auth for OAuth2-proxy routes

**Fix:**
```cfg
cookie_domains = [".example.com"]  # Must include subdomain
skip_auth_routes = ["^/oauth2/.*"]
```

### Issue: "Invalid Client" Error
**Causes:**
- Wrong `client_id` or `client_secret`
- Redirect URL mismatch in provider

**Fix:**
- Verify client credentials in Keycloak/provider
- Ensure `redirect_url` exactly matches provider configuration

### Issue: Cookie Too Large
**Causes:**
- Too many scopes/claims in token
- Large group memberships

**Fix:**
```cfg
session_store_type = "redis"  # Move session to server-side storage
redis_connection_url = "redis://redis:6379"
```

### Issue: Token Expired
**Causes:**
- `cookie_expire` too short
- No token refresh configured

**Fix:**
```cfg
cookie_expire = "168h"  # 7 days
cookie_refresh = "1h"   # Refresh token hourly
```

## Best Practices

1. **Always use HTTPS** in production with `force_https = true`
2. **Store secrets securely** in Kubernetes Secrets or external secret managers
3. **Use Redis** for session storage in production with multiple replicas
4. **Implement proper logging** and monitoring for auth failures
5. **Rotate cookie secrets** regularly
6. **Test authentication flows** thoroughly before production deployment
7. **Use minimal skip-auth routes** - only for health checks and public assets
8. **Implement rate limiting** on authentication endpoints
9. **Monitor OAuth2-proxy metrics** for authentication success/failure rates
10. **Document provider-specific configurations** for your team

## Related Skills

- **keycloak-config**: Configure Keycloak realms and clients
- **k8s-optimizer**: Optimize OAuth2-proxy Kubernetes deployments
- **istio-advisor**: Integrate OAuth2-proxy with Istio service mesh
