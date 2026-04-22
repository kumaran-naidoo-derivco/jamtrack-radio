---
name: monitor-performance
description: p50/p95/p99 latency analysis vs. pre-deploy baseline using ClickHouse percentile queries. Phase-aware. Run as MONITORING Step 3 after /monitor-errors passes. Gate — p99 latency within 20% of baseline.
disable-model-invocation: true
argument-hint: [service name or "all"]
---

You are a DevOps Engineer analysing performance metrics after a Jamtrack Radio deployment. Your goal is to confirm the new deployment has not introduced a latency regression.

If `$ARGUMENTS` is provided, scope the analysis to that service.

---

## Required Context

Before running, collect:
- **Pre-deploy baseline p99 latency**: the p99 latency from the 1-hour window before deployment, per service
- **Deployment timestamp**
- **Services affected**

---

## Phase 2 — Docker Compose (application logs)

Serilog logs request duration on every request. Extract from logs:

```bash
# Extract request durations from structured logs (last 1 hour)
docker compose logs --since 1h identity-service 2>&1 | \
  grep '"ElapsedMilliseconds"' | \
  jq -r '.ElapsedMilliseconds' 2>/dev/null | \
  sort -n | \
  awk '
    BEGIN { count=0; sum=0; }
    { vals[count++] = $1; sum += $1; }
    END {
      print "Count: " count;
      print "Min: " vals[0] "ms";
      print "p50: " vals[int(count*0.50)] "ms";
      print "p95: " vals[int(count*0.95)] "ms";
      print "p99: " vals[int(count*0.99)] "ms";
      print "Max: " vals[count-1] "ms";
    }
  '
```

Note: Phase 2 has limited performance data (single-node Docker). Use as a directional indicator only.

---

## Phase 9+ — ClickHouse Latency Queries

```sql
-- p50, p95, p99 latency by service, post-deploy vs. pre-deploy
SELECT
    service_name,
    endpoint,
    quantile(0.50)(elapsed_ms) AS p50_post,
    quantile(0.95)(elapsed_ms) AS p95_post,
    quantile(0.99)(elapsed_ms) AS p99_post
FROM jamtrack.request_metrics
WHERE timestamp > toDateTime('<deployment-timestamp>')
GROUP BY service_name, endpoint
ORDER BY p99_post DESC;

-- Pre-deploy baseline (same query, different time window)
SELECT
    service_name,
    endpoint,
    quantile(0.50)(elapsed_ms) AS p50_pre,
    quantile(0.95)(elapsed_ms) AS p95_pre,
    quantile(0.99)(elapsed_ms) AS p99_pre
FROM jamtrack.request_metrics
WHERE timestamp BETWEEN toDateTime('<1hr-before-deploy>') AND toDateTime('<deployment-timestamp>')
GROUP BY service_name, endpoint
ORDER BY p99_pre DESC;

-- Combined comparison with change %
WITH
    pre AS (
        SELECT service_name, endpoint,
            quantile(0.99)(elapsed_ms) AS p99
        FROM jamtrack.request_metrics
        WHERE timestamp BETWEEN toDateTime('<1hr-before-deploy>') AND toDateTime('<deployment-timestamp>')
        GROUP BY service_name, endpoint
    ),
    post AS (
        SELECT service_name, endpoint,
            quantile(0.99)(elapsed_ms) AS p99
        FROM jamtrack.request_metrics
        WHERE timestamp > toDateTime('<deployment-timestamp>')
        GROUP BY service_name, endpoint
    )
SELECT
    post.service_name,
    post.endpoint,
    pre.p99 AS p99_before,
    post.p99 AS p99_after,
    round((post.p99 - pre.p99) / pre.p99 * 100, 1) AS change_pct
FROM post
LEFT JOIN pre USING (service_name, endpoint)
ORDER BY change_pct DESC;

-- Throughput (requests per minute) post-deploy
SELECT
    toStartOfMinute(timestamp) AS minute,
    service_name,
    count() AS requests_per_minute
FROM jamtrack.request_metrics
WHERE timestamp > now() - INTERVAL 2 HOUR
GROUP BY minute, service_name
ORDER BY minute DESC;

-- Slow requests (over threshold) post-deploy
SELECT
    timestamp,
    service_name,
    endpoint,
    elapsed_ms,
    trace_id
FROM jamtrack.request_metrics
WHERE
    elapsed_ms > 500  -- adjust threshold per SLA
    AND timestamp > toDateTime('<deployment-timestamp>')
ORDER BY elapsed_ms DESC
LIMIT 20;
```

---

## Phase 9+ — Kibana APM (if configured)

Navigate to APM → select service → Latency tab:
- Compare "before" and "after" deployment marker
- Check for new slow transactions
- Identify traces where latency degraded most

---

## Analysis Table

| Service | Endpoint | p50 before | p50 after | p95 before | p95 after | p99 before | p99 after | p99 change | Status |
|---------|----------|-----------|-----------|-----------|-----------|-----------|-----------|------------|--------|
| Identity | RegisterUser | _ms | _ms | _ms | _ms | _ms | _ms | __% | ✅ |
| Identity | Login | _ms | _ms | _ms | _ms | _ms | _ms | __% | ✅ |

---

## Gate

**Pass**: p99 latency within 20% of pre-deploy baseline for all services. Proceed to `/monitor-report`.

**Warning (20–50% increase)**: Investigate before proceeding. Check for:
- New database queries introduced (missing index?)
- N+1 query pattern in new code
- Synchronous blocking call introduced (`.Result`, `.Wait()`)
- External dependency call added to critical path

**Fail (>50% increase)**: Significant regression. **Investigate and likely rollback.**

---

## Common Latency Regression Causes

| Symptom | Likely cause | Investigation |
|---------|-------------|---------------|
| p99 spike on DB-heavy endpoints | Missing index on new query | `EXPLAIN ANALYZE` the query, check migration |
| All endpoints affected | Connection pool exhaustion | Check `max_connections` in PostgreSQL, npgsql pool size |
| Only new endpoints slow | N+1 query in new code | Add logging to count DB calls per request |
| Random spikes | GC pressure (large object allocations) | Review new code for large array/stream allocations |
| Timeout errors | External dependency timeout | Check downstream service latency (gRPC call, blob storage) |
