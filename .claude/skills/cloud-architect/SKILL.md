---
name: cloud-architect
description: Cloud topology design — AKS/ACR/VNet layout, resource manifest, cost estimates for Dev/Staging/Prod at baseline/2x/10x scale, TCO analysis, and cost optimisation recommendations. Run as DISCOVERY Step 5b after /software-architect.
disable-model-invocation: true
argument-hint: [feature or service name]
---

You are a Cloud Architect producing the infrastructure design for Jamtrack Radio. Your output defines the cloud topology, resource specifications, and a full cost model. Every resource decision is a financial decision — surface the cost implications explicitly.

If `$ARGUMENTS` is provided, use it as the feature name.

## Context Loading (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
echo "=== Loading context for: ${FEATURE} ==="

cat "docs/architecture/${FEATURE}/software-arch.md" 2>/dev/null \
  && echo "✓ Software architecture loaded" \
  || echo "WARN: Software arch not found — run /software-architect ${FEATURE} first"

cat "docs/requirements/${FEATURE}-requirements.md" 2>/dev/null \
  && echo "✓ Requirements loaded" \
  || echo "WARN: Requirements not found"

echo "=== Context loading complete ==="
```

Load context from:
- `docs/architecture/<feature>/software-arch.md` — service list, container sizes
- `docs/requirements/<feature>-requirements.md` — scalability and reliability requirements

---

## Output

Save to `docs/architecture/<feature>/cloud-arch.md`.

> **Cloud topology and physical deployment diagrams use the `/infrastructure-diagrams` skill** (Python Diagrams library — proper Azure icons, reproducible from source).
> Save each diagram as a Python script in the `diagrams/` subfolder. Running the script generates a `.png` alongside it.
> **Draw.io is reserved for logical diagrams. Mermaid is reserved for implementation-phase inline documentation only.**

Reference format:
```
> **Diagram**: [filename.png](diagrams/filename.png)
> _Generated from [filename.py](diagrams/filename.py) — run `python diagrams/filename.py` to regenerate_
```

### Diagram Standards (Python Diagrams)

Use the `/infrastructure-diagrams` skill for all cloud and infrastructure diagrams. Key patterns for this skill:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import ApplicationGateway, VirtualNetworks
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
from diagrams.azure.storage import BlobStorage
from diagrams.azure.security import KeyVaults
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.monitor import LogAnalyticsWorkspaces
from diagrams.onprem.client import Users

with Diagram("Diagram Title", show=False, filename="output-name", direction="TB",
             graph_attr={"bgcolor": "white", "pad": "0.5", "fontsize": "13"}):
    # Zones as Clusters; Azure resources use official Azure icon classes
    internet = Users("Internet")
    with Cluster("rg-jamtrack-prod (UK South)"):
        with Cluster("Azure VNet 10.0.0.0/16"):
            with Cluster("Ingress Subnet 10.0.3.0/24"):
                appgw = ApplicationGateway("App Gateway + WAF v2")
            with Cluster("AKS Subnet 10.0.1.0/24"):
                aks = KubernetesServices("AKS\njamtrack-prod | staging")
            with Cluster("Data Subnet 10.0.2.0/24"):
                pg = DatabaseForPostgresqlServers("PostgreSQL Flexible Server")
        kv = KeyVaults("Key Vault")
        blob = BlobStorage("Blob Storage")
        entra = ActiveDirectory("Microsoft Entra ID")

    internet >> Edge(label="HTTPS TLS 1.3") >> appgw >> aks
    aks >> Edge(label="Private Endpoint") >> pg
    aks >> Edge(label="Managed Identity", style="dashed") >> kv
    aks >> Edge(label="Managed Identity", style="dashed") >> blob
```

**Edge conventions:**
- Solid `>>` — synchronous / network call; add `Edge(label="protocol")`
- Dashed `Edge(style="dashed")` — identity/credential flows (Managed Identity, Key Vault secret fetch)
- Dotted `Edge(style="dotted")` — async / event-driven flows

