# Jamtrack Radio — Development Workflow

**Prerequisite**: `DISCOVERY.md` completed, architecture sign-off obtained, project plan and all GitHub issues created via `/project-plan`.

This document defines the end-to-end development lifecycle for every feature, bug fix, or change in the Jamtrack Radio project. Each step has a corresponding Claude Code skill and an assigned agent persona. Follow the steps in order — each gate must be passed before moving on.

After Step 7, proceed to `MONITORING.md`.

---

## Pre-flight Checklist

Before starting DEVELOPMENT, verify all of the following:

- [ ] DISCOVERY.md completed for this feature:
  - [ ] `/requirements` output exists in `docs/requirements/`
  - [ ] `/market-research` report exists in `docs/market-research/` (or explicitly waived with documented reason)
  - [ ] PRD approved and saved to `docs/prds/`
  - [ ] `/ui-prototype` screens exist in `docs/prototypes/<feature>/`
  - [ ] `/software-architect` output exists in `docs/architecture/<feature>/software-arch.md`
  - [ ] `/cloud-architect` output exists in `docs/architecture/<feature>/cloud-arch.md`
  - [ ] `/data-architect` output exists in `docs/architecture/<feature>/data-arch.md`
  - [ ] `/arch-security` output exists in `docs/architecture/<feature>/security-arch.md`
  - [ ] `/architect` sign-off completed (cross-view consistency check passed)
  - [ ] `/project-plan` run — GitHub milestone created, all issues (dev + DevOps + testing) created and assigned to milestone
- [ ] `dotnet build` passes on `main` with zero warnings
- [ ] Local Docker Compose stack (Postgres) is running (Phase 2+)

---

## The Workflow

```
Design → Implement → Quality Pass → Review → Test → Deploy Staging → Integration Test → Deploy Production
```

| Step | Skill | Agent | Gate to pass before moving on |
|------|-------|-------|-------------------------------|
| 1. Design | `/design` | Senior Developer | Design document approved, acceptance criteria agreed |
| — | **PM Checkpoint** | Project Manager | GitHub issues refined for the sprint (details below) |
| 2. Implement | `/implement` | Senior Developer | Code compiles, follows Clean Architecture, PR raised |
| 3. Quality Pass | `/robust` `/security` `/scalable` `/performant` | Senior Developer | All quality findings resolved |
| 4. Review | `/review` | Senior Developer | All review findings resolved, PR approved |
| 5. Test | `/test` | Senior Developer | All integration tests written and passing in CI |
| 6. Deploy Staging | `/deploy-staging` | DevOps Engineer | Service healthy, smoke tests passing |
| 7. Integration Test | `/integration-test` | DevOps Engineer | All integration tests passing against staging |
| 8. Deploy Production | `/deploy-prod` | DevOps Engineer | Deployment verified, rollback plan confirmed |

---

## Project Manager Checkpoint (Between Steps 1 and 2)

After the Senior Developer completes Step 1 (`/design`), the **Project Manager** reviews the design doc and refines the GitHub issues for the current sprint:

