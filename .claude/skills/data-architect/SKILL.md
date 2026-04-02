---
name: data-architect
description: Data architecture — ER diagram, schema ownership matrix, data flow, observability events, retention/compliance policies, and storage cost estimation. Run as DISCOVERY Step 5c after /cloud-architect.
disable-model-invocation: true
argument-hint: [feature or service name]
---

You are a Data Architect producing the data model and data flow for a Jamtrack Radio feature. Your output defines what data exists, who owns it, how it flows through the system, and what it costs to store and query.

If `$ARGUMENTS` is provided, use it as the feature name.

## Context Loading (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
echo "=== Loading context for: ${FEATURE} ==="

cat "docs/architecture/${FEATURE}/software-arch.md" 2>/dev/null \
  && echo "✓ Software architecture loaded" \
  || echo "WARN: Software arch not found — run /software-architect ${FEATURE} first"

cat "docs/architecture/${FEATURE}/cloud-arch.md" 2>/dev/null \
  && echo "✓ Cloud architecture loaded" \
  || echo "WARN: Cloud arch not found — run /cloud-architect ${FEATURE} first"

cat "docs/requirements/${FEATURE}-requirements.md" 2>/dev/null \
  && echo "✓ Requirements loaded" \
  || echo "WARN: Requirements not found"

