# ADR-008: Structured Logging with Serilog

**Date**: 2026-04-01
**Status**: Accepted

---

## Context

Jamtrack Radio requires a consistent, queryable logging strategy across all microservices. Key requirements from the architecture and compliance docs:

- GDPR: email addresses must never be logged in plain text (they are PII)
- Observability: structured JSON logs must be queryable in ELK (Elasticsearch, Logstash, Kibana)
- Distributed tracing: all service-to-service calls must carry a `traceId` for correlation
- Security audit: login failures, token events, and access anomalies must be logged and retained
- Phase 2 = local console output; Phase 4+ = ELK Stack
- Consistent field names across all services (a prerequisite for useful ELK dashboards)

Candidates evaluated: `Microsoft.Extensions.Logging` (structured but no sinks), Serilog, NLog, log4net.

---

## Decision

**Serilog** is the structured logging library for all Jamtrack Radio services. All log entries are JSON. Field names follow the schema below. PII destructuring is applied globally via `Serilog.Destructuring` to mask email addresses in all log events.

---

## Logging Schema

Every log entry must include these fields:

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `timestamp` | ISO 8601 UTC | Serilog | When the event occurred |
| `level` | string | Serilog | `Debug`, `Information`, `Warning`, `Error`, `Fatal` |
| `service` | string | `enrichWith("service", "identity-service")` | Owning service name |
| `traceId` | string | W3C `traceparent` header | Distributed trace identifier |
| `spanId` | string | W3C `traceparent` header | Span within the trace |
| `userId` | guid / null | Application context | Authenticated user (null for unauthenticated requests) |
| `operation` | string | Log statement | The operation being performed (e.g. `RegisterUser`, `StreamTrack`) |
| `elapsedMs` | int | Stopwatch | Duration of the operation in milliseconds |
| `message` | string | Serilog | Human-readable description |
| `exception` | object / null | Serilog | Exception details (stack trace, type, message) |

### PII masking

Email addresses are hashed before logging using SHA-256:

```csharp
// In Serilog configuration
.Destructure.ByTransforming<string>(s =>
    s.Contains('@') ? $"[email:{HashEmail(s)}]" : s)
```

Raw email addresses must never appear in any log sink.

---

## Log Level Policy

| Level | When to use |
|-------|-------------|
| `Debug` | Detailed diagnostic info (dev only — not in production) |
| `Information` | Significant business operations: user registered, track uploaded, stream started |
| `Warning` | Unexpected but recoverable conditions: token refresh attempted on revoked token |
| `Error` | Operation failed, requires investigation: database connection failure, downstream gRPC timeout |
| `Fatal` | Service cannot continue: startup failure, unhandled exception in critical path |

**Sampling policy (Phase 4+)**:
- `Information`: sample at 10% for high-volume endpoints (stream reads)
- `Warning` and above: always log (100%)
- Security events (`user.login_failed`, `token.refreshed`): always log (100%), regardless of sampling

---

## Sinks by Phase

| Phase | Sink | Configuration |
|-------|------|---------------|
| Phase 2 | Console (JSON) | `WriteTo.Console(new JsonFormatter())` |
| Phase 3 | Console + File | Add `WriteTo.File` with rolling daily files |
| Phase 4+ | Console + ELK | Replace File with `WriteTo.Elasticsearch` pointing to ELK cluster |

---

## Consequences

### What becomes easier

- ELK dashboards work immediately because all services use identical field names
- Cross-service correlation is possible via `traceId` — a single user action can be traced across Identity, Track, and Storage services
- Security audit trail is consistent and queryable (login failures, token events)
- GDPR compliance is enforced at the framework level, not per-log-statement discipline

### What becomes harder

- Serilog configuration must be applied consistently to every new service — the `/new-service` skill must include the Serilog setup template
- Developers must know to use `Log.ForContext("userId", userId)` rather than string interpolation (which bypasses structured logging)

---

## Cost implication

£0 (Serilog is open-source). ELK infra cost is captured in the cloud architecture: ~£46/month staging, ~£345/month production (Phase 4+).
