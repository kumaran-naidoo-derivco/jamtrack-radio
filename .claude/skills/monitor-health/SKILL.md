---
name: monitor-health
description: Health endpoint checks, pod status, and migration verification post-deployment. Phase-aware (Docker Compose / K8s / Azure). Run as MONITORING Step 1 immediately after deployment. Gate — all endpoints 200, zero pod restarts.
disable-model-invocation: true
argument-hint: [service name or "all"]
---

You are a DevOps Engineer verifying that a Jamtrack Radio deployment is healthy. Run immediately after every deployment — staging or production.

If `$ARGUMENTS` is provided, use it to scope the check (specific service, or "all").

---

## Pre-flight

Record before running:
- Deployment timestamp: ______
- PR number: ______
- Services deployed: ______
- Previous image tag (for rollback): ______

---

## Phase 2 — Docker Compose Health Check

```bash
# Verify all containers are running
docker compose ps

# Check health status (all should show "healthy")
docker inspect --format='{{.Name}}: {{.State.Health.Status}}' $(docker compose ps -q)

# Test health endpoints
echo "=== Identity Service ===" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health/live && echo " /live" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/health/ready && echo " /ready"

echo "=== Track Service ===" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/health/live && echo " /live" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5002/health/ready && echo " /ready"

echo "=== Streaming Service ===" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health/live && echo " /live" && \
  curl -s -o /dev/null -w "%{http_code}" http://localhost:5003/health/ready && echo " /ready"

# Verify migrations ran successfully
docker compose logs db-migrator 2>&1 | tail -20
```

Expected: All endpoints return `200`. No `unhealthy` containers. Migration logs show "migration successful".

---

## Phase 3 — Azure VM Health Check

```bash
VM_IP=<azure-vm-public-ip>

# Check service status via systemd
ssh azureuser@$VM_IP "systemctl is-active identity-service track-service streaming-service"

# Test health endpoints
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5001/health/live && echo " identity /live"
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5001/health/ready && echo " identity /ready"
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5002/health/live && echo " track /live"
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5002/health/ready && echo " track /ready"
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5003/health/live && echo " streaming /live"
curl -s -o /dev/null -w "%{http_code}" http://$VM_IP:5003/health/ready && echo " streaming /ready"

# Check recent service logs
ssh azureuser@$VM_IP "journalctl -u identity-service --since '10 minutes ago'"

# Verify migration completed
ssh azureuser@$VM_IP "journalctl -u db-migrator --since '30 minutes ago' | tail -20"
```

---

## Phase 7+ — Azure AKS Health Check

```bash
NAMESPACE=jamtrack-prod  # or jamtrack-staging

# Ensure correct cluster context
kubectl config current-context  # expect aks-jamtrack-prod

# Pod health
kubectl get pods -n $NAMESPACE -o wide

# Restart check
kubectl get pods -n $NAMESPACE --no-headers | awk '{if ($4 > 0) print "RESTART: " $1 " (" $4 " restarts)"}'

# Health endpoints via Application Gateway
curl -s -o /dev/null -w "%{http_code}" https://api.jamtrack.io/health/ready && echo " api gateway /ready"

# Internal health via kubectl exec (bypass ingress)
kubectl exec -n $NAMESPACE deploy/identity-service -- \
  wget -qO- http://localhost:8080/health/ready

# Check AKS node health
kubectl get nodes -o wide
kubectl describe nodes | grep -A5 "Conditions:"

# Check HPA status (ensure not at max replicas)
kubectl get hpa -n $NAMESPACE
```

---

## Checklist

After running the checks, verify:

- [ ] All health endpoints return HTTP 200
- [ ] Zero pod restarts since deployment (Phase 3+)
- [ ] No `CrashLoopBackOff` or `Error` pod states
- [ ] Migration job completed successfully
- [ ] No error events in `kubectl get events` (Phase 3+)
- [ ] HPA not at max replicas (indicates load, not a failure, but worth noting)
- [ ] AKS nodes all `Ready` (Phase 4+)

---

## Gate

**Pass**: All checkboxes ticked. Proceed to `/monitor-errors`.

**Fail**: Any unhealthy endpoint, crash loop, or failed migration. **Stop. Roll back.**

Rollback procedure (Phase 2):
```bash
docker compose down
git checkout <previous-tag>
docker compose up -d
```

Rollback procedure (Phase 7+):
```bash
helm rollback <release-name> -n $NAMESPACE
kubectl rollout status deployment/<service> -n $NAMESPACE
```
