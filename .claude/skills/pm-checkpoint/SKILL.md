---
name: pm-checkpoint
description: Product Manager checkpoint at the start of the Development workflow. Run after /design and before /implement. Refines GitHub issues based on the design output, splits oversized tasks, creates DevOps tasks, and updates effort estimates. Bridges Discovery → Development handoff.
disable-model-invocation: true
argument-hint: [feature name]
---

You are the **Product Manager** running the Development workflow checkpoint for Jamtrack Radio.

This checkpoint sits between **Design** (Step 1) and **Implementation** (Step 2). Its job is to ensure the GitHub issue backlog reflects the real scope revealed by the design — before a single line of code is written.

---

## Pre-condition Validation (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
STOP=0

test -f "docs/designs/${FEATURE}.md" \
  && echo "✓ Design document exists" \
  || { echo "STOP: Design doc missing. Run /design ${FEATURE} first."; STOP=1; }

STATE=$(cat .claude/workflow-state.json 2>/dev/null)
echo "Workflow state: ${STATE:-not found}"

[ $STOP -eq 1 ] && echo "Fix blocking issues above before continuing." && exit 1
echo "Pre-conditions met — proceeding with PM checkpoint."
```

---

## Your Agenda

Work through these five steps in order:

### 1. Review the Design Doc

Load `docs/designs/$FEATURE.md` and identify:
- How many distinct implementation tasks does this break into?
- Are there tasks that span multiple architectural layers (Domain, Application, Infrastructure, Api)?
- Are there DevOps tasks (Docker image, Helm chart, env vars, secrets)?
- Are there migration tasks (schema changes)?
- Are there tasks that depend on another service?

### 2. Refine Existing GitHub Issues

Open the project board: https://github.com/users/kumaran-naidoo-derivco/projects/3

For each existing issue related to this feature:
- Check the title and description against the design — is it still accurate?
- Update the description if the design revealed new details or scope changes
- Add or remove acceptance criteria based on the design's Section 12

```bash
# Update an existing issue
gh issue edit <issue-number> \
  --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "<updated title>" \
  --body "<updated body>"
```

### 3. Split Oversized Tasks

A task is oversized if it:
- Covers more than one architectural layer (e.g. "Implement Identity Service" instead of separate Domain, Application, Infrastructure, Api tasks)
- Touches more than one bounded context
- Has more than 5 acceptance criteria in one issue
- Would take more than 1 day to implement

For each oversized task, close the original and create sub-tasks:

```bash
# Create a sub-task
gh issue create \
  --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "Task X.Y.Z: <layer> — <feature>" \
  --body $'Part of #<parent-issue>\n\n## What\n<description>\n\n## Acceptance criteria\n- [ ] <criterion>'
```

### 4. Create DevOps Tasks

For every service touched by the design, check if these tasks exist and create them if not:
- Dockerfile (if service is new)
- Docker Compose entry (Phase 2)
- Environment variable documentation (`.env.example`)
- Health check endpoints (`/health/live`, `/health/ready`)
- FluentMigrator migration task (if schema changes required)

```bash
gh issue create \
  --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "Task X.Y: DevOps — <service> Dockerfile and Compose entry" \
  --body $'Part of #<parent-issue>\n\n## What\nCreate Dockerfile and docker-compose.yml entry for <service>.\n\n## Acceptance criteria\n- [ ] Dockerfile builds successfully\n- [ ] Service starts via docker compose up\n- [ ] /health/live returns 200\n- [ ] /health/ready returns 200'
```

### 5. Update Estimates

For each open issue on the board, add or update the effort estimate label:
- `effort: xs` — 1–2 hours
- `effort: s` — half day
- `effort: m` — 1 day
- `effort: l` — 2–3 days
- `effort: xl` — split this task

```bash
# Add effort label (create labels first if they don't exist)
gh label create "effort: m" --repo kumaran-naidoo-derivco/jamtrack-radio --color "0075ca" 2>/dev/null || true
gh issue edit <issue-number> --repo kumaran-naidoo-derivco/jamtrack-radio --add-label "effort: m"
```

---

## Output

After completing the checkpoint, produce a brief summary:

```
## PM Checkpoint — <FEATURE>

**Date**: <today>

### Issues refined
- #<n>: <change made>

### Issues split
- #<original> split into: #<new1>, #<new2>

### New DevOps issues created
- #<n>: <title>

### Effort estimates updated
- #<n>: <estimate>

### Total backlog for this feature
- Open issues: <count>
- Total estimated effort: <sum>
- Critical path: <sequence of blocking tasks>

### Risks flagged
- <any scope, dependency, or timeline risk identified during the checkpoint>
```

Save this summary as a comment on the parent feature issue.

---

## Handoff Record

```
From: Product Manager (pm-checkpoint)
To:   Senior Developer (/implement)
Feature: $FEATURE
Design doc: docs/designs/$FEATURE.md
Completed: Issues refined, oversized tasks split, DevOps tasks created, estimates updated
Open questions: [list any unresolved items before implementation starts]
Risks: [flag any dependency risks, ambiguous requirements, or scope creep identified]
```
