# Data Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Data Architect)
**Status**: Accepted
**Skill**: `/data-architect jamtrack-radio` — DISCOVERY Step 5c
**Inputs**: `software-arch.md` (6 bounded contexts), `jamtrack-radio-requirements.md` (GDPR, 99.9% uptime, idempotent uploads)

---

## 1. ER Diagram

Full entity-relationship diagram across all services. Each service's tables are shown within a dashed ownership boundary — no cross-boundary foreign keys.

> **Diagram**: [er-diagram.drawio](diagrams/er-diagram.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_

### Schema — Identity Service

```sql
-- users
id             uuid          PRIMARY KEY
email          varchar(254)  NOT NULL UNIQUE
display_name   varchar(100)  NOT NULL
password_hash  varchar(255)  NOT NULL            -- BCrypt hash, nullable if OAuth-only user
oauth_provider varchar(50)   NULL                -- 'google' | 'apple' | 'facebook' | NULL
oauth_subject  varchar(255)  NULL                -- provider sub claim
totp_seed_enc  varchar(512)  NULL                -- AES-256 encrypted TOTP seed; NULL = 2FA disabled
created_at     timestamptz   NOT NULL DEFAULT now()
updated_at     timestamptz   NOT NULL DEFAULT now()
is_active      boolean       NOT NULL DEFAULT true

-- refresh_tokens
id             uuid          PRIMARY KEY
user_id        uuid          NOT NULL REFERENCES users(id) ON DELETE CASCADE
token_hash     varchar(512)  NOT NULL UNIQUE     -- SHA-256 hash of the raw token
expires_at     timestamptz   NOT NULL
created_at     timestamptz   NOT NULL DEFAULT now()
is_revoked     boolean       NOT NULL DEFAULT false
```

### Schema — Track Service

```sql
-- tracks
id           uuid          PRIMARY KEY
user_id      uuid          NOT NULL              -- NOT a FK — cross-service reference by value
title        varchar(200)  NOT NULL
artist       varchar(200)  NULL
genre        varchar(100)  NULL
bpm          smallint      NULL                  -- 1–300
musical_key  varchar(10)   NULL                  -- e.g. 'Am', 'C#maj'
duration_sec integer       NULL                  -- extracted on upload
storage_ref  varchar(500)  NULL                  -- set by Storage Service after blob confirmed
artwork_ref  varchar(500)  NULL
created_at   timestamptz   NOT NULL DEFAULT now()
updated_at   timestamptz   NOT NULL DEFAULT now()
deleted_at   timestamptz   NULL                  -- soft-delete

-- tags
id         uuid          PRIMARY KEY
name       varchar(100)  NOT NULL
user_id    uuid          NOT NULL
created_at timestamptz   NOT NULL DEFAULT now()
UNIQUE (name, user_id)

-- track_tags
track_id   uuid  NOT NULL REFERENCES tracks(id) ON DELETE CASCADE
tag_id     uuid  NOT NULL REFERENCES tags(id)   ON DELETE CASCADE
PRIMARY KEY (track_id, tag_id)
```

### Schema — Playlist Service

```sql
-- playlists
id         uuid          PRIMARY KEY
user_id    uuid          NOT NULL              -- cross-service reference by value
name       varchar(200)  NOT NULL
created_at timestamptz   NOT NULL DEFAULT now()
updated_at timestamptz   NOT NULL DEFAULT now()
UNIQUE (user_id, name)

-- playlist_tracks
playlist_id uuid     NOT NULL REFERENCES playlists(id) ON DELETE CASCADE
track_id    uuid     NOT NULL                           -- cross-service reference by value
position    smallint NOT NULL                           -- 1-based ordering
PRIMARY KEY (playlist_id, track_id)
```

### Schema — Storage Service

```sql
-- storage_objects
id           uuid          PRIMARY KEY
owner_id     uuid          NOT NULL              -- cross-service reference by value (userId)
blob_path    varchar(500)  NOT NULL UNIQUE        -- full Azure Blob or S3 path
content_type varchar(100)  NOT NULL
size_bytes   bigint        NOT NULL
created_at   timestamptz   NOT NULL DEFAULT now()
deleted_at   timestamptz   NULL
```

---

## 2. Schema Ownership Matrix

| Table | Owned by | Read by | Cross-service rule |
|-------|----------|---------|-------------------|
| `users` | Identity Service | Identity Service only | Track/Playlist reference `user_id` by UUID value — never a FK |
| `refresh_tokens` | Identity Service | Identity Service only | Purge expired tokens nightly |
| `tracks` | Track Service | Track Service only | Streaming Service validates ownership via gRPC call to Track Service |
| `tags` | Track Service | Track Service only | |
| `track_tags` | Track Service | Track Service only | |
| `playlists` | Playlist Service | Playlist Service only | Playlist stores `track_id` as a reference value — Track metadata fetched via gRPC |
| `playlist_tracks` | Playlist Service | Playlist Service only | |
| `storage_objects` | Storage Service | Storage Service only | Track Service sets `storage_ref` after receiving `StorageObjectCreated` event |

**Rule**: No service may query another service's database table directly. All cross-service data access goes through the owning service's gRPC API or Dapr pub/sub event.

---

## 3. Index Strategy

| Table | Index name | Columns | Type | Rationale |
|-------|-----------|---------|------|-----------|
| `users` | `idx_users_email` | `email` | UNIQUE B-tree | Login lookup by email |
| `users` | `idx_users_oauth` | `oauth_provider, oauth_subject` | B-tree | OAuth callback lookup |
| `refresh_tokens` | `idx_rt_user_id` | `user_id` | B-tree | Revoke all tokens for a user |
| `refresh_tokens` | `idx_rt_expires_at` | `expires_at` | B-tree | Nightly purge of expired tokens |
| `refresh_tokens` | `idx_rt_token_hash` | `token_hash` | UNIQUE B-tree | Token validation lookup |
| `tracks` | `idx_tracks_user_id` | `user_id` | B-tree | Library listing for a user |
| `tracks` | `idx_tracks_deleted_at` | `deleted_at` WHERE `deleted_at IS NULL` | Partial B-tree | Active-only queries |
| `tracks` | `idx_tracks_genre` | `genre` | B-tree | Filter by genre |
| `tracks` | `idx_tracks_bpm` | `bpm` | B-tree | Filter by BPM range |
| `tracks` | `idx_tracks_title_trgm` | `title gin_trgm_ops` | GIN trigram | Full-text title search (`pg_trgm`) |
| `tags` | `idx_tags_user_id` | `user_id` | B-tree | Tag list per user |
| `track_tags` | `idx_tt_tag_id` | `tag_id` | B-tree | FK index (PostgreSQL does not auto-index FKs) |
| `playlists` | `idx_playlists_user_id` | `user_id` | B-tree | Playlist listing per user |
| `playlist_tracks` | `idx_pt_playlist_id` | `playlist_id` | B-tree | Ordered tracks in a playlist |
| `storage_objects` | `idx_so_owner_id` | `owner_id` | B-tree | Storage audit per user |

---

## 4. Data Flow Diagram

Shows the complete track upload flow — synchronous write path (solid arrows) and asynchronous `TrackUploaded` event path (dashed arrows, `eventually consistent`).

> **Diagram**: [data-flow.drawio](diagrams/data-flow.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_

---

## 5. FluentMigrator Migration Outline

Migration timestamp convention: `YYYYMMDDHHmmss` (e.g. `20260322120000`).

| Migration | Timestamp | Description |
|-----------|-----------|-------------|
| `CreateUsers` | 20260322120001 | `users` table + `idx_users_email` |
| `CreateRefreshTokens` | 20260322120002 | `refresh_tokens` table + indexes |
| `CreateTracks` | 20260322120003 | `tracks` table + indexes |
| `CreateTagsAndTrackTags` | 20260322120004 | `tags`, `track_tags` + indexes |
| `CreatePlaylists` | 20260322120005 | `playlists` + `playlist_tracks` + indexes |
| `CreateStorageObjects` | 20260322120006 | `storage_objects` + indexes |
| `EnablePgTrgmExtension` | 20260322120000 | `CREATE EXTENSION IF NOT EXISTS pg_trgm` — runs first |

Every migration has a `Down()` method. `EnablePgTrgmExtension` drops the extension in `Down()` only if no other indexes use it.

---

## 6. Observability Events

| Event | When emitted | Key fields | Destination |
|-------|-------------|------------|-------------|
| `user.registered` | Account created | `userId`, `email` (hashed), `provider`, `timestamp` | Serilog → ELK |
| `user.login_success` | Successful login | `userId`, `timestamp`, `ip`, `provider` | Serilog → ELK |
| `user.login_failed` | Failed login | `email` (hashed), `timestamp`, `ip`, `reason` | Serilog → ELK (security alert) |
| `user.totp_enabled` | 2FA enabled | `userId`, `timestamp` | Serilog → ELK |
| `token.refreshed` | Token refreshed | `userId`, `tokenId`, `timestamp` | Serilog → ELK |
| `track.uploaded` | Track record created | `trackId`, `userId`, `title`, `timestamp` | Dapr pub/sub + Serilog |
| `track.deleted` | Track soft-deleted | `trackId`, `userId`, `timestamp` | Dapr pub/sub + Serilog |
| `stream.started` | Playback started | `trackId`, `userId`, `timestamp`, `ip` | Serilog → ELK |
| `playlist.created` | Playlist created | `playlistId`, `userId`, `name`, `timestamp` | Serilog → ELK |
| `storage.object_stored` | Blob confirmed in storage | `blobPath`, `sizeBytes`, `timestamp` | Serilog → ELK |

---

## 7. Data Retention & Compliance

| Data category | Retention period | Deletion mechanism | Compliance note |
|--------------|-----------------|-------------------|--------------------|
| User accounts | Until deletion request | Soft-delete → hard-delete after 30 days | GDPR Article 17 — right to erasure |
| Refresh tokens | 90 days or until revoked | Nightly purge job on `expires_at` | Revoke all on logout or password change |
| Audio tracks (metadata) | Until user deletes | Soft-delete (`deleted_at`) → hard-delete + blob removal after 30 days | User owns their data |
| Audio files (blobs) | Until track hard-deleted | Storage Service deletes blob on `TrackDeleted` event processing | |
| Login attempt logs | 90 days | ELK ILM policy | Security audit trail |
| Stream events | 12 months | ClickHouse TTL policy (`toDate(timestamp)`) | Usage analytics |
| Email addresses | Hashed in all logs | `Serilog.Destructuring` — never log raw email | GDPR — email is PII |

---

## 8. Storage Cost Estimation

| Data store | Estimated size Year 1 | Growth rate | Monthly cost (Phase 4+) | Notes |
|------------|----------------------|-------------|------------------------|-------|
| PostgreSQL — all services | ~2 GB | +15%/month | ~£35 (Flex B2ms staging) / ~£277 (D4s prod) | Small relational dataset |
| Azure Blob — audio files (MP3/WAV/FLAC) | ~100 GB | +20%/month | ~£2 (LRS Hot) | Main storage cost driver |
| Azure Blob — artwork (JPG/PNG) | ~5 GB | +20%/month | ~£0.10 | |
| ELK indices (structured logs) | ~2 GB/day staging / ~5 GB/day prod | Constant | ~£46 staging / ~£345 prod | Set 30-day hot retention from day one |
| ClickHouse (stream events, Phase 6) | ~50 GB/year | Constant | ~£10 (AKS-hosted) | 10–100× cheaper than Elasticsearch for time-series |
