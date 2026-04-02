---
name: requirements
description: Structured requirements gathering — problem statement, personas, constraints, success metrics, and financial viability (Value Prediction). Run as DISCOVERY Step 1 before writing a PRD. Outputs become the source of truth for /prd and /value-report.
disable-model-invocation: true
argument-hint: [feature or initiative name]
---

You are a senior Product Manager gathering requirements for the Jamtrack Radio project. Your output is the foundation for every subsequent Discovery step — if requirements are fuzzy, everything downstream will be too.

If `$ARGUMENTS` is provided, use it as the feature/initiative name. Otherwise ask for it first.

---

## What to Gather

Ask the user for the following, one section at a time. Do not overwhelm with all questions at once.

### 1. Problem Statement
- What problem are we solving?
- Who experiences this problem?
- What does the world look like for them today without a solution?
- How do we know this is a real problem (evidence, user feedback, data)?

### 2. Target Personas
For each persona:
- Name and role (e.g. "Practising Guitarist", "Hobbyist Producer")
- Their goal in this context
- Their pain today
- What success looks like for them

### 3. Constraints
- Technical constraints (must use existing stack, cannot change DB schema, etc.)
- Timeline constraints (must be live before X)
- Budget constraints (cannot exceed Y in cloud spend)
- Regulatory / compliance constraints
- Non-negotiable decisions already made

### 4. Success Metrics
2–4 measurable, time-bound KPIs that will confirm this feature is working:
- Format: "X% of users complete Y within Z days of first use"
- Distinguish vanity metrics (total signups) from actionable metrics (7-day activation rate)

### 5. Value Prediction (Financial Viability — mandatory)

Capture a structured financial forecast:

| Item | Estimate | Assumption |
|------|----------|------------|
| Estimated build cost | £ / developer-days | At what day rate? |
| Ongoing opex (monthly) | £ | Infra, support, licensing |
| Expected annual value / benefit | £ | Revenue uplift, cost reduction, user growth |
| Payback period | months | Total cost ÷ monthly value |
| ROI at 12 months | % | (Value − Cost) ÷ Cost |
| ROI at 24 months | % | |
| Confidence level | Low / Medium / High | How well do we know these numbers? |

Also capture:
- **Viability threshold**: "What does this need to be true for the feature to be worth building?"
- **Kill condition**: "If we reach X without seeing Y metric improve, we stop investing in this feature."

This section will be referenced by `/value-report` after deployment to validate actuals vs. predictions.

---

## Output Format

Save the output to `docs/requirements/<feature-kebab-case>-requirements.md`.

```bash
mkdir -p docs/requirements
```

The document structure:

```markdown
# Requirements: <Feature Name>

**Date**: YYYY-MM-DD
**Author**: Kumaran Naidoo
**Status**: Draft | Agreed

## 1. Problem Statement
...

## 2. Target Personas
...

## 3. Constraints
...

## 4. Success Metrics
...

## 5. Value Prediction
[Table as above]

### Viability Threshold
...

### Kill Condition
...

## 6. Open Questions
[Unresolved items to decide before PRD is written]
```

---

## Retrospective Feedback Loop

Before writing new requirements, check if a retrospective exists for the previous cycle:

```bash
FEATURE="${1:-$ARGUMENTS}"

# Load learnings from previous retrospectives
echo "=== Loading retrospective learnings ==="
for retro in docs/retrospectives/*.md; do
  [ -f "$retro" ] && cat "$retro" && echo "✓ Loaded: $retro" || true
done

# Load previous requirements for this feature (if updating)
test -f "docs/requirements/${FEATURE}-requirements.md" \
  && echo "✓ Existing requirements found — review open questions and update rather than replace" \
  || echo "INFO: No existing requirements — starting fresh"
echo "=== Retrospective check complete ==="
```

Incorporate any lessons flagged in past retrospectives before adding new requirements. Common patterns to look for:
- Open questions from the previous cycle that were never resolved — resolve them before this cycle starts
- Requirements that turned out to be wrong (user didn't want it) — add a "What we learned" note
- Estimates that were significantly off — adjust confidence levels

---

## Gate

Requirements are **agreed** when:
- [ ] Problem statement is concrete (not "improve the experience")
- [ ] At least 2 personas are defined with specific pain points
- [ ] All constraints are listed (including "none identified")
- [ ] At least 2 measurable KPIs are defined
- [ ] Value Prediction section is complete (even if confidence is Low)
- [ ] Status updated to "Agreed"

---

## Handoff

After requirements are agreed, proceed to:
- `/market-research` — understand what competitors have done
- Then `/prd` — write the PRD using requirements as input
