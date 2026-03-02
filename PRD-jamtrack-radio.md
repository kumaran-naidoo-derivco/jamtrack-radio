# PRD: Jamtrack Radio

## 1. Overview

Jamtrack Radio is a self-hosted music streaming platform for solo musicians and hobbyists to upload, organise, and stream their personal jam tracks. It is built as a cloud-native application using ASP.NET Core microservices, deployed via Docker and Kubernetes, and hosted on Azure with AWS as a secondary target. The platform serves both as a functional product and as a hands-on vehicle for learning modern DevOps and cloud-native development practices.

---

## 2. Problem Statement

Musicians who record jam sessions, practice tracks, or personal compositions have no good self-hosted option to store, organise, and stream their own music. Consumer platforms (Spotify, SoundCloud) are not designed for private personal libraries with structured metadata like BPM, musical key, and genre tagging. A solo musician needs a private, self-controlled platform where they can upload tracks, apply rich metadata, organise into playlists, and stream from any device — without relying on third-party hosting.

---

## 3. Goals

- Allow a solo musician to register, log in, and maintain a private music library
- Support track upload with rich musical metadata (title, artist, genre, BPM, key, tags, artwork)
- Enable playlist creation and management for organising tracks
- Provide low-latency audio streaming via HTTP range requests (progressive streaming)
- Deploy the platform as a cloud-native application runnable locally, on Azure, and on AWS
- Serve as a practical learning system covering microservices, containers, K8s, CI/CD, and observability

---

## 4. Non-Goals

- **No social features** — no sharing, following, or public profiles in this version
- **No music discovery** — no recommendations, radio, or curated content
- **No DRM or licensing** — tracks are assumed to be owned by the uploader
- **No real-time collaboration** — no shared playlists or multi-user editing
- **No mobile native apps** — browser-based only for now; React/Blazor frontend is deferred
- **No payments or subscriptions** — platform is self-hosted and free to the operator

---

## 5. User Stories

```
As a solo musician, I want to create an account using my email or an OAuth provider
(Google, Apple, Facebook), so that I can access my personal music library securely.

As a solo musician, I want to log in and have my session persisted across devices,
so that I don't have to re-authenticate frequently.

As a solo musician, I want to upload an audio track with metadata (title, genre, BPM,
key, tags) and cover artwork, so that my library is organised and visually browsable.

As a solo musician, I want to create and manage playlists,
so that I can group tracks by mood, session type, or project.

As a solo musician, I want to stream a track directly in the browser without downloading it,
so that I can listen on any device instantly.

As a solo musician, I want to tag tracks with custom labels and filter by those tags,
so that I can quickly find the track I'm looking for.
```

---

## 6. Functional Requirements

### Authentication & Identity
- **MUST** support account registration via email and password
- **MUST** support OAuth 2.0 login via Google, Apple, and Facebook
- **MUST** issue JWT access tokens and refresh tokens on login
- **MUST** enforce token expiry and refresh flows
- **SHOULD** support password reset via email

### Track Management
- **MUST** allow authenticated users to upload audio files (MP3, WAV, FLAC)
- **MUST** store track metadata: title, artist, genre, BPM, musical key, duration, upload date
- **MUST** allow users to attach cover artwork (JPG, PNG) to a track
- **MUST** support custom tags per track (e.g. "blues", "practice", "session-2025")
- **MUST** allow users to edit and delete their own tracks
- **SHOULD** extract duration and basic audio properties automatically on upload

### Playlist Management
- **MUST** allow users to create, rename, and delete playlists
- **MUST** allow tracks to be added to and removed from a playlist
- **MUST** support ordered tracks within a playlist
- **SHOULD** allow a track to exist in multiple playlists

### Streaming
- **MUST** support audio streaming via HTTP range requests (enables seek and progressive load)
- **MUST** restrict streaming to authenticated and authorised users only
- **SHOULD** support multiple audio quality levels (original + compressed alternative)

### Tagging & Discovery
- **MUST** support user-defined tags on tracks
- **MUST** allow filtering the track library by one or more tags
- **SHOULD** support search by title, artist, genre, or tag

---

## 7. Non-Functional Requirements

### Performance
- Track streaming must begin playback within **2 seconds** on a standard broadband connection
- Track upload acknowledgement (metadata saved, file accepted) within **5 seconds** for files up to 100MB
- API responses for playlist and track listing under **200ms** at p95

