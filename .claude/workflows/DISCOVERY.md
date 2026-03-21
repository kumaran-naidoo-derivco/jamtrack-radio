# Jamtrack Radio — Feature Discovery Workflow

> **This is Feature Discovery.** It covers one service or capability at a time.
>
> **Pre-condition**: Product Discovery (`PRODUCT-DISCOVERY.md`) must be complete before starting Feature Discovery. The design system (`docs/design-system/`) and system-level architecture docs (`docs/architecture/jamtrack-radio/`) must exist.
>
> If Product Discovery has not been run yet, start there first.

This workflow runs **before any code is written**. It ensures every feature is grounded in validated requirements, competitive research, approved design, and a concrete delivery plan before the first line of C# is touched.

After completing all steps, proceed to `DEVELOPMENT.md`.

---

## Pre-flight Checklist

Before starting Feature Discovery, verify:

- [ ] **Product Discovery is complete** — `docs/architecture/jamtrack-radio/` has 5 files (software-arch, cloud-arch, data-arch, security-arch, architect-signoff)
- [ ] **Design system exists** — `docs/design-system/jamtrack-radio-design-system.md` is present (Product Discovery Step 4a)
- [ ] GitHub repo exists and `main` branch is up to date
- [ ] Phase milestone exists on GitHub (created during Product Discovery Step 7)
- [ ] `CLAUDE.md` is current (project conventions, phase status)
- [ ] No open DEVELOPMENT or MONITORING cycles pending for the same feature
- [ ] Retrospective from the previous cycle has been reviewed (if applicable)
- [ ] Action items from the last retrospective have been logged as GitHub issues (if applicable)

If any item is unchecked, resolve it before proceeding.

---

## The Workflow

```
PM: /requirements → /market-research → /prd
  → Product Designer: /ux-research (optional) → /ui-prototype
    → Architect: /software-architect → /cloud-architect → /data-architect → /arch-security
      → Architect: sign-off
        → PM: /project-plan
```

| Step | Skill | Agent | Gate |
|------|-------|-------|------|
| 1 | `/requirements` | Product Manager | Problem, personas, constraints, success metrics, and financial viability agreed |
| 2 | `/market-research` | Product Manager | Competitor analysis produced, differentiation strategy agreed |
| 3 | `/prd` | Product Manager | PRD approved, user stories and acceptance criteria signed off |
| 4a | `/ux-research` *(optional)* | Product Designer | User journey maps produced, accessibility checklist completed, screen inventory agreed |
| 4b | `/ui-prototype` | Product Designer | All feature screens mocked (using design system), user flow covers happy + error paths |
| 5a | `/software-architect` | Architect | Service boundaries and domain model agreed (consistent with system-level baseline) |
| 5b | `/cloud-architect` | Architect | Cloud topology and cost envelope agreed |
| 5c | `/data-architect` | Architect | ER diagram and data ownership agreed |
| 5d | `/arch-security` | Architect | Threat model and security controls agreed |
| 6 | `/architect` review | Architect | All 4 views consistent, cross-view consistency with system baseline verified, total cost accepted |
| 7 | `/project-plan` | Project Manager | Sprint-level GitHub issues created in existing milestone — proceed to DEVELOPMENT |

**To start**: Run `/product-manager` to activate the Product Manager persona for Steps 1–3. After Step 3, run `/product-designer` for Steps 4a–4b.

---

## Step 1 — Requirements (`/requirements`)

**Agent**: Product Manager

**Feature scope**: This feature/service only — not the whole product.

**Purpose**: Capture the problem this feature solves, define the relevant personas, document feature-specific constraints and success metrics, and produce a Value Prediction (is this feature worth building now?).

**Context to load**: `docs/requirements/jamtrack-radio-requirements.md` (product-level personas and constraints as baseline).

**Output saved to**: `docs/requirements/<feature>-requirements.md`

**Gate**: Problem statement concrete, personas defined, KPIs measurable, Value Prediction documented.

---

## Step 2 — Market Research (`/market-research`)

**Agent**: Product Manager

**Feature scope**: How do competitors handle this specific feature or capability? What can we learn?

**Purpose**: Targeted competitor analysis for this feature. Understand what has been built elsewhere, where it falls short, and where this feature can differentiate.

**Context to load**: `docs/market-research/jamtrack-radio-market-research.md` (product-level competitive landscape as baseline).

**Output saved to**: `docs/market-research/<feature>-market-research.md`

**Gate**: At least 3 comparable features analysed, differentiation opportunities identified, strategic narrative written.

---

## Step 3 — PRD (`/prd`)

**Agent**: Product Manager

**Inputs**: Feature requirements + market research output as context.

**Purpose**: Feature-specific PRD with user stories, acceptance criteria, and a Business Case section referencing the Value Prediction.

