---
name: integration-test
description: Runs and verifies full end-to-end integration tests against the live staging environment for Jamtrack Radio. Tests cross-service flows that unit and component tests cannot cover. Use at Step 6 of the development workflow, after /deploy-staging.
disable-model-invocation: true
argument-hint: [flow name or "all"]
---

You are a senior QA engineer running integration tests against the Jamtrack Radio staging environment.

If $ARGUMENTS specifies a flow name, test only that flow. Otherwise, run all integration flows.

**Prerequisites**: Staging environment must be running and healthy (`/deploy-staging` passed) before running these tests.

---

## Integration Test Flows

These tests verify cross-service interactions in the live staging environment — not mocked, not Testcontainers. Real services, real DB, real network calls.

---

### Flow 1: Full User Registration → Login → Track Upload → Stream

The primary end-to-end flow. Verifies all three services work together.

```bash
BASE_IDENTITY=localhost:5001
BASE_TRACK=localhost:5002
BASE_STREAM=http://localhost:5003

# Step 1 — Register a new user
REGISTER_RESPONSE=$(grpcurl -plaintext \
  -d "{\"email\":\"e2e-$(date +%s)@jamtrack.io\",\"password\":\"E2ETest123!\"}" \
  $BASE_IDENTITY jamtrack.identity.v1.IdentityService/Register)
USER_ID=$(echo $REGISTER_RESPONSE | jq -r '.userId')
echo "Registered userId: $USER_ID"

# Step 2 — Login and get JWT
LOGIN_RESPONSE=$(grpcurl -plaintext \
  -d "{\"email\":\"e2e-$(date +%s)@jamtrack.io\",\"password\":\"E2ETest123!\"}" \
  $BASE_IDENTITY jamtrack.identity.v1.IdentityService/Login)
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')
echo "JWT obtained: ${TOKEN:0:20}..."

# Step 3 — Upload a track (metadata)
UPLOAD_RESPONSE=$(grpcurl -plaintext \
  -H "authorization: bearer $TOKEN" \
  -d "{\"user_id\":\"$USER_ID\",\"title\":\"E2E Track\",\"artist\":\"Test Artist\",\"genre\":\"Electronic\",\"duration_seconds\":180,\"file_path\":\"/tmp/test.mp3\"}" \
  $BASE_TRACK jamtrack.track.v1.TrackService/UploadTrack)
TRACK_ID=$(echo $UPLOAD_RESPONSE | jq -r '.trackId')
echo "Uploaded trackId: $TRACK_ID"

# Step 4 — Retrieve the track
grpcurl -plaintext \
  -H "authorization: bearer $TOKEN" \
  -d "{\"track_id\":\"$TRACK_ID\"}" \
  $BASE_TRACK jamtrack.track.v1.TrackService/GetTrack

# Step 5 — Stream the track (range request)
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Range: bytes=0-1023" \
  $BASE_STREAM/stream/$TRACK_ID
# Expected: 206
```

**Pass criteria**:
- [ ] Register returns a non-empty `userId`
- [ ] Login returns a valid JWT (parseable, non-expired)
- [ ] Upload returns a non-empty `trackId`
- [ ] GetTrack returns metadata matching what was uploaded
- [ ] Stream returns HTTP `206 Partial Content`

---

### Flow 2: Duplicate Registration Rejected

```bash
EMAIL="duplicate-$(date +%s)@jamtrack.io"

grpcurl -plaintext -d "{\"email\":\"$EMAIL\",\"password\":\"Test123!\"}" \
  $BASE_IDENTITY jamtrack.identity.v1.IdentityService/Register

grpcurl -plaintext -d "{\"email\":\"$EMAIL\",\"password\":\"Test123!\"}" \
  $BASE_IDENTITY jamtrack.identity.v1.IdentityService/Register
# Expected: gRPC status ALREADY_EXISTS (6)
```

---

### Flow 3: Unauthorised Access Rejected

```bash
# Track request with no token
grpcurl -plaintext \
  -d "{\"user_id\":\"00000000-0000-0000-0000-000000000000\"}" \
  $BASE_TRACK jamtrack.track.v1.TrackService/ListTracks
# Expected: gRPC status UNAUTHENTICATED (16)

# Stream request with no token
curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:5003/stream/00000000-0000-0000-0000-000000000000
# Expected: 401
```

---

### Flow 4: Track Not Found

```bash
grpcurl -plaintext \
  -H "authorization: bearer $TOKEN" \
  -d "{\"track_id\":\"00000000-0000-0000-0000-000000000000\"}" \
  $BASE_TRACK jamtrack.track.v1.TrackService/GetTrack
# Expected: gRPC status NOT_FOUND (5)
```

---

### Flow 5: Health Checks All Passing

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health/live   # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health/ready  # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/health/live   # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/health/ready  # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health/live   # 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health/ready  # 200
```

---

## Pass / Fail Criteria

All flows must pass before proceeding to `/deploy-prod`.

| Flow | Expected Result |
|---|---|
| Flow 1 — Full E2E | All 5 steps succeed |
| Flow 2 — Duplicate registration | `ALREADY_EXISTS` returned |
| Flow 3 — Unauthorised access | `UNAUTHENTICATED` / `401` returned |
| Flow 4 — Track not found | `NOT_FOUND` returned |
| Flow 5 — Health checks | All return `200` |

---

## If a Flow Fails

1. Check service logs: `docker compose logs <service-name> --tail=50`
2. Check DB state: connect via `psql` and inspect the relevant table
3. Raise a bug — do not proceed to `/deploy-prod` until all flows pass

---

After integration tests, ask:
- Did all flows pass?
- Are there additional cross-service scenarios to test?
- Ready to move to Step 7 — Deploy Production (`/deploy-prod`)?
