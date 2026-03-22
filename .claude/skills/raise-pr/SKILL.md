---
name: raise-pr
description: Executes the mandatory Jamtrack Radio git workflow — create a GitHub sub-task issue linked to the parent task, branch, commit with issue reference, push, and open a PR with Closes #<issue>. Use for every change, no matter how small.
disable-model-invocation: true
argument-hint: [parent issue number and brief description of the work]
---

You are executing the mandatory Jamtrack Radio git workflow. Every change — no matter how small — must go through: sub-task issue → branch → commit → PR → CI → merge.

If `$ARGUMENTS` is provided, use it as context for the issue title and parent issue number.

---

## Step 1 — Sync main

Ensure local main is up to date before creating any branch:

```bash
git checkout main && git pull origin main
```

---

## Step 2 — Create a sub-task GitHub issue

Every branch must trace back to a GitHub issue. Create the sub-task now, linking it to the parent task issue.

```bash
gh issue create --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "Task X.Y: <brief description>" \
  --body $'Part of #<parent-issue-number>\n\n## What\n<one paragraph describing the work>\n\n## Acceptance criteria\n- [ ] <criterion 1>\n- [ ] <criterion 2>'
```

Note the issue number returned (e.g. `#68`). Use it in every subsequent step.

**Title convention**: `Task X.Y: <description>` — align with the current phase and task number. Sub-tasks use a letter suffix: `Task 2.4a`, `Task 2.4b`, etc.

**Body convention**:
- `Part of #<parent>` — links this sub-task to the parent task issue on GitHub
- `## What` — one paragraph describing the scope
- `## Acceptance criteria` — bullet list of testable conditions that define done

---

## Step 3 — Create a branch

```bash
git checkout -b kumarann/<type>/<description>
```

Branch naming: `kumarann/<type>/<description>` where `<type>` is the Conventional Commits prefix (`feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`).

---

## Step 4 — Make changes and commit

Stage specific files by name — never `git add .` or `git add -A`.

Every commit message must include the issue number at the end of the subject line:

```bash
git add <specific-file-1> <specific-file-2>
git commit -m "<type>: <subject> (#<issue>)"
```

For multi-commit branches, every commit must carry the issue reference. The final squash commit on `main` (produced by `gh pr merge --squash`) will also carry it.

---

## Step 5 — Push the branch

```bash
git push origin kumarann/<type>/<description>
```

---

## Step 6 — Create the PR

Use `Closes #<issue>` in the PR body to auto-close the sub-task when the PR merges. Fill in all checklist items and select the correct type of change:

```bash
gh pr create --repo kumaran-naidoo-derivco/jamtrack-radio \
  --base main \
  --head kumarann/<type>/<description> \
  --title "<type>: <subject>" \
  --body "$(cat <<'EOF'
## Description

<What does this PR do and why?>

## Closes #<issue>

## Type of change

- [ ] `feat` — new feature
- [ ] `fix` — bug fix
- [ ] `docs` — documentation only
- [ ] `chore` — maintenance / tooling / config
- [ ] `ci` — CI/CD pipeline changes
- [ ] `refactor` — code restructure, no behaviour change
- [ ] `test` — adding or updating tests

## Checklist

- [ ] Branch is up to date with `main`
- [ ] Commit message follows Conventional Commits and includes issue number (`#<issue>`)
- [ ] Issue is linked above (`Closes #`)
- [ ] Self-reviewed — code does what it says, no debug artifacts left in
EOF
)"
```

---

## Step 7 — Wait for CI

```bash
gh pr checks <pr-number> --repo kumaran-naidoo-derivco/jamtrack-radio
```

The `build` check must be green. Do not merge a failing PR. If CI fails, fix the issue on the same branch, push again, and re-check.

---

## Step 8 — Merge the PR

Squash merge. Delete the branch on merge.

```bash
gh pr merge <pr-number> --repo kumaran-naidoo-derivco/jamtrack-radio --squash --delete-branch
```

---

## Step 9 — Sync local main

```bash
git checkout main && git pull origin main
```

---

## Conventions

| Convention | Rule |
|------------|------|
| Commit format | `<type>: <subject> (#<issue>)` — issue number mandatory |
| PR body | Must contain `Closes #<issue>` to auto-close sub-task on merge |
| Sub-task body | Must contain `Part of #<parent>` to link to parent task issue |
| Branch naming | `kumarann/<type>/<description>` |
| Staging | Specific files only — never `git add .` or `git add -A` |
| Merge strategy | Squash merge preferred — keeps main history clean |
| CI gate | `build` check must be green before any merge |
