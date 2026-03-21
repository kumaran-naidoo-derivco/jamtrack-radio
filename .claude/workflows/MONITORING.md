# Jamtrack Radio — Monitoring Workflow

This workflow runs **after every deployment** — staging or production. It verifies that the deployment is healthy, quantifies any regressions, produces an audit report, and closes the lifecycle loop with a retrospective.

After completing Step 5 (retrospective), notify the Product Manager that the value report can be run once sufficient usage data is available (typically 1–4 weeks post-deployment).

---

## Pre-flight Checklist

Before starting MONITORING, verify:

- [ ] DEVELOPMENT.md all 8 steps complete:
  - [ ] `/design` approved
  - [ ] `/implement` merged to `main`
  - [ ] Quality pass (`/robust`, `/security`) resolved
  - [ ] `/review` approved and PR merged
  - [ ] `/test` — all integration tests passing in CI
  - [ ] `/deploy-staging` successful — service healthy
  - [ ] `/integration-test` — all flows green against staging
  - [ ] `/deploy-prod` completed (or explicitly skipped for Phase 2 local-only)
- [ ] Baseline metrics recorded pre-deployment:
  - [ ] Error rate (errors/hour, by service)
  - [ ] p99 latency (by service and endpoint)
- [ ] Deployment timestamp noted
- [ ] PR number noted
- [ ] Previous image tag noted (rollback reference)

---

## The Workflow

```
Health Check → Error Analysis → Performance Analysis → Report → Retrospective → [Value Report, later]
```

| Step | Skill | Agent | Gate to pass before moving on |
|------|-------|-------|-------------------------------|
| 1 | `/monitor-health` | DevOps Engineer | All health endpoints 200, zero pod restarts |
| 2 | `/monitor-errors` | DevOps Engineer | Error rate within 5% of pre-deploy baseline |
| 3 | `/monitor-performance` | DevOps Engineer | p99 latency within 20% of baseline |
| 4 | `/monitor-report` | DevOps Engineer | HTML report saved to `docs/monitoring-reports/` |
| 5 | `/retrospective` | DevOps Engineer / Senior Developer | Lessons captured, action items logged as GitHub issues |
| 6 | `/value-report` | **Product Manager** | Value determination completed — predicted vs. actual documented |

> **Note on Step 6**: `/value-report` is NOT run immediately at deploy time. It requires 1–4 weeks of real usage data. The Product Manager runs it when sufficient data is available. Steps 1–5 should be completed within the first hour after deployment.

To start, run `/devops-engineer` to activate the DevOps Engineer agent persona.

---

## Step 1 — Health Check (`/monitor-health`)

**Agent**: DevOps Engineer

**Purpose**: Verify all health endpoints are responding, no pods are in restart loops, and database migrations ran successfully.

**Phase 2 (Docker Compose)**: Check all container health statuses and `curl` each `/health/live` and `/health/ready` endpoint.

**Phase 3+ (K8s)**: Check pod status, restart count, events, and migration job status.

**Phase 4+ (Azure)**: Add AKS node health and Application Gateway health to the checks.

**Gate**: All endpoints return HTTP 200. Zero pod restarts. Migration logs show success.

**If gate fails**: **Stop. Roll back immediately.** Do not proceed to Step 2.

---

## Step 2 — Error Analysis (`/monitor-errors`)

**Agent**: DevOps Engineer

**Purpose**: Compare error rate before and after deployment. Identify any new error types introduced.

**Phase 2**: Analyse Docker container logs (grep for `"level":"Error"` in Serilog JSON output).

**Phase 4+ (ELK)**: KQL queries in Kibana against the `jamtrack-*` index.

**Phase 4+ (ClickHouse)**: SQL queries comparing error counts in the pre-deploy and post-deploy windows.

**Gate**: Error rate within 5% of pre-deploy baseline.

**If gate fails (>20% increase)**: Investigate immediately. Consider rollback.

---

## Step 3 — Performance Analysis (`/monitor-performance`)

**Agent**: DevOps Engineer

**Purpose**: Compare p50/p95/p99 latency before and after deployment by service and endpoint.

**Phase 2**: Extract `ElapsedMilliseconds` from Serilog JSON logs.

**Phase 4+ (ClickHouse)**: `quantile(0.99)(elapsed_ms)` queries comparing pre-deploy and post-deploy windows.

**Gate**: p99 latency within 20% of pre-deploy baseline.

**If gate fails (>50% increase)**: Investigate immediately. Consider rollback.

---

## Step 4 — Monitoring Report (`/monitor-report`)

**Agent**: DevOps Engineer

**Purpose**: Aggregate all health, error, and performance results into a standalone HTML report. This is the permanent audit record of the deployment's monitoring outcome.

**Output**: `docs/monitoring-reports/YYYY-MM-DD-PR<N>-<service>.html`

**Gate**: Report saved. All three monitoring sections populated. Overall verdict stated.

---

## Step 5 — Retrospective (`/retrospective`)

**Agent**: DevOps Engineer / Senior Developer (collaborative)

**Purpose**: Structured post-deployment retrospective. What worked, what didn't, performance trends, lessons learned, and concrete action items.

**Output**: `docs/retrospectives/YYYY-MM-DD-<feature>-retro.md` + GitHub issues for High priority actions.

**Gate**: All 7 retrospective sections complete. Action items created as GitHub issues.

---

## Step 6 — Value Report (`/value-report`) — DELAYED

**Agent**: Product Manager

**Purpose**: Compare the Value Prediction (from `/requirements` in Discovery) against actual usage data, costs, and business outcomes. Determine whether the feature delivered its predicted value.

**Output**: `docs/value-reports/YYYY-MM-DD-<feature>.md`

**When to run**: 1–4 weeks after deployment — when you have real usage data.

**Gate**: All KPI actuals collected, verdict documented, recommendations for next iteration written.

---

## Rollback Procedures

### Phase 2 (Docker Compose)
```bash
# Stop current stack
docker compose down

# Roll back to previous image tag (update docker-compose.yml image tags)
git checkout <previous-tag> -- docker-compose.yml

# Start with previous version
docker compose up -d

# Verify health
curl http://localhost:5001/health/ready
```

### Phase 3 (K8s / Helm)
```bash
# List revision history
helm history <release-name> -n jamtrack-staging

# Roll back one revision
helm rollback <release-name> -n jamtrack-staging

# Verify rollback
kubectl rollout status deployment/<service> -n jamtrack-staging
```

### Phase 4+ (Azure AKS)
```bash
# Same Helm rollback, pointing at AKS cluster
kubectl config use-context aks-jamtrack-prod
helm rollback <release-name> -n jamtrack-prod
kubectl rollout status deployment/<service> -n jamtrack-prod
```

---

## docs/ Directory Convention

| Directory | Created by |
|-----------|-----------|
| `docs/monitoring-reports/` | `/monitor-report` (YYYY-MM-DD-PR<N>-<service>.html) |
| `docs/retrospectives/` | `/retrospective` (YYYY-MM-DD-<feature>-retro.md) |
| `docs/value-reports/` | `/value-report` (YYYY-MM-DD-<feature>.md) |

---

## Next-Cycle Discovery — Additional Pre-flight

When starting a new DISCOVERY cycle for a new feature or phase, add these checks:

- [ ] Previous MONITORING cycle complete (Steps 1–5 done, or waived for first-ever feature with reason)
- [ ] `/retrospective` from last cycle reviewed
- [ ] Action items from retrospective logged as GitHub issues
- [ ] Phase task file (`project-tasks/Phase-N.md`) updated with completed task status
- [ ] `/value-report` planned (even if not run yet)
