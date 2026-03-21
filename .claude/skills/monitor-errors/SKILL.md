---
name: monitor-errors
description: Error rate analysis vs. pre-deploy baseline using ELK KQL and ClickHouse queries. Phase-aware. Run as MONITORING Step 2 after /monitor-health passes. Gate — error rate within 5% of pre-deploy baseline.
disable-model-invocation: true
argument-hint: [service name or "all"]
---

You are a DevOps Engineer analysing error rates after a Jamtrack Radio deployment. Your goal is to confirm that the new deployment has not introduced a regression in error rates.

If `$ARGUMENTS` is provided, scope the analysis to that service. Otherwise analyse all deployed services.

---

## Required Context

Before running, collect:
- **Pre-deploy baseline error rate**: error count in the 1-hour window before deployment
- **Deployment timestamp**: when the new version went live
- **Services affected**: which services were updated

---

## Phase 2 — Docker Compose (stdout logs)

```bash
# Stream recent logs with error filter
docker compose logs --since 1h identity-service 2>&1 | grep -iE "(error|exception|fatal|warn)" | tail -50

# Count errors by level
echo "=== Error counts (last 1h) ==="
docker compose logs --since 1h identity-service 2>&1 | grep -c '"level":"Error"' && echo " errors"
docker compose logs --since 1h identity-service 2>&1 | grep -c '"level":"Fatal"' && echo " fatals"

# Identify error patterns
docker compose logs --since 1h identity-service 2>&1 | \
  grep '"level":"Error"' | \
  jq -r '.messageTemplate' 2>/dev/null | \
  sort | uniq -c | sort -rn | head -10
```

---

## Phase 4+ — ELK (Kibana KQL)

Open Kibana → Discover → select `jamtrack-*` index.

**Time range**: Last 2 hours (spanning deployment timestamp).

**KQL queries**:

```
# All errors in the deployed services
level: "Error" OR level: "Fatal"

# Errors after deployment only
level: "Error" AND @timestamp > "2024-01-15T14:30:00.000Z"

# Errors by service
level: "Error" AND serviceName: "IdentityService"

# HTTP 5xx responses
level: "Information" AND statusCode >= 500

# Specific exception types
exceptionType: "System.Data.Postgres*"

# Auth failures (potential security indicator)
messageTemplate: "Login failed*" OR messageTemplate: "JWT validation failed*"
```

**Dashboard**: Navigate to "Jamtrack Error Rate" dashboard and check the error spike chart around the deployment timestamp.

---

## Phase 4+ — ClickHouse Queries

```sql
-- Error count by service, last 2 hours vs. previous 2 hours
SELECT
    service_name,
    countIf(timestamp > now() - INTERVAL 2 HOUR AND log_level IN ('Error', 'Fatal')) AS post_deploy_errors,
    countIf(timestamp BETWEEN now() - INTERVAL 4 HOUR AND now() - INTERVAL 2 HOUR AND log_level IN ('Error', 'Fatal')) AS pre_deploy_errors,
    round((post_deploy_errors - pre_deploy_errors) / nullIf(pre_deploy_errors, 0) * 100, 1) AS change_pct
FROM jamtrack.log_events
WHERE timestamp > now() - INTERVAL 4 HOUR
GROUP BY service_name
ORDER BY change_pct DESC;

-- Top error messages post-deployment
SELECT
    message_template,
    count() AS occurrences,
    max(timestamp) AS last_seen
FROM jamtrack.log_events
WHERE
    log_level IN ('Error', 'Fatal')
    AND timestamp > now() - INTERVAL 2 HOUR
GROUP BY message_template
ORDER BY occurrences DESC
LIMIT 20;

-- Error rate as % of total requests, per minute
SELECT
    toStartOfMinute(timestamp) AS minute,
    countIf(log_level IN ('Error', 'Fatal')) AS errors,
    count() AS total,
    round(errors / total * 100, 2) AS error_rate_pct
FROM jamtrack.log_events
WHERE timestamp > now() - INTERVAL 2 HOUR
GROUP BY minute
ORDER BY minute;
```

---

## Analysis

Compare post-deploy vs. pre-deploy:

| Service | Pre-deploy errors/hr | Post-deploy errors/hr | Change | Status |
|---------|--------------------|-----------------------|--------|--------|
| Identity Service | ___ | ___ | ___% | ✅ / ⚠️ / ❌ |
| Track Service | ___ | ___ | ___% | ✅ / ⚠️ / ❌ |
| Streaming Service | ___ | ___ | ___% | ✅ / ⚠️ / ❌ |

Record the top 3 error types (if any) and whether they existed pre-deployment.

---

## Gate

**Pass**: Error rate within 5% of pre-deploy baseline for all services. Proceed to `/monitor-performance`.

**Warning (5–20% increase)**: Investigate before proceeding. Not necessarily a rollback trigger — may be expected (new validation, new error handling). Document the reason.

**Fail (>20% increase)**: New errors introduced. **Investigate immediately.** Consider rollback.

---

## Escalation Checklist

If error rate has increased:
- [ ] Are the new errors related to the deployed code changes?
- [ ] Are they affecting user-facing requests or internal background jobs?
- [ ] Is the error rate stable or still climbing?
- [ ] Are there database connection errors? (Check migration compatibility)
- [ ] Are there new dependency failures? (Downstream service, blob storage)
- [ ] Is this affecting the pre-deploy version too? (Infra issue, not a code regression)
