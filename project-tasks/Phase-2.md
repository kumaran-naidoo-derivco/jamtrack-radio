# Project: 🎵 Jamtrack Radio

## Phase 2: Local Dev Environment — C# + PostgreSQL

**Phase Description**:
Build the local v0.1 MVP — three ASP.NET Core microservices (Identity, Track, Streaming) using Clean Architecture, backed by a locally Dockerised PostgreSQL database, with Dapper for data access and FluentMigrator for schema management. CI is extended to build and test dotnet projects. This phase delivers a fully running local stack before any containerisation or cloud deployment.

The phase follows the full delivery lifecycle: Product Discovery → Feature Discovery (per service) → Development. Tasks 2.3–2.5 produce the foundational docs that inform every subsequent dev task.

**Priority**: High
**Labels**: phase-2, backend, csharp, postgresql, grpc

---

### Task 2.1: Scaffold solution structure and Clean Architecture projects

- **Description**:
  Create the top-level `jamtrack-radio.sln` and all C# project folders following Clean Architecture. Each service gets four layers: `Domain`, `Application`, `Infrastructure`, `Api`. A shared `tests/` folder holds integration test projects for each service.

  **Folder structure to create**:
  ```
  src/
    IdentityService/
      IdentityService.Domain/
      IdentityService.Application/
      IdentityService.Infrastructure/
      IdentityService.Api/
    TrackService/
      TrackService.Domain/
      TrackService.Application/
      TrackService.Infrastructure/
      TrackService.Api/
    StreamingService/
      StreamingService.Domain/
      StreamingService.Application/
      StreamingService.Infrastructure/
      StreamingService.Api/
  tests/
    IdentityService.Tests/
    TrackService.Tests/
    StreamingService.Tests/
  ```

  **Commands (WSL Ubuntu)**:
  ```bash
  # Create solution
  dotnet new sln -n jamtrack-radio

  # Identity Service layers
  dotnet new classlib -o src/IdentityService/IdentityService.Domain
  dotnet new classlib -o src/IdentityService/IdentityService.Application
  dotnet new classlib -o src/IdentityService/IdentityService.Infrastructure
  dotnet new webapi  -o src/IdentityService/IdentityService.Api

  # Track Service layers
  dotnet new classlib -o src/TrackService/TrackService.Domain
  dotnet new classlib -o src/TrackService/TrackService.Application
  dotnet new classlib -o src/TrackService/TrackService.Infrastructure
  dotnet new webapi  -o src/TrackService/TrackService.Api

  # Streaming Service layers
  dotnet new classlib -o src/StreamingService/StreamingService.Domain
  dotnet new classlib -o src/StreamingService/StreamingService.Application
  dotnet new classlib -o src/StreamingService/StreamingService.Infrastructure
  dotnet new webapi  -o src/StreamingService/StreamingService.Api

  # Test projects
  dotnet new xunit -o tests/IdentityService.Tests
  dotnet new xunit -o tests/TrackService.Tests
  dotnet new xunit -o tests/StreamingService.Tests

  # Add all projects to solution
  dotnet sln add $(find src tests -name "*.csproj")

  # Wire up project references (Clean Architecture dependency rule)
  # Application depends on Domain
  dotnet add src/IdentityService/IdentityService.Application reference src/IdentityService/IdentityService.Domain
  # Infrastructure depends on Application
  dotnet add src/IdentityService/IdentityService.Infrastructure reference src/IdentityService/IdentityService.Application
  # Api depends on Application (and Infrastructure for DI wiring)
  dotnet add src/IdentityService/IdentityService.Api reference src/IdentityService/IdentityService.Application
  dotnet add src/IdentityService/IdentityService.Api reference src/IdentityService/IdentityService.Infrastructure
  # Repeat for TrackService and StreamingService...
  ```

  **Add a `.editorconfig`** at the solution root to enforce Microsoft C# style conventions.

  **Expected outcome**: `dotnet build` at the solution root succeeds with zero errors and zero warnings.

- **Labels**: phase-2, backend, csharp, setup
- **Estimated Effort**: Medium
- **Status**: Done
- **Dependencies**: Phase 1 completed

