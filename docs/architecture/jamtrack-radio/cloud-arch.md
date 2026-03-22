# Cloud Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Cloud Architect)
**Status**: Accepted
**Skill**: `/cloud-architect jamtrack-radio` — DISCOVERY Step 5b
**Inputs**: `software-arch.md` (6 services defined), `jamtrack-radio-requirements.md` (budget: £50–100/month Azure from Phase 4)

---

## 1. Phase-Aware Infrastructure Overview

| Component | Phase 2 (local) | Phase 3 (local K8s) | Phase 4+ (Azure) |
|-----------|-----------------|---------------------|------------------|
| Compute | Docker Compose | Rancher Desktop K8s | Azure Kubernetes Service (AKS) |
| Container registry | Local Docker | Local Docker | Azure Container Registry (ACR) |
| Database | Docker PostgreSQL 16 | Docker PostgreSQL 16 | Azure Database for PostgreSQL Flexible Server |
| Secrets | `.env.local` (gitignored) | K8s Secrets | Azure Key Vault |
| Ingress | `localhost` ports | Traefik (Rancher Desktop) | Azure Application Gateway + WAF v2 |
| DNS | — | — | Azure DNS |
| Monitoring | stdout logs | stdout logs | ELK on AKS + ClickHouse |
| Blob storage | Local filesystem mock | Azure Blob (remote) or local MinIO | Azure Blob Storage (Hot tier) |
| Service mesh / sidecar | Dapr (local) | Dapr (K8s mode) | Dapr (K8s mode on AKS) |
| Pub/sub broker | Redis (Docker) | Redis (Docker/K8s) | Azure Service Bus (Standard) |
| Secrets vault | `.env.local` | K8s Secrets | Azure Key Vault |

---

## 2. Azure Network Topology Diagram (Phase 4+)