### Scalability
- Initial target: support a single user library of up to **10,000 tracks**
- Designed to scale horizontally — each microservice deployable as multiple replicas in K8s
- Blob storage (Azure Blob / S3) used for audio and artwork to decouple storage scaling from compute

### Reliability
- Target **99.9% uptime** for streaming and auth services
- Track uploads must be idempotent — retrying a failed upload must not create duplicates
- Failed uploads must not leave orphaned files in blob storage

### Security
- All API traffic over **HTTPS**
- JWT tokens signed with RS256; private key managed via secrets (K8s Secrets / Azure Key Vault)
- OAuth tokens must never be stored — exchange for internal JWT immediately
- Audio files and artwork accessible only via pre-signed URLs or authenticated endpoints
- User data isolated — a user can only access their own tracks and playlists

### Observability
- Structured JSON logging on all services (correlated by `traceId`)
- Metrics collected via ELK Stack and ClickStack
- Distributed tracing across service-to-service calls (via Dapr)
- Health check endpoints (`/health/live`, `/health/ready`) on every service

---

## 8. Technical Considerations

### Microservices Breakdown

| Service | Responsibility | Internal API |
|---------|---------------|-------------|
| Identity Service | Registration, login, OAuth, JWT issuance | gRPC |
| Track Service | Track metadata CRUD, tag management | gRPC |
| Playlist Service | Playlist CRUD, track ordering | gRPC |
| Streaming Service | Audio file delivery via HTTP range requests | REST (HTTP) |
| Storage Service | Blob upload/download abstraction (Azure Blob / S3) | gRPC |
| API Gateway | External-facing entry point, routing, auth enforcement | REST (HTTPS) |

### Data Model (PostgreSQL)
- `users` — id, email, provider, created_at
- `tracks` — id, user_id, title, artist, genre, bpm, musical_key, duration, storage_ref, artwork_ref, created_at
- `tags` — id, name, user_id
- `track_tags` — track_id, tag_id
- `playlists` — id, user_id, name, created_at
- `playlist_tracks` — playlist_id, track_id, position

### Infrastructure
- **Dapper** used for all database access (SQL-first micro-ORM)
- **FluentMigrator** used for schema migrations (versioned, code-defined migration scripts)
- **Dapr** used for service invocation and pub/sub (e.g. "track uploaded" event triggers storage processing)
- **Docker Compose** for local development
- **Kubernetes + Helm** for staging and production deployments
- **Terraform** for provisioning Azure / AWS infrastructure (blob storage, K8s cluster, DNS)
- **GitHub Actions** for CI/CD — build, test, container image push, Helm deploy

---

## 9. Phasing / Milestones

| Milestone | Scope | Maps to |
|-----------|-------|---------|
| v0.1 — Local MVP | Identity service (email auth only), Track service (upload + metadata), basic streaming, PostgreSQL | Phase 2 |
| v0.2 — Containerised | All services in Docker Compose, Playlist service, tag filtering | Phase 3 |
| v0.3 — Cloud (Azure) | K8s on AKS, Terraform infra, Azure Blob Storage, OAuth login | Phase 4 |
| v0.4 — Multi-cloud | AWS deployment (EKS + S3), Terraform modules for both clouds | Phase 5 |
| v0.5 — Observable | ELK Stack + ClickStack integrated, structured logging, dashboards | Phase 6 |
| v1.0 — Complete | Full documentation, architecture diagrams, packaging | Phase 7 |

---

## 10. Open Questions

- **OAuth provider setup**: Apple OAuth requires a paid Apple Developer account — confirm availability before Phase 4
- **Frontend**: React vs Blazor — decision deferred, but API must be frontend-agnostic from day one
- **Audio transcoding**: Should the platform transcode uploads to a standard format (e.g. MP3 320kbps)? Requires a transcoding job/worker
- **Storage cost model**: Azure Blob vs S3 pricing for audio at scale — evaluate during Phase 4/5
- **Search**: Full-text search on track metadata — PostgreSQL `tsvector` sufficient, or introduce Elasticsearch from ELK?

---

## 11. Success Metrics

- A track can be uploaded, tagged, added to a playlist, and streamed end-to-end within **5 minutes** of account creation
- Streaming latency (time to first byte) is under **2 seconds** for 95% of requests in production
- All services pass health checks and emit structured logs visible in the ELK dashboard
- Zero data leakage between users — verified by integration tests asserting cross-user access returns `403`