---

### Task 2.2: Set up Claude Code workflows and skills ecosystem

- **Description**:
  Build a comprehensive Claude Code skills and workflows ecosystem that supports the **full development lifecycle** — from initial discovery through post-deployment value measurement. This four-layer system replaces ad-hoc coding assistance with a structured, role-based coaching framework.

  **Architecture — four layers**:

  ```
  Layer 1: Workflows      — PRODUCT-DISCOVERY → FEATURE-DISCOVERY → DEVELOPMENT → MONITORING
  Layer 2: Specialist     — domain-specific skills per workflow step
  Layer 3: Agent Personas — orchestrator skills that activate role + sequence
  Layer 4: Ad-hoc         — standalone skills usable outside formal workflows
  ```

  ---

  **Four workflows** (under `.claude/workflows/`):

  | Workflow | File | Purpose |
  |----------|------|---------|
  | Product Discovery | `PRODUCT-DISCOVERY.md` | Whole-product discovery: requirements → market research → PRD → design system → prototypes → 4 architecture views → sign-off → project plan |
  | Feature Discovery | `DISCOVERY.md` | Per-service discovery: same steps, feature-scoped, loads product baseline |
  | Development | `DEVELOPMENT.md` | Design → Implement → Quality Pass → Review → Test → Deploy Staging → Integration Test → Deploy Prod |
  | Monitoring | `MONITORING.md` | Health → Errors → Performance → Report → Retrospective → Value Report |

  ---

  **Agent Persona skills (6)**:

  | Skill | Agent | Workflow Ownership |
  |-------|-------|--------------------|
  | `/product-manager` | Product Manager | Discovery Steps 1–3 (requirements, market research, PRD) + MONITORING value report |
  | `/product-designer` | Product Designer | Discovery Step 4 (design system, UX research, prototypes) + ad-hoc design-review |
  | `/architect` | Architect | Discovery Steps 5–6 (four architecture views + sign-off) |
  | `/project-manager` | Project Manager | Discovery Step 7 + DEVELOPMENT checkpoint |
  | `/senior-developer` | Senior Developer | DEVELOPMENT Steps 1–5 |
  | `/devops-engineer` | DevOps Engineer | DEVELOPMENT Steps 6–8 + all MONITORING |

  ---

  **Product Designer skills (4)**:

  | Skill | Purpose |
  |-------|---------|
  | `/design-system` | Establishes Jamtrack Radio design language — colours, typography, components, dark theme. Run once at Product Discovery. |
  | `/ux-research` | User journey maps, accessibility checklist, screen inventory. Optional Feature Discovery step 4a. |
  | `/ui-prototype` | Multi-screen HTML prototypes + Mermaid user flow. Uses design system for consistency. |
  | `/design-review` | Ad-hoc post-implementation screen audit against prototypes. UI features only. |

  ---

  **Discovery skills (9)**:

  | Skill | Purpose |
  |-------|---------|
  | `/requirements` | Problem, personas, constraints, success metrics, Value Prediction (financial viability) |
  | `/market-research` | Competitor analysis, positioning map, differentiation opportunities, strategic narrative |
  | `/prd` | Full Product Requirements Document with Business Case |
  | `/software-architect` | Service context diagram, domain model, ADRs, build-vs-buy analysis |
  | `/cloud-architect` | Cloud topology, TCO table (Dev/Staging/Prod + 2×/10× scale), cost optimisation |
  | `/data-architect` | ER diagram, schema ownership, DDL, index strategy, retention/compliance, storage costs |
  | `/arch-security` | Trust boundaries, STRIDE, security controls, OWASP Top 10, cost/risk tradeoffs |
  | `/project-plan` | Creates GitHub milestone + all issues (dev + DevOps + testing) after architect sign-off |

  **Expected outcome**:
  - `ls .claude/skills/` shows all skill directories including the four new Product Designer skills
  - `ls .claude/workflows/` shows 6 files: README.md, PRODUCT-DISCOVERY.md, DISCOVERY.md, DEVELOPMENT.md, MONITORING.md, WORKFLOW.md (retired redirect)
  - Running `/product-designer` activates the Product Designer persona and guides through Steps 4a–4b
  - Running `/design-system` produces `docs/design-system/` with tokens, components, and showcase HTML
  - Product Discovery and Feature Discovery are clearly separated workflows

