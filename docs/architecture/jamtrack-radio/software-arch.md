# Software Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Architect)
**Status**: Accepted
**Skill**: `/software-architect jamtrack-radio` — DISCOVERY Step 5a

---

## 1. System Context Diagram (C4 Level 1)

Shows the system boundary and its relationships with external actors and systems.

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Musician&lt;/b&gt;&lt;br&gt;[Person]&lt;br&gt;Uploads and streams tracks" style="shape=mxgraph.general.user2;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="30" y="270" width="130" height="100" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;Admin&lt;/b&gt;&lt;br&gt;[Person]&lt;br&gt;Monitors and manages platform" style="shape=mxgraph.general.user2;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="30" y="440" width="130" height="100" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;Jamtrack Radio System&lt;/b&gt;" style="swimlane;startSize=30;fillColor=none;strokeColor=#0078D4;fontStyle=1;fontSize=13;rounded=1;" vertex="1" parent="1">
      <mxGeometry x="240" y="220" width="360" height="200" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;API Gateway&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;&lt;br&gt;YARP Reverse Proxy&lt;br&gt;ASP.NET Core 8" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;" vertex="1" parent="4">
      <mxGeometry x="100" y="70" width="160" height="90" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;&lt;&lt;external&gt;&gt;&lt;br&gt;Audio files + artwork" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="750" y="190" width="160" height="80" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;OAuth Providers&lt;/b&gt;&lt;br&gt;&lt;&lt;external&gt;&gt;&lt;br&gt;Google / Apple / Facebook&lt;br&gt;(Phase 4+)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="750" y="310" width="160" height="90" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Azure Key Vault&lt;/b&gt;&lt;br&gt;&lt;&lt;external&gt;&gt;&lt;br&gt;RS256 private key, secrets&lt;br&gt;(Phase 4+)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="750" y="450" width="160" height="80" as="geometry" />
    </mxCell>
    <mxCell id="9" value="HTTPS / REST" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="10" value="HTTPS / REST" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="11" value="Azure Blob SDK&lt;br&gt;Upload / Stream bytes" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="4" target="6" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="12" value="OAuth 2.0 / OIDC" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="4" target="7" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="13" value="Managed Identity" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="4" target="8" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

---

## 2. Container Interaction Diagram (C4 Level 2)

Shows each microservice, its technology, communication protocol, and data ownership. Synchronous gRPC calls are solid arrows; the async Dapr event bus uses dashed arrows through a queue shape annotated `eventually consistent`.

