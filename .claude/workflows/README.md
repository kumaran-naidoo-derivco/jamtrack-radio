# Jamtrack Radio — Workflows

This directory contains the end-to-end workflow documentation for the Jamtrack Radio project. Every feature — from initial idea to post-deployment value measurement — follows a structured four-workflow lifecycle.

---

## The Four Workflows

```
PRODUCT-DISCOVERY → FEATURE-DISCOVERY → DEVELOPMENT → MONITORING
```

| Workflow | File | When to run | Primary agents |
|----------|------|-------------|----------------|
| **Product Discovery** | `PRODUCT-DISCOVERY.md` | Once at product inception (or major pivot) — covers the whole product | Product Manager, Product Designer, Architect, Project Manager |
| **Feature Discovery** | `DISCOVERY.md` | Before any code is written — for every new service or feature | Product Manager, Product Designer, Architect, Project Manager |
| **Development** | `DEVELOPMENT.md` | After Feature Discovery sign-off — to build and deploy the feature | Senior Developer, DevOps Engineer |
| **Monitoring** | `MONITORING.md` | After every deployment — to verify health and measure value | DevOps Engineer, Product Manager |
| **Git Workflow** | `GIT-WORKFLOW.md` | Every change — cross-cutting, applies at any workflow step that produces a PR | All agents |

> **Product vs Feature Discovery**: Product Discovery runs once and answers "Should we build this product?" — it produces the master PRD, design system, system-level architecture, and all GitHub milestones. Feature Discovery runs before each service build and answers "Should we add this feature now?" — it scopes to a single bounded context and creates sprint-level issues. See `PRODUCT-DISCOVERY.md` for a full comparison table.

---

## How the Workflows Chain Together

```
┌─────────────────────────────────────────────────────────────────┐
│ PRODUCT DISCOVERY  (run once at inception)                       │
│                                                                  │
│  PM: /requirements → /market-research → /prd                    │
│    → Product Designer: /design-system → /ui-prototype           │
│      → Architect: /software-architect → /cloud-architect        │
│        → /data-architect → /arch-security                       │
│          → /architect (sign-off) → PM: /project-plan            │
│                                                                  │
│  Outputs: docs/requirements/   docs/prds/                       │
│           docs/design-system/  docs/prototypes/jamtrack-radio/  │
│           docs/architecture/jamtrack-radio/  docs/decisions/    │
│           docs/project-plan/   GitHub milestones (all phases)   │
└────────────────────────────┬────────────────────────────────────┘
                             │ Product baseline established
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ FEATURE DISCOVERY  (run before each service / feature)           │
│                                                                  │
│  PM: /requirements → /market-research → /prd                    │
│    → Product Designer: /ux-research (opt) → /ui-prototype       │
│      → Architect: /software-architect → /cloud-architect        │
│        → /data-architect → /arch-security                       │
│          → /architect (sign-off) → PM: /project-plan            │
│                                                                  │
│  Outputs: docs/requirements/<service>-requirements.md           │
│           docs/prds/<service>.md                                 │
│           docs/ux-research/<service>-ux-research.md (opt)       │
│           docs/prototypes/<service>/                             │
│           docs/architecture/<service>/                           │
│           GitHub sprint-level issues in existing milestone       │
└────────────────────────────┬────────────────────────────────────┘
                             │ Feature sign-off obtained
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ DEVELOPMENT                                                      │
│                                                                  │
│  /design → [PM checkpoint] → /implement → quality pass          │
│    → /review → /test → /deploy-staging                          │
│      → [/design-review if UI feature] → /integration-test       │
│        → /deploy-prod                                           │
│                                                                  │
│  Outputs: merged PR, passing CI, deployed service               │
└────────────────────────────┬────────────────────────────────────┘
                             │ Deployment complete
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ MONITORING                                                       │
│                                                                  │
│  /monitor-health → /monitor-errors → /monitor-performance       │
│    → /monitor-report → /retrospective                           │
│      → /value-report (1–4 weeks later, by Product Manager)     │
│                                                                  │
│  Outputs: docs/monitoring-reports/, docs/retrospectives/,       │
│           docs/value-reports/, GitHub issues for action items   │
└────────────────────────────┬────────────────────────────────────┘
                             │ Cycle complete
                             ▼
                    Next FEATURE DISCOVERY cycle
```

