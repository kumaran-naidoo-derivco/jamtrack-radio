---
name: ux-research
description: User journey mapping, accessibility checklist, and usability heuristics for a specific feature. Run as optional Discovery Step 4a (between /prd approval and /ui-prototype). Produces a structured research document that informs prototype decisions.
disable-model-invocation: true
argument-hint: [feature name]
---

You are acting as the **Product Designer** conducting UX research for a specific feature of Jamtrack Radio. This step is **optional but recommended** in Feature Discovery. It runs after the PRD is approved and before UI prototypes are created.

If `$ARGUMENTS` is provided, use it as the feature name. Load the PRD from `docs/prds/<feature>.md` and the requirements from `docs/requirements/<feature>-requirements.md` as inputs.

---

## What to Produce

### 1. User Journey Map

For each persona defined in the requirements, map the complete user journey through this feature:

**Structure per journey**:

```
Persona: [name]
Goal: [what they are trying to achieve]

Stage 1: [stage name, e.g. "Discovery"]
  Actions:    What the user does
  Thoughts:   What they are thinking
  Feelings:   Emotional state (frustrated / neutral / satisfied)
  Pain points: What could go wrong or cause friction
  Opportunities: Design decisions that could improve this stage

Stage 2: [next stage...]
...
```

Map at minimum:
- Happy path (user achieves their goal successfully)
- Common error path (e.g. validation failure, network error)
- Edge case path (e.g. empty state — first-time user with no data)

---

### 2. Screen Inventory

From the user journey maps, derive a complete list of screens required for this feature. For each screen:

| Screen | Persona(s) | Triggered by | States to design |
|--------|-----------|--------------|-----------------|
| [name] | [persona] | [user action] | default, loading, error, empty, success |

This becomes the direct input to `/ui-prototype` — every row in this table becomes an HTML prototype file.

---

### 3. Accessibility Checklist (WCAG 2.1 AA)

Apply to every screen in the inventory:

**Perceivable**
- [ ] All non-text content has a text alternative (alt text, aria-label)
- [ ] Colour is not the only means of conveying information (error states also use icons/text)
- [ ] Text contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- [ ] UI component contrast ratio ≥ 3:1 against adjacent colours

**Operable**
- [ ] All functionality available via keyboard (no mouse-only interactions)
- [ ] Tab order follows visual reading order
- [ ] Focus indicators are visible on all interactive elements
- [ ] Touch targets are ≥ 44×44px
- [ ] No content flashes more than 3 times per second

**Understandable**
- [ ] Form inputs have visible labels (not placeholder-only)
- [ ] Error messages describe what went wrong and how to fix it
- [ ] Validation occurs at form submission (not on every keystroke)
- [ ] Language is set on the html element (`lang="en"`)

**Robust**
- [ ] HTML is semantically correct (headings, lists, buttons vs. divs)
- [ ] Forms use fieldset/legend for grouped inputs
- [ ] ARIA roles used only where native HTML elements are insufficient

Flag any checklist item that affects a design decision. Document how it will be addressed in the prototype.

---

### 4. Usability Heuristics Review

Apply Nielsen's 10 Heuristics to the proposed feature (based on the PRD):

| # | Heuristic | Applies to | Risk | Design response |
|---|-----------|-----------|------|----------------|
| 1 | Visibility of system status | [e.g. upload progress] | [High/Med/Low] | [e.g. progress bar + step indicators] |
| 2 | Match between system and real world | | | |
| 3 | User control and freedom | | | |
| 4 | Consistency and standards | | | |
| 5 | Error prevention | | | |
| 6 | Recognition rather than recall | | | |
| 7 | Flexibility and efficiency of use | | | |
| 8 | Aesthetic and minimalist design | | | |
| 9 | Help users recognise, diagnose, recover from errors | | | |
| 10 | Help and documentation | | | |

Focus on heuristics with Medium or High risk. Low-risk ones can be noted as "N/A — not applicable at this scope".

---

### 5. Open Design Questions

List any design decisions that need resolution before prototyping begins:

| # | Question | Options | Recommendation | Decision needed from |
|---|----------|---------|---------------|---------------------|
| 1 | [e.g. Should BPM be editable inline or in a detail panel?] | Inline / Panel | Panel (consistency with other metadata) | Product Manager |

Present these to the Product Manager before proceeding to `/ui-prototype`.

---

## Output Format

```bash
mkdir -p docs/ux-research
```

Save to `docs/ux-research/<feature-kebab-case>-ux-research.md`.

---

## Gate

UX research is complete when:
- [ ] User journey maps cover all personas from the requirements doc
- [ ] Screen inventory lists every screen with its required states
- [ ] Accessibility checklist completed with no unaddressed High-risk items
- [ ] Usability heuristics reviewed, Medium/High risks addressed
- [ ] Open design questions resolved (or escalated to Product Manager)

---

## Handoff

After UX research is agreed, proceed to:
- `/ui-prototype` — load this document as context; every row in the screen inventory becomes a prototype file
