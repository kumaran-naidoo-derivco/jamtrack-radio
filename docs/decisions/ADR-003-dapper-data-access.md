# ADR-003: Dapper over EF Core for Data Access

**Status**: Accepted
**Date**: 2026-03-22

## Context

All services need a .NET data access layer for PostgreSQL. The principal choices are EF Core (ORM) and Dapper (micro-ORM). This is a **constrained decision** — the project requirements mandate Dapper + FluentMigrator — but the architectural rationale is documented here for completeness.

## Decision

Use **Dapper** (micro-ORM) for all database access, with **FluentMigrator** for schema migrations.

- All SQL is written explicitly by the developer
- Dapper maps `IDataReader` results to typed C# objects
- FluentMigrator provides versioned, code-defined migration scripts with `Up()` and `Down()` methods
- Migrations run on service startup (or via a separate migration runner job in Phase 3+)

## Consequences

**What becomes easier:**
- SQL control: every query is explicit. No hidden N+1 queries. No unexpected JOIN strategies. Performance is predictable.
- Learning outcome: writing SQL explicitly is a core skill this project is designed to build
- Clean Architecture alignment: Dapper lives entirely in the Infrastructure layer. No ORM abstractions leak into Domain or Application.
- Testability: SQL queries can be tested against a real PostgreSQL instance (Testcontainers) without needing an ORM mock

**What becomes harder:**
- Boilerplate: INSERT/UPDATE statements must be written by hand. EF Core generates these. Dapper does not.
- Schema changes: renaming a column requires a migration AND updating all affected queries. EF Core regenerates queries automatically.
- No lazy loading, no change tracking: every write must be explicit. This is a feature (predictability) and a cost (verbosity).

## Cost implication

£0. Both Dapper and FluentMigrator are free OSS libraries.
