# Cloud Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Cloud Architect)
**Status**: Accepted
**Skill**: `/cloud-architect jamtrack-radio` — DISCOVERY Step 5b
**Inputs**: `software-arch.md` (6 services defined), `jamtrack-radio-requirements.md` (budget: £50–100/month target; reconciled to £200–300/month staging)

---

## 1. Phase-Aware Infrastructure Overview

| Component | Phase 2 (local) | Phase 3 (Azure VMs) | Phase 5 (Docker + ACR) | Phase 6 (ACA) | Phase 7+ (AKS) |
|-----------|-----------------|---------------------|----------------------|---------------|----------------|
| Compute | `dotnet run` | Azure Linux VMs (B1s/B2s) | Docker on VMs | Azure Container Apps | Azure Kubernetes Service |
| Container registry | — | — | Azure Container Registry (Basic) | ACR | ACR |
| Database | Docker PostgreSQL 16 | Azure Database for PostgreSQL Flexible Server | Same (Flex Server) | Same (Flex Server) | Same (Flex Server) |
| Secrets | `.env.local` (gitignored) | Azure Key Vault + VM Managed Identity | Key Vault + Managed Identity | ACA Key Vault references | Workload Identity + Key Vault |
| Ingress | `localhost` ports | Nginx reverse proxy on VM | Nginx on VM | ACA built-in HTTPS ingress | Application Gateway + WAF v2 |
| DNS | — | — | — | ACA managed domain | Azure DNS |
| Monitoring | stdout logs | stdout + journalctl | stdout logs | ACA Log Analytics | ELK on AKS + ClickHouse |
| Blob storage | Local filesystem mock | Azure Blob Storage (Hot LRS) | Same | Same | Same |
| Service mesh / sidecar | Dapr (local) | Dapr CLI on VM | Dapr CLI in container | ACA built-in Dapr | Dapr (K8s mode on AKS) |
| Pub/sub broker | Redis (Docker) | Redis (Docker on VM) | Redis (Docker on VM) | Azure Service Bus (Standard) | Azure Service Bus |
| Est. monthly cost | £0 | ~£37–50 | ~£50 | ~£55–70 | ~£60–100 (spot nodes) |

> **Phase 4** (Feature Completion) uses the same Azure VM infrastructure as Phase 3 — it adds services, not infrastructure changes.

---

## 2. Azure Network Topology Diagram (Phase 7+ / AKS)

Hub-spoke VNet topology. Internet traffic enters via Application Gateway + WAF v2, routes through the AKS subnet, and connects to the data tier via private endpoints. Azure services outside the VNet authenticate via Managed Identity.

![Azure Network Topology](diagrams/cloud-network-topology.drawio.svg)

> Source: [`diagrams/cloud-network-topology.drawio.svg`](diagrams/cloud-network-topology.drawio.svg) — draw.io editable SVG (embedded diagram)

---

## 3. AKS Node Pool Sizing

| Environment | Node pool | Node SKU | Min | Max | Rationale |
|-------------|-----------|----------|-----|-----|-----------|
| Staging | `system` | Standard_B2s | 1 | 2 | System pods only — burstable, cost-optimised |
| Staging | `user` | Standard_B4ms | 1 | 3 | App workloads — burstable is sufficient for staging |
| Production | `system` | Standard_D2s_v5 | 2 | 3 | HA system workloads |
| Production | `user` | Standard_D4s_v5 | 2 | 10 | App workloads — HPA-controlled auto-scale |

**Namespace strategy**:
- `jamtrack-prod` — production workloads
- `jamtrack-staging` — staging workloads
- `jamtrack-system` — shared infrastructure (Dapr control plane, Redis, monitoring agents)

Each namespace has a `ResourceQuota` to cap CPU and memory, and a default-deny `NetworkPolicy`.

---

## 4. Service-to-Infrastructure Mapping