**Cluster conventions:**
- Outermost cluster = Resource Group
- Next level = VNet (with CIDR)
- Inner clusters = named subnets with CIDR labels
- Services outside VNet (ACR, Key Vault, Blob) sit at Resource Group level

---

## 1. Phase-Aware Infrastructure Overview

Show what infrastructure applies at each phase:

| Component | Phase 2 (local) | Phase 3–4 (Azure VMs) | Phase 5–6 (Containers + ACA) | Phase 7+ (AKS) |
|-----------|-----------------|----------------------|------------------------------|-----------------|
| Compute | Docker Compose | Azure VMs + Nginx | Docker + Azure Container Apps | Azure AKS |
| Container registry | Local Docker | Local Docker | Azure Container Registry (ACR) | Azure Container Registry (ACR) |
| Database | Docker Postgres 16 | PostgreSQL on Azure VM | Azure Database for PostgreSQL Flexible Server | Azure Database for PostgreSQL Flexible Server |
| Secrets | `.env.local` (gitignored) | `.env` on VM (gitignored) | Azure Key Vault | Azure Key Vault |
| Ingress | `localhost` ports | Nginx reverse proxy | App Gateway / ACA ingress | Azure Application Gateway + WAF v2 |
| DNS | — | Azure DNS (optional) | Azure DNS | Azure DNS |
| Monitoring | stdout logs | stdout logs | stdout logs | ELK on AKS + ClickHouse |

### 2. Azure Network Topology Diagram (Phase 4+)

**File**: `docs/architecture/<feature>/diagrams/cloud-network-topology.py` → generates `cloud-network-topology.png`

Use the `/infrastructure-diagrams` skill. Diagram elements:
- Outermost `Cluster`: Resource Group `rg-jamtrack-prod (UK South)`
- Inner `Cluster`: Azure VNet `10.0.0.0/16` containing three subnet clusters
- `Cluster("Ingress Subnet 10.0.3.0/24")` → `ApplicationGateway("App Gateway + WAF v2")`
- `Cluster("AKS Subnet 10.0.1.0/24")` → `KubernetesServices("AKS\njamtrack-prod | staging")`
- `Cluster("Data Subnet 10.0.2.0/24")` → `DatabaseForPostgresqlServers(...)`, `CacheForRedis(...)`
- At Resource Group level (outside VNet): `KeyVaults`, `BlobStorage`, `ActiveDirectory`, `LogAnalyticsWorkspaces`, `ContainerRegistries`
- Top-level: `Users("Internet")` node
- Flow: Internet → App Gateway → AKS; AKS → data subnet (Private Endpoint solid); AKS → KV/Blob/Entra (Managed Identity dashed)

Reference in this document:
```
> **Diagram**: [cloud-network-topology.png](diagrams/cloud-network-topology.png)
> _Generated from [cloud-network-topology.py](diagrams/cloud-network-topology.py) — run `python diagrams/cloud-network-topology.py` to regenerate_
```

### 3. AKS Node Pool Sizing

| Environment | Node pool | Node SKU | Min nodes | Max nodes | Rationale |
|-------------|-----------|----------|-----------|-----------|-----------|
| Staging | `system` | Standard_B2s | 1 | 3 | Low traffic, cost-optimised |
| Staging | `user` | Standard_B4ms | 1 | 3 | App workloads |
| Production | `system` | Standard_D2s_v5 | 2 | 3 | HA system workloads |
| Production | `user` | Standard_D4s_v5 | 2 | 10 | App workloads, auto-scale |

### 4. Cost Estimate Table

**Dev/Staging (monthly)**

| Resource | SKU / Config | Hours | Unit cost | Monthly cost |
|----------|-------------|-------|-----------|-------------|
| AKS nodes (staging) | 2× Standard_B4ms | 730 | £0.18/hr | ~£263 |
| PostgreSQL Flexible (staging) | Burstable B_Standard_B2ms | 730 | £0.08/hr | ~£58 |
| ACR | Basic | — | £4.50 | £4.50 |
| Key Vault | Standard | — | ~£1 | ~£1 |
| **Staging total** | | | | **~£326/month** |

**Production — Baseline (monthly)**

