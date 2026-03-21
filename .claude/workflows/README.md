# Jamtrack Radio — Workflows

This directory contains the end-to-end workflow documentation for the Jamtrack Radio project. Every feature — from initial idea to post-deployment value measurement — follows a structured three-workflow lifecycle.

---

## The Three Workflows

```
DISCOVERY → DEVELOPMENT → MONITORING
```

| Workflow | File | When to run | Primary agents |
|----------|------|-------------|----------------|
| **Discovery** | `DISCOVERY.md` | Before any code is written — for every new feature or phase | Product Manager, Architect, Project Manager |
| **Development** | `DEVELOPMENT.md` | After Discovery sign-off — to build and deploy the feature | Senior Developer, DevOps Engineer |
| **Monitoring** | `MONITORING.md` | After every deployment — to verify health and measure value | DevOps Engineer, Product Manager |

---

## How the Workflows Chain Together

```
┌─────────────────────────────────────────────────────────────────┐
│ DISCOVERY                                                        │
│                                                                  │
│  /requirements → /market-research → /prd → /ui-prototype        │
│    → /software-architect → /cloud-architect                      │
│      → /data-architect → /arch-security                          │
│        → /architect (sign-off) → /project-plan                  │
│                                                                  │
│  Outputs: docs/requirements/, docs/prds/, docs/architecture/,   │
│           docs/prototypes/, GitHub milestone + issues            │
└────────────────────────────┬────────────────────────────────────┘
                             │ Sign-off obtained
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ DEVELOPMENT                                                      │
│                                                                  │
│  /design → [PM checkpoint] → /implement → quality pass           │
│    → /review → /test → /deploy-staging                           │
│      → /integration-test → /deploy-prod                          │
│                                                                  │
│  Outputs: merged PR, passing CI, deployed service                │
└────────────────────────────┬────────────────────────────────────┘
                             │ Deployment complete
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ MONITORING                                                       │
│                                                                  │
│  /monitor-health → /monitor-errors → /monitor-performance        │
│    → /monitor-report → /retrospective                            │
│      → /value-report (1–4 weeks later, by Product Manager)      │
│                                                                  │
│  Outputs: docs/monitoring-reports/, docs/retrospectives/,        │
│           docs/value-reports/, GitHub issues for action items    │
└────────────────────────────┬────────────────────────────────────┘
                             │ Cycle complete
                             ▼
                    Next DISCOVERY cycle
```

---

## Agent Personas

Each workflow is owned by specific agent personas. Invoke them with a skill:

| Agent | Skill | Workflow Ownership |
|-------|-------|-------------------|
| Product Manager | `/product-manager` | DISCOVERY Steps 1–4, MONITORING Step 6 |
| Architect | `/architect` | DISCOVERY Steps 5–6 |
| Project Manager | `/project-manager` | DISCOVERY Step 7, DEVELOPMENT checkpoint |
| Senior Developer | `/senior-developer` | DEVELOPMENT Steps 1–5 |
| DevOps Engineer | `/devops-engineer` | DEVELOPMENT Steps 6–8, all of MONITORING Steps 1–5 |

### When to invoke each persona

- **Starting a new feature?** → Run `/product-manager` first
- **PRD and prototypes approved, ready to design architecture?** → Run `/architect`
- **Architecture signed off, ready to create GitHub issues?** → Run `/project-manager`
- **Issues created, ready to implement?** → Run `/senior-developer`
- **PR merged, ready to deploy?** → Run `/devops-engineer`

---

## Specialist Skills by Workflow Layer

### Discovery Skills

| Skill | Purpose |
|-------|---------|
| `/requirements` | Problem, personas, constraints, success metrics, Value Prediction |
| `/market-research` | Competitor analysis, positioning map, differentiation opportunities |
| `/prd` | Full Product Requirements Document |
| `/ui-prototype` | Multi-screen HTML prototypes + Mermaid user flow |
| `/software-architect` | Service context, domain model, ADRs, build-vs-buy |
| `/cloud-architect` | Cloud topology, TCO, cost optimisation (phase-aware) |
| `/data-architect` | ER diagram, schema ownership, retention, storage costs |
| `/arch-security` | Trust boundaries, STRIDE, OWASP Top 10, cost/risk tradeoffs |
| `/project-plan` | GitHub milestone + all issues (dev + DevOps + testing) |

### Development Skills

| Skill | Purpose |
|-------|---------|
| `/design` | Technical design: domain model, API contract, DB schema, sequence diagram |
| `/implement` | Production-quality C# across all Clean Architecture layers |
| `/robust` | Input validation, error handling, fault tolerance |
| `/security` | OWASP Top 10, auth/authz, secrets hygiene |
| `/scalable` | Async correctness, connection pooling, pagination |
| `/performant` | N+1 queries, missing indexes, blocking calls |
| `/review` | Architecture correctness, SOLID, observability, no secrets in code |
| `/test` | Integration tests with WebApplicationFactory + Testcontainers |
| `/deploy-staging` | Phase-aware staging deployment |
| `/integration-test` | Cross-service integration tests in staging |
| `/deploy-prod` | Production deployment with rollback plan |

### Scaffolding Skills

| Skill | Purpose |
|-------|---------|
| `/new-service` | Scaffold a full Clean Architecture microservice |
| `/new-migration` | Scaffold a numbered FluentMigrator migration |
| `/new-grpc-endpoint` | Scaffold a .proto RPC + Application handler + Api stub |

### Monitoring Skills

| Skill | Purpose |
|-------|---------|
| `/monitor-health` | Health endpoint checks, pod status, migration verification |
| `/monitor-errors` | Error rate analysis vs. pre-deploy baseline |
| `/monitor-performance` | p50/p95/p99 latency analysis vs. baseline |
| `/monitor-report` | Standalone HTML deployment monitoring report |
| `/retrospective` | Structured post-deployment retrospective |
| `/value-report` | Predicted vs. actual value validation (run weeks after deployment) |

---

## Ad-hoc Skills

These skills can be used independently, outside of a formal workflow:

| Skill | When to use |
|-------|-------------|
| `/arch-diagram` | Ad-hoc architecture diagrams (not as part of structured Discovery) |
| `/prd` | Ad-hoc PRD without a full Discovery workflow (for simple changes) |

---

## docs/ Directory Convention

Each workflow produces outputs in specific `docs/` subdirectories:

```
docs/
  requirements/           ← /requirements outputs
  market-research/        ← /market-research outputs
  prds/                   ← /prd outputs
  prototypes/<feature>/   ← /ui-prototype outputs
  architecture/<feature>/ ← /software-architect, /cloud-architect, /data-architect, /arch-security, /architect
  decisions/              ← ADRs from /software-architect (ADR-NNN-title.md)
  project-plan/           ← /project-plan delivery narratives
  designs/                ← /design technical design docs
  monitoring-reports/     ← /monitor-report HTML files (YYYY-MM-DD-PR<N>-<service>.html)
  retrospectives/         ← /retrospective markdown files
  value-reports/          ← /value-report markdown files (YYYY-MM-DD-<feature>.md)
```

---

## Deprecated

`WORKFLOW.md` — superseded by `DEVELOPMENT.md`. See that file for the redirect note.
