---
name: istio-advisor
description: Validate and optimize Istio configurations following production best practices. Use when creating or editing VirtualService, DestinationRule, Gateway YAML files, configuring mTLS policies, or implementing traffic routing rules.
---

# Istio Advisor Skill

Provide expert Istio service mesh guidance, validate configurations, and automatically apply best practices for traffic management, security, and observability.

## When to Use This Skill

Use this skill when:

1. Creating VirtualService, DestinationRule, or Gateway YAML files
2. Configuring mTLS and security policies
3. Implementing traffic management strategies
4. Setting up circuit breakers and fault injection
5. Configuring distributed tracing and observability
6. Debugging service mesh issues
7. Discussing Istio architecture or patterns
8. Planning canary deployments or A/B tests
9. Implementing authorization policies
10. Troubleshooting Envoy proxy issues

## Core Capabilities

### Traffic Management Best Practices
- **VirtualService validation**: Ensure proper routing rules, weight distribution, header matching
- **DestinationRule optimization**: Configure connection pools, circuit breakers, load balancing
- **Gateway configuration**: Validate TLS settings, port mappings, SNI routing
- **Traffic splitting**: Implement safe canary rollouts with proper percentage distribution
- **Fault injection**: Add delay and abort injection for testing resilience
- **Timeout and retry policies**: Configure appropriate timeouts and retry strategies

### Security Configuration
- **mTLS enforcement**: Validate PeerAuthentication policies for STRICT mode
- **Authorization policies**: Review RBAC rules for service-to-service access
- **RequestAuthentication**: Configure JWT validation and OAuth2 integration
- **Security best practices**: Ensure zero-trust principles, least privilege access
- **Certificate management**: Validate cert rotation, expiration monitoring

### Observability Setup
- **Distributed tracing**: Configure trace sampling, context propagation
- **Metrics collection**: Validate Prometheus integration, custom metrics
- **Dashboard setup**: Guide Kiali, Grafana, Jaeger configuration
- **Logging configuration**: Set up access logs, Envoy logs with proper format
- **Telemetry optimization**: Balance observability vs performance impact

### Resiliency Patterns
- **Circuit breaker configuration**: Set appropriate thresholds for consecutive errors
- **Outlier detection**: Configure failure percentage, ejection time, base ejection time
- **Retry policies**: Implement retry budgets, per-try timeout, retry conditions
- **Timeout strategies**: Set request timeout, idle timeout, connection timeout
- **Connection pooling**: Configure max connections, max requests, TCP settings

## Automatic Validations

When working with Istio resources, automatically check for:

1. **VirtualService Issues**
   - Missing or incorrect host references
   - Invalid weight distribution (must sum to 100)
   - Conflicting routing rules
   - Missing subset definitions in DestinationRule
   - Improper header matching syntax
   - Invalid URI regex patterns

2. **DestinationRule Issues**
   - Circuit breaker thresholds too high/low
   - Missing TLS settings for mTLS
   - Improper load balancing configuration
   - Connection pool limits too restrictive
   - Outlier detection misconfiguration

3. **Gateway Issues**
   - Missing TLS certificates for HTTPS
   - Incorrect port protocol mapping
   - SNI host mismatch
   - Security vulnerabilities (e.g., TLS 1.0/1.1)
   - Missing CORS configuration

4. **Security Policy Issues**
   - PeerAuthentication mode not STRICT in production
   - AuthorizationPolicy allowing all traffic by default
   - Missing JWT validation for external traffic
   - Overly permissive RBAC rules
   - Egress traffic not controlled

5. **Observability Gaps**
   - Missing trace sampling configuration
   - No access logs enabled
   - Missing custom metrics
   - Incomplete dashboard setup
   - No alerting configured

## Production Readiness Checklist

Automatically verify:

- [ ] mTLS enabled in STRICT mode for all workloads
- [ ] Circuit breakers configured with reasonable thresholds
- [ ] Distributed tracing enabled with appropriate sampling rate
- [ ] Access logs enabled for debugging
- [ ] Gateway configured with proper TLS certificates
- [ ] Authorization policies implemented (default deny)
- [ ] Resource limits set on sidecar proxies
- [ ] Timeout policies defined for all services
- [ ] Retry policies configured with retry budget
- [ ] Health checks configured (liveness, readiness, startup)
- [ ] Monitoring dashboards created (Kiali, Grafana)
- [ ] Alerting rules configured for control plane and data plane
- [ ] Egress traffic controlled with ServiceEntry
- [ ] Virtual services have proper host matching
- [ ] Destination rules reference existing subsets

## Common Patterns and Examples

### Canary Deployment Pattern
Automatically suggest progressive traffic shifting:
- Start with 5% traffic to canary
- Monitor error rates, latency, success rates
- Increase to 25%, 50%, 75%, 100% based on metrics
- Provide rollback strategy

### Circuit Breaker Pattern
Recommend thresholds based on service characteristics:
- HTTP services: 5 consecutive errors, 30s ejection time
- gRPC services: 10 consecutive errors, 60s ejection time
- Critical services: Lower thresholds, longer ejection
- Non-critical services: Higher thresholds, shorter ejection

### Zero-Trust Security Pattern
Enforce security best practices:
- Start with PERMISSIVE mTLS, migrate to STRICT
- Implement default-deny authorization
- Add explicit allow rules per service
- Configure JWT validation for ingress
- Control egress with ServiceEntry

### Observability Pattern
Set up comprehensive observability:
- 1% trace sampling for high-volume services
- 10% trace sampling for medium-volume services
- 100% trace sampling for critical user flows
- Access logs with JSON format for parsing
- Custom metrics for business logic

## Troubleshooting Guidance

Automatically diagnose common issues:

- **503 Service Unavailable**: Check circuit breaker ejection, upstream health
- **Connection timeout**: Verify DestinationRule connection pool settings
- **mTLS errors**: Validate PeerAuthentication mode, certificate validity
- **Route not found**: Check VirtualService host matching, Gateway configuration
- **High latency**: Analyze distributed traces, check retry/timeout policies
- **Authorization denied**: Review AuthorizationPolicy rules, verify workload identity

## Anti-Patterns to Avoid

Warn about:

- Using PERMISSIVE mTLS in production
- Not configuring circuit breakers on external services
- Setting timeout values too high (> 60s)
- Enabling 100% trace sampling on high-volume services
- Allowing all traffic in AuthorizationPolicy default rules
- Not setting resource limits on sidecar proxies
- Using weight-based routing without monitoring
- Configuring too aggressive retry policies
- Missing health checks on workloads
- Not controlling egress traffic

## Integration with Other Tools

- **kubectl**: Validate resources before apply
- **istioctl**: Suggest analysis and validation commands
- **kiali**: Guide dashboard navigation and troubleshooting
- **prometheus**: Configure metrics scraping and alerting
- **jaeger**: Set up trace collection and analysis

## Auto-Fix Capabilities

When possible, automatically suggest fixes for:

- Adding missing circuit breaker configuration
- Setting appropriate timeout and retry policies
- Enabling mTLS in STRICT mode
- Configuring distributed tracing
- Adding health checks to deployments
- Setting resource limits on sidecars
- Creating authorization policies
- Enabling access logs

## Output Format

Provide:
- Validated Istio YAML configurations
- Explanation of traffic routing logic
- Security policy recommendations
- Troubleshooting commands (istioctl analyze, kubectl describe)
- Monitoring queries (PromQL for metrics)
- Dashboard links (Kiali, Grafana, Jaeger)
- Production readiness assessment
- Step-by-step implementation guide