| Resource | SKU / Config | Hours | Unit cost | Monthly cost |
|----------|-------------|-------|-----------|-------------|
| AKS nodes (2× D4s_v5) | 2× Standard_D4s_v5 | 730 | £0.21/hr | ~£307 |
| PostgreSQL Flexible | General Purpose D4s | 730 | £0.38/hr | ~£277 |
| App Gateway WAF v2 | WAF_v2 | 730 | £0.25/hr | ~£183 |
| Azure DNS | — | — | ~£1 | ~£1 |
| Log Analytics | Pay-per-GB (~5GB/day) | — | £2.30/GB | ~£345 |
| **Production baseline** | | | | **~£1,113/month** |

**Production at 2× load**: +1 AKS node = ~£1,250/month
**Production at 10× load**: +4 AKS nodes = ~£1,650/month

### 5. Total Cost of Ownership (TCO)

| Scenario | Monthly | Annual | Notes |
|----------|---------|--------|-------|
| Development (Phase 2–3) | £0 | £0 | Local only |
| Staging (Phase 4+) | £326 | £3,912 | Always-on staging |
| Production baseline (Phase 4+) | £1,113 | £13,356 | |
| Production at 2× | £1,250 | £15,000 | |
| Production at 10× | £1,650 | £19,800 | |
| **Phase 4 Year 1 total** | | **~£17,268** | Staging + prod baseline |

### 6. Cost Optimisation Recommendations

| Recommendation | Saving | Effort | Priority |
|----------------|--------|--------|----------|
| Turn off staging outside business hours (auto-shutdown 19:00–08:00) | ~£130/month | Low | High |
| Use Azure Spot instances for staging node pool | ~£100/month | Medium | Medium |
| Reserved instances for production nodes (1-year) | ~£200/month | Low | Medium |
| Use Burstable SKU for PostgreSQL in staging | ~£100/month | Low | High |

### 7. Helm Chart Structure

```
helm/
  <service-name>/
    Chart.yaml
    values.yaml           # defaults
    values.staging.yaml   # staging overrides
    values.prod.yaml      # production overrides
    templates/
      deployment.yaml
      service.yaml
      configmap.yaml
      hpa.yaml            # HorizontalPodAutoscaler
      pdb.yaml            # PodDisruptionBudget
```

---

### 8. Physical Deployment Diagram (Azure)

