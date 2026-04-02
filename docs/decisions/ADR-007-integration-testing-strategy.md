# ADR-007: Integration Testing Strategy

**Date**: 2026-04-01
**Status**: Accepted

---

## Context

Jamtrack Radio requires a testing strategy that catches real bugs without creating a large test suite that is expensive to maintain. Key constraints and learnings:

- Services use gRPC internally and expose no REST API except the Streaming Service — unit tests of controllers/handlers in isolation test plumbing, not behaviour
- Prior incident (noted in team retrospectives): mock-based tests passed while a real database migration failed in production — tests that mock the database do not catch integration failures
- ASP.NET Core `WebApplicationFactory<T>` + Testcontainers is the idiomatic way to spin up a real service with a real database in CI
- The project is a learning environment — tests must demonstrate real-world practices, not shortcuts
- Each service owns its own database — cross-service behaviour is tested by calling the owning service's API, not by querying another service's database

Candidates evaluated: unit tests with mocking, integration tests with in-memory database (EF Core InMemory / SQLite), integration tests with real PostgreSQL (Testcontainers).

---

## Decision

**Integration tests against a real PostgreSQL database** using `WebApplicationFactory<T>` and `Testcontainers.PostgreSql`. Unit tests are written only for complex isolated calculations (e.g. custom parsers, pricing algorithms). No database mocking.

---

## Rationale

1. **Catches the full call chain**: an integration test that calls the gRPC endpoint exercises the handler, repository, SQL query, and database constraint in one shot — the most likely failure modes (wrong SQL, constraint violation, missing index) are all caught
2. **Eliminates mock/prod divergence**: the database in CI is the same PostgreSQL version as production; migrations run before each test suite, so schema drift is caught immediately
3. **Low maintenance overhead**: tests are written once against the real service contract; they do not need to be updated when internal implementation details change (as mock expectations do)
4. **Testcontainers is production-ready**: each test class gets a fresh PostgreSQL container; the container is shared within a test class via `IAsyncLifetime` to avoid per-test startup overhead

---

## Consequences

### What becomes easier

- Schema migrations are validated on every CI run — broken migrations cannot reach production
- SQL query correctness is validated — N+1 bugs and missing index hints are visible in test execution time
- Tests serve as executable documentation of the API contract
- No test doubles to maintain as implementation evolves

### What becomes harder

- Tests run slower than unit tests (container startup ~2–5 seconds per suite, typically tolerable)
- Requires Docker in CI (GitHub Actions runners have Docker pre-installed; this is a non-issue)
- Test data setup is more verbose — each test must insert its own rows rather than relying on in-memory state

### Test structure conventions

- One test project per service: `tests/<Service>.Tests/`
- One `PostgresFixture` class per test project, shared across all test classes via `IClassFixture<PostgresFixture>`
- AAA pattern (Arrange / Act / Assert) with a blank line separating each section
- Each test is self-contained: inserts its own data, does not depend on test ordering
- Test coverage targets: happy path, validation errors, not-found, duplicate/conflict, auth failure, boundary values

---

## Cost implication

£0 — Testcontainers is open-source; Docker runs in GitHub Actions free tier; no external test database required.
