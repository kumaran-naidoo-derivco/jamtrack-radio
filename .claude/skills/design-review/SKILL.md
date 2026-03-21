---
name: design-review
description: Ad-hoc post-implementation design review. Compares rendered screens against Discovery prototypes, checks for UX regressions, and produces an accessibility audit. UI-only — do not run for backend-only services. Run after /deploy-staging when there are user-facing screens to review.
disable-model-invocation: true
argument-hint: [feature name]
---

You are acting as the **Product Designer** conducting a post-implementation design review for a specific feature of Jamtrack Radio.

This skill is **ad-hoc and optional** — run it after a feature is deployed to staging, but only when the feature has user-facing screens. Do not run for backend-only services (Identity gRPC, Track gRPC, etc. have no screens to review).

If `$ARGUMENTS` is provided, use it as the feature name. Load the prototypes from `docs/prototypes/<feature>/` and the UX research (if it exists) from `docs/ux-research/<feature>-ux-research.md` as the baseline to review against.

---

## What to Produce

### 1. Screen-by-Screen Comparison

For each prototype screen in `docs/prototypes/<feature>/`, compare the prototype against the deployed staging implementation:

| Screen | Prototype file | Deployed URL | Status | Findings |
|--------|---------------|-------------|--------|---------|
| [name] | `01-welcome.html` | `https://staging/.../` | ✅ Match / ⚠️ Minor drift / ❌ Regression | [notes] |

**Status definitions**:
- ✅ **Match** — implemented screen is consistent with prototype in layout, content, and interaction
- ⚠️ **Minor drift** — small differences (spacing, label wording) that don't affect UX — acceptable
- ❌ **Regression** — layout broken, key element missing, wrong interaction pattern, or accessibility failure — must be fixed before deploy-prod

For every ❌ regression, document:
- **What was expected** (describe or screenshot the prototype)
- **What was found** (describe the actual implementation)
- **Severity**: Critical (blocks user goal) / High (degrades UX significantly) / Medium (minor UX issue)
- **Recommended fix**: specific change needed
- **GitHub issue**: create a tracking issue and record the link

---

### 2. Interaction Review

Check that all interactive states are implemented:

| Element | States to check | Status |
|---------|----------------|--------|
| All buttons | Default, hover, focus, disabled, loading | |
| All form inputs | Default, focus, error, disabled | |
| Error messages | Inline validation, submit-time errors | |
| Empty states | First-time user with no data | |
| Loading states | Skeleton or spinner while data loads | |
| Confirmation dialogs | Destructive actions (delete, sign out) | |

---

### 3. Accessibility Spot-Check

For each screen, manually check (or note for developer to check):

| Check | Method | Status | Notes |
|-------|--------|--------|-------|
| Keyboard navigation — tab through all interactive elements | Keyboard only | | |
| Focus indicators visible on all interactive elements | Visual inspection | | |
| Colour contrast — text on background | Browser DevTools / axe | | |
| All images / icons used as controls have accessible labels | DevTools accessibility tree | | |
| Form inputs have visible labels (not placeholder-only) | Visual inspection | | |
| Error messages are descriptive | Trigger an error, read the message | | |
| Page title is meaningful | `<title>` element in browser tab | | |

---

### 4. Design System Compliance

Verify that the implementation uses the design system tokens from `docs/design-system/jamtrack-radio-design-system.md`:

| Token category | Compliant | Deviations |
|---------------|-----------|-----------|
| Colours | | |
| Typography | | |
| Spacing | | |
| Border radius | | |
| Component styles | | |

Any deviation from the design system must either be corrected or (if justified) trigger an update to the design system document.

---

### 5. Summary and Verdict

**Overall status**: ✅ Approved / ⚠️ Approved with minor notes / ❌ Blocked — regressions must be fixed

**Critical issues** (must fix before deploy-prod):
1. [list]

**Minor notes** (should fix, not blocking):
1. [list]

**Design system updates needed** (update `docs/design-system/` after merging):
1. [list]

---

## Output Format

```bash
mkdir -p docs/design-reviews
```

Save to `docs/design-reviews/YYYY-MM-DD-<feature>-design-review.md`.

If any ❌ regressions are found, create GitHub issues for them:
```bash
gh issue create --repo kumaran-naidoo-derivco/jamtrack-radio \
  --title "design: [description of regression]" \
  --label "bug,ux" \
  --body "..."
```

---

## Gate

Design review is complete when:
- [ ] All prototype screens compared against staging
- [ ] All ❌ regressions have GitHub issues created
- [ ] All interactive states checked
- [ ] Accessibility spot-check completed
- [ ] Design system compliance checked
- [ ] Overall verdict documented

If the verdict is ❌ Blocked, the feature must not proceed to `/deploy-prod` until critical issues are resolved and a follow-up review is passed.