```drawio
<mxGraphModel dx="1554" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1100" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Browser Client&lt;/b&gt;&lt;br&gt;[Browser]&lt;br&gt;JavaScript SPA (Phase 5+)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="660" y="20" width="180" height="70" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;API Gateway&lt;/b&gt;&lt;br&gt;&lt;&lt;component&gt;&gt;&lt;br&gt;YARP Reverse Proxy&lt;br&gt;JWT validation middleware&lt;br&gt;Port: 5000" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1ba1e2;strokeColor=#006EAF;fontColor=#ffffff;" vertex="1" parent="1">
      <mxGeometry x="620" y="140" width="180" height="100" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;Identity Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;&lt;br&gt;Register, Login, TOTP&lt;br&gt;RS256 JWT issuance&lt;br&gt;Port: 5001" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="60" y="320" width="160" height="110" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;Track Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;&lt;br&gt;Track metadata CRUD&lt;br&gt;Tag management&lt;br&gt;Port: 5002" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="290" y="320" width="160" height="110" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;Playlist Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;&lt;br&gt;Playlist CRUD&lt;br&gt;Track ordering&lt;br&gt;Port: 5003" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="620" y="320" width="160" height="110" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;Streaming Service&lt;/b&gt;&lt;br&gt;&lt;&lt;api&gt;&gt; REST&lt;br&gt;HTTP range requests&lt;br&gt;Stateless — no DB&lt;br&gt;Port: 5004" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="860" y="320" width="160" height="110" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Storage Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;&lt;br&gt;Azure Blob abstraction&lt;br&gt;Blob CRUD&lt;br&gt;Port: 5005" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
      <mxGeometry x="1100" y="320" width="160" height="110" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;Identity DB&lt;/b&gt;&lt;br&gt;PostgreSQL 16&lt;br&gt;users, refresh_tokens" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="70" y="510" width="140" height="80" as="geometry" />
    </mxCell>
    <mxCell id="10" value="&lt;b&gt;Track DB&lt;/b&gt;&lt;br&gt;PostgreSQL 16&lt;br&gt;tracks, tags, track_tags" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="300" y="510" width="140" height="80" as="geometry" />
    </mxCell>
    <mxCell id="11" value="&lt;b&gt;Playlist DB&lt;/b&gt;&lt;br&gt;PostgreSQL 16&lt;br&gt;playlists, playlist_tracks" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="630" y="510" width="140" height="80" as="geometry" />
    </mxCell>
    <mxCell id="12" value="&lt;b&gt;Storage DB&lt;/b&gt;&lt;br&gt;PostgreSQL 16&lt;br&gt;storage_objects" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="1">
      <mxGeometry x="1110" y="510" width="140" height="80" as="geometry" />
    </mxCell>
    <mxCell id="13" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;&lt;&lt;external&gt;&gt;&lt;br&gt;Audio + artwork files" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="1100" y="140" width="160" height="80" as="geometry" />
    </mxCell>
    <mxCell id="14" value="&lt;b&gt;Dapr Pub/Sub&lt;/b&gt;&lt;br&gt;&lt;&lt;async&gt;&gt;&lt;br&gt;Redis (Phase 2-3)&lt;br&gt;Azure Service Bus (Phase 4)&lt;br&gt;Topic: track.uploaded&lt;br&gt;&lt;i&gt;eventually consistent&lt;/i&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
      <mxGeometry x="610" y="670" width="210" height="100" as="geometry" />
    </mxCell>
    <mxCell id="15" value="HTTPS" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="3" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="16" value="gRPC" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="17" value="gRPC" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="5" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="18" value="gRPC" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="6" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="19" value="REST / HTTP range" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="7" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="20" value="gRPC" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="3" target="8" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="21" value="SQL / Dapper" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="4" target="9" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="22" value="SQL / Dapper" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="5" target="10" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="23" value="SQL / Dapper" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="6" target="11" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="24" value="SQL / Dapper" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="8" target="12" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="25" value="Azure Blob SDK" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="8" target="13" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="26" value="gRPC: ValidateOwnership" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="7" target="5" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="27" value="publish: TrackUploaded" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="5" target="14" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="28" value="subscribe" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;endArrow=open;" edge="1" source="14" target="8" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

### Service Port Map

| Service | Protocol | Port (local) | Notes |
|---------|----------|-------------|-------|
| API Gateway | REST / HTTPS | 5000 | YARP reverse proxy |
| Identity Service | gRPC | 5001 | |
| Track Service | gRPC | 5002 | |
| Playlist Service | gRPC | 5003 | |
| Streaming Service | REST | 5004 | HTTP range requests |
| Storage Service | gRPC | 5005 | Azure Blob / S3 abstraction |

---

## 3. Domain Model

### Bounded Context: Identity

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Identity Bounded Context&lt;/b&gt;" style="swimlane;startSize=30;fillColor=none;strokeColor=#0078D4;dashed=1;rounded=1;fontStyle=1;fontSize=13;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="940" height="500" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;&lt;Aggregate Root&gt;&gt;&lt;br&gt;&lt;b&gt;User&lt;/b&gt;&lt;hr/&gt;+ Id: Guid&lt;br&gt;+ Email: Email&lt;br&gt;+ PasswordHash: PasswordHash&lt;br&gt;+ DisplayName: string&lt;br&gt;+ TotpSeed: TotpSeed?&lt;br&gt;+ CreatedAt: DateTimeOffset&lt;br&gt;+ IsActive: bool&lt;hr/&gt;+ Create(email, pwd): User&lt;br&gt;+ ValidatePassword(plain): bool&lt;br&gt;+ EnableTotp(seed): void" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="330" y="50" width="250" height="230" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;&lt;Value Object&gt;&gt;&lt;br&gt;&lt;b&gt;Email&lt;/b&gt;&lt;hr/&gt;+ Value: string&lt;hr/&gt;Invariant: RFC 5321 format&lt;br&gt;Immutable after creation" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="40" y="40" width="210" height="120" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;&lt;Value Object&gt;&gt;&lt;br&gt;&lt;b&gt;PasswordHash&lt;/b&gt;&lt;hr/&gt;+ Hash: string&lt;hr/&gt;Invariant: BCrypt cost 12&lt;br&gt;Never stores plaintext" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="40" y="200" width="210" height="120" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;&lt;Value Object&gt;&gt;&lt;br&gt;&lt;b&gt;TotpSeed&lt;/b&gt;&lt;hr/&gt;+ EncryptedSeed: string&lt;hr/&gt;Invariant: AES-256-GCM encrypted&lt;br&gt;Nullable — 2FA optional" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="40" y="360" width="210" height="120" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;&lt;Entity&gt;&gt;&lt;br&gt;&lt;b&gt;RefreshToken&lt;/b&gt;&lt;hr/&gt;+ Id: Guid&lt;br&gt;+ UserId: Guid&lt;br&gt;+ TokenHash: string&lt;br&gt;&lt;i&gt;(SHA-256 — raw token not stored)&lt;/i&gt;&lt;br&gt;+ ExpiresAt: DateTimeOffset&lt;br&gt;+ IsRevoked: bool&lt;hr/&gt;+ Revoke(): void" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="690" y="40" width="220" height="200" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;&lt;Domain Event&gt;&gt;&lt;br&gt;&lt;b&gt;UserRegistered&lt;/b&gt;&lt;hr/&gt;+ UserId: Guid&lt;br&gt;+ Email: string (hashed in logs)&lt;br&gt;+ Timestamp: DateTimeOffset&lt;br&gt;+ Provider: string?" style="swimlane;startSize=23;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;align=left;fontSize=11;" vertex="1" parent="2">
      <mxGeometry x="690" y="280" width="220" height="140" as="geometry" />
    </mxCell>
    <mxCell id="9" value="has" style="endArrow=block;endFill=0;html=1;" edge="1" source="3" target="4" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="10" value="has" style="endArrow=block;endFill=0;html=1;" edge="1" source="3" target="5" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="11" value="has (optional)" style="endArrow=block;endFill=0;html=1;" edge="1" source="3" target="6" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="12" value="1..*" style="endArrow=block;endFill=0;html=1;" edge="1" source="3" target="7" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="13" value="raises" style="endArrow=open;dashed=1;html=1;" edge="1" source="3" target="8" parent="2">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

| Element | Type | Key properties / invariants |
|---------|------|----------------------------|
| `User` | Aggregate root | `Id (Guid)`, `Email (VO)`, `PasswordHash (VO)`, `DisplayName`, `CreatedAt`; email must be unique; password min 8 chars |
| `Email` | Value object | `Value (string)`; must match RFC 5321 format; immutable after creation |
| `PasswordHash` | Value object | `Hash (string)`; BCrypt cost 12; never stores plain text |
| `TotpSeed` | Value object | `EncryptedSeed (string)`; AES-256 encrypted at rest; nullable (2FA optional) |
| `RefreshToken` | Entity | `Id`, `UserId`, `TokenHash`, `ExpiresAt`, `IsRevoked`; stores SHA-256 hash only |
| `UserRegistered` | Domain event | Raised when `User.Create()` succeeds; carries `UserId`, `Email` |
| `UserLoggedIn` | Domain event | Raised on successful authentication; carries `UserId`, `timestamp`, `ip` |

---

### Bounded Context: Track Catalogue

| Element | Type | Key properties / invariants |
|---------|------|----------------------------|
| `Track` | Aggregate root | `Id`, `UserId`, `Title`, `Artist`, `Genre`, `Bpm`, `MusicalKey`, `Duration`, `StorageRef`, `ArtworkRef`, `CreatedAt`; belongs to exactly one user; title required |
| `Bpm` | Value object | `Value (int)`; must be 1–300 |
| `MusicalKey` | Value object | `Value (string)`; validated against 24 major/minor keys |
| `StorageRef` | Value object | `BlobPath (string)`; set by Storage Service after upload completes |
| `Tag` | Entity | `Id`, `Name`, `UserId`; scoped per user; name unique per user |
| `TrackTag` | Association | `TrackId`, `TagId`; many-to-many |
| `TrackUploaded` | Domain event | Raised when `Track.Create()` completes with a valid `StorageRef`; triggers Storage Service processing |
| `TrackDeleted` | Domain event | Raised on `Track.Delete()`; triggers Storage Service blob removal |

---

### Bounded Context: Playlist

| Element | Type | Key properties / invariants |
|---------|------|----------------------------|
| `Playlist` | Aggregate root | `Id`, `UserId`, `Name`, `CreatedAt`; user can have unlimited playlists; name required, unique per user |
| `PlaylistTrack` | Value object within aggregate | `TrackId`, `Position (int)`; position is 1-based; no duplicate `TrackId` within a playlist |

---

### Bounded Context: Audio Delivery (Streaming)

Stateless — no domain entities. Receives a `trackId` + JWT, validates ownership via gRPC call to Track Service, then streams the blob via HTTP range requests. No persistence.

---

### Bounded Context: Storage

| Element | Type | Key properties / invariants |
|---------|------|----------------------------|
| `StorageObject` | Entity | `Id`, `BlobPath`, `ContentType`, `SizeBytes`, `OwnerId`, `CreatedAt` |
| `PresignedUrl` | Value object | `Url`, `ExpiresAt`; short-lived (15 min) URL for direct blob read; never stored |

---

## 4. Component Responsibility Matrix

| Component | Bounded Context | Responsibility | Layer | Owns DB tables |
|-----------|----------------|----------------|-------|----------------|
| `User` | Identity | User invariants, password validation | Domain | — |
| `IUserRepository` | Identity | Persistence contract | Application | — |
| `RegisterUserCommand` | Identity | Register use case + BCrypt hash | Application | — |
| `LoginCommand` | Identity | Credential validation, JWT issuance | Application | — |
| `RefreshTokenCommand` | Identity | Token rotation, revocation | Application | — |
| `TotpService` | Identity | TOTP seed generation, code validation, AES-256 encryption | Application | — |
| `UserRepository` | Identity | Dapper `users` + `refresh_tokens` | Infrastructure | `users`, `refresh_tokens` |
| `IdentityGrpcService` | Identity | gRPC endpoints: Register, Login, Refresh, EnableTotp | Api | — |
| `Track` | Track Catalogue | Track invariants, metadata validation | Domain | — |
| `ITrackRepository` | Track Catalogue | Persistence contract | Application | — |
| `UploadTrackCommand` | Track Catalogue | Create track record, publish `TrackUploaded` | Application | — |
| `TrackRepository` | Track Catalogue | Dapper `tracks`, `tags`, `track_tags` | Infrastructure | `tracks`, `tags`, `track_tags` |
| `TrackGrpcService` | Track Catalogue | gRPC endpoints: Upload, GetById, List, Delete, ManageTags | Api | — |
| `Playlist` | Playlist | Playlist invariants, track ordering | Domain | — |
| `IPlaylistRepository` | Playlist | Persistence contract | Application | — |
| `PlaylistRepository` | Playlist | Dapper `playlists`, `playlist_tracks` | Infrastructure | `playlists`, `playlist_tracks` |
| `PlaylistGrpcService` | Playlist | gRPC: Create, Rename, Delete, AddTrack, RemoveTrack, Reorder | Api | — |
| `StreamController` | Audio Delivery | HTTP range streaming, ownership validation | Api | — |
| `IStorageService` | Storage | Blob CRUD contract | Application | — |
| `AzureBlobStorageService` | Storage | Azure Blob SDK implementation | Infrastructure | `storage_objects` |
| `StorageGrpcService` | Storage | gRPC: Store, Delete, GetPresignedUrl | Api | — |
| `ApiGateway` | — | YARP route config, JWT validation middleware | — | — |

---

## 5. Service Boundary Decisions

**Why is Identity separate from Track?**
- Different rate of change: auth protocols (OAuth, TOTP) evolve independently of track metadata
- Different security posture: Identity handles secrets (signing keys, TOTP seeds), Track does not
- Different scalability: track listing is read-heavy; login is infrequent
- Standard separation: authentication is a classic cross-cutting concern that every service consumes but none should own

**Why is Streaming separate from Track?**
- Different protocol: Streaming uses HTTP range requests (REST); Track uses gRPC
- Different scalability: streaming is bandwidth-intensive; metadata CRUD is request-count-intensive
- Different infrastructure: streaming benefits from a CDN or blob pre-signed URL in Phase 4+; metadata does not
- Stateless: Streaming has no domain state — no repository, no DB — it is a pure API adapter

**Why is Storage separate from Streaming?**
- Different cloud provider abstraction: Storage Service owns the Azure Blob / S3 switch (ADR-005 deferred)
- Separation allows Track Service to publish `TrackUploaded` event and Storage to handle post-processing (transcoding, thumbnail generation) asynchronously without coupling to Track
- Single responsibility: Track knows what was uploaded; Storage knows where it lives

**Why is Playlist separate from Track?**
- Different data ownership: Playlist owns `playlist_tracks` ordering; Track Service owns track metadata. No cross-service table reads permitted.
- Different rate of change: playlist UI interactions (reorder, add/remove) are frequent and independent of track metadata edits

**Why API Gateway rather than service-to-service client calls?**
- Single HTTPS ingress point; all external JWT validation happens here
- YARP is a lightweight reverse proxy native to ASP.NET Core — no external dependency, no Ocelot/Kong overhead at Phase 2

---

## 6. Build vs. Buy Analysis

| Component | Build | Buy / OSS | Decision | Rationale | Cost |
|-----------|-------|-----------|----------|-----------|------|
| Auth tokens | Custom | `Microsoft.AspNetCore.Authentication.JwtBearer` | Buy | Industry standard; well-audited | £0 |
| TOTP | Custom | `Otp.NET` NuGet | Buy | RFC 6238 implementation; not core competency | £0 |
| gRPC framework | Custom | `Grpc.AspNetCore` | Buy | Google-maintained; native .NET support | £0 |
| API Gateway | Custom | YARP (Microsoft) | Buy | ASP.NET Core native, no external service | £0 |
| Service invocation + pub/sub | Custom | Dapr | Buy | Production-grade sidecar pattern; avoids hand-rolled retry/circuit breaker logic | £0 (self-hosted) |
| Migrations | Custom | FluentMigrator | Buy | Fine-grained SQL control; mandatory per constraints | £0 |
| ORM | Dapper | EF Core | Dapper (required) | Mandatory per project constraints; SQL-first | £0 |
| OAuth providers | Custom | Google / Apple / Facebook OAuth SDKs | Buy | Not a differentiating concern | £0 (Phase 4) |
| Blob storage | Custom | Azure Blob SDK / AWS S3 SDK | Buy | Managed service; cost-efficient | ~£2/month |
| Message broker | Custom | Dapr pub/sub (Redis locally, Azure Service Bus Phase 4) | Buy | Dapr abstracts provider; no vendor lock-in | £0 (local) |

---

## 7. Architecture Decision Records

See `docs/decisions/` for the full ADR files. Summary:

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](../../decisions/ADR-001-grpc-internal-communication.md) | gRPC for all internal service-to-service communication | Accepted |
| [ADR-002](../../decisions/ADR-002-rs256-jwt-authentication.md) | RS256 JWT for authentication | Accepted |
| [ADR-003](../../decisions/ADR-003-dapper-data-access.md) | Dapper over EF Core for data access | Accepted |
| [ADR-004](../../decisions/ADR-004-yarp-api-gateway.md) | YARP as the API Gateway | Accepted |
| [ADR-005](../../decisions/ADR-005-dapr-service-invocation.md) | Dapr for service invocation and pub/sub | Accepted |
