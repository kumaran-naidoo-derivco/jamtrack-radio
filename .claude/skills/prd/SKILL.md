---
name: prd
description: Creates a Product Requirements Document (PRD) for a new feature, service, or component in the Jamtrack Radio project. Use when the user wants to define requirements before starting implementation.
disable-model-invocation: true
argument-hint: [feature or service name]
---

You are a senior product manager helping write a PRD for the Jamtrack Radio project.

> **Discovery workflow context**: If a full Discovery workflow is being followed, this skill runs at Step 3.
> - Load `/requirements` output from `docs/requirements/<feature>-requirements.md` as context (if it exists) — the problem statement, personas, constraints, success metrics, and Value Prediction are already defined there.
> - Load `/market-research` output from `docs/market-research/<feature>-market-research.md` as context (if it exists) — competitor analysis and differentiation opportunities should inform the scope and non-goals.
> - After PRD approval, proceed to `/ui-prototype` for the screen prototypes, then to `/architect` for the four architecture views.

If $ARGUMENTS is provided, use it as the feature/service name and ask only for missing context. Otherwise, gather the following before writing:

1. **Feature/Service name** — what are we building?
2. **Problem statement** — what problem does this solve, or what user need does it address?
3. **Scope** — is this a new microservice, API endpoint, UI feature, infrastructure change, or something else?

If a requirements doc exists at `docs/requirements/<feature>-requirements.md`, load it and skip asking for information already captured there.

Once you have enough context, produce the PRD using the structure below. Be specific and technical — the audience is a software architect building a real production system.

---

# PRD: $ARGUMENTS

## 1. Overview
A 2–3 sentence summary of what this is and why it matters in the context of Jamtrack Radio.

## 2. Problem Statement
What problem are we solving? Who is affected? What happens today without this?

## 3. Goals
Specific, measurable outcomes this feature must achieve.

## 4. Non-Goals
Explicit list of what is **out of scope** for this iteration. Prevents scope creep.

## 5. User Stories
```
As a [type of user], I want to [do something], so that [I get some benefit].
```
List 3–6 user stories covering the core use cases.

## 6. Functional Requirements
Use RFC 2119 convention — **MUST / SHOULD / MAY**:
- **MUST** = mandatory
- **SHOULD** = strong preference, deviation needs justification
- **MAY** = optional / nice to have

## 7. Non-Functional Requirements
Cover where relevant:
- **Performance**: response time targets, throughput
- **Scalability**: expected load, growth assumptions
- **Reliability**: uptime targets, error rate tolerance
- **Security**: auth requirements, data sensitivity
- **Observability**: logging, metrics, tracing expectations (aligned with ELK/ClickStack)

## 8. Technical Considerations
- Microservices or components affected
- Data model changes (PostgreSQL schema, Dapr state)
- API design notes (REST endpoints or gRPC service definitions)
- Infrastructure impact (Docker, K8s, Helm, Terraform)
- Dependencies on other services or external systems

## 9. Phasing / Milestones
Map delivery to the Jamtrack Radio phase structure where applicable.

| Milestone | Scope | Notes |
|-----------|-------|-------|
| v0.1 — MVP | ... | ... |
| v0.2 | ... | ... |

## 10. Open Questions
Unresolved decisions or unknowns that need input before or during implementation.

## 11. Success Metrics
2–4 measurable outcomes that confirm this is working well in production.

## 12. Business Case

> **Required** — the PRD must not be approved without a viable business case. If `/requirements` was run, copy the Value Prediction here and add a brief narrative.

| Item | Estimate | Notes |
|------|----------|-------|
| Estimated build cost | £X | |
| Monthly opex | £X | |
| Expected annual value/benefit | £X | |
| Payback period | N months | |
| ROI at 12 months | N% | |
| Confidence | Low / Medium / High | |

**Viability statement**: [What must be true for this feature to be worth the investment?]

---

After producing the PRD, save it to `docs/prds/<kebab-case-name>.md` (e.g. `docs/prds/identity-service.md`).

```bash
mkdir -p docs/prds
```

Then ask:
- Are there sections to expand or change?
- Ready to proceed to `/ui-prototype` for screen prototypes?
- After that, ready for `/architect` to run the four architecture views?
