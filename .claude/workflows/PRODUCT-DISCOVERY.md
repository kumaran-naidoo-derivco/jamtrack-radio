# Jamtrack Radio — Product Discovery Workflow

> **This is Product Discovery.** Run it **once** at product inception (or revisit at a major pivot). It establishes the product baseline — master PRD, design system, system-level architecture, and all GitHub milestones — that every Feature Discovery cycle inherits from.
>
> After completing Product Discovery, proceed to **Feature Discovery** (`DISCOVERY.md`) for the first service.

---

## Product Discovery vs Feature Discovery

| Dimension | Product Discovery (this file) | Feature Discovery (`DISCOVERY.md`) |
|-----------|------------------------------|-------------------------------------|
| When | Once at inception; revisited at major pivots | Before every new service or significant feature |
| Scope | Whole product — all services, all personas | One service or capability |
| Market research | Full market landscape, all competitors | How competitors handle this specific feature |
| PRD | Master PRD covering entire product | Feature/service-specific PRD |
| Design system | Established here — run `/design-system` | Already exists — load from `docs/design-system/` |
| UX research | Not needed — product journeys covered by prototypes | Optional (`/ux-research`) — recommended for complex features |
| Prototypes | Key user journeys across the whole product | Screens for this feature only |
| Architecture | All 4 views at system level | All 4 views scoped to this service/bounded context |
| Project plan | All GitHub milestones (one per phase) + top-level issues | Sprint-level GitHub issues in an existing milestone |
| Pre-condition | None (this is the first cycle) | Product Discovery must be complete |
| Value question | "Should we build this product?" | "Should we add this feature now?" |

---

## Pre-flight Checklist

Before starting Product Discovery, verify:

- [ ] GitHub repo exists and `main` branch is up to date
- [ ] `CLAUDE.md` is current (project conventions, tech stack, dev environment)
- [ ] No existing `docs/` directory from a previous incomplete run (if re-running, archive first)
- [ ] Product vision is at least loosely articulated — even informally

---

## The Workflow

```
PM: /requirements → /market-research → /prd
  → Product Designer: /design-system → /ui-prototype
    → Architect: /software-architect → /cloud-architect → /data-architect → /arch-security
      → Architect: sign-off
        → PM: /project-plan
```

| Step | Skill | Agent | Gate |
|------|-------|-------|------|
| 1 | `/requirements` | Product Manager | Full product vision, all personas, total Value Prediction agreed |
| 2 | `/market-research` | Product Manager | Full market landscape, all competitors, overall positioning agreed |
| 3 | `/prd` | Product Manager | Master PRD approved, all user stories and acceptance criteria signed off |
| 4a | `/design-system` | Product Designer | Design language established — colours, typography, components, dark theme documented |
| 4b | `/ui-prototype` | Product Designer | Key product-level user journeys mocked, flow covers happy + error paths |
| 5a | `/software-architect` | Architect | All service boundaries and system-level domain model agreed |
| 5b | `/cloud-architect` | Architect | Full phase-aware cloud topology and total cost envelope agreed |
| 5c | `/data-architect` | Architect | Full ER diagram, schema ownership, retention policies agreed |
| 5d | `/arch-security` | Architect | System-wide threat model and security controls agreed |
| 6 | `/architect` review | Architect | All 4 views consistent, total TCO accepted by Product Manager |
| 7 | `/project-plan` | Project Manager | All GitHub milestones created, top-level issues per phase documented |

**To start**: Run `/product-manager` to activate the Product Manager persona. After Step 3, run `/product-designer` to activate the Product Designer for Steps 4a–4b.

---

## Step 1 — Requirements (`/requirements`)

**Agent**: Product Manager

**Product-level scope**: Full product vision — all services, all personas across the entire product.