1. Reviews the design document's detailed task breakdown
2. Splits any oversized issues into sub-tasks (linked via GitHub's tasklist syntax)
3. Creates any newly-discovered DevOps tasks (e.g. "Add health check endpoint to Helm chart")
4. Updates effort estimates on all issues in the milestone
5. Closes any issues that turned out to be out of scope

Run `/project-manager` or invoke the Project Manager agent to perform this checkpoint.

---

## Step 1 — Design (`/design`)

**Agent**: Senior Developer

**Purpose**: Think before coding. Produce a concrete design so implementation has clear direction.

**Pre-conditions**: If a Discovery workflow was run, load architecture docs from `docs/architecture/<feature>/` as context before designing.

**Inputs**: Feature name, task description, or GitHub issue number.

**Outputs**:
- Domain model (entities, value objects, domain events)
- API contract (`.proto` RPC definitions or REST spec)
- DB schema changes (table/column additions, FluentMigrator migration outline)
- Clean Architecture layer breakdown (what belongs in each layer)
- Mermaid sequence diagram of the primary flow
- Acceptance criteria (used in Step 5 to drive tests)

**Gate**: Design reviewed and agreed before any code is written.

---

## Step 2 — Implement (`/implement`)

**Agent**: Senior Developer

**Purpose**: Write production-quality code that satisfies the design.

**Inputs**: Design output from Step 1.

**Outputs**:
- C# code across all four Clean Architecture layers in order: Domain → Application → Infrastructure → Api
- DI wiring in `Program.cs`
- Serilog structured logging on every significant operation
- Health endpoints (`/health/live`, `/health/ready`)
- `.proto` file updated if a gRPC endpoint was added
- FluentMigrator migration if schema changed

**Gate**: `dotnet build` passes with zero warnings. PR raised against `main`.

---

## Step 3 — Quality Pass

**Agent**: Senior Developer

**Purpose**: Enforce production-grade code quality before review.

Run after `/implement` and before `/review`. `/robust` and `/security` are mandatory on every feature. `/scalable` and `/performant` apply to features touching DB access, list endpoints, or high-frequency operations.

| Skill | Purpose | When |
|-------|---------|------|
| `/robust` | Input validation, error handling, transient faults, cancellation, partial failure | Always |
| `/security` | Injection, auth/authz, secrets, OWASP Top 10, data exposure | Always |
| `/scalable` | Async correctness, stateless design, connection pooling, pagination | DB / service-to-service features |
| `/performant` | N+1 queries, missing indexes, blocking calls, unbounded result sets | List endpoints, high-frequency ops |

**Gate**: All quality findings resolved.

---

## Step 4 — Review (`/review`)

**Agent**: Senior Developer

**Purpose**: Catch issues before merge — architecture correctness, security, observability, code quality.

**Inputs**: The diff of the PR branch against `main`.

**Checks**:
- Clean Architecture dependency rules not violated
- SOLID principles followed
- No framework references in Domain or Application layers
- Input validation at the API boundary
- All exceptions handled or mapped to a gRPC/HTTP status code
- No secrets in code
- Serilog logging present on all significant operations
- No synchronous blocking calls (`.Result`, `.Wait()`, `Thread.Sleep`)

**Gate**: All findings resolved. PR approved.

---

## Step 5 — Test (`/test`)

**Agent**: Senior Developer

**Purpose**: Prove the implementation works end-to-end with a real database.

**Inputs**: Implemented feature + acceptance criteria from Step 1.

**Outputs**:
- Integration tests in `tests/<Service>.Tests/` using WebApplicationFactory + Testcontainers
- AAA pattern throughout
- All acceptance criteria covered by at least one test
- Edge cases and error paths tested

**Gate**: `dotnet test` passes. CI `build` check green.

---

## Step 6 — Deploy Staging (`/deploy-staging`)

**Agent**: DevOps Engineer

**Purpose**: Deploy to staging and verify the service starts correctly.

**Phase 2 (local)**: Staging = local Docker Compose stack.
**Phase 3+ (K8s)**: Staging = local K8s cluster via Rancher Desktop.
**Phase 4+ (Azure)**: Staging = Azure AKS staging namespace.

**Gate**: All services healthy (`/health/ready` returns 200). No migration failures.

---

## Step 7 — Integration Test (`/integration-test`)

**Agent**: DevOps Engineer

**Purpose**: Verify the full system works in staging — not just the unit under test but cross-service interactions.

**Inputs**: Running staging environment from Step 6.

**Gate**: All integration tests green against staging. No regressions.

---

## Step 8 — Deploy Production (`/deploy-prod`)

**Agent**: DevOps Engineer

**Purpose**: Safely promote to production with a confirmed rollback plan.

**Phase 2**: Not applicable (local only).
**Phase 4+**: Azure AKS production namespace.

**Checklist**:
- [ ] All staging gates passed
- [ ] Migrations are backward compatible
- [ ] Rollback plan documented (previous image tag, down migration)
- [ ] Health checks verified post-deploy
- [ ] Smoke tests passing in production
- [ ] Logs monitored for 10 minutes post-deploy

**Gate**: Production healthy. No error spike in monitoring.

---

## Scaffolding Skills

Use these to generate boilerplate instead of repeating manual steps:

| Skill | Purpose |
|-------|---------|
| `/new-service [ServiceName]` | Scaffold a full Clean Architecture microservice (Domain/Application/Infrastructure/Api + Tests) |
| `/new-migration [Description]` | Scaffold a numbered FluentMigrator migration with Up/Down stubs |
| `/new-grpc-endpoint [Service Method]` | Scaffold a .proto RPC, Application command/query handler, and Api service stub |

---

After completing all 8 steps, proceed to `MONITORING.md`.