**Context to load**: `docs/prds/jamtrack-radio.md` (master PRD — ensure this feature's requirements are consistent with the product baseline).

**Output saved to**: `docs/prds/<feature>.md`

**Gate**: PRD approved. Acceptance criteria specific and testable. No conflicts with master PRD.

---

## Step 4a — UX Research (`/ux-research`) *(Optional — Recommended)*

**Agent**: Product Designer

**Inputs**: Approved feature PRD.

**Purpose**: User journey maps for this feature, accessibility checklist, usability heuristics review, and a screen inventory that directly feeds `/ui-prototype`. Skip for very simple features with one or two screens; use for anything complex or user-journey-heavy.

**Output saved to**: `docs/ux-research/<feature>-ux-research.md`

**Gate**: User journey maps cover all personas, screen inventory is complete, accessibility considerations documented.

---

## Step 4b — UI Prototypes (`/ui-prototype`)

**Agent**: Product Designer

**Inputs**: Approved feature PRD + design system (`docs/design-system/`) + UX research output (if Step 4a was run).

**Purpose**: Multi-screen HTML prototypes for every user interaction in this feature, using the Jamtrack Radio design system for visual consistency. Plus a Mermaid user flow diagram.

**Output saved to**: `docs/prototypes/<feature>/`

**Gate**: All key screens mocked, design system tokens used consistently, user flow covers happy + error paths, prototype reviewed.

---

## Step 5 — Four Architecture Views

**Agent**: Architect (run `/architect` to activate)

**Feature scope**: All 4 views scoped to this service or bounded context. Must be consistent with the system-level baseline in `docs/architecture/jamtrack-radio/`.

The Architect orchestrates four specialist skills in sequence. Each view informs the next.

### Step 5a — Software Architecture (`/software-architect`)

**Purpose**: Service context diagram, domain model for this bounded context, component responsibility matrix, feature-level ADRs, build-vs-buy decisions.

**Context to load**: `docs/architecture/jamtrack-radio/software-arch.md` — ensure service boundaries are consistent with the system baseline.

**Outputs saved to**: `docs/architecture/<feature>/software-arch.md`, `docs/decisions/ADR-NNN-*.md`

**Gate**: Service boundaries agreed and consistent with system baseline, domain model agreed.

### Step 5b — Cloud Architecture (`/cloud-architect`)

**Purpose**: Topology for this service, resource sizing, cost contribution to total TCO, deployment config additions (Helm values, K8s resources).

**Context to load**: `docs/architecture/jamtrack-radio/cloud-arch.md` — this service slots into the existing topology.

**Output saved to**: `docs/architecture/<feature>/cloud-arch.md`

**Gate**: Service topology agreed, cost contribution accepted.

### Step 5c — Data Architecture (`/data-architect`)

**Purpose**: ER diagram for this service's tables, schema ownership, DDL + migration outline, index strategy, observability events, retention policies.

**Context to load**: `docs/architecture/jamtrack-radio/data-arch.md` — tables must be consistent with the system-level ER.

**Output saved to**: `docs/architecture/<feature>/data-arch.md`

**Gate**: ER agreed, schema ownership documented.

### Step 5d — Security Architecture (`/arch-security`)

**Purpose**: Trust boundaries for this service, STRIDE for this service's attack surface, security controls (scoped to this service), auth/authz map for this service's endpoints.

**Context to load**: `docs/architecture/jamtrack-radio/security-arch.md` — controls must be consistent with the system-level baseline.

**Output saved to**: `docs/architecture/<feature>/security-arch.md`

**Gate**: Threat model reviewed, security controls agreed for current phase.

---

## Step 6 — Architect Sign-off (`/architect`)

**Agent**: Architect

**Purpose**: Cross-view consistency check for this feature. Do service boundaries (software) match K8s namespace additions (cloud)? Does schema ownership (data) match service responsibilities (software)? Are security controls applied to every new data store and service boundary? Is this feature consistent with the system-level baseline?

Produce a cost contribution summary and get Product Manager sign-off.

**Output saved to**: `docs/architecture/<feature>/architect-signoff.md`

**Gate**: All four views consistent. Feature consistent with system baseline. Cost accepted.

---

## Step 7 — Project Plan (`/project-plan`)

**Agent**: Project Manager (run `/project-manager` to activate)

**Feature scope**: Sprint-level GitHub issues in the existing phase milestone. No new milestones needed — they were created during Product Discovery.

**Purpose**: Generate all GitHub issues for this feature's delivery (dev tasks + DevOps tasks + testing tasks), apply labels and effort estimates, produce a delivery narrative.

**Output saved to**: `docs/project-plan/<feature>-plan.md`, GitHub issues in existing milestone

**Gate**: All issues created and assigned, delivery narrative produced.

---

## After Step 7

Proceed to `DEVELOPMENT.md`. The Senior Developer begins with Step 1 (`/design`), loading the architecture docs from `docs/architecture/<feature>/` as context.

---

## docs/ Directory Convention

| Directory | Created by |
|-----------|-----------|
| `docs/requirements/<feature>-requirements.md` | `/requirements` |
| `docs/market-research/<feature>-market-research.md` | `/market-research` |
| `docs/prds/<feature>.md` | `/prd` |
| `docs/ux-research/<feature>-ux-research.md` | `/ux-research` (optional) |
| `docs/prototypes/<feature>/` | `/ui-prototype` |
| `docs/architecture/<feature>/` | `/software-architect`, `/cloud-architect`, `/data-architect`, `/arch-security`, `/architect` |
| `docs/decisions/ADR-NNN-*.md` | `/software-architect` |
| `docs/project-plan/<feature>-plan.md` | `/project-plan` |