| Service | Replicas (prod baseline) | CPU request/limit | Memory request/limit | HPA target |
|---------|-------------------------|-------------------|----------------------|------------|
| API Gateway (YARP) | 2 | 100m / 500m | 128Mi / 256Mi | CPU 70% |
| Identity Service | 2 | 100m / 300m | 128Mi / 256Mi | CPU 70% |
| Track Service | 2 | 100m / 300m | 128Mi / 256Mi | CPU 70% |
| Playlist Service | 1 | 50m / 200m | 64Mi / 128Mi | CPU 70% |
| Streaming Service | 2 | 200m / 1000m | 256Mi / 512Mi | CPU 60% (bandwidth-intensive) |
| Storage Service | 1 | 50m / 200m | 64Mi / 128Mi | CPU 70% |
| Dapr sidecar (each) | — | 10m / 100m | 32Mi / 64Mi | — |

---

## 5. Cost Estimate Table

### Phase 3 — Azure VMs (monthly)

| Resource | SKU / Config | Monthly cost |
|----------|-------------|-------------|
| Linux VMs (2× Standard_B1s) | Burstable, Ubuntu 22.04 LTS | ~£12 |
| PostgreSQL Flexible Server | Burstable B_Standard_B1ms | ~£12 |
| Azure Key Vault — Standard | Key operations | ~£1 |
| Public IP (Basic, static) | | ~£3 |
| OS disks (2× Premium SSD P4 30GB) | | ~£8 |
| Bandwidth egress (dev traffic) | | ~£1 |
| **Phase 3 total** | | **~£37/month** |

> Upgrade app VM to Standard_B2s (~£12/month) if B1s is too small for 3 services. Total ~£50/month.

### Phase 6 — Azure Container Apps (monthly)

| Resource | SKU / Config | Monthly cost |
|----------|-------------|-------------|
| Container Apps (×6) | Consumption plan, scale-to-zero | ~£5–15 |
| Log Analytics Workspace | Pay-per-GB (2 GB/day) | ~£30 |
| Azure Service Bus — Standard | Per operation | ~£8 |
| PostgreSQL Flexible Server | Burstable B_Standard_B1ms | ~£12 |
| Azure Container Registry — Basic | 10 GB included | ~£4.50 |
| Azure Key Vault — Standard | | ~£1 |
| Azure Blob Storage (audio) — Hot LRS | 100 GB | ~£2 |
| **Phase 6 total** | | **~£55–70/month** |

> ACA Consumption plan charges per vCPU-second and GiB-second. With scale-to-zero, idle services cost £0. Dev workloads are low cost.

### Phase 7 — AKS Staging (monthly)

| Resource | SKU / Config | Monthly cost |
|----------|-------------|-------------|
| AKS nodes — staging (2× Standard_B4ms) | Burstable | ~£100 |
| PostgreSQL Flexible Server — staging | Burstable B_Standard_B2ms | ~£35 |
| Azure Service Bus — Standard | Per operation | ~£8 |
| Azure Container Registry — Basic | 10 GB included | ~£4.50 |
| Azure Key Vault — Standard | Key operations | ~£1 |
| Azure Blob Storage (audio) — Hot LRS | 100 GB | ~£2 |
| Log Analytics — staging (2 GB/day, 30-day retention) | Pay-per-GB | ~£46 |
| **Staging total** | | **~£197/month** |

> **Note**: This is below the £326 in the skill template because staging node pools are burstable B-series (lower cost). Apply the 30% buffer from the financial lens: **~£256/month worst case**.

### Production — Baseline (monthly, Phase 7+)