- **Labels**: phase-2, setup
- **Estimated Effort**: Large
- **Status**: Done
- **Dependencies**: Task 2.1

---

### Task 2.3: Product Discovery — Steps 1–4 (Requirements, Design & Prototypes)

- **Description**:
  Execute the first half of the Product Discovery workflow (`PRODUCT-DISCOVERY.md`) — requirements through to UI prototypes. This produces the product vision, PRD, design system, and all functional HTML screens that the architecture steps in Task 2.4 will be built upon.

  **Workflow to follow**: `.claude/workflows/PRODUCT-DISCOVERY.md`

  **Steps covered by this task**:

  | Step | Skill | Output |
  |------|-------|--------|
  | 1 | `/requirements` | `docs/requirements/jamtrack-radio-requirements.md` |
  | 2 | `/market-research` | `docs/market-research/jamtrack-radio-market-research.md` |
  | 3 | `/prd` | `docs/prds/jamtrack-radio.md` |
  | 4a | `/design-system` | `docs/design-system/jamtrack-radio-design-system.md` + `components.html` |
  | 4b | `/ui-prototype` | `docs/prototypes/jamtrack-radio/` (9 screens + flow.md) |

  **Key learning moments**:
  - How a Product Manager frames a learning project using commercial PM frameworks (Value Prediction, Business Case)
  - How a Product Designer creates a design system before writing any screen-level UI
  - How prototypes are kept functional (JS state machines, social sign-in, 2FA flows) rather than static mockups

  **Expected outcome**:
  - `docs/requirements/`, `docs/market-research/`, `docs/prds/` populated
  - `docs/design-system/` has tokens file + component showcase
  - `docs/prototypes/jamtrack-radio/` has 9 functional HTML screens + flow.md
  - Design system dark teal + neon cyan theme renders correctly in browser

- **Labels**: phase-2, discovery, setup
- **Estimated Effort**: Large
- **Status**: In Progress
- **Dependencies**: Task 2.2

---

### Task 2.4: Product Discovery — Steps 5–7 (Architecture, Sign-off & Project Plan)

- **Description**:
  Execute the second half of the Product Discovery workflow — four architecture views, architect sign-off, and project plan. This produces the system-level technical foundation that all Feature Discovery and development tasks will inherit from.

  **Pre-condition**: Task 2.3 must be complete — PRD and design system must exist before architecture begins.

  **Workflow to follow**: `.claude/workflows/PRODUCT-DISCOVERY.md`

  **Steps covered by this task**:

  | Step | Skill | Output |
  |------|-------|--------|
  | 5a | `/software-architect` | `docs/architecture/jamtrack-radio/software-arch.md` + ADRs in `docs/decisions/` |
  | 5b | `/cloud-architect` | `docs/architecture/jamtrack-radio/cloud-arch.md` |
  | 5c | `/data-architect` | `docs/architecture/jamtrack-radio/data-arch.md` |
  | 5d | `/arch-security` | `docs/architecture/jamtrack-radio/security-arch.md` |
  | 6 | `/architect` | `docs/architecture/jamtrack-radio/architect-signoff.md` |
  | 7 | `/project-plan` | `docs/project-plan/jamtrack-radio-plan.md` + GitHub milestones confirmed |

  **Key learning moments**:
  - How four architecture views (software, cloud, data, security) produce a consistent, cost-aware system design
  - How a Project Manager maps a delivery plan to GitHub milestones and issues
  - How the architect sign-off cross-checks all four views for consistency before development begins

  **Expected outcome**:
  - All 5 architecture files present under `docs/architecture/jamtrack-radio/`
  - At least 3 ADRs in `docs/decisions/`
  - `docs/project-plan/jamtrack-radio-plan.md` links to all GitHub milestones
  - GitHub milestones for Phases 2–7 confirmed to exist