echo "=== Context loading complete ==="
```

Load context from:
- `docs/architecture/<feature>/software-arch.md` — domain model and service boundaries
- `docs/requirements/<feature>-requirements.md` — data retention and compliance requirements

---

## Output

Save to `docs/architecture/<feature>/data-arch.md`.

> **Draw.io is the required diagramming tool for all architecture documents.**
> Use draw.io's **Entity Relationship** shape library for ER diagrams and **Software + UML** for data flow diagrams.
> Save each diagram as a separate `.drawio` file in the `diagrams/` subfolder next to the markdown output file, then reference it from the markdown using the format below.
> **Mermaid diagrams are reserved for the implementation phase only.**

Reference format:
```
> **Diagram**: [filename.drawio](diagrams/filename.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_
```

### Diagram Visual Standards

**Style templates** — use these as the visual reference for every diagram you produce:

| Template | Use for |
|----------|---------|
| `.claude/redemptions.png` | All logical, flow, and interaction diagrams (ER diagram, data flow) |
| `.claude/network.png` | Cloud topology and physical deployment diagrams |

**Edge routing rules** — apply to every edge in every diagram:

| Rule | draw.io style property |
|------|----------------------|
| Route edges as L-shaped paths (no diagonals) | `edgeStyle=orthogonalEdgeStyle` |
| White bubble behind every edge label | `labelBackgroundColor=#ffffff;labelBorderColor=none;` |
| Fan-out from one source to many targets: spread exit points evenly | `exitX=0.1`, `0.3`, `0.5`, `0.7`, `0.9` (one per target) |
| Async / event edges | `dashed=1;endArrow=open;` |

**Jump arc rules** — when two edges must cross:

- **Vertical-primary edges** (travel mostly top-to-bottom): add `jumpStyle=arc;jumpSize=10;` → shows a semicircle arc at the crossing
- **Horizontal-primary edges** (travel mostly left-to-right): add `jumpStyle=none;` → never show arcs
- **Consistency rule**: ALL jumps arc in the same direction (vertical lines always jump; horizontal lines never jump)

Example styles:
```xml
<!-- Vertical edge crossing another — shows arc -->
style="edgeStyle=orthogonalEdgeStyle;jumpStyle=arc;jumpSize=10;labelBackgroundColor=#ffffff;labelBorderColor=none;"

<!-- Horizontal edge — no arc, never jumps -->
style="edgeStyle=orthogonalEdgeStyle;jumpStyle=none;labelBackgroundColor=#ffffff;labelBorderColor=none;"
```

**Legend** — every diagram must include a colour legend in the bottom-left corner. Use this XML template, adding one row per colour used in the diagram:

```xml
<mxCell id="legend" value="Legend" style="swimlane;startSize=22;fillColor=#f5f5f5;strokeColor=#666666;fontStyle=1;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="20" y="[BOTTOM_Y]" width="220" height="[ROW_COUNT*26+32]" as="geometry" />
</mxCell>
<!-- One row per colour: -->
<mxCell id="legend_r1" value="" style="rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="legend">
  <mxGeometry x="10" y="32" width="20" height="16" as="geometry" />
</mxCell>
<mxCell id="legend_r1_lbl" value="Service boundary" style="text;html=1;align=left;" vertex="1" parent="legend">
  <mxGeometry x="36" y="30" width="170" height="20" as="geometry" />
</mxCell>
```

**Standard colour palette** — use consistently across all diagrams:

| Meaning | Fill | Stroke |
|---------|------|--------|
| API Gateway | `#1ba1e2` | `#006EAF` |
| Internal microservice | `#dae8fc` | `#6c8ebf` |
| External system / browser | `#f5f5f5` | `#666666` |
| PostgreSQL database | `#f3e5f5` | `#9e3799` |
| Redis cache | `#fff3e0` | `#E65100` |
| Async / event bus | `#fff2cc` | `#d6b656` |
| Azure resource (icon shape) | `#0078D4` | `#005A9E` (white font) |
| Trust zone — Internet | `#ffcccc` | `#b71c1c` |
| Trust zone — DMZ | `#ffe6cc` | `#e65100` |
| Trust zone — Internal | `#dae8fc` | `#0078D4` |
| Trust zone — Data | `#f3e5f5` | `#7b1fa2` |
| Sticky-note annotation | `#ffffcc` | `#999900` |

---

## 1. ER Diagram

Full entity-relationship diagram for all tables in scope.

**File**: `docs/architecture/<feature>/diagrams/er-diagram.drawio`
**Shape library**: Entity Relationship (`View → Shapes → Entity Relation`)

Diagram elements — use the **swimlane-header + text-body** pattern for entity tables:

```xml
<!-- Entity table: swimlane with table name as header -->
<mxCell id="t_tablename" value="table_name"
  style="swimlane;startSize=24;fillColor=#dae8fc;strokeColor=#6c8ebf;
         align=center;fontStyle=1;fontSize=11;"
  vertex="1" parent="svc_boundary">
  <mxGeometry x="25" y="45" width="310" height="HEIGHT" as="geometry"/>
</mxCell>
<!-- Column list as a single left-aligned text child -->
<mxCell id="t_tablename_body"
  value="&lt;b&gt;PK&lt;/b&gt;  id: uuid&lt;br&gt;
         &lt;font color=&quot;#b05300&quot;&gt;&lt;b&gt;FK&lt;/b&gt;&lt;/font&gt;  fk_col: uuid → other(id)&lt;br&gt;
         &lt;font color=&quot;#2e7d32&quot;&gt;&lt;b&gt;UK&lt;/b&gt;&lt;/font&gt;  unique_col: varchar(254)&lt;br&gt;
         &amp;nbsp;&amp;nbsp;regular_col: varchar(100)?&lt;br&gt;
         &lt;i&gt;UNIQUE(col_a, col_b)&lt;/i&gt;"
  style="text;html=1;align=left;whiteSpace=wrap;verticalAlign=top;
         fontSize=10;spacingLeft=6;spacingTop=4;"
  vertex="1" parent="t_tablename">
  <mxGeometry x="0" y="24" width="310" height="CONTENT_HEIGHT" as="geometry"/>
</mxCell>
```

**Height formula**: `CONTENT_HEIGHT` = N_lines × 16px + 8px padding. `HEIGHT` = 24 (header) + `CONTENT_HEIGHT`.

Badge conventions (inline HTML in the `value`):
- `PK` — `&lt;b&gt;PK&lt;/b&gt;` (bold, inherits table fill)
- `FK` — `&lt;font color="#b05300"&gt;&lt;b&gt;FK&lt;/b&gt;&lt;/font&gt;` (amber bold)
- `UK` — `&lt;font color="#2e7d32"&gt;&lt;b&gt;UK&lt;/b&gt;&lt;/font&gt;` (green bold)
- Cross-service value ref — `&lt;font color="#888"&gt;&lt;i&gt;ref&lt;/i&gt;&lt;/font&gt;` (grey italic)
- Regular column — `&amp;nbsp;&amp;nbsp;col_name: type` (indented)
- Constraint note — `&lt;i&gt;UNIQUE(...)&lt;/i&gt;` (italic, last line)

Service boundary swimlanes — service fill colours:
- Identity Service: `fillColor=#E3F2FD;strokeColor=#0078D4`
- Track Service: `fillColor=#E8F5E9;strokeColor=#2E7D32`
- Playlist Service: `fillColor=#FFF3E0;strokeColor=#E65100`
- Storage Service: `fillColor=#F3E5F5;strokeColor=#7B1FA2`

Table fill colours (match each service's palette):
- Identity tables: `fillColor=#dae8fc;strokeColor=#6c8ebf`
- Track tables: `fillColor=#d5e8d4;strokeColor=#82b366`
- Playlist tables: `fillColor=#fff2cc;strokeColor=#d6b656`
- Storage tables: `fillColor=#e1d5e7;strokeColor=#9673a6`

**Relationship lines**: connect between entity swimlane cells (not body text cells). Use `endArrow=ERmanyToOne;startArrow=ERmandOne` for crow's foot notation. No cross-service FK lines — add a `shape=note;fillColor=#ffffcc;strokeColor=#999900` annotation documenting cross-service value references.

Reference in this document:
```
> **Diagram**: [er-diagram.drawio](diagrams/er-diagram.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_
```

Rules:
- All tables use `uuid` for primary keys (not serial/auto-increment)
- All timestamps use `timestamptz` (UTC-aware)
- Include `created_at` on every table
- Include `updated_at` on mutable tables
- Soft-delete with `is_active` or `deleted_at` (document which pattern and why)

### 2. Schema Ownership Matrix

| Table | Owned by service | Read by | Notes |
|-------|-----------------|---------|-------|
| `users` | Identity Service | Identity Service | No cross-service DB reads |
| `refresh_tokens` | Identity Service | Identity Service | Purge expired tokens nightly |
| `tracks` | Track Service | Track Service | |
| `genres` | Track Service | Track Service, Streaming Service | If Streaming reads genres, it must go via gRPC call to Track Service — not direct DB read |

**Rule**: No service may read another service's database tables directly. Cross-service data access must go through the owning service's API.

### 3. Database Schema (DDL)

For each new table or column, provide the FluentMigrator migration outline:

```csharp
[Migration(20240101120000)]
public class Migration_CreateUsers : Migration
{
    public override void Up()
    {
        Create.Table("users")
            .WithColumn("id").AsGuid().PrimaryKey().NotNullable()
            .WithColumn("email").AsString(254).NotNullable().Unique()
            .WithColumn("display_name").AsString(100).NotNullable()
            .WithColumn("password_hash").AsString(255).NotNullable()
            .WithColumn("created_at").AsDateTimeOffset().NotNullable().WithDefaultValue(SystemMethods.CurrentUTCDateTime)
            .WithColumn("updated_at").AsDateTimeOffset().NotNullable().WithDefaultValue(SystemMethods.CurrentUTCDateTime)
            .WithColumn("is_active").AsBoolean().NotNullable().WithDefaultValue(true);
    }

    public override void Down()
    {
        Delete.Table("users");
    }
}
```

### 4. Index Strategy

| Table | Index | Columns | Type | Rationale |
|-------|-------|---------|------|-----------|
| `users` | `idx_users_email` | `email` | UNIQUE B-tree | Login by email |
| `refresh_tokens` | `idx_tokens_user_id` | `user_id` | B-tree | Delete all tokens for a user |
| `refresh_tokens` | `idx_tokens_expires_at` | `expires_at` | B-tree | Nightly purge of expired tokens |

Rule: every foreign key column must have an index. Every column used in a `WHERE` clause in a hot query must have an index.

### 5. Data Flow Diagram

Show how data moves through the system for the key scenario, using interaction diagram notation to make synchronous vs. asynchronous flows explicit.

**File**: `docs/architecture/<feature>/diagrams/data-flow.drawio`
**Shape library**: Software + UML

Layout rules for data flow diagrams:
- Arrange shapes left-to-right for synchronous calls; reserve a lower row for async callbacks
- Avoid negative x/y coordinates — all shapes must be within the page bounds
- When two edges share the same source and target (e.g. INSERT and UPDATE to same DB), offset their entry points: use `entryX=0.4` and `entryX=0.6` so labels don't overlap
- Edge labels for multi-step numbered flows: use format `N. action: detail` (e.g. `3. INSERT track`)
- Async back-edges (dashed): route via explicit waypoints below the main flow row to avoid crossing solid edges

Diagram elements — follow the interaction diagram symbol conventions:
- **`<<component>>`** shapes for services
- **Cylinder** shapes for databases and event stores
- **Queue/envelope** shape for any async event bus — label `<<async>>` and annotate with `eventually consistent` where the consumer's state lags the producer
- **Solid arrows** for synchronous calls (gRPC, REST, SQL) — label with operation name
- **Dashed arrows** for domain events — label with event name (e.g. `UserRegistered`)
- Show the full write path (client → service → DB) and async publication path separately

Reference in this document:
```
> **Diagram**: [data-flow.drawio](diagrams/data-flow.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_
```

### 6. Observability Events

List all domain events that should be emitted for observability (structured logs, metrics, future event bus):

| Event | When emitted | Key fields | Destination |
|-------|-------------|------------|-------------|
| `user.registered` | User created | userId, email (hashed), timestamp | Serilog → ELK |
| `user.login_success` | Successful login | userId, timestamp, ip | Serilog → ELK |
| `user.login_failed` | Failed login attempt | email (hashed), timestamp, ip, reason | Serilog → ELK (security alert) |
| `token.refreshed` | Token refreshed | userId, tokenId, timestamp | Serilog → ELK |

### 7. Data Retention & Compliance

| Data category | Retention period | Deletion mechanism | Compliance note |
|--------------|-----------------|-------------------|-----------------|
| User accounts | Indefinite (until account deletion request) | Soft delete → hard delete after 30 days | GDPR right to erasure |
| Refresh tokens | 90 days from creation or until revoked | Nightly purge job | Revoke on logout |
| Login attempt logs | 90 days | Log rotation (ELK ILM policy) | Security audit trail |
| Audio stream events | 12 months | ClickHouse TTL policy | Usage analytics |

### 8. Storage Cost Estimation

| Data store | Estimated size (Year 1) | Growth rate | Monthly cost | Notes |
|------------|------------------------|-------------|-------------|-------|
| PostgreSQL (users, tracks) | ~1 GB | +10%/month | ~£15 (Azure Flex) | Small dataset |
| PostgreSQL (stream events) | ~10 GB | +50%/month | ~£25 | Move to ClickHouse at Phase 6 |
| Azure Blob (audio files) | ~100 GB | +20%/month | ~£2 (LRS) | Hot tier |
| ELK indices (logs) | ~5 GB/day | Constant | ~£115/month | 30-day retention |

---

## Financial Lens (mandatory)

Data is cheap to store but expensive to query unoptimised. Every data design decision has a cost implication.

- A missing index on a 10M-row table is a latency spike and a CPU cost spike simultaneously. Index strategy is not optional.
- ELK log ingestion is often the largest unexpected cost in production. A service emitting verbose debug logs to ELK at 5 GB/day costs ~£115/month in Log Analytics alone. Set ILM retention policies from the first deployment.
- ClickHouse is dramatically cheaper than Elasticsearch for time-series analytics (10–100× compression ratio). Plan the migration path from ELK to ClickHouse before ELK costs spiral in Phase 6.
- Blob storage is cheap (Azure LRS ~£0.02/GB/month) but egress is not. Design streaming to minimise unnecessary full-file downloads.

---

## Best Practice Patterns

**Data modelling principles**
- *Single source of truth*: each piece of data is owned by exactly one service. Read projections (cached summaries, denormalised views) are acceptable for performance, but authoritative data lives in exactly one place.
- *UUID primary keys*: use UUIDs (not serial/auto-increment) for all primary keys. UUIDs are portable across databases, safe to generate client-side, and avoid enumeration attacks.
- *UTC everywhere*: store all timestamps as `timestamptz` (UTC-aware). Never store local time in the database. Convert to local time only at display.
- *Soft-delete before hard-delete*: mark records as deleted (`deleted_at timestamp`) rather than physically deleting them. After a configurable retention period, a background job hard-deletes. This protects against accidental data loss and supports audit trails.
- *Enums over booleans for state*: model state as an enum (`account_status: active | suspended | deleted`) rather than proliferating boolean columns. Easier to query, extend, and document.
- *Normalise to 3NF by default; denormalise with evidence*: start normalised. Only denormalise specific hot read paths when you have measured query performance evidence that normalisation is the bottleneck.

**PostgreSQL-specific patterns**
- *Table partitioning*: partition event and log tables by month (range partitioning on `created_at`). Essential for tables that grow indefinitely — queries scan only the relevant partition.
- *`pg_trgm` for full-text search*: enables trigram-based search on track titles and artist names without introducing Elasticsearch. Use `CREATE INDEX ... USING GIN (column gin_trgm_ops)` for `ILIKE` and similarity queries.
- *Connection pooling*: PostgreSQL has a hard connection limit (~100 by default). At Phase 4, use PgBouncer (transaction pooling mode) or Npgsql's built-in connection pool. Never let each service replica open unbounded connections.
- *EXPLAIN ANALYSE before indexing*: use `EXPLAIN (ANALYSE, BUFFERS)` on all hot-path queries before adding indexes. Index blindly and you'll slow down writes without helping the reads you intended.
- *Partial indexes for filtered queries*: if a query always filters on `deleted_at IS NULL`, a partial index `WHERE deleted_at IS NULL` is smaller and faster than a full index.

**Schema evolution patterns**
- *Backward-compatible migrations*: migrations must be backward-compatible with the previous version of the service. Add columns as nullable first; backfill data; then add the `NOT NULL` constraint in a subsequent migration.
- *Versioned migrations with rollback*: every FluentMigrator `Up()` migration must have a working `Down()`. This is non-negotiable — it is what enables safe rollbacks.
- *Zero-downtime column renames*: never rename a column in a single migration if the service is live. Add the new column, backfill it, update application code, then drop the old column in a subsequent deployment.

**Event and observability patterns**
- *Domain events for observability*: emit a structured domain event (via Serilog) for every meaningful state transition: `user.registered`, `track.uploaded`, `stream.started`, `user.login_failed`. These become the raw material for dashboards, alerts, and audit trails.
- *Event sourcing for audit trails*: consider storing state changes as an append-only event log for domains where auditability matters (user account changes, billing). Not required at Phase 2 but design the schema to allow it later.
- *CQRS when read and write patterns diverge*: if the Track Service query (list all tracks with metadata) is structurally different from the write model (upload track + tag assignment), introduce a read model. Start without CQRS; introduce when query complexity becomes a problem.

---

## Anti-Patterns / Don'ts

**Schema design anti-patterns**
- **EAV (Entity-Attribute-Value) tables**: `properties(entity_id, attribute_name, attribute_value)` as a catch-all flexible schema. EAV tables cannot be indexed efficiently, cannot be typed, and produce nightmarish queries. Use JSONB columns or dedicated tables instead.
- **JSONB for structured queryable data**: storing `{"bpm": 120, "key": "Am"}` as a JSONB column when BPM and key are always queried. These should be typed columns. JSONB is appropriate for truly dynamic, schema-less data only.
- **Boolean proliferation**: `is_active`, `is_deleted`, `is_verified`, `is_premium` as separate boolean columns. Use a status enum. Adding the fifth boolean state requires an ALTER TABLE.
- **Natural keys as primary keys**: using email address or username as the primary key. Natural keys change (people change email addresses). Use a surrogate UUID PK and put a unique index on the natural key separately.
- **Storing passwords or signing keys in plain text**: passwords must be hashed with BCrypt (cost factor 12) or Argon2id. Signing keys must be in Key Vault / K8s Secrets. Plain text secrets in a DB column is a critical vulnerability.
- **Timestamps without time zone**: `timestamp` (without timezone) stores local time. When the server changes timezone or the data moves to another region, all timestamps become ambiguous. Always use `timestamptz`.

**Query and performance anti-patterns**
- **N+1 query problem**: fetching a list of 100 tracks and then making 100 individual queries to fetch tags for each track. Use a JOIN or a batch query (`WHERE id IN (...)`).
- **`SELECT *` in application queries**: selecting all columns when only 3 are needed. This transfers unnecessary data, prevents index-only scans, and breaks when columns are added or removed.
- **Missing index on foreign keys**: PostgreSQL does NOT automatically index foreign key columns. Every FK column needs an explicit index, or cascade deletes and joins will be sequential scans.
- **Unbounded queries**: a `SELECT * FROM tracks WHERE user_id = ?` with no `LIMIT` will return the entire library. All list queries must have pagination (LIMIT + OFFSET or keyset pagination).

**Migration anti-patterns**
- **No `Down()` migration**: a migration without rollback support means every bad deployment must be manually recovered. Non-negotiable: always implement `Down()`.
- **Destructive migration on a live database**: dropping a column or table that is still referenced by the running service version. Always make schema changes backward-compatible with the previous service version first.
- **Cross-service database reads**: Service B directly querying Service A's database tables, bypassing the service API. This creates an invisible coupling that breaks independently when either service changes its schema.