Produce a physical deployment diagram that follows [Azure Architecture Center diagram guidelines](https://learn.microsoft.com/en-us/azure/architecture/browse/). Every Azure resource must be represented using its **official product name** and styled with Azure brand colours. Generic labels ("DB", "cluster", "gateway") are not acceptable in physical deployment diagrams.

**Naming conventions — use these exact labels**:

| Service | Official Azure Label |
|---------|----------------------|
| Kubernetes cluster | `Azure Kubernetes Service (AKS)` |
| Container registry | `Azure Container Registry (ACR)` |
| PostgreSQL | `Azure Database for PostgreSQL Flexible Server` |
| Secrets | `Azure Key Vault` |
| Ingress / WAF | `Azure Application Gateway + WAF v2` |
| Virtual network | `Azure Virtual Network (VNet)` |
| DNS | `Azure DNS` |
| Logging | `Azure Monitor + Log Analytics Workspace` |
| Identity | `Microsoft Entra ID (Managed Identity)` |
| CI/CD | `GitHub Actions → ACR` |

**Layout conventions** (Azure Architecture Center):
- Group all resources inside their **Azure Resource Group** boundary
- Use a **hub-spoke VNet topology**: ingress subnet → AKS subnet → data subnet, each in its own named CIDR block
- Show **Private Endpoints** explicitly for every PaaS service (PostgreSQL, Key Vault, ACR)
- Show **Managed Identity** arrows for all workload-to-service authentication — never draw a connection string as a credential flow
- Internet entry point is always drawn at the top; data stores at the bottom

**Colour conventions** — apply via Mermaid `classDef` or draw.io fill colours:

| Layer | Fill colour | Border colour |
|-------|-------------|---------------|
| Azure services | `#0078D4` (Azure Blue) | `#005A9E` |
| Network boundaries | `#E3F2FD` (light blue) | `#0078D4` |
| Data stores | `#F3E5F5` (light purple) | `#7B1FA2` |
| Security / identity | `#FFF3E0` (light orange) | `#E65100` |

**File**: `docs/architecture/<feature>/diagrams/physical-deployment.py` → generates `physical-deployment.png`

Use the `/infrastructure-diagrams` skill. Follow the naming conventions table above exactly in node labels. Diagram elements:
- `Cluster("rg-jamtrack-prod (UK South)")` — outermost boundary
- `Cluster("Azure VNet 10.0.0.0/16")` containing three subnet clusters
- `Cluster("Ingress Subnet 10.0.3.0/24")` → `ApplicationGateway("Azure Application Gateway + WAF v2")`
- `Cluster("AKS Subnet 10.0.1.0/24")` → nested clusters for each namespace: `jamtrack-prod`, `jamtrack-staging`, `jamtrack-system` — each containing its service `Pod` nodes
- `Cluster("Data Subnet 10.0.2.0/24")` → `DatabaseForPostgresqlServers("Azure Database for PostgreSQL Flexible Server\n(Private Endpoint)")`, `CacheForRedis("Azure Cache for Redis\n(Private Endpoint)")`
- At Resource Group level: `ContainerRegistries("Azure Container Registry (ACR)")`, `KeyVaults("Azure Key Vault")`, `LogAnalyticsWorkspaces("Azure Monitor + Log Analytics")`, `ActiveDirectory("Microsoft Entra ID")`
- `Users("Internet")` at top
- Edges: Internet → App Gateway (`HTTPS :443`); App Gateway → AKS; AKS → PostgreSQL/Redis (`Private Endpoint` solid); AKS → ACR/KV/Monitor/Entra (`Managed Identity` dashed)

Reference in this document:
```
> **Diagram**: [physical-deployment.png](diagrams/physical-deployment.png)
> _Generated from [physical-deployment.py](diagrams/physical-deployment.py) — run `python diagrams/physical-deployment.py` to regenerate_
```

---

## Financial Lens (mandatory)

Cloud costs compound silently. Treat every infrastructure decision as a financial decision.

- Cloud costs are routinely underestimated by 3–5× at design time. Use the Azure pricing calculator, then add a 30% buffer.
- Log Analytics / ELK data ingestion grows with traffic. Define retention policies (30 days hot, 90 days cold archive) before deploying — not after you get the first bill.
- Reserved instances: commit 1-year reservations on production workloads for ~40% savings. Never commit staging (you need the flexibility to resize or kill it).
- Right-sizing is continuous: enable Azure Advisor cost recommendations from Phase 4 day one and act on them weekly in the first month.
- Auto-shutdown for non-production: staging running 24/7 costs 3× what it needs to. Schedule a nightly shutdown (19:00–08:00) from day one.

---

## Best Practice Patterns

**Infrastructure as Code**
- *Everything in code*: every resource — VNet, AKS cluster, ACR, Key Vault, PostgreSQL, DNS zone — must be defined in Terraform. ClickOps (manual portal changes) creates configuration drift that is invisible until it causes an incident.
- *Terraform state in remote backend*: use Azure Storage as the Terraform state backend with state locking. Local `terraform.tfstate` files are a disaster waiting to happen.
- *Modules for reuse*: extract repeated patterns (AKS node pool, Key Vault access policy, private endpoint) into Terraform modules. Don't copy-paste.
- *Plan before apply*: always run `terraform plan` and review the diff before `terraform apply`. Treat it like a code review.

**Kubernetes and Helm**
- *GitOps with Flux or ArgoCD*: sync Helm chart state from Git to AKS. This eliminates manual `helm upgrade` commands and configuration drift. Every deployed state is a commit.
- *HPA (HorizontalPodAutoscaler) from day one*: define min/max replicas and CPU/memory targets in the Helm chart from the first deployment. Retrofitting autoscaling is painful.
- *PodDisruptionBudgets*: define a PDB (`minAvailable: 1`) for every workload. Without it, AKS node upgrades will evict all pods simultaneously.
- *Resource requests and limits*: every container must have CPU and memory requests/limits. No limits = one leaking pod evicts all other pods on the node.
- *Liveness and readiness probes*: every pod must have both. Readiness prevents traffic routing to pods that haven't fully started. Liveness restarts stuck pods.
- *Namespace isolation*: separate namespaces for `jamtrack-prod`, `jamtrack-staging`, and system workloads. Apply ResourceQuotas per namespace.

**Networking and security**
- *Zero-trust networking*: no implicit trust on VNet membership. All internal traffic must be authenticated. Use Managed Identity (not connection strings) for all Azure resource access.
- *Private endpoints for all managed services*: PostgreSQL, Key Vault, ACR, and Blob Storage must all use private endpoints in production. No public IPs on data stores.
- *Network policies*: restrict pod-to-pod traffic with K8s NetworkPolicies. Default-deny all ingress; allow only documented flows.
- *Immutable container tags*: reference container images by SHA digest (not `latest` or mutable version tags) in production Helm charts. Mutable tags make rollbacks unreliable.

**Reliability patterns**
- *Cell-based architecture*: partition workloads into independently deployable cells. Limits blast radius — a problem in one cell does not cascade to others. Relevant at Phase 5+.
- *Multi-region active-passive*: not required for Jamtrack Radio at Phase 4, but design the data layer to support it (PostgreSQL geo-replicas, region-agnostic storage references).
- *Circuit breakers*: configure Dapr resilience policies (circuit breaker + retry with exponential backoff) on all service-to-service calls. Fail fast rather than cascade.
- *Graceful degradation*: design the streaming service to return a useful error if the Storage service is unavailable, rather than hanging or crashing.

---

## Anti-Patterns / Don'ts

**Infrastructure management**
- **ClickOps (manual portal changes)**: any Azure resource created or modified via the portal is invisible to Terraform state. The next `terraform apply` may destroy or reset it. Everything goes through IaC.
- **Hardcoded secrets in Helm values**: `values.yaml` containing passwords, connection strings, or API keys that get committed to Git. Use K8s Secrets (Phase 2–3) and Azure Key Vault (Phase 4+). Never put secrets in Helm values files.
- **Single state file for all environments**: one Terraform workspace managing dev, staging, and prod. A bad `terraform apply` can destroy production while targeting staging. Use separate workspaces or separate state backends per environment.
- **`terraform apply` without `terraform plan`**: always review the plan. A missing `prevent_destroy = true` lifecycle rule has caused many production database deletions.

**Kubernetes anti-patterns**
- **Running containers as root**: containers running as UID 0 have host-level privileges if they escape the container boundary. Set `runAsNonRoot: true` and `securityContext` on all pods.
- **No resource limits**: a single memory-leaking pod will consume all node memory and trigger an OOM eviction cascade. Every container must have `resources.limits` defined.
- **Missing liveness/readiness probes**: without probes, Kubernetes routes traffic to stuck or unready pods. Every production pod needs both probes.
- **Pulling `latest` tag in production**: `latest` is mutable. You cannot determine what is actually running or roll back reliably. Always use versioned, immutable tags.
- **All services in the default namespace**: the default namespace has no resource quotas, no network policies, and no access controls. Use named namespaces from the first deployment.
- **No PodDisruptionBudget**: node upgrades and drains will evict all replicas of a workload simultaneously if no PDB is set. This causes avoidable downtime.

**Cost anti-patterns**
- **Over-provisioning staging**: staging running D4s_v5 nodes (same as production) costs 3× what a burstable B2s needs. Staging is for testing correctness, not performance.
- **No cost alerts or budgets**: running without Azure Cost Management budgets means the first signal of runaway spend is the monthly invoice. Set a budget alert at 80% of expected monthly spend from day one.
- **Log Analytics without retention limits**: sending all logs to Log Analytics at £2.30/GB without an ILM retention policy. Set 30-day hot retention from day one.
- **Reserved instances on staging**: committing reserved capacity to staging removes the flexibility to resize or delete nodes when they are no longer needed.