- **Labels**: phase-2, discovery, setup
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.3

---

### Task 2.5: Run Feature Discovery for Identity Service

- **Description**:
  Execute the Feature Discovery workflow (`DISCOVERY.md`) scoped to the Identity Service — the first service to be built. Feature Discovery produces the service-specific requirements, PRD, UX research, prototypes, and architecture that the Senior Developer will load when implementing Task 2.7.

  **Pre-condition**: Task 2.3 (Product Discovery) must be complete — the design system and system-level architecture baseline must exist.

  **Workflow to follow**: `.claude/workflows/DISCOVERY.md`

  **Steps** (run in order):

  | Step | Skill | Output |
  |------|-------|--------|
  | 1 | `/requirements` | `docs/requirements/identity-service-requirements.md` |
  | 2 | `/market-research` | `docs/market-research/identity-service-market-research.md` |
  | 3 | `/prd` | `docs/prds/identity-service.md` |
  | 4a | `/ux-research` *(optional)* | `docs/ux-research/identity-service-ux-research.md` |
  | 4b | `/ui-prototype` | `docs/prototypes/identity-service/` (login, register, error states) |
  | 5a | `/software-architect` | `docs/architecture/identity-service/software-arch.md` |
  | 5b | `/cloud-architect` | `docs/architecture/identity-service/cloud-arch.md` |
  | 5c | `/data-architect` | `docs/architecture/identity-service/data-arch.md` |
  | 5d | `/arch-security` | `docs/architecture/identity-service/security-arch.md` |
  | 6 | `/architect` | `docs/architecture/identity-service/architect-signoff.md` |
  | 7 | `/project-plan` | `docs/project-plan/identity-service-plan.md` + GitHub issues |

  **Key learning moments**:
  - Feature-scoped requirements vs. product-level requirements — what changes, what stays the same
  - How UX research produces a screen inventory that directly drives prototype decisions
  - How feature-level architecture documents stay consistent with the system-level baseline
  - How the Project Manager converts an architect-signed-off design into concrete GitHub issues

  **Expected outcome**:
  - All identity-service docs present under `docs/*/identity-service*`
  - Architecture docs consistent with the system-level baseline from Task 2.3
  - GitHub issues created for Identity Service implementation tasks
  - Task 2.7 (Build Identity Service) can reference `docs/architecture/identity-service/` as design input

- **Labels**: phase-2, discovery, identity-service
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.4

---

### Task 2.6: Run PostgreSQL locally via Docker Compose

