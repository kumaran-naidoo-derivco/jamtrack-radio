# Project: 🎵 Jamtrack Radio

## Phase 2: Local Dev Environment — C# + PostgreSQL

**Phase Description**:
Build the local v0.1 MVP — three ASP.NET Core microservices (Identity, Track, Streaming) using Clean Architecture, backed by a locally Dockerised PostgreSQL database, with Dapper for data access and FluentMigrator for schema management. CI is extended to build and test dotnet projects. This phase produces a fully running local stack before any containerisation or cloud deployment.

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
- **Status**: Todo
- **Dependencies**: Phase 1 completed

---

### Task 2.2: Run PostgreSQL locally via Docker Compose

- **Description**:
  Create a `docker-compose.yml` at the repo root that runs a PostgreSQL 16 container with a persistent named volume. Add a `.env.local` (gitignored) for credentials. Verify connectivity using `psql` from WSL.

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
- **Dependencies**: Task 2.1

---

### Task 2.3: Set up FluentMigrator — initial database schema

- **Description**:
  Create a standalone `src/Migrations/` C# console project that uses FluentMigrator to manage schema migrations. Write the initial migration(s) to create tables for `users`, `tracks`, and `playlists`. The migration runner is executed manually (or via `dotnet run`) before starting services locally.

  **Tables to create in the initial migration**:
  - `users` — id (uuid PK), email (unique), password_hash, created_at, updated_at
  - `tracks` — id (uuid PK), user_id (FK → users), title, artist, genre, duration_seconds, file_path, created_at, updated_at
  - `playlists` — id (uuid PK), user_id (FK → users), name, description, created_at, updated_at
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

  **Expected outcome**: `\dt` in psql shows all four tables. Re-running migrations is idempotent (no-op if already applied).

- **Labels**: phase-2, postgresql, migrations, backend
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.2

---

### Task 2.4: Build Identity Service (register, login, JWT)

- **Description**:
  Implement the Identity Service end-to-end using Clean Architecture. Supports email/password registration and login, issuing a signed JWT on success. The internal API is exposed as a gRPC endpoint; the service does NOT expose REST publicly (the API Gateway will handle that in a later phase — for now, gRPC is tested directly).

  **Domain layer** (`IdentityService.Domain`):
  - `User` entity: Id (Guid), Email, PasswordHash, CreatedAt, UpdatedAt
  - Domain exception: `DuplicateEmailException`, `InvalidCredentialsException`

  **Application layer** (`IdentityService.Application`):
  - `IUserRepository` interface
  - `RegisterUserCommand` + handler
  - `LoginCommand` + handler
  - `ITokenService` interface

  **Infrastructure layer** (`IdentityService.Infrastructure`):
  - `UserRepository` — Dapper implementation of `IUserRepository`
  - `JwtTokenService` — `ITokenService` implementation (System.IdentityModel.Tokens.Jwt)
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

- **Labels**: phase-2, backend, csharp, grpc, identity
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.3

---

### Task 2.5: Build Track Service (track metadata CRUD)

- **Description**:
  Implement the Track Service end-to-end using Clean Architecture. Manages track metadata (title, artist, genre, duration, file path). Audio file upload (to local disk in this phase) is handled here — the file path is stored in the `tracks` table. Exposed via gRPC.

  **Domain layer** (`TrackService.Domain`):
  - `Track` entity: Id, UserId, Title, Artist, Genre, DurationSeconds, FilePath, CreatedAt, UpdatedAt
  - Domain exception: `TrackNotFoundException`

  **Application layer** (`TrackService.Application`):
  - `ITrackRepository` interface
  - Use cases: `UploadTrackCommand`, `GetTrackQuery`, `ListTracksQuery`, `DeleteTrackCommand`
  - `IFileStorageService` interface (local disk in this phase, swapped for Azure Blob in Phase 4)

  **Infrastructure layer** (`TrackService.Infrastructure`):
  - `TrackRepository` — Dapper implementation
  - `LocalFileStorageService` — saves uploaded files to a configurable local path

  **Api layer** (`TrackService.Api`):
  - gRPC service definition (`track.proto`) with `UploadTrack`, `GetTrack`, `ListTracks`, `DeleteTrack` RPCs
  - `TrackGrpcService`
  - DI wiring, Serilog, health endpoints (same as Identity Service)

  **Expected outcome**: Can upload a track (metadata + file path), retrieve it, list all tracks for a user, and delete a track.