---

## Agent Personas

Each workflow is owned by specific agent personas. Invoke them with a skill:

| Agent | Skill | Workflow Ownership |
|-------|-------|-------------------|
| Product Manager | `/product-manager` | Discovery Steps 1–3 (requirements, market research, PRD) + MONITORING Step 6 |
| Product Designer | `/product-designer` | Discovery Step 4 (design system, UX research, prototypes) + ad-hoc `/design-review` |
| Architect | `/architect` | Discovery Steps 5–6 (four architecture views + sign-off) |
| Project Manager | `/project-manager` | Discovery Step 7 + DEVELOPMENT checkpoint |
| Senior Developer | `/senior-developer` | DEVELOPMENT Steps 1–5 |
| DevOps Engineer | `/devops-engineer` | DEVELOPMENT Steps 6–8 + all of MONITORING Steps 1–5 |

### When to invoke each persona

- **Starting a new product?** → Run `/product-manager` first (Product Discovery)
- **Starting a new feature/service?** → Run `/product-manager` first (Feature Discovery)
- **PRD approved, ready to design?** → Run `/product-designer`
- **Prototypes approved, ready for architecture?** → Run `/architect`
- **Architecture signed off, ready for GitHub issues?** → Run `/project-manager`
- **Issues created, ready to implement?** → Run `/senior-developer`
- **PR merged, ready to deploy?** → Run `/devops-engineer`
- **UI feature deployed to staging, need a design check?** → Run `/design-review` (ad-hoc)

---

## Specialist Skills by Workflow Layer

### Discovery Skills

| Skill | Agent | Purpose |
|-------|-------|---------|
| `/requirements` | Product Manager | Problem, personas, constraints, success metrics, Value Prediction |
| `/market-research` | Product Manager | Competitor analysis, positioning map, differentiation opportunities |
| `/prd` | Product Manager | Full Product Requirements Document with Business Case |
| `/design-system` | Product Designer | Colour palette, typography, components, dark theme — run once at Product Discovery |
| `/ux-research` | Product Designer | User journey maps, accessibility checklist, screen inventory (optional in Feature Discovery) |
| `/ui-prototype` | Product Designer | Multi-screen HTML prototypes + Mermaid user flow (uses design system) |
| `/software-architect` | Architect | Service context, domain model, ADRs, build-vs-buy |
| `/cloud-architect` | Architect | Cloud topology, TCO, cost optimisation (phase-aware) |
| `/data-architect` | Architect | ER diagram, schema ownership, retention, storage costs |
| `/arch-security` | Architect | Trust boundaries, STRIDE, OWASP Top 10, cost/risk tradeoffs |
| `/project-plan` | Project Manager | GitHub milestone + all issues (dev + DevOps + testing) |

### Git Workflow Skill

| Skill | Purpose |
|-------|---------|
| `/raise-pr` | Full git workflow — sub-task issue → branch → commit with issue ref → push → PR with `Closes #` → CI → merge |

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
| `/design-review` | Ad-hoc post-implementation design audit — UI features only, after deploy-staging |

---

## docs/ Directory Convention

Each workflow produces outputs in specific `docs/` subdirectories:

```
docs/
  requirements/           ← /requirements outputs
  market-research/        ← /market-research outputs
  prds/                   ← /prd outputs
  design-system/          ← /design-system outputs (components.html + design-system.md)
  ux-research/            ← /ux-research outputs (optional Feature Discovery step)
  prototypes/<feature>/   ← /ui-prototype outputs
  architecture/<feature>/ ← /software-architect, /cloud-architect, /data-architect, /arch-security, /architect
  decisions/              ← ADRs from /software-architect (ADR-NNN-title.md)
  project-plan/           ← /project-plan delivery narratives
  designs/                ← /design technical design docs
  monitoring-reports/     ← /monitor-report HTML files (YYYY-MM-DD-PR<N>-<service>.html)
  retrospectives/         ← /retrospective markdown files
  value-reports/          ← /value-report markdown files (YYYY-MM-DD-<feature>.md)
  design-reviews/         ← /design-review audit reports (YYYY-MM-DD-<feature>-design-review.md)
```

---

## Deprecated

`WORKFLOW.md` — superseded by `DEVELOPMENT.md`. See that file for the redirect note.
