---
name: keycloak-config
description: Configure Keycloak realms, clients, users, and identity providers with enterprise best practices. Use when creating or editing Keycloak realm exports, client configurations, authentication flows, or OIDC/SAML provider settings.
---

# Keycloak Configuration Skill

Expert guidance for configuring Keycloak identity and access management (IAM) for enterprise authentication and authorization.

## When to Use This Skill

Use this skill when:
- Creating new Keycloak realm configurations
- Setting up OIDC or SAML clients
- Configuring user federation (LDAP, Active Directory)
- Implementing custom authentication flows
- Setting up social login providers
- Defining authorization policies and permissions
- Exporting/importing realm configurations
- Migrating between Keycloak versions

## Realm Configuration

### Basic Realm Setup

```json
{
  "realm": "company",
  "displayName": "Company SSO",
  "displayNameHtml": "<b>Company</b> Single Sign-On",
  "enabled": true,
  "sslRequired": "external",
  "registrationAllowed": false,
  "registrationEmailAsUsername": true,
  "rememberMe": true,
  "verifyEmail": true,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5
}
```

### Realm Security Settings

```json
{
  "realm": "company",
  "passwordPolicy": "length(12) and upperCase(1) and lowerCase(1) and digits(1) and specialChars(1) and notUsername and passwordHistory(6) and forceExpiredPasswordChange(90)",
  "defaultSignatureAlgorithm": "RS256",
  "revokeRefreshToken": true,
  "refreshTokenMaxReuse": 0,
  "accessTokenLifespan": 300,
  "accessTokenLifespanForImplicitFlow": 900,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "ssoSessionIdleTimeoutRememberMe": 0,
  "ssoSessionMaxLifespanRememberMe": 0,
  "offlineSessionIdleTimeout": 2592000,
  "offlineSessionMaxLifespanEnabled": false,
  "accessCodeLifespan": 60,
  "accessCodeLifespanUserAction": 300,
  "accessCodeLifespanLogin": 1800
}
```

### Email Configuration

```json
{
  "realm": "company",
  "smtpServer": {
    "host": "smtp.company.com",
    "port": "587",
    "from": "noreply@company.com",
    "fromDisplayName": "Company SSO",
    "replyTo": "support@company.com",
    "replyToDisplayName": "Support Team",
    "auth": "true",
    "user": "smtp-user",
    "password": "**********",
    "starttls": "true",
    "ssl": "false"
  },
  "verifyEmail": true,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false
}
```

## Client Configuration

### OIDC Confidential Client (Web Application)

```json
{
  "clientId": "web-app",
  "name": "Web Application",
  "description": "Main company web application",
  "enabled": true,
  "protocol": "openid-connect",
  "publicClient": false,
  "bearerOnly": false,
  "standardFlowEnabled": true,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": false,
  "serviceAccountsEnabled": false,
  "authorizationServicesEnabled": false,

  "rootUrl": "https://app.company.com",
  "baseUrl": "/",
  "redirectUris": [
    "https://app.company.com/*",
    "https://app.company.com/oauth2/callback"
  ],
  "webOrigins": [
    "https://app.company.com"
  ],
  "adminUrl": "https://app.company.com",

  "attributes": {
    "pkce.code.challenge.method": "S256",
    "post.logout.redirect.uris": "https://app.company.com/*",
    "backchannel.logout.session.required": "true",
    "backchannel.logout.revoke.offline.tokens": "true",
    "access.token.lifespan": "300",
    "client.session.idle.timeout": "1800",
    "client.session.max.lifespan": "36000"
  },

  "defaultClientScopes": [
    "profile",
    "email",
    "roles",
    "web-origins"
  ],
  "optionalClientScopes": [
    "address",
    "phone",
    "offline_access",
    "microprofile-jwt"
  ],

  "protocolMappers": [
    {
      "name": "groups",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-group-membership-mapper",
      "consentRequired": false,
      "config": {
        "full.path": "false",
        "id.token.claim": "true",
        "access.token.claim": "true",
        "claim.name": "groups",
        "userinfo.token.claim": "true"
      }
    },
    {
      "name": "audience",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-audience-mapper",
      "consentRequired": false,
      "config": {
        "included.client.audience": "web-app",
        "id.token.claim": "false",
        "access.token.claim": "true"
      }
    }
  ]
}
```

