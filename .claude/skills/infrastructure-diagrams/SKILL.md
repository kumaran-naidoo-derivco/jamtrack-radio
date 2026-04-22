---
name: infrastructure-diagrams
description: "Generate deployed cloud and network infrastructure diagrams for Jamtrack Radio as PNG files using Python's Diagrams library. Use when someone wants to visualise running infrastructure \u2014 Azure VMs, AKS clusters, Container Apps, EKS nodes, VNets, subnets, or how deployed services connect to databases and storage. Trigger on phrases like 'draw the phase N architecture', 'show me the infrastructure', 'topology diagram', 'visualise the AKS/ACA/EKS setup', 'diagram the services and their databases', 'picture of the azure vm layout'. Has ready-made templates for microservices layout, Phase 3 (Azure VMs + Nginx), Phase 6 (ACA), Phase 7 (AKS + Helm), Phase 8 (AWS EKS), hub-and-spoke, hybrid cloud, three-tier, and DR. Outputs PNG. Do NOT use for sequence diagrams, class diagrams, flowcharts, ER/schema diagrams, STRIDE threat models, wireframes, draw.io files, or conceptual Clean Architecture layer diagrams \u2014 those have dedicated skills."
---

# Infrastructure Diagrams Skill

Generate Jamtrack Radio infrastructure diagrams using Python's Diagrams library.

## Step 1 — Check Dependencies

Run this first. It is a no-op if already installed:

```bash
pip install diagrams --quiet --break-system-packages 2>/dev/null
which dot >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y graphviz -qq 2>/dev/null)
which dot >/dev/null 2>&1 && echo "OK" || echo "MISSING"
```

If the last line prints `MISSING`, Graphviz could not be installed. Stop and tell the user:
> "Graphviz is not available in this environment. Use `/drawio` to create an editable diagram instead."

## Step 2 — Pick an Approach

### A. Use a project template (fastest)

The bundled script has Jamtrack Radio-specific templates:

```bash
python .claude/skills/infrastructure-diagrams/scripts/generate_diagram.py \
  --type <type> --output docs/architecture/jamtrack-radio/<filename>
```

| `--type` | What it draws |
|----------|--------------|
| `microservices` | All Jamtrack Radio services: Identity, Track, Streaming, API Gateway + PostgreSQL |
| `phase3-vm` | Phase 3: Azure VMs behind Nginx, single region |
| `phase6-aca` | Phase 6: Azure Container Apps with DAPR |
| `phase7-aks` | Phase 7: AKS + Helm + ACR + PostgreSQL + Key Vault |
| `phase8-eks` | Phase 8: AWS EKS equivalent |
| `hub-spoke` | Azure hub-and-spoke network topology |
| `hybrid` | Hybrid on-premises ↔ Azure connectivity |
| `three-tier` | Classic three-tier web application |
| `dr` | Multi-region disaster recovery |

### B. Write a custom diagram

When no template fits, write Python directly. Full pattern:

```python
from diagrams import Diagram, Cluster, Edge
# Import nodes — see the section below

with Diagram(
    "Diagram Title",
    show=False,           # always False — no display in WSL
    filename="docs/architecture/jamtrack-radio/output-name",  # no extension
    direction="LR",       # LR (flow) or TB (hierarchy)
    graph_attr={"bgcolor": "white", "pad": "0.5"},
):
    with Cluster("Azure"):
        # resources go here
        pass
```

Run the script with `python diagram_name.py` and it will write a PNG.

## Step 3 — Save and Present

The templates save directly to the path you gave `--output`. For custom scripts, confirm the file is in `docs/architecture/jamtrack-radio/`.

Tell the user:
- The full path to the PNG
- What the diagram shows
- Whether to open in VS Code (image preview) or GitHub

---

## Import Reference for Jamtrack Radio

Use these imports — they are verified to work in the installed Diagrams version:

```python
# Compute
from diagrams.azure.compute import (
    VM, VMScaleSet, KubernetesServices,
    ContainerInstances, ContainerApps, ContainerRegistries,
    FunctionApps, AppServices
)

# Networking
from diagrams.azure.network import (
    VirtualNetworks, LoadBalancers, ApplicationGateway,
    VirtualNetworkGateways, Firewall, TrafficManagerProfiles,
    DNSZones, CDNProfiles
)

# Database
from diagrams.azure.database import (
    DatabaseForPostgresqlServers, SQLDatabases, CosmosDb, CacheForRedis
)

# Storage
from diagrams.azure.storage import BlobStorage, StorageAccounts

# Security
from diagrams.azure.security import KeyVaults

# Identity
from diagrams.azure.identity import ManagedIdentities, ActiveDirectory

# Monitoring
from diagrams.azure.monitor import LogAnalyticsWorkspaces, ApplicationInsights

# Kubernetes internals (for AKS diagrams)
from diagrams.k8s.compute import Pod, Deployment, StatefulSet
from diagrams.k8s.network import Service, Ingress

# On-premises / external
from diagrams.onprem.client import Users
from diagrams.onprem.network import Nginx, HAProxy
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.compute import Server

# AWS (Phase 8)
from diagrams.aws.compute import EKS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
```

**Import pitfall**: `azure.network` and `azure.networking` are two different modules with different classes. When in doubt, use `azure.network` — it has broader coverage.

---

## Edge Styling Cheat Sheet

```python
a >> b                              # simple arrow
a >> Edge(label="HTTPS") >> b       # labelled
a >> Edge(color="green", style="bold") >> b
a >> Edge(style="dashed", label="Failover", color="orange") >> b
a - b                               # bidirectional
a >> [b, c, d]                      # fan-out
```

## Cluster Colours

```python
with Cluster("Production", graph_attr={"bgcolor": "lightgreen"}):
    pass
with Cluster("Development", graph_attr={"bgcolor": "lightyellow"}):
    pass
with Cluster("DR / Standby", graph_attr={"bgcolor": "lightsalmon"}):
    pass
```

---

## Reference Files

For the complete node catalogue, consult:
- `references/azure-nodes.md` — every Azure provider class and its import
- `references/onprem-nodes.md` — on-premises and generic provider classes
- `references/patterns.md` — ready-to-run code for 7 common topologies
