---
name: arch-diagram
description: Creates an architecture block diagram with numbered interaction flows for a system, feature, or service. Use when the user wants to visualise components and how they communicate.
disable-model-invocation: true
argument-hint: [system or feature name]
---

> **Ad-hoc diagrams only.** Use this skill for quick, standalone architecture diagrams when you don't need the full Discovery workflow.
>
> For structured Discovery, use the specialist architecture skills instead:
> - `/software-architect` — service context diagram, domain model, ADRs
> - `/cloud-architect` — cloud topology, TCO, resource sizing
> - `/data-architect` — ER diagram, schema ownership, data flows
> - `/arch-security` — trust boundaries, threat model, security controls
>
> Those skills save their outputs to `docs/architecture/<feature>/` and feed directly into subsequent workflow steps.

You are a software architect creating architecture documentation for the Jamtrack Radio project.

If $ARGUMENTS is provided, use it as the system/feature name and ask only for missing context. Otherwise, gather the following before producing output:

1. **System or feature name** — what are we diagramming?
2. **Components involved** — list the services, databases, queues, external systems, or clients
3. **Primary scenario** — what is the main interaction flow to document? (e.g. "user requests a track", "playlist sync")
4. **Direction preference** — top-down (default) or left-right layout?

---

## Output Format

> **Draw.io is the required diagramming tool for all architecture documents.**
> Save diagrams as `.drawio` files. Reference in markdown with a PNG export for inline preview.
> **Mermaid diagrams are reserved for the implementation phase only** (development workflow, inline code docs).

Produce the following in order:

### 1. Interaction Diagram

Produce a draw.io interaction diagram using the **Software + UML** shape libraries (`View → Shapes`). This is not a simple box-and-line flowchart — it uses typed symbols that convey the nature of each component and communication pattern.

**File**: `diagrams/<system-name>.drawio` (alongside `ARCHITECTURE.md`)

**Symbol conventions**:

| Element | Shape | Label convention |
|---------|-------|-----------------|
| Service / component | Rounded rectangle | `<<component>>` stereotype |
| External system | Rounded rectangle | `<<external>>`, grey fill |
| REST API surface | Rounded rectangle | `<<api>>` stereotype |
| gRPC service | Rounded rectangle | `<<gRPC>>` stereotype |
| Database (PostgreSQL) | Cylinder | Standard DB shape, purple fill |
| Cache (Redis) | Cylinder | `<<cache>>`, orange fill |
| Message queue / event bus | Queue/envelope shape | `<<async>>`, yellow fill |
| Event store | Cylinder | `<<event store>>`, yellow fill |
| Synchronous call | Solid arrow, filled arrowhead | Protocol label: `gRPC`, `REST`, `SQL` |
| Asynchronous event | Dashed arrow, open arrowhead | Event name label |
| Eventual consistency | Dashed arrow through queue shape | Annotate: `eventually consistent` |
| Bounded context / zone | Dashed rectangle container | Context or zone name as header |

**Cloud resources** (Phase 4+): use the **Microsoft Azure 2023** shape library and official Azure service names.

Embed in the markdown:
```
> **Diagram**: [<system-name>.drawio](diagrams/<system-name>.drawio)
> ![<System Name> Architecture](diagrams/<system-name>.png)
```

### 2. Component Inventory

A table listing each component, its role, and technology:

| # | Component | Role | Technology |
|---|-----------|------|------------|
| 1 | ... | ... | ... |

### 3. Interaction Flow

Describe the primary scenario as a numbered hierarchy. Group related steps under a parent number. Use the format:

**Scenario: [scenario name]**

1. **[Group name]**
   - 1.1. [First step — actor → component: action]
   - 1.2. [Next step]
2. **[Group name]**
   - 2.1. [Step]
   - 2.2. [Step]
   - 2.3. [Step]

Each step must state: **who initiates**, **what they send/request**, **which component receives it**, and **what it does next**. Keep each step to one sentence.

### 4. Key Design Decisions

Bullet list of 3–5 architectural choices visible in the diagram and why they were made (e.g. "gRPC used for internal service communication for performance and strong typing").

---

After producing the output, append it to `ARCHITECTURE.md` at the project root (next to `README.md` and `PRD-jamtrack-radio.md`). Use the following rules:

- If `ARCHITECTURE.md` does not exist, create it with a top-level heading `# Jamtrack Radio — Architecture` and a brief intro line, then append the diagram content.
- If `ARCHITECTURE.md` already exists, append the new diagram as a new named section using a `##` heading derived from the system/feature name. Do not overwrite existing content.

Then ask:
- Should additional scenarios be documented with their own interaction flows?
- Are there any components missing or incorrectly represented?
