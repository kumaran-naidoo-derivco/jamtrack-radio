# Jamtrack Radio — Git Workflow

This workflow is **cross-cutting** — it applies to every change in the project, regardless of which other workflow (DEVELOPMENT, DISCOVERY, MONITORING) the change originates from.

Use the `/raise-pr` skill to execute this workflow step-by-step.

---

## The Workflow

```
Sync main → Sub-task issue → Branch → Commit(s) → Push → PR → CI → Merge → Sync main
```

| Step | Action | Skill / Command |
|------|--------|----------------|
| 1 | Sync `main` | `git checkout main && git pull origin main` |
| 2 | Create sub-task GitHub issue linked to parent task | `gh issue create` |
| 3 | Create branch | `git checkout -b kumarann/<type>/<description>` |
| 4 | Make changes, commit with issue reference | `git commit -m "<type>: <subject> (#<issue>)"` |
| 5 | Push branch | `git push origin kumarann/<type>/<description>` |
| 6 | Open PR with `Closes #<issue>` in body | `gh pr create` |
| 7 | Wait for CI `build` check to pass | `gh pr checks <number>` |
| 8 | Squash merge, delete branch | `gh pr merge <number> --squash --delete-branch` |
| 9 | Sync `main` | `git checkout main && git pull origin main` |

See `/raise-pr` for the exact commands and body templates for each step.

---

## Issue Linking — How It Works

Every piece of work in Jamtrack Radio is tracked at two levels:

```
GitHub Milestone (Phase)
  └── Parent Task Issue  (e.g. "Task 2.4: Architecture — Steps 5a–5d")
        └── Sub-task Issue  (e.g. "Task 2.4a: Update arch skills for draw.io")
              └── Branch  →  Commit(s)  →  PR
```

| Link | How it's created | Effect |
|------|-----------------|--------|
| Sub-task → Parent | `Part of #<parent>` in sub-task issue body | GitHub shows a reference on the parent issue |
| Commit → Sub-task | `(#<issue>)` at end of commit subject | GitHub shows commit in the sub-task timeline |
| PR → Sub-task | `Closes #<issue>` in PR body | Sub-task auto-closes when PR is squash-merged |

This creates a traceable chain: **milestone → task → sub-task → PR → commit** — every change is fully attributable.

---

## Conventions

### Branch naming
```
kumarann/<type>/<short-description>
```
Examples:
- `kumarann/feat/identity-service-register`
- `kumarann/docs/update-architecture-readme`
- `kumarann/chore/update-arch-skills-drawio`

### Conventional Commits types

| Type | When to use |
|------|-------------|
| `feat` | New feature or behaviour |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `chore` | Maintenance, tooling, config, skills |
| `ci` | CI/CD pipeline changes |
| `refactor` | Code restructure, no behaviour change |
| `test` | Adding or updating tests |

### Sub-task issue title
```
Task X.Y: <description>          ← top-level task
Task X.Ya: <description>         ← first sub-task
Task X.Yb: <description>         ← second sub-task
```

### Commit subject
```
<type>: <imperative subject, ≤72 chars> (#<issue>)
```
Examples:
- `chore: add Azure symbols to cloud-architect skill (#68)`
- `feat: add register endpoint to Identity Service (#71)`

### PR title
Matches the commit subject of the primary commit (or the squash subject):
```
<type>: <subject>
```

---

## Rules

- **Never commit directly to `main`** — all changes go through a PR
- **Never merge a failing PR** — `build` CI check must be green
- **Every branch has an issue** — create the sub-task issue before the branch, not after
- **Stage specific files** — never `git add .` or `git add -A`
- **Squash merge** — keeps `main` history clean and linear

---

## Quick Reference

```bash
# 1. Sync
git checkout main && git pull origin main

# 2. Sub-task issue
gh issue create --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "Task X.Y: <description>" \
  --body $'Part of #<parent>\n\n## What\n...\n\n## Acceptance criteria\n- [ ] ...'

# 3. Branch
git checkout -b kumarann/<type>/<description>

# 4. Commit (repeat as needed)
git add <files>
git commit -m "<type>: <subject> (#<issue>)"

# 5. Push
git push origin kumarann/<type>/<description>

# 6. PR
gh pr create --repo kumaran-naidoo-derivco/jamtrack-radio \
  --base main --head kumarann/<type>/<description> \
  --title "<type>: <subject>" \
  --body "## Description\n...\n\n## Closes #<issue>\n\n..."

# 7. CI check
gh pr checks <number> --repo kumaran-naidoo-derivco/jamtrack-radio

# 8. Merge
gh pr merge <number> --repo kumaran-naidoo-derivco/jamtrack-radio --squash --delete-branch

# 9. Sync
git checkout main && git pull origin main
```
