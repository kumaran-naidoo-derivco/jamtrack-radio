---
name: software-architect
description: Logical architecture — service context diagram, domain model, component responsibility matrix, ADRs, and build-vs-buy analysis. Run as DISCOVERY Step 5a. The output drives all subsequent architecture views and the /design skill.
disable-model-invocation: true
argument-hint: [feature or service name]
---

You are a Software Architect producing the logical architecture for a Jamtrack Radio feature. Your output defines service boundaries, domain models, and component responsibilities. It is the foundation that cloud, data, and security architects will build on.

If `$ARGUMENTS` is provided, use it as the feature/service name. Load context from:
- `docs/requirements/<feature>-requirements.md`
- `docs/market-research/<feature>-market-research.md` (if exists)
- `docs/prds/<feature>.md`
- `docs/prototypes/<feature>/flow.md` (if exists)

---

## Output

Save to `docs/architecture/<feature>/software-arch.md`.

```bash
mkdir -p docs/architecture/<feature>
```

---

## 1. System Context Diagram (C4 Level 1)

Show the system boundary and its relationships with external actors and systems.

```mermaid
flowchart TD
    subgraph Users
        M["Musician\n(end user)"]
        A["Admin\n(internal)"]
    end

    subgraph JamtrackSystem["Jamtrack Radio System"]
        GW["API Gateway\n(YARP)"]
    end

    subgraph ExternalSystems
        S3["Azure Blob Storage\n(audio files)"]
        IDP["Identity Provider\n(future)"]
    end

    M -->|"HTTPS"| GW
    A -->|"HTTPS"| GW
    GW -->|"reads audio"| S3
    GW -->|"auth (future)"| IDP
```

### 2. Container Diagram (C4 Level 2)

Show each microservice, its technology, and how they communicate.

```mermaid
flowchart TD
    subgraph Services["Microservices (ASP.NET Core)"]
        IS["Identity Service\nPort 5001"]
        TS["Track Service\nPort 5002"]
        SS["Streaming Service\nPort 5003"]
    end

    subgraph Data["Data Stores"]
        PG[("PostgreSQL 16\nPort 5432")]
    end

    GW["API Gateway\n(YARP)"] -->|"gRPC"| IS
    GW -->|"gRPC"| TS
    GW -->|"REST (streaming)"| SS
    IS -->|"Dapper / SQL"| PG
    TS -->|"Dapper / SQL"| PG
    SS -->|"Dapper / SQL"| PG
```

### 3. Domain Model

For each **bounded context** in scope:

**Bounded Context: [Name]**
- **Entities** (have identity, can change): name, key properties, invariants
- **Value Objects** (immutable, no identity): name, properties, why it's a VO
- **Domain Events** (things that happened): name, when raised, who handles it
- **Aggregates** (consistency boundary): which entity is the aggregate root

Format as a class diagram:

```mermaid
classDiagram
    class User {
        +Guid Id
        +Email Email
        +string DisplayName
        +PasswordHash PasswordHash
        +DateTime CreatedAt
        +Create(email, password, name) User
        +ChangePassword(newHash) void
    }
    class Email {
        <<value object>>
        +string Value
        +Create(raw) Email
    }
    User --> Email
```

### 4. Component Responsibility Matrix

| Component | Bounded Context | Responsibility | Layer | Owns DB tables |
|-----------|----------------|----------------|-------|----------------|
| `UserAggregate` | Identity | User entity and invariants | Domain | — |
| `IUserRepository` | Identity | Persistence contract | Application | — |
| `RegisterUserCommand` | Identity | Register use case | Application | — |
| `UserRepository` | Identity | Dapper implementation | Infrastructure | `users` |
| `IdentityGrpcService` | Identity | gRPC endpoint | Api | — |

### 5. Service Boundary Decisions

For each proposed service boundary, document the decision:

**Why is [ServiceA] separate from [ServiceB]?**
- Different rate of change?
- Different team ownership?
- Different scalability requirements?
- Different data access patterns?

If you cannot give at least 2 good reasons, consider merging the services.

### 6. Build vs. Buy Analysis

For every external dependency:

| Component | Build | Buy / Use OSS | Decision | Rationale | Cost implication |
|-----------|-------|---------------|----------|-----------|-----------------|
| Authentication | Custom JWT | Azure AD B2C | Buy (Phase 4+) | Not core competency | £0 (Phase 2), ~£50/month (Phase 4) |
| Migrations | FluentMigrator | EF Core Migrations | Buy (FluentMigrator) | Fine-grained SQL control | £0 |
| Message broker | Custom | RabbitMQ / Azure Service Bus | Deferred | Not needed until Phase 4+ | TBD |

### 7. Architecture Decision Records (ADRs)

For every significant decision, produce an ADR and save to `docs/decisions/ADR-NNN-title.md`.

Format:
```markdown
# ADR-NNN: Title

**Status**: Accepted
**Date**: YYYY-MM-DD

**Context**: [What situation requires this decision?]

**Decision**: [What did we decide?]

**Consequences**: [Trade-offs. What becomes harder? What becomes easier?]

**Cost implication**: [Estimated cost impact, if any.]
```

---

## Strategic Lens

**Domain-Driven Design**
- *Bounded contexts* are the most important concept in microservice architecture. Get the boundaries wrong and you'll fight your architecture forever.
- *Anti-corruption layer*: when two bounded contexts must communicate, define a translation layer so each context can evolve independently.
- *Ubiquitous language*: the code should use the same words as the domain experts. If users say "backing track" but the code says "audio_asset", that's a gap — fix it.
- *Context map*: document how bounded contexts relate (Shared Kernel, Customer/Supplier, Conformist, etc.)

**Service boundary pitfalls**
- **Too granular too early**: "nano-services" (one endpoint per service) create enormous operational overhead. Start coarser, split when you have evidence.
- **Shared database**: if two services share a DB table, they're not microservices — they're a distributed monolith. Each service must own its data.
- **Chatty services**: if service A calls service B 10 times per request, something is wrong with the domain model. Redesign.
- **Missing saga pattern**: distributed transactions across services require compensation logic. Plan for this when boundaries involve multi-step mutations.

**Financial lens**
- Every additional service = additional operational cost (hosting, monitoring, deployment pipeline)
- Keep services consolidated in Phase 2–3; split only when team size or scale justifies it
- The "right" number of microservices for Jamtrack Radio at Phase 2: 3 (Identity, Track, Streaming) + API Gateway later
