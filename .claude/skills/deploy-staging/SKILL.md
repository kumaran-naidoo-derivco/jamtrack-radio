---
name: deploy-staging
description: Deploys Jamtrack Radio services to the staging environment and verifies they are healthy. Phase-aware — uses Docker Compose locally (Phase 2), Rancher Desktop K8s (Phase 3), or Azure AKS staging (Phase 4+). Run after /review and passing tests. Use at Step 5 of the development workflow.
disable-model-invocation: true
argument-hint: [service name or "all"]
---

## Pre-condition Validation (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
STOP=0

# Check tests passed (look for test result artifacts)
test -f "docs/designs/${FEATURE}.md" \
  && echo "✓ Design document exists" \
  || { echo "STOP: Design doc missing — deploy without a design is high risk."; STOP=1; }

# Check architect sign-off
test -f "docs/architecture/${FEATURE}/architect-signoff.md" \
  || test -f "docs/architecture/jamtrack-radio/architect-signoff.md" \
  && echo "✓ Architect sign-off exists" \
  || echo "WARN: Architect sign-off not found."

STATE=$(cat .claude/workflow-state.json 2>/dev/null)
echo "Workflow state: ${STATE:-not found}"

[ $STOP -eq 1 ] && echo "Fix blocking issues above before continuing." && exit 1
echo "Pre-conditions met — proceeding with deployment."
```

---

You are a senior DevOps engineer deploying Jamtrack Radio to the staging environment.

If $ARGUMENTS specifies a service name, deploy only that service. If $ARGUMENTS is "all" or omitted, deploy all services.

First, detect the current phase from `project-tasks/Phase-2.md` (or ask the user) to determine which deployment target to use.

---

## Phase Detection

| Phase | Staging Target | Stack |
|---|---|---|
| Phase 2 | Local Docker Compose | `docker compose up` |
| Phase 3 | Rancher Desktop (local K8s) | `kubectl` / `helm` |
| Phase 4+ | Azure AKS — staging namespace | `az aks` / `helm` |

---

## Phase 2 — Docker Compose (Local)

### Pre-deploy Checklist

- [ ] `dotnet build` passes with zero warnings on the solution
- [ ] All quality skills (`/robust`, `/security`, `/scalable`, `/performant`) run and `BLOCKER`/`MAJOR` findings resolved
- [ ] `/review` approved
- [ ] All integration tests passing (`dotnet test`)
- [ ] Docker Desktop / Rancher Desktop is running
- [ ] `.env.local` exists at the repo root with valid credentials (not committed)

### Steps

```bash
# 1. Build service images
docker compose build

# 2. Run database migrations
dotnet run --project src/Migrations -- \
  --connection "Host=localhost;Database=jamtrack_dev;Username=jamtrack;Password=$(grep POSTGRES_PASSWORD .env.local | cut -d= -f2)"

# 3. Start the stack
docker compose up -d

# 4. Verify all containers are healthy
docker compose ps

# 5. Check health endpoints
curl -s http://localhost:5001/health/ready   # Identity Service
curl -s http://localhost:5002/health/ready   # Track Service
curl -s http://localhost:5003/health/ready   # Streaming Service
```

### Smoke Tests

```bash
# Identity Service — register a user
grpcurl -plaintext -d '{"email":"smoke@jamtrack.io","password":"SmokeTest123!"}' \
  localhost:5001 jamtrack.identity.v1.IdentityService/Register

# Identity Service — login
grpcurl -plaintext -d '{"email":"smoke@jamtrack.io","password":"SmokeTest123!"}' \
  localhost:5001 jamtrack.identity.v1.IdentityService/Login

# Track Service — list tracks (empty)
grpcurl -plaintext -H "authorization: bearer <token>" \
  -d '{"user_id":"<userId>"}' \
  localhost:5002 jamtrack.track.v1.TrackService/ListTracks

# Streaming Service — health
curl -s http://localhost:5003/health/ready
```

### Pass Criteria

- [ ] All containers show `healthy` in `docker compose ps`
- [ ] All `/health/ready` endpoints return `200`
- [ ] Smoke test register returns a `userId`
- [ ] Smoke test login returns a JWT
- [ ] No `ERROR` entries in `docker compose logs` at startup

### Rollback

```bash
# Stop the stack
docker compose down

# Revert to previous image (if built and tagged)
docker compose up -d --no-build
```

---

## Phase 3 — Rancher Desktop (Local K8s)

> To be expanded in Phase 3. Steps will cover: `helm upgrade --install`, namespace verification, `kubectl rollout status`, health check via port-forward.

---

## Phase 4+ — Azure AKS Staging

> To be expanded in Phase 4. Steps will cover: `az acr build`, `helm upgrade --install --namespace staging`, `kubectl rollout status`, smoke tests against the staging ingress URL.

---

After deploying, ask:
- Are all health endpoints returning 200?
- Are there any error logs to investigate?
- Ready to move to Step 6 — Integration Test (`/integration-test`)?
