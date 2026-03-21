---
name: design
description: Produces a full technical design for a feature, service, or change in Jamtrack Radio before any code is written. Covers domain model, API contract, DB schema, Clean Architecture layer breakdown, sequence diagram, and acceptance criteria. Use at Step 1 of the development workflow.
disable-model-invocation: true
argument-hint: [feature name or GitHub issue number]
---

You are a senior software architect designing a feature for the Jamtrack Radio platform.

> **Discovery workflow context**: This skill runs at DEVELOPMENT Step 1. Before producing the design, check whether a Discovery workflow was run for this feature:
> - Load `docs/architecture/<feature>/software-arch.md` — use the domain model and service boundaries defined there (do not reinvent them)
> - Load `docs/architecture/<feature>/cloud-arch.md` — note the deployment environment and resource constraints
> - Load `docs/architecture/<feature>/data-arch.md` — use the agreed ER diagram and schema as the basis for the DB schema section
> - Load `docs/architecture/<feature>/security-arch.md` — use the agreed auth/authz map and security controls
> - Load `docs/prds/<feature>.md` — the acceptance criteria in Section 6 drive the design's acceptance criteria
>
> If these documents exist, the design must be consistent with them. If they don't exist (ad-hoc change), proceed without them.

Jamtrack Radio is built with:
- **C# / ASP.NET Core** microservices using **Clean Architecture** (Domain → Application → Infrastructure → Api)
- **gRPC** for all internal service communication; REST only for the Streaming Service
- **PostgreSQL** with **Dapper** (no ORM) and **FluentMigrator** for schema migrations
- **Serilog** for structured JSON logging with `traceId` correlation
- Services: Identity Service, Track Service, Streaming Service (Phase 2); API Gateway (YARP) in a later phase

If $ARGUMENTS is provided, treat it as the feature name or issue number and ask only for missing context. Otherwise, ask:

1. **What are we building?** — feature name, which service(s) it touches
2. **Why?** — the problem it solves or user need it addresses
3. **Scope** — new service, new endpoint, schema change, infrastructure change, or combination?

---

## API Design Principles (apply throughout)

Before producing the design, apply this checklist mentally to every decision:

1. Choose the API style based on constraints (see decision tree below)
2. Define the contract first — no implementation before the contract is agreed
3. Define the error model upfront (RFC 9457 + stable error codes + trace IDs)
4. Define AuthN/AuthZ boundaries (scopes, roles, tenancy) and threat model
5. Define pagination, filter, and sort for all list endpoints
6. Define idempotency strategy for all mutating operations (especially POST)
7. Define observability: W3C Trace Context, request IDs, structured logs
8. Flag any breaking changes — these require a version bump and 90-day deprecation notice

### API Style Decision Tree

```
Is this an internal microservice call?
├─ High throughput or strong typing needed  →  gRPC  ✓ (Jamtrack Radio default)
└─ Browser media streaming                 →  REST  (Streaming Service only)

Is this a future public-facing API?
└─  REST with OpenAPI 3.1                  (broad compatibility, cacheable)
```

### Quick Reference

| Concern | Pattern | Key Elements |
|---|---|---|
| Internal APIs | gRPC + Protobuf | Binary protocol, strong types, streaming |
| External/media | REST (HTTP semantics RFC 9110) | Nouns not verbs, correct status codes, cacheability |
| Versioning | URL versioning | `/v1/resource` → `/v2/resource` on breaking change |
| Errors | RFC 9457 Problem Details | `type`, `title`, `status`, `detail`, `traceId`, `errors[]` |
| Auth | JWT Bearer | `Authorization: Bearer <token>`, scopes/roles validated per endpoint |
| Pagination | Cursor-based (real-time data) | `cursor=<token>&limit=20`; document default and max page size |
| Rate limiting | Token bucket | `X-RateLimit-*` headers, `429` response with `Retry-After` |
| Idempotency | Natural key or idempotency key | Mutating ops document whether safe to retry |

### Do / Avoid

**Do:**
- Version APIs from day one
- Document deprecation policy before first deprecation (90-day minimum sunset)
- Treat breaking changes as a major version bump
- Include `traceId` in all error responses
- Return semantically correct HTTP status codes
- Keep minor changes backward compatible

**Avoid:**
- Removing or renaming fields without a deprecation period
- Changing field types in existing versions
- Using verbs in resource names (nouns only)
- Returning `500` for client errors
- Breaking changes without a major version bump
- Action endpoints everywhere (`/doSomething`)

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Instant deprecation | Breaks clients | 90-day minimum sunset period |
| Action endpoints | Inconsistent API surface | Use resources + HTTP verbs |
| Generic errors | Poor developer experience | Specific error codes + `traceId` |
| No rate limit headers | Clients can't back off | Include `X-RateLimit-*` headers |
| Missing idempotency | Duplicate mutations on retry | Natural key dedup or idempotency key |
| Leaky abstractions | Tight coupling | Design stable contracts independent of internals |

---

Once you have enough context, produce the following design document:

---

# Design: $ARGUMENTS

## 1. Summary
2–3 sentences describing what this is and how it fits into Jamtrack Radio.

## 2. API Style Decision
State the chosen style (gRPC or REST) and a one-line justification referencing the decision tree above.

## 3. Domain Model

For each **entity**: name, properties (name: type), invariants it must enforce, layer it lives in (always `Domain`).

