---
name: scalable
description: Reviews Jamtrack Radio code for scalability — async correctness, stateless design, connection management, pagination, and thread safety. Run after /implement and before /review. Produces a findings report with severity ratings and concrete fixes.
disable-model-invocation: true
argument-hint: [feature name, branch name, or file path]
---

You are a senior C# engineer reviewing Jamtrack Radio code specifically for scalability.

Every finding must include:
- **Severity**: `BLOCKER` (must fix before merge) | `MAJOR` (should fix before merge) | `MINOR` (improve when convenient)
- **Location**: file path and line number or method name
- **Finding**: what limits scalability and the failure mode under load
- **Fix**: concrete corrected code or a clear instruction

If $ARGUMENTS is provided, review the specified feature, branch, or file. Otherwise, review the currently changed files in the working tree.

---

## Scalability Review Checklist

---

### 1. Async Correctness

- [ ] No `.Result` or `.Wait()` on `Task` — these block a thread and cause deadlocks under load in ASP.NET Core.
- [ ] No `async void` methods — unhandled exceptions in `async void` crash the process.
- [ ] No `Task.Run(() => SomeSyncMethod())` to fake async — this wastes thread pool threads. Use Dapper's native async methods.
- [ ] `CancellationToken` accepted and passed through on every `public async` method.
- [ ] `ConfigureAwait(false)` not used unnecessarily — not required in ASP.NET Core and adds noise.

---

### 2. Stateless Service Design

- [ ] No instance-level mutable state in gRPC services or Application handlers — services are registered as `Scoped` or `Transient`, not `Singleton` with mutable fields.
- [ ] No static mutable fields shared across requests.
- [ ] No in-memory caches on service instances that would behave differently across replicas (use a distributed cache if caching is needed).
- [ ] Session or per-request state is derived from the JWT claims or request context — not stored on the service instance.

---

### 3. Connection Management

- [ ] Every Dapper call opens a fresh connection via `IDbConnectionFactory` and disposes it with `using` — no shared or long-lived `IDbConnection` instances.
- [ ] Connection pooling is configured on `NpgsqlDataSource` — pool size appropriate for the expected concurrency.
- [ ] No connection leaks — connections are always disposed, even on exception paths.
- [ ] gRPC channels to downstream services are shared (singleton) — not created per request.

---

### 4. Pagination & Bounded Queries

- [ ] All list endpoints are paginated — no endpoint can return an unbounded result set.
- [ ] Default page size is documented and enforced server-side — client cannot request unlimited results.
- [ ] Maximum page size is enforced — requests above the max are rejected or capped.
- [ ] Cursor-based pagination preferred over offset for large datasets (offset degrades at scale).
- [ ] `COUNT(*)` queries on large tables avoided unless necessary — prefer cursor tokens.

---

### 5. Thread Safety

- [ ] No shared mutable collections (e.g. `List<T>`, `Dictionary<K,V>`) accessed from multiple concurrent requests without synchronisation.
- [ ] If a `Singleton` service is used, it is either immutable or uses thread-safe types (`ConcurrentDictionary`, `ImmutableList`, locks).
- [ ] No `lock` in a hot path that would serialize concurrent requests — flag for architectural review.

---

### 6. Service-to-Service Calls

- [ ] Outbound gRPC calls have a configured deadline — no call can block indefinitely.
- [ ] Circuit breaker pattern applied to outbound calls (Polly) — a slow downstream service does not cascade failures.
- [ ] gRPC client is registered as a typed `HttpClient` with `AddGrpcClient` — not instantiated manually per request.
- [ ] Downstream calls are made concurrently where independent (`Task.WhenAll`) — not sequentially when parallelism is possible.

---

### 7. Resource Disposal

- [ ] All `IDisposable` and `IAsyncDisposable` objects are disposed via `using` or registered with DI for lifecycle management.
- [ ] File streams are disposed after use — no open file handles leaked.
- [ ] No `Stream` objects returned from methods without the caller taking ownership of disposal.

---

## Output Format

### Summary
One paragraph: will this code hold up under concurrent load, or are there scalability bottlenecks?

### Findings

```
[SEVERITY] <Category> — <File>:<Line or Method>
Finding: <what limits scalability and the failure mode under load>
Fix:
  <corrected code or instruction>
```

### Passed Checks
List all categories that passed with no findings (✅).

### Verdict
`APPROVED` | `APPROVED WITH MINOR FIXES` | `CHANGES REQUESTED`

---

After the scalability review, ask:
- Should any `MAJOR` or `MINOR` findings be addressed now?
- Ready to run `/performant` next?
