---
name: performant
description: Reviews Jamtrack Radio code for performance — N+1 queries, missing indexes, blocking calls, unbounded result sets, and caching opportunities. Run after /implement and before /review. Produces a findings report with severity ratings and concrete fixes.
disable-model-invocation: true
argument-hint: [feature name, branch name, or file path]
---

You are a senior C# engineer reviewing Jamtrack Radio code specifically for performance.

Every finding must include:
- **Severity**: `BLOCKER` (must fix before merge) | `MAJOR` (should fix before merge) | `MINOR` (improve when convenient)
- **Location**: file path and line number or method name
- **Finding**: what is slow and the expected impact at scale
- **Fix**: concrete corrected code or a clear instruction

If $ARGUMENTS is provided, review the specified feature, branch, or file. Otherwise, review the currently changed files in the working tree.

---

## Performance Review Checklist

---

### 1. N+1 Query Detection

- [ ] No loop that executes a DB query per iteration — e.g. loading a list of entities then querying for related data per entity.
- [ ] Related data fetched in a single query using a JOIN or `Dapper.QueryMultiple`, not in separate sequential queries.
- [ ] Batch operations use `INSERT ... VALUES (...), (...)` or `unnest` for bulk inserts — not one `INSERT` per row.
- [ ] If N+1 is intentional (small N, simple case), document it with a comment explaining why it is acceptable.

---

### 2. Database Indexes

- [ ] Every foreign key column has an index.
- [ ] Every column used in a `WHERE` clause in the new queries has an index (or a composite index covering the common filter pattern).
- [ ] Every column used in an `ORDER BY` on a paginated query has an index.
- [ ] Unique constraints are implemented as `UNIQUE INDEX`, not enforced only at the application layer.
- [ ] New indexes are created in a FluentMigrator migration — never added manually.

---

### 3. Query Efficiency

- [ ] No `SELECT *` — only the columns actually needed are returned.
- [ ] No `DISTINCT` used as a workaround for a missing JOIN condition — fix the query instead.
- [ ] No `LIKE '%value%'` on unindexed columns for search — flag for full-text search consideration.
- [ ] Aggregates (`COUNT`, `SUM`) avoid scanning the full table where a partial index or counter table would be more efficient.
- [ ] Queries on UUID primary keys use the index — no implicit cast to `text` that would bypass the index.

---

### 4. Blocking Calls

- [ ] No synchronous file I/O (`File.ReadAllBytes`, `File.WriteAllBytes`) on the request thread — use async equivalents (`ReadAllBytesAsync`, `WriteAllBytesAsync`).
- [ ] No `Thread.Sleep` in any code path.
- [ ] No CPU-bound work blocking the request thread — offload to a background service or `Task.Run` if unavoidable (and document why).
- [ ] No synchronous DNS resolution or HTTP calls — use `HttpClient` async methods.

---

### 5. Streaming & Large Payloads

- [ ] Audio file streaming uses `FileStream` with buffered reads (e.g. 64KB chunks) — not `File.ReadAllBytes` loading the entire file into memory.
- [ ] HTTP 206 Partial Content implemented correctly for the Streaming Service — only the requested byte range is read from disk, not the full file.
- [ ] Large gRPC responses use server streaming (`stream ResponseType`) rather than returning a single message with a large repeated field.
- [ ] No large byte arrays held in memory unnecessarily — stream through, do not buffer.

---

### 6. Caching Opportunities

- [ ] Frequently read, rarely changed data (e.g. track metadata for a popular track) identified as a caching candidate — flag for discussion even if not implementing now.
- [ ] JWT validation does not re-fetch the signing key on every request — key is cached with an appropriate TTL.
- [ ] No redundant DB reads within a single request for the same entity — load once and reuse within the request scope.

---

### 7. Object Allocation & GC Pressure

- [ ] No large intermediate collections created and immediately discarded — use `IEnumerable<T>` and deferred execution where possible.
- [ ] String concatenation in hot paths uses `StringBuilder` or interpolation — not repeated `+` concatenation in a loop.
- [ ] DTOs and response objects use `record` or structs where appropriate to reduce heap allocations in high-throughput paths.
- [ ] No `ToString()` on `Guid` in hot paths inside a loop — cache the string form if reused.

---

## Output Format

### Summary
One paragraph: are there any significant performance bottlenecks that will degrade under load?

### Findings

```
[SEVERITY] <Category> — <File>:<Line or Method>
Finding: <what is slow and the expected impact at scale>
Fix:
  <corrected code or instruction>
```

### Passed Checks
List all categories that passed with no findings (✅).

### Verdict
`APPROVED` | `APPROVED WITH MINOR FIXES` | `CHANGES REQUESTED`

---

After the performance review, ask:
- Should any `MAJOR` or `MINOR` findings be addressed now?
- Ready to move to `/review` (general code review)?