Hub-spoke VNet topology. Internet traffic enters via Application Gateway + WAF v2, routes through the AKS subnet, and connects to the data tier via private endpoints. Azure services outside the VNet authenticate via Managed Identity.

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="900" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Internet&lt;/b&gt;" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="460" y="10" width="160" height="70" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;Azure Virtual Network&lt;/b&gt;&lt;br&gt;10.0.0.0/16 — UK South (rg-jamtrack-prod)" style="swimlane;startSize=35;fillColor=#E3F2FD;strokeColor=#0078D4;fontStyle=1;fontSize=11;" vertex="1" parent="1">
      <mxGeometry x="160" y="120" width="780" height="560" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;Ingress Subnet&lt;/b&gt; 10.0.3.0/24" style="swimlane;startSize=25;fillColor=#FFF3E0;strokeColor=#E65100;dashed=1;fontSize=11;" vertex="1" parent="3">
      <mxGeometry x="240" y="40" width="300" height="110" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;Azure Application Gateway&lt;/b&gt;&lt;br&gt;+ WAF v2 (OWASP ruleset)&lt;br&gt;TLS 1.3 termination" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#005A9E;fontColor=#ffffff;" vertex="1" parent="4">
      <mxGeometry x="40" y="35" width="220" height="60" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;AKS Subnet&lt;/b&gt; 10.0.1.0/24" style="swimlane;startSize=25;fillColor=#E8F5E9;strokeColor=#2E7D32;dashed=1;fontSize=11;" vertex="1" parent="3">
      <mxGeometry x="80" y="190" width="620" height="170" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;Azure Kubernetes Service&lt;/b&gt;&lt;br&gt;NS: jamtrack-prod | jamtrack-staging | jamtrack-system&lt;br&gt;6 microservices + Dapr sidecars&lt;br&gt;HPA on all workload pods" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#005A9E;fontColor=#ffffff;" vertex="1" parent="6">
      <mxGeometry x="90" y="35" width="440" height="110" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Data Subnet&lt;/b&gt; 10.0.2.0/24" style="swimlane;startSize=25;fillColor=#F3E5F5;strokeColor=#7B1FA2;dashed=1;fontSize=11;" vertex="1" parent="3">
      <mxGeometry x="80" y="400" width="620" height="120" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;Azure Database for PostgreSQL&lt;/b&gt;&lt;br&gt;Flexible Server — Private Endpoint&lt;br&gt;Prod: D4s | Staging: B2ms" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="8">
      <mxGeometry x="50" y="25" width="220" height="75" as="geometry" />
    </mxCell>
    <mxCell id="10" value="&lt;b&gt;Azure Cache for Redis&lt;/b&gt;&lt;br&gt;Private Endpoint&lt;br&gt;Dapr pub/sub backing (Phase 3)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#fff3e0;strokeColor=#E65100;" vertex="1" parent="8">
      <mxGeometry x="350" y="25" width="220" height="75" as="geometry" />
    </mxCell>
    <mxCell id="11" value="&lt;b&gt;Azure Container Registry&lt;/b&gt;&lt;br&gt;acr-jamtrack&lt;br&gt;Image pull via AKS Managed Identity" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="20" y="180" width="120" height="90" as="geometry" />
    </mxCell>
    <mxCell id="12" value="&lt;b&gt;Azure Key Vault&lt;/b&gt;&lt;br&gt;kv-jamtrack-prod&lt;br&gt;RS256 key, DB connection strings" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="20" y="310" width="120" height="90" as="geometry" />
    </mxCell>
    <mxCell id="13" value="&lt;b&gt;Azure Service Bus&lt;/b&gt;&lt;br&gt;sb-jamtrack (Standard)&lt;br&gt;Dapr pub/sub (Phase 4+)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="980" y="180" width="130" height="90" as="geometry" />
    </mxCell>
    <mxCell id="14" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;stjamtrack&lt;br&gt;Audio + artwork (Hot LRS)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="980" y="310" width="130" height="90" as="geometry" />
    </mxCell>
    <mxCell id="15" value="&lt;b&gt;Log Analytics&lt;/b&gt;&lt;br&gt;+ Azure Monitor&lt;br&gt;ELK on AKS (Phase 4+)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="980" y="440" width="130" height="80" as="geometry" />
    </mxCell>
    <mxCell id="16" value="&lt;b&gt;Microsoft Entra ID&lt;/b&gt;&lt;br&gt;Workload Identity&lt;br&gt;Managed Identity (AKS pods)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;" vertex="1" parent="1">
      <mxGeometry x="20" y="440" width="120" height="90" as="geometry" />
    </mxCell>
    <mxCell id="17" value="HTTPS TLS 1.3" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="18" value="" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="4" target="6" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="19" value="Private Endpoint" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="6" target="8" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="20" value="Managed Identity" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="6" target="12" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="21" value="Managed Identity" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="6" target="14" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="22" value="AMQP (Phase 4+)" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="6" target="13" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```

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

### Dev / Staging (monthly, Phase 4+)

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

### Production — Baseline (monthly, Phase 4+)

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
| Development (Phase 2–3) | £0 | £0 | Local only |
| Staging (Phase 4+) | £197–256 | £2,364–3,072 | Always-on |
| Production baseline (Phase 4+) | £1,142 | £13,704 | |
| Production at 2× | £1,295 | £15,540 | |
| Production at 10× | £1,700 | £20,400 | |
| **Phase 4 Year 1 total** | | **~£16,068–17,000** | Staging + prod baseline |

> **Budget check**: The personal budget constraint is £50–100/month (requirements §3). This architecture significantly exceeds it at full Phase 4 deployment. **Mitigation**: Phase 4 development runs on staging only (£197–256/month with auto-shutdown — see §7). Production-grade sizing applies only if the platform is used for live streaming.

---

## 7. Cost Optimisation Recommendations

| Recommendation | Saving | Effort | Priority |
|----------------|--------|--------|----------|
| Auto-shutdown staging 19:00–08:00 | ~£100/month (staging) | Low | High |
| Use Azure Spot instances for staging node pool | ~£50–80/month | Medium | Medium |
| 1-year reserved instances for production compute | ~£120/month | Low | Medium (Phase 4+) |
| Burstable B-series for PostgreSQL staging | Already applied | — | Done |
| Set Log Analytics retention to 30 days hot / archive cold | ~£100/month at prod scale | Low | High |
| Use Azure Blob Cool tier for tracks not accessed in 30 days | ~£5/month | Low | Phase 5 |
| Budget alert at 80% of expected spend | £0 | Low | High — do this on day one |

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

## 9. Physical Deployment Diagram (Azure — Phase 4+)

Full Azure resource group view using official Azure service names and Azure Architecture Center icon conventions.

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1554" pageHeight="1000" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Internet&lt;/b&gt;&lt;br&gt;HTTPS TLS 1.3" style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="1">
      <mxGeometry x="620" y="10" width="160" height="70" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;Resource Group: rg-jamtrack-prod (UK South)&lt;/b&gt;" style="swimlane;startSize=30;fillColor=#f0f0f0;strokeColor=#333333;fontStyle=1;fontSize=12;" vertex="1" parent="1">
      <mxGeometry x="60" y="110" width="1300" height="780" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;Azure Virtual Network&lt;/b&gt;&lt;br&gt;vnet-jamtrack-prod — 10.0.0.0/16" style="swimlane;startSize=30;fillColor=#E3F2FD;strokeColor=#0078D4;fontStyle=1;" vertex="1" parent="3">
      <mxGeometry x="200" y="50" width="700" height="620" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;Ingress Subnet&lt;/b&gt; 10.0.3.0/24" style="swimlane;startSize=25;fillColor=#FFF3E0;strokeColor=#E65100;dashed=1;fontSize=11;" vertex="1" parent="4">
      <mxGeometry x="160" y="40" width="380" height="100" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;Azure Application Gateway v2&lt;/b&gt;&lt;br&gt;agw-jamtrack-prod&lt;br&gt;WAF v2 — OWASP 3.2 ruleset&lt;br&gt;TLS termination — cert from Key Vault" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#005A9E;fontColor=#ffffff;" vertex="1" parent="5">
      <mxGeometry x="40" y="30" width="300" height="55" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;AKS Subnet&lt;/b&gt; 10.0.1.0/24" style="swimlane;startSize=25;fillColor=#E8F5E9;strokeColor=#2E7D32;dashed=1;fontSize=11;" vertex="1" parent="4">
      <mxGeometry x="30" y="180" width="640" height="250" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Azure Kubernetes Service&lt;/b&gt;&lt;br&gt;aks-jamtrack-prod&lt;br&gt;System pool: 2× Standard_D2s_v5&lt;br&gt;User pool: 2–10× Standard_D4s_v5 (HPA)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#0078D4;strokeColor=#005A9E;fontColor=#ffffff;" vertex="1" parent="7">
      <mxGeometry x="30" y="35" width="300" height="90" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;Namespace: jamtrack-prod&lt;/b&gt;&lt;br&gt;API Gateway, Identity, Track,&lt;br&gt;Playlist, Streaming, Storage&lt;br&gt;+ Dapr sidecars" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="7">
      <mxGeometry x="360" y="35" width="250" height="90" as="geometry" />
    </mxCell>
    <mxCell id="10" value="&lt;b&gt;Namespace: jamtrack-staging&lt;/b&gt;&lt;br&gt;Staging workloads&lt;br&gt;Auto-shutdown 19:00–08:00" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="7">
      <mxGeometry x="30" y="160" width="250" height="75" as="geometry" />
    </mxCell>
    <mxCell id="11" value="&lt;b&gt;Namespace: jamtrack-system&lt;/b&gt;&lt;br&gt;Dapr control plane, Redis,&lt;br&gt;Monitoring agents" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="7">
      <mxGeometry x="360" y="160" width="250" height="75" as="geometry" />
    </mxCell>
    <mxCell id="12" value="&lt;b&gt;Data Subnet&lt;/b&gt; 10.0.2.0/24" style="swimlane;startSize=25;fillColor=#F3E5F5;strokeColor=#7B1FA2;dashed=1;fontSize=11;" vertex="1" parent="4">
      <mxGeometry x="30" y="470" width="640" height="120" as="geometry" />
    </mxCell>
    <mxCell id="13" value="&lt;b&gt;Azure Database for PostgreSQL&lt;/b&gt;&lt;br&gt;psql-jamtrack-prod&lt;br&gt;Flexible Server — D4s_v5&lt;br&gt;Private Endpoint — encrypted at rest" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="12">
      <mxGeometry x="30" y="25" width="270" height="80" as="geometry" />
    </mxCell>
    <mxCell id="14" value="&lt;b&gt;Azure Cache for Redis&lt;/b&gt;&lt;br&gt;redis-jamtrack-prod&lt;br&gt;Private Endpoint" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#fff3e0;strokeColor=#E65100;" vertex="1" parent="12">
      <mxGeometry x="370" y="25" width="230" height="80" as="geometry" />
    </mxCell>
    <mxCell id="15" value="&lt;b&gt;Azure Container Registry&lt;/b&gt;&lt;br&gt;acr-jamtrack&lt;br&gt;Basic SKU — image pull via&lt;br&gt;AKS Managed Identity" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="3">
      <mxGeometry x="30" y="60" width="150" height="100" as="geometry" />
    </mxCell>
    <mxCell id="16" value="&lt;b&gt;Azure Key Vault&lt;/b&gt;&lt;br&gt;kv-jamtrack-prod&lt;br&gt;RS256 signing key&lt;br&gt;DB connection strings&lt;br&gt;Managed Identity RBAC" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;" vertex="1" parent="3">
      <mxGeometry x="30" y="200" width="150" height="110" as="geometry" />
    </mxCell>
    <mxCell id="17" value="&lt;b&gt;Azure Service Bus&lt;/b&gt;&lt;br&gt;sb-jamtrack (Standard)&lt;br&gt;Dapr pub/sub backing store&lt;br&gt;Phase 4+ replaces Redis" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="3">
      <mxGeometry x="1020" y="60" width="150" height="110" as="geometry" />
    </mxCell>
    <mxCell id="18" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;stjamtrack&lt;br&gt;Audio files + artwork&lt;br&gt;Hot LRS — ~100 GB Year 1&lt;br&gt;Authenticated access only" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="3">
      <mxGeometry x="1020" y="200" width="150" height="120" as="geometry" />
    </mxCell>
    <mxCell id="19" value="&lt;b&gt;Log Analytics Workspace&lt;/b&gt;&lt;br&gt;law-jamtrack-prod&lt;br&gt;ELK on AKS (Serilog)&lt;br&gt;5 GB/day — 30-day hot&lt;br&gt;~£345/month prod" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="3">
      <mxGeometry x="1020" y="360" width="150" height="120" as="geometry" />
    </mxCell>
    <mxCell id="20" value="&lt;b&gt;Microsoft Entra ID&lt;/b&gt;&lt;br&gt;Workload Identity&lt;br&gt;AKS pod → Azure services&lt;br&gt;No credential secrets in pods" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;" vertex="1" parent="3">
      <mxGeometry x="30" y="360" width="150" height="100" as="geometry" />
    </mxCell>
    <mxCell id="21" value="&lt;b&gt;Azure DNS&lt;/b&gt;&lt;br&gt;jamtrackradio.com" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" vertex="1" parent="3">
      <mxGeometry x="30" y="500" width="150" height="70" as="geometry" />
    </mxCell>
    <mxCell id="22" value="HTTPS TLS 1.3" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="5" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="23" value="" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="5" target="7" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="24" value="Private Endpoint SSL" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="7" target="12" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="25" value="Managed Identity" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="7" target="16" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="26" value="Managed Identity" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="7" target="18" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="27" value="AMQP" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="7" target="17" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
  </root>
</mxGraphModel>
```