- **Description**:
  Create a `docker-compose.yml` at the repo root that runs a PostgreSQL 16 container with a persistent named volume. Add a `.env.local` (gitignored) for credentials. Verify connectivity using `psql` from WSL.

  **Context**: The database schema is informed by the data architecture produced in Task 2.4 (`docs/architecture/jamtrack-radio/data-arch.md`). Load that document before creating the Docker Compose configuration to ensure the database name and user align with what's documented.

  **Files to create**:
  - `docker-compose.yml` — Postgres 16 service, named volume, health check
  - `.env.local` — `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (gitignored)
  - `.env.example` — safe template to commit (no real secrets)

  **Commands (WSL Ubuntu)**:
  ```bash
  # Start the stack
  docker compose up -d

  # Verify Postgres is healthy
  docker compose ps

  # Connect via psql
  psql -h localhost -p 5432 -U jamtrack -d jamtrack_dev

  # Stop when done
  docker compose down
  ```

  **Learning moment**: Docker named volumes persist data between `docker compose down` / `up` cycles. `docker compose down -v` removes the volume — use only when you want a clean slate.

- **Labels**: phase-2, docker, postgresql, setup
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 2.5

---

### Task 2.7: Set up FluentMigrator — initial database schema

- **Description**:
  Create a standalone `src/Migrations/` C# console project that uses FluentMigrator to manage schema migrations. Write the initial migration(s) to create all tables as defined in `docs/architecture/jamtrack-radio/data-arch.md`.

  **Context**: Load `docs/architecture/jamtrack-radio/data-arch.md` and `docs/architecture/identity-service/data-arch.md` before writing migrations. The migration must create all tables documented in the data architecture, not just the ones needed for the first service.

  **Tables to create in the initial migration**:
  - `users` — id (uuid PK), email (unique), password_hash, provider, provider_id, display_name, created_at, updated_at
  - `refresh_tokens` — id (uuid PK), user_id (FK → users), token_hash, expires_at, created_at
  - `tracks` — id (uuid PK), user_id (FK → users), title, artist, genre, bpm, musical_key, duration_seconds, storage_ref, artwork_ref, created_at, updated_at
  - `tags` — id (uuid PK), user_id (FK), name
  - `track_tags` — track_id (FK), tag_id (FK), PK(track_id, tag_id)
  - `playlists` — id (uuid PK), user_id (FK), name, created_at, updated_at
  - `playlist_tracks` — playlist_id (FK), track_id (FK), position, PK(playlist_id, track_id)

  **Commands (WSL Ubuntu)**:
  ```bash
  dotnet new console -o src/Migrations
  dotnet sln add src/Migrations/Migrations.csproj

  # Add FluentMigrator packages
  dotnet add src/Migrations package FluentMigrator
  dotnet add src/Migrations package FluentMigrator.Runner
  dotnet add src/Migrations package FluentMigrator.Runner.Postgres

  # Run migrations
  dotnet run --project src/Migrations -- --connection "Host=localhost;Database=jamtrack_dev;Username=jamtrack;Password=<pwd>"
  ```

  **Expected outcome**: `\dt` in psql shows all tables. Re-running migrations is idempotent (no-op if already applied).

- **Labels**: phase-2, postgresql, migrations
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.6

---

### Task 2.8: Build Identity Service (register, login, JWT)

- **Description**:
  Implement the Identity Service end-to-end using Clean Architecture. Supports email/password registration and login, issuing a signed JWT on success. The internal API is exposed as a gRPC endpoint.

  **Context**: Load the following before implementing:
  - `docs/architecture/identity-service/software-arch.md` — domain model, service boundaries, API contract
  - `docs/architecture/identity-service/data-arch.md` — schema and DDL
  - `docs/architecture/identity-service/security-arch.md` — security controls (BCrypt, RS256 JWT, refresh token hashing)
  - `docs/prds/identity-service.md` — acceptance criteria

  **Domain layer** (`IdentityService.Domain`):
  - `User` entity: Id (Guid), Email, PasswordHash, Provider, ProviderId, DisplayName, CreatedAt, UpdatedAt
  - Domain exceptions: `DuplicateEmailException`, `InvalidCredentialsException`

  **Application layer** (`IdentityService.Application`):
  - `IUserRepository` interface
  - `IRefreshTokenRepository` interface
  - `RegisterUserCommand` + handler
  - `LoginCommand` + handler
  - `ITokenService` interface

  **Infrastructure layer** (`IdentityService.Infrastructure`):
  - `UserRepository` — Dapper implementation of `IUserRepository`
  - `RefreshTokenRepository` — Dapper implementation
  - `JwtTokenService` — `ITokenService` implementation (RS256, System.IdentityModel.Tokens.Jwt)
  - Passwords hashed with BCrypt (`BCrypt.Net-Next`)

  **Api layer** (`IdentityService.Api`):
  - gRPC service definition (`identity.proto`) with `Register` and `Login` RPCs
  - `IdentityGrpcService` mapping proto requests to Application commands
  - DI wiring in `Program.cs`
  - Structured logging with `Serilog` (JSON to console, `traceId` in every log entry)
  - `/health/live` and `/health/ready` endpoints

  **Key packages**:
  - `Grpc.AspNetCore`, `Google.Protobuf`, `Grpc.Tools`
  - `Dapper`, `Npgsql`
  - `BCrypt.Net-Next`
  - `Microsoft.IdentityModel.Tokens`, `System.IdentityModel.Tokens.Jwt`
  - `Serilog.AspNetCore`, `Serilog.Sinks.Console`

  **Expected outcome**: Service starts, registers a user, stores bcrypt-hashed password in `users` table, returns a valid JWT on login.

- **Labels**: phase-2, grpc, identity-service
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.7

---

### Task 2.9: Build Track Service (track metadata CRUD)

- **Description**:
  Implement the Track Service end-to-end using Clean Architecture. Manages track metadata (title, artist, genre, BPM, musical key, duration, file path). Audio file upload (to local disk in this phase) is handled here. Exposed via gRPC.

  **Context**: Load `docs/architecture/jamtrack-radio/software-arch.md` and `docs/architecture/jamtrack-radio/data-arch.md` before implementing.

  **Domain layer** (`TrackService.Domain`):
  - `Track` entity: Id, UserId, Title, Artist, Genre, Bpm, MusicalKey, DurationSeconds, StorageRef, ArtworkRef, CreatedAt, UpdatedAt
  - Domain exceptions: `TrackNotFoundException`

  **Application layer** (`TrackService.Application`):
  - `ITrackRepository` interface, `ITagRepository` interface
  - Use cases: `UploadTrackCommand`, `GetTrackQuery`, `ListTracksQuery`, `DeleteTrackCommand`
  - `IFileStorageService` interface (local disk in this phase, swapped for Azure Blob in Phase 4)

  **Infrastructure layer** (`TrackService.Infrastructure`):
  - `TrackRepository` — Dapper implementation
  - `LocalFileStorageService` — saves uploaded files to a configurable local path

  **Api layer** (`TrackService.Api`):
  - gRPC service definition (`track.proto`) with `UploadTrack`, `GetTrack`, `GetTracksBatch`, `ListTracks`, `DeleteTrack` RPCs
  - `TrackGrpcService`, DI wiring, Serilog, health endpoints

  **Expected outcome**: Can upload a track (metadata + file path), retrieve it by ID, list all tracks for a user, delete a track.

- **Labels**: phase-2, grpc
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.8

---

### Task 2.10: Build Streaming Service (audio file delivery)

- **Description**:
  Implement the Streaming Service, which serves audio files over HTTP using range requests (enables seek/scrub in a browser audio player). This service exposes a REST endpoint — browsers cannot use gRPC directly for media streaming. It calls Track Service (gRPC) to resolve the file path for a given track ID, then streams the file from local disk.

  **Context**: Load `docs/architecture/jamtrack-radio/software-arch.md` and `docs/architecture/jamtrack-radio/data-arch.md` before implementing.

  **Domain layer** (`StreamingService.Domain`):
  - `StreamRequest` value object: TrackId, RequestedRange (start/end bytes)
  - Domain exception: `TrackNotStreamableException`

  **Application layer** (`StreamingService.Application`):
  - `ITrackResolver` interface (gets file path from Track Service)
  - `StreamTrackQuery` + handler

  **Infrastructure layer** (`StreamingService.Infrastructure`):
  - `GrpcTrackResolver` — calls TrackService gRPC to get file path
  - `LocalFileStream` — opens and streams a local file with byte-range support

  **Api layer** (`StreamingService.Api`):
  - REST controller: `GET /stream/{trackId}` with HTTP 206 Partial Content support
  - Sets `Accept-Ranges: bytes`, `Content-Range` headers correctly
  - Serilog, health endpoints

  **Expected outcome**: Hitting `GET /stream/{trackId}` with a `Range: bytes=0-` header returns the audio file in chunks. Test using `curl --range 0-1023 http://localhost:5003/stream/{trackId}`.