### OIDC Public Client (Single Page Application)

```json
{
  "clientId": "spa-app",
  "name": "Single Page Application",
  "enabled": true,
  "protocol": "openid-connect",
  "publicClient": true,
  "bearerOnly": false,
  "standardFlowEnabled": true,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": false,

  "redirectUris": [
    "http://localhost:3000/*",
    "https://spa.company.com/*"
  ],
  "webOrigins": [
    "http://localhost:3000",
    "https://spa.company.com"
  ],

  "attributes": {
    "pkce.code.challenge.method": "S256",
    "post.logout.redirect.uris": "+"
  },

  "defaultClientScopes": [
    "profile",
    "email",
    "roles"
  ]
}
```

### Service Account Client (M2M)

```json
{
  "clientId": "backend-service",
  "name": "Backend Service",
  "enabled": true,
  "protocol": "openid-connect",
  "publicClient": false,
  "bearerOnly": false,
  "standardFlowEnabled": false,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": false,
  "serviceAccountsEnabled": true,
  "authorizationServicesEnabled": true,

  "attributes": {
    "access.token.lifespan": "1800"
  },

  "defaultClientScopes": [
    "profile",
    "email",
    "roles"
  ]
}
```

### Bearer-Only Client (API/Resource Server)

```json
{
  "clientId": "api-server",
  "name": "API Server",
  "enabled": true,
  "protocol": "openid-connect",
  "publicClient": false,
  "bearerOnly": true,
  "standardFlowEnabled": false,
  "implicitFlowEnabled": false,
  "directAccessGrantsEnabled": false,
  "serviceAccountsEnabled": false,

  "attributes": {
    "access.token.lifespan": "300"
  }
}
```

## User Federation

### LDAP Configuration

```json
{
  "name": "corporate-ldap",
  "providerId": "ldap",
  "providerType": "org.keycloak.storage.UserStorageProvider",
  "config": {
    "vendor": ["Active Directory"],
    "connectionUrl": ["ldaps://ldap.company.com:636"],
    "bindDn": ["cn=keycloak,ou=services,dc=company,dc=com"],
    "bindCredential": ["ldap-password"],
    "usersDn": ["ou=users,dc=company,dc=com"],
    "searchScope": ["2"],
    "useTruststoreSpi": ["ldapsOnly"],
    "connectionPooling": ["true"],
    "pagination": ["true"],
    "startTls": ["false"],
    "authType": ["simple"],

    "editMode": ["READ_ONLY"],
    "syncRegistrations": ["false"],
    "importEnabled": ["true"],
    "batchSizeForSync": ["1000"],
    "fullSyncPeriod": ["604800"],
    "changedSyncPeriod": ["86400"],

    "usernameLDAPAttribute": ["sAMAccountName"],
    "rdnLDAPAttribute": ["cn"],
    "uuidLDAPAttribute": ["objectGUID"],
    "userObjectClasses": ["person", "organizationalPerson", "user"],

    "customUserSearchFilter": ["(&(objectClass=user)(!(objectClass=computer)))"],

    "allowKerberosAuthentication": ["false"],
    "useKerberosForPasswordAuthentication": ["false"]
  }
}
```

### LDAP Group Mapper

```json
{
  "name": "ldap-groups",
  "providerId": "group-ldap-mapper",
  "providerType": "org.keycloak.storage.ldap.mappers.LDAPStorageMapper",
  "config": {
    "groups.dn": ["ou=groups,dc=company,dc=com"],
    "group.name.ldap.attribute": ["cn"],
    "group.object.classes": ["groupOfNames"],
    "membership.ldap.attribute": ["member"],
    "membership.attribute.type": ["DN"],
    "membership.user.ldap.attribute": ["cn"],
    "groups.ldap.filter": [""],
    "mode": ["READ_ONLY"],
    "user.roles.retrieve.strategy": ["LOAD_GROUPS_BY_MEMBER_ATTRIBUTE"],
    "memberof.ldap.attribute": ["memberOf"],
    "preserve.group.inheritance": ["true"],
    "drop.non.existing.groups.during.sync": ["false"]
  }
}
```

