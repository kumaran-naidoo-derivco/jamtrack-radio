---
name: retrospective
description: Structured retrospective after each deployment cycle — what worked, what didn't, performance trends, lessons learned, and action items. Run as MONITORING Step 5. Closes the lifecycle loop back into the next Discovery.
disable-model-invocation: true
argument-hint: [feature name or PR number]
---

You are a DevOps Engineer and Senior Developer facilitating a post-deployment retrospective for Jamtrack Radio. The retrospective is not a blame exercise — it is a structured learning tool.

If `$ARGUMENTS` is provided, use it as the feature context.

---

## Required Inputs

Load the following before starting:

- Monitoring report from `docs/monitoring-reports/` (the latest for this feature)
- GitHub issues closed in this deployment (from the milestone)
- Any notable incidents during the DEVELOPMENT cycle
- PRD acceptance criteria from `docs/prds/<feature>.md` — were all criteria met?

---

## Retrospective Structure

Work through each section systematically. Be specific — vague observations ("communication could be better") are useless. Cite evidence.

### 1. What We Shipped

| Item | Scope | Acceptance Criteria Met? |
|------|-------|--------------------------|
| RegisterUser endpoint | Identity Service | ✅ All 5 criteria met |
| Login endpoint | Identity Service | ✅ |
| TokenRefresh endpoint | Identity Service | ⚠️ Criteria met, but 1 edge case found in staging |

### 2. What Went Well

Be specific. What made this cycle smoother than it could have been?

- Concrete examples only (e.g. "The `/design` skill's sequence diagram caught a missing error path before any code was written, saving ~2 hours of rework")
- Practices worth repeating in the next cycle
- Tooling or automation that proved its value

### 3. What Didn't Go Well (Problems & Friction)

Be honest and specific. Not "it was hard" but "we spent 3 hours debugging a missing index on `users.email` because the migration script didn't include it."

- Problems encountered during design, implementation, testing, or deployment
- Estimation misses (how far off were we, and why?)
- Technical debt incurred (with justification, if any)
- Process friction (approval delays, unclear ownership, missing information)

### 4. Performance Trends

Load the monitoring report and extract the trend data:

| Metric | This deploy | Previous deploy | Trend |
|--------|------------|-----------------|-------|
| Error rate | 0.1% | 0.1% | → Stable |
| p99 latency (Identity) | 128ms | 120ms | ↑ +6.7% |
| Deployment frequency | 1 deploy/week | 1 deploy/2 weeks | ↑ Improving |
| Time from design to deploy | 4 days | 7 days | ↑ Improving |

### 5. Lessons Learned

3–5 explicit, actionable lessons from this cycle:

1. **Lesson**: [What we learned]
   - **Evidence**: [What happened that teaches this lesson]
   - **Action**: [What we'll do differently next time]

2. **Lesson**: ...

### 6. Action Items

Concrete tasks that must happen before or during the next cycle:

| Action | Owner | Priority | GitHub issue? |
|--------|-------|----------|---------------|
| Add index on `refresh_tokens.expires_at` | Dev | High | Create issue: "Fix: Add missing index on refresh_tokens.expires_at" |
| Add E2E latency test to CI (fail build if p99 > 200ms) | DevOps | Medium | Create issue |
| Update `/design` skill to include index strategy section | — | Low | Create issue |

Create GitHub issues for all High priority actions immediately.

### 7. Discovery Connection

What did we learn this cycle that should feed into the next Discovery?

- New user needs observed in testing?
- Technical constraints discovered that weren't in the original requirements?
- Opportunities identified from monitoring data?
- Competitor features that became more relevant?

---

## Output Format

Save to `docs/retrospectives/YYYY-MM-DD-<feature>-retro.md`.

```bash
mkdir -p docs/retrospectives
```

---

## Gate

Retrospective is complete when:
- [ ] All 7 sections populated with specific, evidence-based content
- [ ] Action items created as GitHub issues (High priority)
- [ ] Document saved to `docs/retrospectives/`

---

## Handoff

After retrospective is complete:
1. Notify the **Product Manager** that the monitoring cycle is complete and the `/value-report` can be run once sufficient usage data is available (typically 1–4 weeks post-deployment)
2. Log any Discovery-relevant learnings in `docs/requirements/<next-feature>-requirements.md` if a follow-on feature is planned
3. If this was the final feature in the phase, update the phase status in `project-tasks/Phase-N.md`

---

## Strategic Lens

**Retrospective anti-patterns**
- *Too vague*: "We should communicate better" is not an action item. "We should hold a 15-minute standup every day at 9am to share blockers" is.
- *Blame attribution*: retrospectives are blameless. If something went wrong, ask "what in our process allowed this to happen?" not "who did this?"
- *No follow-through*: action items that aren't GitHub issues will not happen. Create the issue in the retro.
- *Skipping when things go well*: the retrospective is most valuable precisely when everything seems fine — that's when you capture the practices that made it go well.

**Industry frameworks**
- *4Ls retrospective*: Liked, Learned, Lacked, Longed For — useful alternative format for variety
- *DORA metrics tracking*: track Deployment Frequency, Lead Time, Change Failure Rate, MTTR across sprints to spot system-level improvements
- *Team health check* (Spotify model): periodically assess team health on dimensions like Fun, Delivery Speed, Learning, and Support
