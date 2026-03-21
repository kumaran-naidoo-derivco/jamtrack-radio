# Jamtrack Radio — Discovery Workflow

This workflow runs **before any code is written**. It ensures every feature is grounded in validated requirements, competitive research, approved design, and a concrete delivery plan before the first line of C# is touched.

After completing all 7 steps, proceed to `DEVELOPMENT.md`.

---

## Pre-flight Checklist

Before starting DISCOVERY, verify:

- [ ] GitHub repo exists and `main` branch is up to date
- [ ] Phase milestone exists on GitHub (e.g. "Phase 2") — or plan to create one via `/project-plan`
- [ ] `CLAUDE.md` is current (project conventions, phase status)
- [ ] No open DEVELOPMENT or MONITORING cycles pending for the same feature
- [ ] Retrospective from the previous cycle has been reviewed (if applicable)
- [ ] Action items from the last retrospective have been logged as GitHub issues (if applicable)

If any item is unchecked, resolve it before proceeding.

---

## The Workflow

```
Requirements → Market Research → PRD → UI Prototypes
  → Software Arch → Cloud Arch → Data Arch → Security Arch
    → Architect Sign-off → Project Plan
```

| Step | Skill | Agent | Gate to pass before moving on |
|------|-------|-------|-------------------------------|
| 1 | `/requirements` | Product Manager | Problem, personas, constraints, success metrics, and financial viability agreed |
| 2 | `/market-research` | Product Manager | Competitor analysis produced, differentiation strategy agreed |
| 3 | `/prd` | Product Manager | PRD approved, user stories and acceptance criteria signed off |
| 4 | `/ui-prototype` | Product Manager | Key screens mocked, user flow documented |
| 5a | `/software-architect` | Architect | Service boundaries and domain model agreed |
| 5b | `/cloud-architect` | Architect | Cloud topology and cost envelope agreed |
| 5c | `/data-architect` | Architect | ER diagram and data ownership agreed |
| 5d | `/arch-security` | Architect | Threat model and security controls agreed |
| 6 | `/architect` review | Architect | All 4 views consistent, total system cost accepted |
| 7 | `/project-plan` | Project Manager | GitHub milestone created, all issues created and assigned — proceed to DEVELOPMENT |

To start, run `/product-manager` to activate the Product Manager agent persona. The agent will guide you through Steps 1–4.

---

## Step 1 — Requirements (`/requirements`)

**Agent**: Product Manager

**Purpose**: Structured requirements gathering before the PRD. Captures the problem, personas, constraints, success metrics, and a financial Value Prediction that `/value-report` will validate post-deployment.

**Outputs saved to**: `docs/requirements/<feature>-requirements.md`

**Gate**: Problem statement concrete, personas defined, KPIs measurable, Value Prediction documented.

---

## Step 2 — Market Research (`/market-research`)

**Agent**: Product Manager

**Purpose**: Competitor analysis and differentiation strategy. Understand what others have built, where they fail, and where Jamtrack Radio can win.

**Outputs saved to**: `docs/market-research/<feature>-market-research.md`

**Gate**: At least 4 competitors analysed, 3 differentiation opportunities identified, strategic narrative written.

---

## Step 3 — PRD (`/prd`)

**Agent**: Product Manager

**Inputs**: Requirements output + market research output as context.

**Purpose**: Full Product Requirements Document with user stories, acceptance criteria, and a Business Case section referencing the Value Prediction.

**Outputs saved to**: `docs/prds/<feature>.md`

**Gate**: PRD approved. Acceptance criteria specific and testable.

---

## Step 4 — UI Prototype (`/ui-prototype`)

**Agent**: Product Manager

**Inputs**: Approved PRD.

**Purpose**: Multi-screen HTML prototypes for every key user interaction, plus a Mermaid user flow diagram.

**Outputs saved to**: `docs/prototypes/<feature>/`

**Gate**: All key screens mocked, user flow covers happy and error paths, prototype reviewed.

---

## Step 5 — Four Architecture Views

**Agent**: Architect (run `/architect` to activate)

The Architect orchestrates four specialist skills in sequence. Each view informs the next.

### Step 5a — Software Architecture (`/software-architect`)

**Purpose**: Service context diagram, domain model, component responsibility matrix, ADRs, build-vs-buy analysis.

**Outputs saved to**: `docs/architecture/<feature>/software-arch.md`, `docs/decisions/ADR-NNN-*.md`

**Gate**: Service boundaries agreed, domain model agreed.

### Step 5b — Cloud Architecture (`/cloud-architect`)

**Purpose**: Cloud topology, resource sizing, TCO table (Dev/Staging/Prod + 2×/10× scale), cost optimisation recommendations.

**Outputs saved to**: `docs/architecture/<feature>/cloud-arch.md`

**Gate**: Cloud topology agreed, cost envelope accepted by Product Manager.

### Step 5c — Data Architecture (`/data-architect`)

**Purpose**: ER diagram, schema ownership, DDL + migration outline, index strategy, observability events, retention/compliance, storage costs.

**Outputs saved to**: `docs/architecture/<feature>/data-arch.md`

**Gate**: ER diagram agreed, schema ownership documented, retention policies defined.

### Step 5d — Security Architecture (`/arch-security`)

**Purpose**: Trust boundary diagram, STRIDE threat model, security controls matrix, auth/authz map, OWASP Top 10 checklist, cost/risk tradeoffs per control.

**Outputs saved to**: `docs/architecture/<feature>/security-arch.md`

**Gate**: Threat model reviewed, security controls agreed for this phase.

---

## Step 6 — Architect Sign-off (`/architect`)

**Agent**: Architect

**Purpose**: Cross-view consistency review. Do service boundaries (software) match K8s namespaces (cloud)? Do DB ownership assignments (data) match service responsibilities (software)? Are security controls applied to every data store and service boundary?

Produce a consolidated TCO summary and get Product Manager sign-off on total system cost.

**Output saved to**: `docs/architecture/<feature>/architect-signoff.md`

**Gate**: All four views consistent. Total system cost accepted.

---

## Step 7 — Project Plan (`/project-plan`)

**Agent**: Project Manager (run `/project-manager` to activate)

**Purpose**: Create the GitHub milestone, generate all GitHub issues for the delivery (dev tasks + DevOps infrastructure tasks + testing tasks), apply labels and effort estimates, and produce a phase-based delivery narrative.

**Output saved to**: `docs/project-plan/<feature>-plan.md`, GitHub milestone + issues

**Gate**: All issues created, milestone exists, delivery narrative produced.

---

## After Step 7

Proceed to `DEVELOPMENT.md`. The Senior Developer begins with Step 1 (`/design`), loading the architecture docs from `docs/architecture/<feature>/` as context.

---

## docs/ Directory Convention

| Directory | Created by |
|-----------|-----------|
| `docs/requirements/` | `/requirements` |
| `docs/market-research/` | `/market-research` |
| `docs/prds/` | `/prd` |
| `docs/prototypes/<feature>/` | `/ui-prototype` |
| `docs/architecture/<feature>/` | `/software-architect`, `/cloud-architect`, `/data-architect`, `/arch-security`, `/architect` |
| `docs/decisions/` | `/software-architect` (ADRs) |
| `docs/project-plan/` | `/project-plan` |