- **Labels**: phase-2, grpc
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.9

---

### Task 2.11: Update CI pipeline — dotnet build and test

- **Description**:
  Uncomment and complete the `dotnet` steps in `.github/workflows/ci.yml`. The CI pipeline should restore, build, and run tests on every PR targeting `main`. A failing test blocks the merge.

  **Steps to add/uncomment in ci.yml**:
  1. `actions/setup-dotnet@v4` — set .NET SDK version
  2. `dotnet restore` — restore NuGet packages
  3. `dotnet build --no-restore --configuration Release`
  4. `dotnet test --no-build --configuration Release --logger trx`

  **Expected outcome**: CI `build` check goes green on a passing PR. A PR with a failing test is blocked from merging.

- **Labels**: phase-2, github
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 2.10

---

### Task 2.12: Write integration tests — Identity Service

- **Description**:
  Write integration tests for the Identity Service gRPC endpoints (`Register` and `Login`) using `Microsoft.AspNetCore.Mvc.Testing` (WebApplicationFactory) with a real test PostgreSQL database (running in Docker via `Testcontainers`). Follow the AAA pattern. Cover all significant input/output combinations.

  **Context**: Load `docs/architecture/identity-service/software-arch.md` and `docs/prds/identity-service.md` — every acceptance criterion in the PRD must have a corresponding test case.

  **Test cases to cover**:
  - Register with valid email + password → 201, user stored in DB with hashed password
  - Register with duplicate email → domain error returned
  - Register with invalid email format → validation error
  - Register with weak/empty password → validation error
  - Login with correct credentials → valid JWT returned
  - Login with wrong password → `InvalidCredentialsException`
  - Login with unknown email → `InvalidCredentialsException`
  - JWT contains expected claims (sub, email, exp)

  **Key packages**:
  - `Microsoft.AspNetCore.Mvc.Testing`
  - `Testcontainers.PostgreSql`
  - `FluentAssertions`
  - `Grpc.Net.Client` (for gRPC client in tests)

  **Expected outcome**: `dotnet test tests/IdentityService.Tests` passes all cases. Tests run against a real Postgres container spun up by Testcontainers — no mocking of the DB layer.