## Identity Providers

### Google Social Login

```json
{
  "alias": "google",
  "providerId": "google",
  "enabled": true,
  "updateProfileFirstLoginMode": "on",
  "trustEmail": true,
  "storeToken": false,
  "addReadTokenRoleOnCreate": false,
  "authenticateByDefault": false,
  "linkOnly": false,
  "firstBrokerLoginFlowAlias": "first broker login",
  "config": {
    "clientId": "google-oauth-client-id",
    "clientSecret": "google-oauth-client-secret",
    "hostedDomain": "company.com",
    "useJwksUrl": "true",
    "syncMode": "IMPORT",
    "hideOnLoginPage": "false",
    "guiOrder": "1"
  }
}
```

### GitHub Social Login

```json
{
  "alias": "github",
  "providerId": "github",
  "enabled": true,
  "updateProfileFirstLoginMode": "on",
  "trustEmail": false,
  "storeToken": false,
  "addReadTokenRoleOnCreate": false,
  "authenticateByDefault": false,
  "linkOnly": false,
  "firstBrokerLoginFlowAlias": "first broker login",
  "config": {
    "clientId": "github-oauth-app-client-id",
    "clientSecret": "github-oauth-app-secret",
    "defaultScope": "user:email",
    "syncMode": "IMPORT",
    "hideOnLoginPage": "false",
    "guiOrder": "2"
  }
}
```

### Azure AD OIDC

```json
{
  "alias": "azure-ad",
  "providerId": "oidc",
  "enabled": true,
  "updateProfileFirstLoginMode": "on",
  "trustEmail": true,
  "storeToken": false,
  "addReadTokenRoleOnCreate": false,
  "authenticateByDefault": false,
  "linkOnly": false,
  "firstBrokerLoginFlowAlias": "first broker login",
  "config": {
    "clientId": "azure-app-client-id",
    "clientSecret": "azure-app-secret",
    "tokenUrl": "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token",
    "authorizationUrl": "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/authorize",
    "logoutUrl": "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/logout",
    "issuer": "https://login.microsoftonline.com/{tenant-id}/v2.0",
    "jwksUrl": "https://login.microsoftonline.com/{tenant-id}/discovery/v2.0/keys",
    "userInfoUrl": "https://graph.microsoft.com/oidc/userinfo",
    "clientAuthMethod": "client_secret_post",
    "syncMode": "IMPORT",
    "defaultScope": "openid profile email",
    "hideOnLoginPage": "false",
    "guiOrder": "3"
  }
}
```

## Authentication Flows

### Custom Browser Flow with MFA

```json
{
  "alias": "browser-with-mfa",
  "description": "Browser authentication with OTP",
  "providerId": "basic-flow",
  "topLevel": true,
  "builtIn": false,
  "authenticationExecutions": [
    {
      "authenticator": "auth-cookie",
      "requirement": "ALTERNATIVE",
      "priority": 10,
      "userSetupAllowed": false
    },
    {
      "authenticator": "identity-provider-redirector",
      "requirement": "ALTERNATIVE",
      "priority": 25,
      "userSetupAllowed": false
    },
    {
      "flowAlias": "browser-with-mfa-forms",
      "requirement": "ALTERNATIVE",
      "priority": 30,
      "userSetupAllowed": false
    }
  ]
}
```

### Registration Flow with Email Verification

```json
{
  "alias": "registration-with-recaptcha",
  "description": "Registration with reCAPTCHA and email verification",
  "providerId": "basic-flow",
  "topLevel": true,
  "builtIn": false,
  "authenticationExecutions": [
    {
      "authenticator": "registration-page-form",
      "requirement": "REQUIRED",
      "priority": 10,
      "flowAlias": "registration-with-recaptcha-form",
      "userSetupAllowed": false
    }
  ]
}
```

## Kubernetes Deployment

### StatefulSet for Production

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: keycloak
  namespace: auth