- **Labels**: phase-2, backend, csharp, grpc, tracks
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.4

---

### Task 2.6: Build Streaming Service (audio file delivery)

- **Description**:
  Implement the Streaming Service, which serves audio files over HTTP using range requests (enables seek/scrub in a browser audio player). This service is the only one that exposes a REST endpoint externally (not gRPC) because browsers cannot use gRPC directly for media streaming. It calls Track Service (gRPC) to resolve the file path for a given track ID, then streams the file from local disk.

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

- **Labels**: phase-2, backend, csharp, streaming, rest
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 2.5

---

### Task 2.7: Update CI pipeline — dotnet build and test

- **Description**:
  Uncomment and complete the `dotnet` steps in `.github/workflows/ci.yml`. The CI pipeline should restore, build, and run tests on every PR targeting `main`. A failing test blocks the merge.

  **Steps to add/uncomment in ci.yml**:
  1. `actions/setup-dotnet@v4` — set .NET SDK version
  2. `dotnet restore` — restore NuGet packages
  3. `dotnet build --no-restore --configuration Release`
  4. `dotnet test --no-build --configuration Release --logger trx`

  **Expected outcome**: CI `build` check goes green on a passing PR. A PR with a failing test is blocked from merging.

- **Labels**: phase-2, ci, github-actions, csharp
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 2.6

---

### Task 2.8: Write integration tests — Identity Service

- **Description**:
  Write integration tests for the Identity Service gRPC endpoints (`Register` and `Login`) using `Microsoft.AspNetCore.Mvc.Testing` (WebApplicationFactory) with a real test PostgreSQL database (running in Docker via `Testcontainers`). Follow the AAA pattern. Cover all significant input/output combinations.

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

- **Labels**: phase-2, testing, identity, postgresql
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.7

---

### Task 2.9: Write integration tests — Track Service

- **Description**:
  Write integration tests for the Track Service gRPC endpoints using the same pattern as Task 2.8 (WebApplicationFactory + Testcontainers). Cover all CRUD operations and file storage interactions.

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

- **Labels**: phase-2, testing, tracks, postgresql
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 2.8

---

### Task 2.10: Create Phase 2 GitHub milestone and issues

- **Description**:
  Create the Phase 2 milestone in GitHub and create one issue per task (2.1–2.9) on the project board. This task mirrors Task 1.7 from Phase 1 and must be done before any Phase 2 development work begins.

  **Commands (WSL Ubuntu)**:
  ```bash
  # Create Phase 2 milestone
  gh api repos/kumaran-naidoo-derivco/jamtrack-radio/milestones \
    -f title="Phase 2: Local Dev Environment" \
    -f description="ASP.NET Core microservices, PostgreSQL, Dapper, FluentMigrator, gRPC, integration tests — all running locally." \
    -f state="open"

  # Create issues (one per task — repeat for each)
  gh issue create \
    --repo kumaran-naidoo-derivco/jamtrack-radio \
    --title "Task 2.1: Scaffold solution structure and Clean Architecture projects" \
    --body "Create the jamtrack-radio.sln and all C# project folders following Clean Architecture. See project-tasks/Phase-2.md for full details." \
    --label "phase-2,backend,csharp,setup" \
    --milestone "Phase 2: Local Dev Environment"
  ```

  **Expected outcome**: Milestone "Phase 2: Local Dev Environment" visible on GitHub. Nine issues (Tasks 2.1–2.9) created and visible on the project board in the backlog column.

- **Labels**: phase-2, github, issues
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: None (can be done first, before any code)

---

## ✅ Phase 2 Summary

Phase 2 delivers the **local v0.1 MVP** — three fully functional microservices running on your machine:

| Service | Transport | What it does |
|---|---|---|
| Identity Service | gRPC | Register + login, JWT issuance |
| Track Service | gRPC | Track metadata CRUD + local file storage |
| Streaming Service | REST (HTTP range) | Audio file delivery with seek support |

**Supporting infrastructure**:
- PostgreSQL 16 in Docker Compose
- FluentMigrator for schema management
- Dapper for all DB access
- Serilog structured logging on all services
- Integration tests with real Postgres (Testcontainers)
- CI pipeline builds and tests on every PR

**After Phase 2, you'll have a working music platform — runnable entirely on your local machine — ready to be containerised in Phase 3.**