- **Labels**: phase-2, postgres, identity-service
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.11

---

### Task 2.13: Write integration tests — Track Service

- **Description**:
  Write integration tests for the Track Service gRPC endpoints using the same pattern as Task 2.11 (WebApplicationFactory + Testcontainers). Cover all CRUD operations and file storage interactions.

  **Test cases to cover**:
  - Upload track with valid metadata + file → stored in DB, file written to disk, track ID returned
  - Upload track with missing required fields → validation error
  - Get track by valid ID → correct metadata returned
  - Get track by unknown ID → `TrackNotFoundException`
  - List tracks for a user → returns correct subset
  - List tracks for a user with no tracks → empty list
  - Delete track by valid ID → removed from DB, file deleted from disk
  - Delete track by unknown ID → `TrackNotFoundException`

  **Expected outcome**: `dotnet test tests/TrackService.Tests` passes all cases against a real Postgres container.

- **Labels**: phase-2, postgres
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.12

---

## ✅ Phase 2 Summary

Phase 2 delivers the **local v0.1 MVP** — three fully functional microservices running on your machine, built on a foundation of proper product and feature discovery.

**Delivery sequence**:
1. **Product Discovery — Steps 1–4** (Task 2.3) → PRD, design system, 9 functional UI prototypes
2. **Product Discovery — Steps 5–7** (Task 2.4) → system-level architecture (4 views), architect sign-off, project plan
3. **Feature Discovery** (Task 2.5) → identity-service PRD, prototypes, service-level architecture, sprint issues
4. **Infrastructure** (Tasks 2.6–2.7) → Postgres + FluentMigrator schema
5. **Services** (Tasks 2.8–2.10) → three microservices implementing the Discovery-defined designs
6. **CI + Tests** (Tasks 2.11–2.13) → green build, integration-tested against real Postgres

| Service | Transport | What it does |
|---|---|---|
| Identity Service | gRPC | Register + login, JWT issuance |
| Track Service | gRPC | Track metadata CRUD + local file storage |
| Streaming Service | REST (HTTP range) | Audio file delivery with seek support |

**Supporting infrastructure**:
- Product and Feature Discovery docs in `docs/`
- Design system in `docs/design-system/`
- System-level and service-level architecture in `docs/architecture/`
- PostgreSQL 16 in Docker Compose
- FluentMigrator for schema management
- Dapper for all DB access
- Serilog structured logging on all services
- Integration tests with real Postgres (Testcontainers)
- CI pipeline builds and tests on every PR

**After Phase 2, you'll have a working music platform — runnable entirely on your local machine — ready to be containerised in Phase 3.**
