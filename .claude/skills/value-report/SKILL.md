---
name: value-report
description: Product value determination — compares predicted vs. actual value for a delivered feature. Loads the Value Prediction from /requirements, collects usage metrics, and produces a verdict. Run by the Product Manager weeks after deployment (not at deploy time).
disable-model-invocation: true
argument-hint: [feature name]
---

## Pre-condition Validation (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
STOP=0

test -f "docs/requirements/${FEATURE}-requirements.md" \
  && echo "✓ Requirements doc exists (Value Prediction source)" \
  || { echo "STOP: Requirements doc missing — no Value Prediction to compare against."; STOP=1; }

test -f "docs/prds/${FEATURE}.md" \
  && echo "✓ PRD exists (success metrics source)" \
  || { echo "STOP: PRD missing — no success metrics to evaluate."; STOP=1; }

# Check deployment is at least 14 days old
DEPLOY_DATE=$(cat .claude/workflow-state.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('lastUpdated','unknown'))" 2>/dev/null)
echo "Last workflow state update: ${DEPLOY_DATE}"
echo "WARN: Ensure at least 14 days have passed since deployment — run this too early and the data is meaningless."

STATE=$(cat .claude/workflow-state.json 2>/dev/null)
echo "Workflow state: ${STATE:-not found}"

[ $STOP -eq 1 ] && echo "Fix blocking issues above before continuing." && exit 1
echo "Pre-conditions met — proceeding with value report."
```

---

You are the Product Manager closing the value loop for a Jamtrack Radio feature. This report answers the most important question in product development: **Was this feature worth building?**

Run this skill 1–4 weeks after a feature is deployed to production — not immediately at deploy time. You need real usage data to validate the prediction.

If `$ARGUMENTS` is provided, use it as the feature name. Load context from:
- `docs/requirements/<feature>-requirements.md` — the original Value Prediction
- `docs/prds/<feature>.md` — the accepted business case and success metrics
- Latest monitoring report from `docs/monitoring-reports/`

---

## Required Data

Collect the following before writing the report:

### Usage metrics (from ELK / ClickHouse)
- Total API calls for the feature endpoints, since launch
- Daily active users using the feature (DAU)
- Retention: % of users who used the feature in week 1 who also used it in week 2
- Feature adoption rate: (users who used this feature) ÷ (total active users)

### Financial actuals
- Actual build cost: developer-days × day rate (from GitHub issue closure timestamps)
- Actual incremental infra cost (from Azure cost management, compared to pre-feature baseline)
- Actual support cost: bug reports, support tickets related to this feature

### Business outcome actuals
- Revenue impact (if any): new subscriptions, upgrades, or retention improvement attributed to this feature
- Cost savings (if any): support cost reduction, manual process automation
- User satisfaction signal: feedback, NPS, ratings, social mentions

---

## Report Structure

Save to `docs/value-reports/YYYY-MM-DD-<feature>.md`.

```bash
mkdir -p docs/value-reports
```

---

# Value Report: [Feature Name]

**Date**: YYYY-MM-DD (must be ≥ 2 weeks post-deployment)
**Feature deployed**: YYYY-MM-DD (PR #N)
**Author**: Kumaran Naidoo / Product Manager
**Status**: Draft | Final

---

## 1. Executive Summary

One paragraph: what was predicted, what actually happened, and the verdict in plain language.

---

## 2. Value Prediction vs. Actuals

| Item | Predicted | Actual | Variance | Notes |
|------|-----------|--------|----------|-------|
| Build cost | £X | £Y | +/-£Z | Reason for variance |
| Monthly opex | £X | £Y | +/-£Z | |
| Year 1 user adoption | N% | N% | | |
| Year 1 value / benefit | £X | £Y | | |
| Payback period | N months | N months | | |
| ROI at 12 months | N% | N% (projected) | | |

### Prediction accuracy

Rate each dimension: `Accurate` / `Optimistic` / `Pessimistic` / `Too Early to Tell`

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Build cost estimate | | |
| Usage/adoption | | |
| Business value | | |
| Technical risk | | |

---

## 3. KPI Actuals vs. Targets

Load the success metrics from `/requirements`. For each KPI:

| KPI | Target | Actual | Status |
|-----|--------|--------|--------|
| 7-day activation rate | 40% | 32% | ⚠️ Below target |
| Week-2 retention | 60% | 68% | ✅ Above target |
| Avg. sessions/week per user | 3 | 4.1 | ✅ Above target |

### Interpretation

What do these KPI actuals tell us? Is the feature delivering the intended behaviour? Are users engaging with it the way we predicted?

---

## 4. Unexpected Findings

Things we didn't predict in Discovery — positive or negative:

- Unexpected usage pattern: [e.g. "Users are using the loop feature far more than the BPM adjuster — suggests we should invest more in loop UX"]
- Unexpected cost: [e.g. "Stream event volume is 3× higher than predicted — ClickHouse schema needs partitioning sooner than planned"]
- Unexpected user need surfaced: [e.g. "5 support tickets requesting export to MIDI — not in scope but showing a real need"]

---

## 5. Viability Threshold Check

Load the viability threshold from `/requirements`:

> "[The viability threshold statement from requirements, e.g. 'This feature needs to drive a 15% increase in week-2 retention to justify the build cost']"

**Assessment**: [Met / Not Met / Partially Met]

**Evidence**: [Cite the specific KPI actuals that support this assessment]

---

## 6. Kill Condition Check

Load the kill condition from `/requirements`:

> "[The kill condition statement from requirements, e.g. 'If 7-day activation rate is below 20% at week 4, we stop investing in this feature']"

**Status**: [Triggered / Not Triggered / Too Early to Evaluate]

---

## 7. Verdict

**Was this feature worth building?**

Choose one:
- ✅ **Yes — validated** — actuals meet or exceed predictions. Continue investment.
- ⚠️ **Partially — iterate** — some value delivered but below prediction. Identify what to change.
- ❌ **No — pivot or stop** — actuals significantly below prediction. Document why and what to do instead.

**Justification**: [2–3 sentences explaining the verdict with evidence]

---

## 8. Recommendations for Next Iteration

What should change in the next Discovery cycle based on this evidence?

1. **Invest more in**: [Feature area or user need that showed higher-than-expected value]
2. **Invest less in**: [Feature area that showed lower-than-expected engagement]
3. **Investigate before building**: [Unanswered question that this data surfaces]

---

## Strategic Lens

**Why this matters**
- Most product teams never measure whether features delivered their predicted value. This is how feature factories are born.
- A feature that cost £20k to build but delivers £5k/year in value is a liability, not an asset. You need to know this.
- Evidence from value reports is the strongest argument for (or against) a feature investment in the next roadmap cycle.

**Common value measurement pitfalls**
- *Attribution errors*: a KPI improved after the feature launched — but would it have improved anyway? Consider control groups or holdout experiments.
- *Survivorship bias*: measuring DAU excludes users who churned because of the feature. Look at both activation and churn.
- *Vanity metric focus*: "10,000 feature uses" is meaningless without knowing how many users tried it once and never returned.
- *Too early*: some features take weeks to become habitual. A 7-day measurement of a weekly-use feature tells you little.

**Evidence-based product development**
- *Continuous discovery* (Teresa Torres): every sprint, talk to users. Validate assumptions before investing in features.
- *Amazon's "working backwards"*: the press release exercise in `/requirements` forces you to state the value before building. The value report tests whether that press release came true.
- *Lean Startup's Build-Measure-Learn loop*: this skill is the "Learn" step. It only works if the "Measure" (KPIs) was set up correctly in Discovery.
