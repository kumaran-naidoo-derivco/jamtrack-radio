---
name: deploy-prod
description: Deploys Jamtrack Radio services to production with a confirmed rollback plan and post-deploy verification. Phase-aware — not applicable in Phase 2 (local only). Azure AKS production in Phase 4+. Use at Step 7 of the development workflow, after /integration-test passes.
disable-model-invocation: true
argument-hint: [service name or "all"]
---

You are a senior DevOps engineer deploying Jamtrack Radio to production.

**Phase 2 note**: Production deployment is not applicable in Phase 2 — all services run locally. This skill becomes active from Phase 4 (Azure AKS). If invoked during Phase 2, remind the user and stop.

If $ARGUMENTS specifies a service name, deploy only that service. If $ARGUMENTS is "all" or omitted, deploy all services.

---

## Pre-Deploy Gate (all must pass)

Before executing any deployment steps, verify every gate is met. Stop and resolve any failures before proceeding.

- [ ] All staging gates passed (`/deploy-staging` healthy, `/integration-test` all flows green)
- [ ] All integration tests passing in CI (`dotnet test` green on the PR)
- [ ] PR approved and merged to `main`
- [ ] Migration is backward compatible — the running production version can operate against the new schema during the rollout window
- [ ] Rollback plan documented (see below) and confirmed with the team
- [ ] Docker image tagged with the commit SHA — not `latest`
- [ ] Secrets and connection strings confirmed in the production secrets store (Azure Key Vault / K8s Secrets) — not in the image

---

## Phase 4+ — Azure AKS Production

### 1. Build & Push Image

```bash
# Build and push to Azure Container Registry
az acr build \
  --registry jamtrackacr \
  --image <service-name>:$(git rev-parse --short HEAD) \
  --file src/<ServiceName>/<ServiceName>.Api/Dockerfile .
```

### 2. Run Migrations

```bash
# Run FluentMigrator against production DB
# Use the migration runner job (K8s Job or dotnet run from a secure context)
kubectl apply -f k8s/migrations/migration-job.yaml -n production
kubectl wait --for=condition=complete job/migration-job -n production --timeout=120s
kubectl logs job/migration-job -n production
```

### 3. Deploy via Helm

```bash
# Upgrade the Helm release (rolling update — zero downtime)
helm upgrade <service-name> ./helm/<service-name> \
  --namespace production \
  --set image.tag=$(git rev-parse --short HEAD) \
  --set replicaCount=2 \
  --atomic \
  --timeout 5m
```

`--atomic` rolls back automatically if the deployment does not become healthy within the timeout.

### 4. Verify Rollout

```bash
# Watch the rollout
kubectl rollout status deployment/<service-name> -n production

# Check pod health
kubectl get pods -n production -l app=<service-name>

# Verify health endpoints via ingress
curl -s https://api.jamtrack.io/health/ready
```

### 5. Post-Deploy Smoke Tests

```bash
# Run the same smoke tests as /deploy-staging but against the production URL
# Use a dedicated smoke-test user — never real user data
curl -s -X POST https://api.jamtrack.io/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"smoke+prod@jamtrack.io","password":"SmokeTest123!"}'
```

### 6. Monitor for 10 Minutes

Watch the following after every production deploy:
- Error rate in logs (ELK / ClickStack): should remain at pre-deploy baseline
- Response latency (p99): should not increase by more than 20%
- Health endpoints: all returning `200`
- Pod restart count: should be zero

```bash
# Watch for errors in production logs
kubectl logs -l app=<service-name> -n production --follow --tail=50
```

---

## Rollback Plan

Document this **before** deploying. Fill in for each deployment:

| Item | Value |
|---|---|
| Previous image tag | `<service-name>:<previous-sha>` |
| Previous Helm release | `helm history <service-name> -n production` |
| Down migration available? | Yes / No |
| Estimated rollback time | < 5 minutes |

### To rollback

```bash
# Option 1 — Helm rollback (preferred)
helm rollback <service-name> <previous-revision> --namespace production

# Option 2 — Redeploy previous image manually
helm upgrade <service-name> ./helm/<service-name> \
  --namespace production \
  --set image.tag=<previous-sha> \
  --atomic --timeout 5m

# Option 3 — Run down migration if schema was changed
kubectl apply -f k8s/migrations/rollback-job.yaml -n production
```

---

## Post-Deploy Checklist

- [ ] All pods `Running` with zero restarts
- [ ] All `/health/ready` endpoints return `200`
- [ ] Smoke tests passing against production URL
- [ ] No error spike in logs during 10-minute monitoring window
- [ ] Rollback plan tested mentally — previous image tag confirmed available

---

After deploying to production, ask:
- Are all health checks green and logs clean?
- Should the migration down-script be retained or can it be cleaned up?
- Ready to close the GitHub issue for this feature?