| Resource | SKU / Config | Monthly cost |
|----------|-------------|-------------|
| AKS nodes — prod (2× Standard_D4s_v5) | General purpose | ~£307 |
| PostgreSQL Flexible Server — prod | General Purpose D4s | ~£277 |
| Azure Application Gateway + WAF v2 | WAF_v2 | ~£183 |
| Azure Service Bus — Standard | Per operation | ~£8 |
| Azure Container Registry — Basic | | ~£4.50 |
| Azure Key Vault | | ~£1 |
| Azure Blob Storage (audio) — Hot LRS | 500 GB + egress | ~£15 |
| Azure DNS | Hosted zone + queries | ~£1 |
| Log Analytics — prod (5 GB/day, 30-day hot) | | ~£345 |
| **Production baseline** | | **~£1,142/month** |

**Production at 2× load**: +1 AKS node (D4s_v5) = ~£1,295/month
**Production at 10× load**: +4 AKS nodes = ~£1,700/month

---

## 6. Total Cost of Ownership (TCO)

| Scenario | Monthly | Annual | Notes |
|----------|---------|--------|-------|
| Development (Phase 2) | £0 | £0 | Local only |
| Azure VMs (Phase 3–4) | ~£37–50 | ~£450–600 | `terraform destroy` when not developing |
| Docker + ACR on VMs (Phase 5) | ~£50 | ~£600 | Adds ACR Basic to VM cost |
| ACA (Phase 6) | ~£55–70 | ~£660–840 | Scale-to-zero; VMs decommissioned |
| AKS staging (Phase 7+) | £197–256 | £2,364–3,072 | Always-on; apply auto-shutdown |
| AKS production baseline (Phase 7+) | £1,142 | £13,704 | |
| Production at 2× | £1,295 | £15,540 | |
| Production at 10× | £1,700 | £20,400 | |

> **Budget check**: The personal budget is £50–100/month (requirements §3, reconciled to £200–300/month for AKS staging). Phases 3–6 comfortably fit within this constraint. AKS (Phase 7+) requires cost optimisation (spot nodes, auto-shutdown) to stay near the upper bound.

---

## 7. Cost Optimisation Recommendations

| Recommendation | Phase | Saving | Effort | Priority |
|----------------|-------|--------|--------|----------|
| VM auto-shutdown at 19:00 (Azure Auto-shutdown) | 3–5 | ~£15/month | Low | High |
| `terraform destroy` when not actively developing | 3–5 | 100% during inactive periods | Low | High |
| Budget alert at £60/month | 3+ | £0 | Low | High — do this on day one |
| ACA scale-to-zero for idle services | 6 | ~£10–20/month | Low | High |
| AKS auto-shutdown staging 19:00–08:00 | 7+ | ~£100/month | Low | High |
| Use Azure Spot instances for AKS user node pool | 7+ | ~£50–80/month | Medium | Medium |
| Burstable B-series for PostgreSQL staging | 3+ | Already applied | — | Done |
| Set Log Analytics retention to 30 days hot / archive cold | 7+ | ~£100/month at prod scale | Low | High |
| 1-year reserved instances for production compute | 7+ | ~£120/month | Low | Medium |
| Use Azure Blob Cool tier for tracks not accessed in 30 days | 4+ | ~£5/month | Low | Low |

---

## 8. Helm Chart Structure

```
helm/
  api-gateway/
    Chart.yaml
    values.yaml
    values.staging.yaml
    values.prod.yaml
    templates/
      deployment.yaml
      service.yaml
      configmap.yaml
      hpa.yaml
      pdb.yaml
  identity-service/
    ...  (same structure)
  track-service/
  playlist-service/
  streaming-service/
  storage-service/
```

All charts share a common pattern. `values.yaml` holds defaults; environment-specific overrides in `values.staging.yaml` and `values.prod.yaml`. Image tags reference SHA digests in production (never `latest`).

---

## 9. Physical Deployment Diagram (Azure — Phase 7+ / AKS)

Full Azure resource group view using official Azure service names and Azure Architecture Center icon conventions.

![Physical Deployment](diagrams/physical-deployment.drawio.svg)

> Source: [`diagrams/physical-deployment.drawio.svg`](diagrams/physical-deployment.drawio.svg) — draw.io editable SVG (embedded diagram)
