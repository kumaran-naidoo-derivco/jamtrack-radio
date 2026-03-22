# Data Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Data Architect)
**Status**: Accepted
**Skill**: `/data-architect jamtrack-radio` — DISCOVERY Step 5c
**Inputs**: `software-arch.md` (6 bounded contexts), `jamtrack-radio-requirements.md` (GDPR, 99.9% uptime, idempotent uploads)

---

## 1. ER Diagram

Full entity-relationship diagram across all services. Each service's tables are shown within a dashed ownership boundary — no cross-boundary foreign keys.

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1554" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Identity Service&lt;/b&gt;" style="swimlane;startSize=25;fillColor=#E3F2FD;strokeColor=#0078D4;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="380" height="420" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;users&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;email: varchar(254) UNIQUE&lt;br&gt;display_name: varchar(100)&lt;br&gt;password_hash: varchar(255)&lt;br&gt;oauth_provider: varchar(50)?&lt;br&gt;oauth_subject: varchar(255)?&lt;br&gt;totp_seed_enc: varchar(512)?&lt;br&gt;created_at: timestamptz&lt;br&gt;updated_at: timestamptz&lt;br&gt;is_active: boolean" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="20" y="35" width="340" height="180" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;refresh_tokens&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;&lt;b&gt;FK&lt;/b&gt; user_id: uuid → users(id)&lt;br&gt;token_hash: varchar(512) UNIQUE&lt;br&gt;expires_at: timestamptz&lt;br&gt;created_at: timestamptz&lt;br&gt;is_revoked: boolean" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="20" y="250" width="340" height="140" as="geometry" />
    </mxCell>
    <mxCell id="5" value="1" style="resizable=0;html=1;align=left;verticalAlign=bottom;" connectable="0" vertex="1" parent="3">
      <mxGeometry x="1" y="1" relative="1" as="geometry"><Array as="sourcePoint" /></mxGeometry>
    </mxCell>
    <mxCell id="6" value="FK CASCADE" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=ERmanyToOne;startArrow=ERmandOne;" edge="1" source="3" target="4" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;Track Service&lt;/b&gt;" style="swimlane;startSize=25;fillColor=#E8F5E9;strokeColor=#2E7D32;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="440" y="20" width="380" height="580" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;tracks&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;user_id: uuid &lt;i&gt;(value ref — no FK)&lt;/i&gt;&lt;br&gt;title: varchar(200)&lt;br&gt;artist: varchar(200)?&lt;br&gt;genre: varchar(100)?&lt;br&gt;bpm: smallint?&lt;br&gt;musical_key: varchar(10)?&lt;br&gt;duration_sec: integer?&lt;br&gt;storage_ref: varchar(500)?&lt;br&gt;artwork_ref: varchar(500)?&lt;br&gt;created_at: timestamptz&lt;br&gt;updated_at: timestamptz&lt;br&gt;deleted_at: timestamptz? &lt;i&gt;(soft-delete)&lt;/i&gt;" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;" vertex="1" parent="7">
      <mxGeometry x="20" y="35" width="340" height="230" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;tags&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;name: varchar(100)&lt;br&gt;user_id: uuid&lt;br&gt;created_at: timestamptz&lt;br&gt;&lt;i&gt;UNIQUE(name, user_id)&lt;/i&gt;" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;" vertex="1" parent="7">
      <mxGeometry x="20" y="295" width="340" height="120" as="geometry" />
    </mxCell>
    <mxCell id="10" value="&lt;b&gt;track_tags&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;FK&lt;/b&gt; track_id: uuid → tracks(id)&lt;br&gt;&lt;b&gt;FK&lt;/b&gt; tag_id: uuid → tags(id)&lt;br&gt;&lt;b&gt;PK&lt;/b&gt;(track_id, tag_id)" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;" vertex="1" parent="7">
      <mxGeometry x="20" y="445" width="340" height="100" as="geometry" />
    </mxCell>
    <mxCell id="11" value="CASCADE" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmanyToOne;startArrow=ERmandOne;" edge="1" source="8" target="10" parent="7">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="12" value="CASCADE" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmanyToOne;startArrow=ERmandOne;" edge="1" source="9" target="10" parent="7">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="13" value="&lt;b&gt;Playlist Service&lt;/b&gt;" style="swimlane;startSize=25;fillColor=#FFF3E0;strokeColor=#E65100;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="860" y="20" width="380" height="380" as="geometry" />
    </mxCell>
    <mxCell id="14" value="&lt;b&gt;playlists&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;user_id: uuid &lt;i&gt;(value ref — no FK)&lt;/i&gt;&lt;br&gt;name: varchar(200)&lt;br&gt;created_at: timestamptz&lt;br&gt;updated_at: timestamptz&lt;br&gt;&lt;i&gt;UNIQUE(user_id, name)&lt;/i&gt;" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;" vertex="1" parent="13">
      <mxGeometry x="20" y="35" width="340" height="150" as="geometry" />
    </mxCell>
    <mxCell id="15" value="&lt;b&gt;playlist_tracks&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;FK&lt;/b&gt; playlist_id: uuid → playlists(id)&lt;br&gt;track_id: uuid &lt;i&gt;(value ref — no FK)&lt;/i&gt;&lt;br&gt;position: smallint &lt;i&gt;(1-based)&lt;/i&gt;&lt;br&gt;&lt;b&gt;PK&lt;/b&gt;(playlist_id, track_id)" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;" vertex="1" parent="13">
      <mxGeometry x="20" y="220" width="340" height="120" as="geometry" />
    </mxCell>
    <mxCell id="16" value="CASCADE" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmanyToOne;startArrow=ERmandOne;" edge="1" source="14" target="15" parent="13">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="17" value="&lt;b&gt;Storage Service&lt;/b&gt;" style="swimlane;startSize=25;fillColor=#F3E5F5;strokeColor=#7B1FA2;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="860" y="440" width="380" height="200" as="geometry" />
    </mxCell>
    <mxCell id="18" value="&lt;b&gt;storage_objects&lt;/b&gt;&lt;hr/&gt;&lt;b&gt;PK&lt;/b&gt; id: uuid&lt;br&gt;owner_id: uuid &lt;i&gt;(value ref — no FK)&lt;/i&gt;&lt;br&gt;blob_path: varchar(500) UNIQUE&lt;br&gt;content_type: varchar(100)&lt;br&gt;size_bytes: bigint&lt;br&gt;created_at: timestamptz&lt;br&gt;deleted_at: timestamptz?" style="swimlane;startSize=23;whiteSpace=wrap;html=1;align=left;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;" vertex="1" parent="17">
      <mxGeometry x="20" y="35" width="340" height="145" as="geometry" />
    </mxCell>
    <mxCell id="19" value="&lt;i&gt;UUID value ref&lt;br&gt;(no relational FK)&lt;/i&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;dashed=1;fontSize=10;" vertex="1" parent="1">
      <mxGeometry x="430" y="480" width="120" height="50" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

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

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Client&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="40" y="200" width="120" height="60" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;API Gateway&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;&lt;br&gt;YARP" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;" vertex="1" parent="1">
      <mxGeometry x="240" y="190" width="130" height="80" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;Track Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="460" y="100" width="130" height="70" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;tracks DB&lt;/b&gt;&lt;br&gt;PostgreSQL" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="680" y="90" width="130" height="80" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;Storage Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="460" y="330" width="130" height="70" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;storage_objects DB&lt;/b&gt;&lt;br&gt;PostgreSQL" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="680" y="325" width="140" height="80" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;&lt;&lt;external&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="900" y="320" width="130" height="70" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;Dapr Pub/Sub&lt;/b&gt;&lt;br&gt;&lt;&lt;async&gt;&gt;&lt;br&gt;Topic: track.uploaded" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
      <mxGeometry x="660" y="200" width="160" height="80" as="geometry" />
    </mxCell>
    <mxCell id="10" value="1. REST: POST /tracks" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="3" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="11" value="2. gRPC: UploadTrack" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="12" value="3. SQL: INSERT track (storage_ref=NULL)" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="4" target="5" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="13" value="4. gRPC: Store (blob bytes)" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="6" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="14" value="5. SDK: UploadBlob" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="6" target="8" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="15" value="6. SQL: INSERT storage_objects" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="6" target="7" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="16" value="7. publish: TrackUploaded" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="4" target="9" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="17" value="8. subscribe: StorageObjectCreated&lt;br&gt;&lt;i&gt;eventually consistent&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="9" target="6" parent="1">
      <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="740" y="440" /></Array></mxGeometry>
    </mxCell>
    <mxCell id="18" value="9. gRPC: SetStorageRef&lt;br&gt;&lt;i&gt;(async callback)&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="6" target="4" parent="1">
      <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="525" y="260" /></Array></mxGeometry>
    </mxCell>
    <mxCell id="19" value="10. SQL: UPDATE tracks SET storage_ref" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="4" target="5" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

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