**Key outputs**:
- Problem statement the product solves
- All target personas (not just one feature's users)
- Constraints (infrastructure, budget, compliance, dev environment)
- Success metrics for the full delivery
- **Value Prediction** — for a learning project: skills gained, portfolio evidence, viability threshold

**Output saved to**: `docs/requirements/jamtrack-radio-requirements.md`

**Gate**: Problem statement concrete, all personas defined, KPIs measurable, Value Prediction documented.

---

## Step 2 — Market Research (`/market-research`)

**Agent**: Product Manager

**Product-level scope**: Full market landscape — all tools the target users currently use across all feature areas.

**Key outputs**:
- Competitor analysis across all relevant tool categories
- Feature comparison matrix (all competitors × all key features)
- Differentiation opportunities (at least 3)
- Strategic positioning narrative

**Output saved to**: `docs/market-research/jamtrack-radio-market-research.md`

**Gate**: At least 5 tools/competitors analysed, 3+ differentiation opportunities identified, strategic narrative written.

---

## Step 3 — PRD (`/prd`)

**Agent**: Product Manager

**Inputs**: Requirements + market research as context.

**Product-level scope**: Master PRD covering all services and all phases.

**Key outputs**:
- All functional requirements (by service: Identity, Track, Playlist, Streaming, Storage, API Gateway)
- Non-functional requirements (performance, reliability, security, observability) — system-wide
- Phasing / milestones (v0.1 through v1.0)
- Business Case (§12) referencing the Value Prediction

**Output saved to**: `docs/prds/jamtrack-radio.md`

**Gate**: Master PRD approved, all services covered, Business Case included.

---

## Step 4a — Design System (`/design-system`)

**Agent**: Product Designer

**Product-level scope**: Run **once** to establish the Jamtrack Radio visual language. All future `/ui-prototype` runs load this as context.

**Key outputs**:
- Colour palette (CSS custom property tokens)
- Typography scale
- Spacing and border radius tokens
- Component library (buttons, inputs, forms, navigation, data display, audio player)
- Accessibility baseline (WCAG 2.1 AA)
- Live component showcase HTML

**Outputs saved to**: `docs/design-system/jamtrack-radio-design-system.md`, `docs/design-system/components.html`

**Gate**: All tokens defined, all components documented, component showcase renders, accessibility baseline agreed.

---

## Step 4b — UI Prototypes (`/ui-prototype`)

**Agent**: Product Designer

**Inputs**: Approved master PRD + design system from Step 4a.

**Product-level scope**: Key user journeys across the **whole product** — the skeleton screens that define the overall UX shape. These are not feature-complete; they establish the product's look, feel, and navigation structure.

**Screens to produce** (minimum for product-level):
- Welcome / landing
- Registration + login
- Main library view (track list with metadata)
- Track upload
- Now-playing / player view
- Playlist management
- Playlist detail

**Outputs saved to**: `docs/prototypes/jamtrack-radio/`

**Gate**: All key screens mocked using design system tokens, user flow covers happy + error paths.

---

## Step 5 — Four Architecture Views

**Agent**: Architect (run `/architect` to activate)

**Product-level scope**: All 4 views at the **system level** — the entire product, not a single bounded context. Each view informs the next.

### Step 5a — Software Architecture (`/software-architect`)

System-level context and container diagrams, domain model across all services, component responsibilities, service boundary decisions, build-vs-buy analysis, 3–5 system-level ADRs.

**Output**: `docs/architecture/jamtrack-radio/software-arch.md`, `docs/decisions/ADR-NNN-*.md`

**Gate**: All service boundaries agreed, system domain model agreed.

### Step 5b — Cloud Architecture (`/cloud-architect`)

Phase-aware topology for all phases (Phase 2 local → Phase 3 K8s → Phase 4 Azure → Phase 5 AWS). Full TCO across all phases. Cost optimisation for Phase 4+. Helm chart structure per service.

**Output**: `docs/architecture/jamtrack-radio/cloud-arch.md`

**Gate**: Full phase-aware topology agreed, total cost envelope accepted.

### Step 5c — Data Architecture (`/data-architect`)

Full ER diagram for all services, schema ownership matrix, DDL outlines in FluentMigrator format, index strategy, observability events, retention policies, storage cost estimation.

**Output**: `docs/architecture/jamtrack-radio/data-arch.md`

**Gate**: Full ER agreed, schema ownership documented, retention policies defined.

### Step 5d — Security Architecture (`/arch-security`)

System-wide trust boundary diagram, data classification, STRIDE across the whole system, security controls per phase, auth/authz map for all endpoints, OWASP Top 10 checklist.

**Output**: `docs/architecture/jamtrack-radio/security-arch.md`

**Gate**: System-wide threat model reviewed, Phase 2 security controls agreed.

---

## Step 6 — Architect Sign-off (`/architect`)

**Agent**: Architect

Cross-view consistency check across the entire system. Consolidated TCO summary. Product Manager sign-off on total cost envelope.

**Output**: `docs/architecture/jamtrack-radio/architect-signoff.md`

**Gate**: All four views consistent. Total system cost accepted.

---

## Step 7 — Project Plan (`/project-plan`)

**Agent**: Project Manager (run `/project-manager` to activate)

**Product-level scope**: Create all GitHub milestones (one per phase). Document top-level issues per phase. Sprint-level issue breakdown is Feature Discovery's job.

**Output**: `docs/project-plan/jamtrack-radio-plan.md`, GitHub milestones

**Gate**: All milestones exist on GitHub, delivery narrative produced, handoff to Feature Discovery documented.

---

## After Step 7

**Product Discovery is complete.**

Proceed to **Feature Discovery** (`DISCOVERY.md`) for the first service. Recommended first service: **Identity Service** — all other services depend on authenticated users.

When starting Feature Discovery, the Architect should load `docs/architecture/jamtrack-radio/software-arch.md` as context so the feature-level design stays consistent with the system baseline.

---

## Output Paths Summary

| Step | Output path |
|------|-------------|
| `/requirements` | `docs/requirements/jamtrack-radio-requirements.md` |
| `/market-research` | `docs/market-research/jamtrack-radio-market-research.md` |
| `/prd` | `docs/prds/jamtrack-radio.md` |
| `/design-system` | `docs/design-system/jamtrack-radio-design-system.md`, `docs/design-system/components.html` |
| `/ui-prototype` | `docs/prototypes/jamtrack-radio/` |
| `/software-architect` | `docs/architecture/jamtrack-radio/software-arch.md` |
| `/cloud-architect` | `docs/architecture/jamtrack-radio/cloud-arch.md` |
| `/data-architect` | `docs/architecture/jamtrack-radio/data-arch.md` |
| `/arch-security` | `docs/architecture/jamtrack-radio/security-arch.md` |
| `/architect` | `docs/architecture/jamtrack-radio/architect-signoff.md` |
| `/project-plan` | `docs/project-plan/jamtrack-radio-plan.md` |
| ADRs | `docs/decisions/ADR-NNN-*.md` |
