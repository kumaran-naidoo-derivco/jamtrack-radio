# ADR-006: PostgreSQL as the Relational Database

**Date**: 2026-04-01
**Status**: Accepted

---

## Context

Jamtrack Radio requires a relational database for all five services: Identity, Track, Playlist, Storage, and (future) any new bounded contexts. The choice of database affects developer experience, cloud cost, operational complexity, and long-term scalability. Key constraints from the requirements:

- GDPR compliance (right to erasure, audit trail)
- Idempotent uploads (duplicate detection via unique constraints)
- Full-text track title search
- 99.9% uptime target (Phase 4+)
- Dapper as the mandatory data access layer (rules out document stores)
- Azure is the primary cloud (managed service availability matters)
- Budget: ~£35/month staging, ~£277/month production (Azure Database for PostgreSQL Flexible Server)

Candidates evaluated: PostgreSQL, MySQL / MariaDB, SQL Server, SQLite (dev only).

---

## Decision

**PostgreSQL** is the relational database for all Jamtrack Radio services.

---

## Consequences

### What becomes easier

- **`pg_trgm` extension**: enables GIN trigram indexes for full-text title search (`idx_tracks_title_trgm`) — MySQL requires a separate full-text index with different syntax and limitations
- **UUID primary keys**: native `uuid` type with efficient B-tree indexing; no performance penalty (unlike MySQL where UUID PKs fragment the clustered index)
- **Partial indexes**: `WHERE deleted_at IS NULL` on the `tracks` table eliminates soft-deleted rows from all active-only queries at zero application-layer cost
- **JSONB columns**: available for future flexibility (e.g. event payload storage) without schema migrations
- **Azure managed service**: Azure Database for PostgreSQL Flexible Server offers automated backups, point-in-time restore, zone-redundant HA, and read replicas — all required for the 99.9% SLA at Phase 4
- **Rich constraint support**: deferred foreign keys, `CHECK` constraints, and exclusion constraints map cleanly to domain invariants
- **Open-source**: zero licence cost; no per-core pricing (unlike SQL Server)
- **Testcontainers support**: `Testcontainers.PostgreSql` NuGet package provides a first-class testing experience with real PostgreSQL instances in CI

### What becomes harder

- PostgreSQL-specific SQL syntax (e.g. `ON CONFLICT DO NOTHING`, `RETURNING`) does not port to SQL Server without changes — acceptable given Azure is the primary cloud
- Team must know `psql` and PostgreSQL-specific tooling (vs. SSMS for SQL Server) — acceptable given the learning project context

### What we are not doing

- **SQL Server**: more expensive (Azure SQL has higher per-unit cost than Flexible Server PostgreSQL), requires paid licence for on-premises dev, and does not support `pg_trgm`
- **MySQL / MariaDB**: inferior UUID handling, less mature JSON support, `pg_trgm` not available, smaller Azure managed service feature set
- **SQLite**: development convenience only; not suitable for Phase 3+ (no concurrent writes, no UUID type, no Azure managed service)

---

## Cost implication

| Environment | SKU | Monthly cost |
|-------------|-----|-------------|
| Dev | Local Docker | £0 |
| Staging | Azure Flexible Server B2ms (2 vCores, 8 GB) | ~£35 |
| Production | Azure Flexible Server D4s v3 (4 vCores, 16 GB) + zone-redundant HA | ~£277 |

All five services share a single PostgreSQL instance per environment, with database-level isolation (one database per service). This avoids the per-instance cost of five separate managed PostgreSQL servers.