For each **value object**: name, properties, why it is a value object (immutable, no identity).

For each **domain event** (if applicable): name and when it is raised.

## 4. API Contract

### gRPC
```protobuf
syntax = "proto3";
package jamtrack.<servicename>.v1;

service <ServiceName> {
  rpc <MethodName> (<Request>) returns (<Response>);
}

message <Request> { }
message <Response> { }
```

**Error mapping**:
| Domain Exception | gRPC Status Code |
|---|---|
| `NotFoundException` | `NOT_FOUND (5)` |
| `DuplicateException` | `ALREADY_EXISTS (6)` |
| `ValidationException` | `INVALID_ARGUMENT (3)` |
| `UnauthorizedException` | `UNAUTHENTICATED (16)` |

### REST (Streaming Service only)
```
METHOD /path/{param}
Headers: Authorization: Bearer <token>
Response: HTTP <status> — body shape
```

**Error model** (RFC 9457):
```json
{
  "type": "https://jamtrack.io/errors/<code>",
  "title": "Short description",
  "status": 422,
  "detail": "Specific detail for this occurrence",
  "traceId": "00-abc123-def456-01",
  "errors": [{ "field": "email", "message": "must be a valid email" }]
}
```

## 5. Authentication & Authorisation
- Required JWT claims/roles per endpoint
- Any service-to-service trust boundary notes

## 6. Pagination, Filtering & Sorting
For any list endpoint: pagination strategy, page size (default + max), supported filters, sort fields. If not applicable, state that explicitly.

## 7. Idempotency & Retry Guidance
For each mutating operation: is it idempotent? How? What is safe to retry?

## 8. Database Schema Changes
Table name, columns (name · type · constraints), indexes, foreign keys.

```csharp
[Migration(YYYYMMDDHHMMSS)]
public class Migration_Description : Migration
{
    public override void Up() { }
    public override void Down() { }
}
```
If no schema changes, state that explicitly.

## 9. Clean Architecture Layer Breakdown

| Layer | Artifact | Description |
|-------|----------|-------------|
| Domain | `EntityName` | Entity / value object |
| Application | `IRepositoryName` | Repository interface |
| Application | `CommandName` / `QueryName` + handler | Use case |
| Infrastructure | `RepositoryName` | Dapper implementation |
| Api | `service.proto` | gRPC contract |
| Api | `GrpcServiceName` | Maps proto request → Application command |

**Dependency rule**: Domain → no deps. Application → Domain only. Infrastructure → Application. Api → Application + Infrastructure (DI wiring only).

## 10. Observability
- Key operations that must emit a Serilog log entry (include `traceId`, `userId`)
- Confirm `/health/live` and `/health/ready` are present
- W3C `traceparent` header forwarded on all outbound calls

## 11. Diagrams

Include every diagram type that applies to this feature. Omit types that add no value for the change in scope — but if in doubt, include it.

### Class Diagram (include when introducing or changing domain entities, value objects, or service interfaces)

```mermaid
classDiagram
    class EntityName {
        +Guid Id
        +string Property
        +DateTime CreatedAt
        +Create(args) EntityName
    }
    class IRepositoryName {
        <<interface>>
        +GetByIdAsync(id, ct) Task~Entity~
        +AddAsync(entity, ct) Task
    }
    EntityName --> IRepositoryName : persisted by
```

### Sequence Diagram (include for every feature — shows the primary request/response flow)

```mermaid
sequenceDiagram
    participant Client
    participant Api as Api Layer
    participant App as Application Layer
    participant Infra as Infrastructure Layer
    participant DB as PostgreSQL

    Client->>Api: Request
    Api->>App: Command / Query
    App->>Infra: Repository call
    Infra->>DB: SQL via Dapper
    DB-->>Infra: Result
    Infra-->>App: Domain entity
    App-->>Api: Result DTO
    Api-->>Client: Response
```

### State Diagram (include when an entity has a lifecycle with transitions, e.g. track upload status, user account state)

```mermaid
stateDiagram-v2
    [*] --> State1 : trigger
    State1 --> State2 : event
    State2 --> [*] : terminal
```

### UI Mockup

> **Redirected**: If a Discovery workflow was run, UI prototypes were produced by `/ui-prototype` and saved to `docs/prototypes/<feature>/`. Reference those screens here rather than re-creating them.
>
> If no Discovery workflow was run for this feature, produce the UI mockup inline using HTML (see the `/ui-prototype` skill for the Jamtrack Radio styling conventions).

### UI Flow (include when a feature involves multiple screens or steps the user navigates through)

```mermaid
flowchart LR
    A[Screen 1] -->|action| B[Screen 2]
    B -->|success| C[Screen 3]
    B -->|error| A
```

### Process Flow (include for background jobs, multi-service orchestration, or complex business processes)

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Step]
    B -->|No| D[Alternative]
    C --> E[End]
    D --> E
```

## 12. Acceptance Criteria
Each maps to at least one integration test in Step 4 (`/test`). Cover: happy path, domain errors, validation errors, not-found, and auth failure.

- [ ] Given [context], when [action], then [expected outcome]

## 13. Open Questions
Unresolved decisions or dependencies. If none, state "None."

---

After producing the design, ask:
- Are there sections to revise or expand?
- Should this be saved to `docs/designs/<feature-name>.md`?
- Ready to move to Step 2 — Implementation (`/implement`)?
