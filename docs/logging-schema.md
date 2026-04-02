# Logging Schema

**Date**: 2026-04-01
**Status**: Accepted
**See also**: [ADR-008 — Logging Strategy](decisions/ADR-008-logging-strategy.md)

---

## Required Fields

Every log entry across all Jamtrack Radio services must include these fields:

| Field | Type | Example | Source |
|-------|------|---------|--------|
| `@t` | ISO 8601 UTC | `2026-04-01T12:34:56.789Z` | Serilog (`@t` in Compact JSON) |
| `@l` | string | `Information` | Serilog level |
| `@m` | string | `User registered successfully` | Serilog message template rendered |
| `@mt` | string | `User {UserId} registered` | Serilog message template (raw) |
| `service` | string | `identity-service` | Enriched via `WithProperty("service", ...)` in `Program.cs` |
| `traceId` | string | `00-abc123-def456-01` | W3C `traceparent` — propagated from HTTP/gRPC headers |
| `spanId` | string | `78901234` | W3C trace span |
| `userId` | guid / null | `3fa85f64-...` | Set in application layer when user is authenticated |
| `operation` | string | `RegisterUser` | Set per operation in command/query handlers |
| `elapsedMs` | int | `42` | Measured in application layer with `Stopwatch` |

---

## Per-Service Log Events

### Identity Service

| Event | Level | `operation` | Required fields | Notes |
|-------|-------|-------------|----------------|-------|
| User registered | Information | `RegisterUser` | `userId`, `provider` | Email hashed in `@m` |
| Login success | Information | `Login` | `userId`, `ip`, `provider` | |
| Login failure | Warning | `Login` | `emailHash`, `ip`, `reason` | Raw email never logged |
| Token refreshed | Information | `RefreshToken` | `userId`, `tokenId` | |
| Token revoked | Information | `RevokeToken` | `userId`, `tokenId`, `reason` | |
| TOTP enabled | Information | `EnableTotp` | `userId` | |
| TOTP validation failed | Warning | `ValidateTotp` | `userId`, `ip` | |

### Track Service

| Event | Level | `operation` | Required fields | Notes |
|-------|-------|-------------|----------------|-------|
| Track uploaded | Information | `UploadTrack` | `userId`, `trackId`, `title` | `TrackUploaded` domain event also emitted |
| Track deleted | Information | `DeleteTrack` | `userId`, `trackId` | Soft-delete; `TrackDeleted` event emitted |
| Track listed | Debug | `ListTracks` | `userId`, `count`, `elapsedMs` | Debug only — high volume |
| Tag created | Information | `CreateTag` | `userId`, `tagId`, `name` | |

### Playlist Service

| Event | Level | `operation` | Required fields | Notes |
|-------|-------|-------------|----------------|-------|
| Playlist created | Information | `CreatePlaylist` | `userId`, `playlistId`, `name` | |
| Track added to playlist | Information | `AddTrackToPlaylist` | `userId`, `playlistId`, `trackId` | |
| Track removed from playlist | Information | `RemoveTrackFromPlaylist` | `userId`, `playlistId`, `trackId` | |
| Playlist reordered | Information | `ReorderPlaylist` | `userId`, `playlistId` | |

### Streaming Service

| Event | Level | `operation` | Required fields | Notes |
|-------|-------|-------------|----------------|-------|
| Stream started | Information | `StreamTrack` | `userId`, `trackId`, `ip` | Sample at 10% (high volume) |
| Ownership validation failed | Warning | `StreamTrack` | `userId`, `trackId`, `reason` | Always log (security) |
| Range request served | Debug | `ServeRange` | `trackId`, `rangeStart`, `rangeEnd`, `elapsedMs` | Debug only |

### Storage Service

| Event | Level | `operation` | Required fields | Notes |
|-------|-------|-------------|----------------|-------|
| Object stored | Information | `StoreObject` | `ownerId`, `blobPath`, `sizeBytes` | |
| Object deleted | Information | `DeleteObject` | `ownerId`, `blobPath` | |
| Presigned URL generated | Debug | `GetPresignedUrl` | `ownerId`, `blobPath`, `expiresAt` | Debug only |

---

## PII Rules

| Data | Rule |
|------|------|
| Email address | **Never log raw email.** Hash with SHA-256 and log as `emailHash` |
| Password / token | **Never log.** Throw an exception if this is attempted |
| TOTP seed | **Never log** |
| IP address | Log as `ip` — acceptable for security audit; no hashing required |
| User ID (GUID) | Log freely — not PII on its own |

---

## Serilog Configuration Template

Add to every service's `Program.cs`:

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("Grpc", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithProperty("service", "identity-service") // change per service
    .Enrich.WithProperty("environment", builder.Environment.EnvironmentName)
    .WriteTo.Console(new CompactJsonFormatter())        // Phase 2
    // Phase 4+: .WriteTo.Elasticsearch(...)
    .CreateLogger();

builder.Host.UseSerilog();
```

### PII masking (add to all services)

```csharp
// Helper — add to a static utility class
private static string HashEmail(string email)
{
    var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(email.ToLowerInvariant()));
    return Convert.ToHexString(bytes)[..16]; // first 16 hex chars for readability
}
```

---

## Sampling Policy (Phase 4+)

| Condition | Sample rate |
|-----------|-------------|
| `Information` on stream endpoints | 10% |
| `Information` on all other endpoints | 100% |
| `Warning` | 100% |
| `Error` / `Fatal` | 100% |
| Security events (login failure, token revoke) | 100% always |

---

## Retention (ELK ILM Policy)

| Index | Hot retention | Delete after |
|-------|--------------|-------------|
| Application logs | 7 days | 30 days |
| Security audit logs | 30 days hot | 90 days total |
| Stream analytics | Forwarded to ClickHouse | 12 months (TTL) |