spec:
  serviceName: keycloak-headless
  replicas: 3
  selector:
    matchLabels:
      app: keycloak
  template:
    metadata:
      labels:
        app: keycloak
    spec:
      containers:
      - name: keycloak
        image: quay.io/keycloak/keycloak:23.0
        args:
        - start
        - --auto-build
        - --http-enabled=true
        - --http-port=8080
        - --hostname-strict=false
        - --proxy=edge
        env:
        - name: KC_DB
          value: postgres
        - name: KC_DB_URL
          value: jdbc:postgresql://postgres:5432/keycloak
        - name: KC_DB_USERNAME
          valueFrom:
            secretKeyRef:
              name: keycloak-db
              key: username
        - name: KC_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: keycloak-db
              key: password
        - name: KEYCLOAK_ADMIN
          value: admin
        - name: KEYCLOAK_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: keycloak-admin
              key: password
        - name: KC_CACHE
          value: ispn
        - name: KC_CACHE_STACK
          value: kubernetes
        - name: JAVA_OPTS_APPEND
          value: "-Djgroups.dns.query=keycloak-headless.auth.svc.cluster.local"
        ports:
        - name: http
          containerPort: 8080
        - name: jgroups
          containerPort: 7600
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 120
          periodSeconds: 10
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 2Gi
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - ALL
```

### Headless Service for Clustering

```yaml
apiVersion: v1
kind: Service
metadata:
  name: keycloak-headless
  namespace: auth
spec:
  clusterIP: None
  selector:
    app: keycloak
  ports:
  - name: http
    port: 8080
    targetPort: 8080
  - name: jgroups
    port: 7600
    targetPort: 7600
```

### External Service and Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: keycloak
  namespace: auth
spec:
  selector:
    app: keycloak
  ports:
  - name: http
    port: 8080
    targetPort: 8080
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: keycloak
  namespace: auth
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-buffer-size: "128k"
spec:
  ingressClassName: nginx
  rules:
  - host: keycloak.company.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: keycloak
            port:
              number: 8080
  tls:
  - hosts:
    - keycloak.company.com
    secretName: keycloak-tls
```

## Best Practices

### Security
- Always use HTTPS in production (`sslRequired: "all"`)
- Enable brute force protection
- Implement strong password policies (length, complexity, history)
- Use separate realms for different environments
- Rotate admin passwords regularly
- Enable audit logging for compliance
- Implement token rotation and revocation
- Use PKCE for public clients

### Performance
- Configure database connection pooling appropriately
- Enable caching (Infinispan for clustering)
- Use StatefulSet for multi-instance deployments
- Optimize LDAP sync schedules
- Monitor JVM heap usage and GC
- Use CDN for theme assets
- Implement health checks and auto-scaling

### High Availability
- Deploy at least 3 instances for quorum
- Use headless service for JGroups discovery
- Configure database replication
- Implement backup and disaster recovery
- Test failover scenarios regularly
- Monitor cluster health and synchronization

### Operations
- Export realm configurations for backup
- Use version control for realm definitions
- Test realm imports in staging first
- Document custom authentication flows
- Monitor authentication success/failure rates
- Implement proper logging and alerting
- Regular security updates and patches

## Validation Checklist

- [ ] SSL/TLS is required for external connections
- [ ] Strong password policy is enforced
- [ ] Brute force protection is enabled
- [ ] Email verification is configured correctly
- [ ] SMTP settings are tested
- [ ] Client redirect URIs are properly restricted
- [ ] Service account clients use appropriate scopes
- [ ] LDAP federation is tested with sync
- [ ] Social login providers are tested end-to-end
- [ ] Token lifespans are appropriate for use case
- [ ] Database credentials are stored in Secrets
- [ ] Admin password is changed from default
- [ ] Audit logging is enabled
- [ ] Backup strategy is implemented
- [ ] Clustering is working (if multi-instance)

## Related Skills

- **oauth2-proxy-config**: Configure OAuth2-proxy to use Keycloak
- **k8s-optimizer**: Optimize Keycloak Kubernetes deployments
- **iac-compliance**: Ensure Keycloak meets compliance requirements
