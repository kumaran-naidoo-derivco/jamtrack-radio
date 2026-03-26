from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
from diagrams.azure.storage import BlobStorage
from diagrams.azure.security import KeyVaults
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.monitor import LogAnalyticsWorkspaces
from diagrams.azure.devops import Pipelines
from diagrams.onprem.client import Users

DIAGRAMS_DIR = "/mnt/c/training/jamtrack-radio/docs/architecture/jamtrack-radio/diagrams"

with Diagram(
    "Jamtrack Radio — Azure Network Topology (Phase 4+)",
    show=False,
    filename=f"{DIAGRAMS_DIR}/cloud-network-topology",
    direction="TB",
    graph_attr={"bgcolor": "white", "pad": "0.8", "fontsize": "14", "fontname": "Helvetica"},
    node_attr={"fontsize": "11", "fontname": "Helvetica"},
    edge_attr={"fontsize": "10", "fontname": "Helvetica"},
):
    internet = Users("Internet")
    cicd = Pipelines("GitHub Actions")

    with Cluster("rg-jamtrack-prod  (UK South)"):
        with Cluster("Azure Virtual Network  10.0.0.0/16"):
            with Cluster("Ingress Subnet  10.0.3.0/24"):
                appgw = ApplicationGateway("Azure Application Gateway\n+ WAF v2\nTLS 1.3 termination")

            with Cluster("AKS Subnet  10.0.1.0/24"):
                aks = KubernetesServices("Azure Kubernetes Service\nNS: jamtrack-prod | staging | system\n6 microservices + Dapr sidecars\nHPA on all workloads")

            with Cluster("Data Subnet  10.0.2.0/24"):
                pg = DatabaseForPostgresqlServers("Azure Database for PostgreSQL\nFlexible Server\n(Private Endpoint)")
                redis = CacheForRedis("Azure Cache for Redis\n(Private Endpoint)\nDapr pub/sub backing")

        kv = KeyVaults("Azure Key Vault\nkv-jamtrack-prod\nRS256 key · DB creds")
        blob = BlobStorage("Azure Blob Storage\nstjamtrack\nAudio + artwork (Hot LRS)")
        monitor = LogAnalyticsWorkspaces("Log Analytics\n+ Azure Monitor\nELK on AKS (Phase 4+)")
        entra = ActiveDirectory("Microsoft Entra ID\nWorkload Identity\nManaged Identity")

    internet >> Edge(label="HTTPS TLS 1.3") >> appgw
    appgw >> Edge(label="HTTP/2") >> aks
    aks >> Edge(label="Private Endpoint") >> pg
    aks >> Edge(label="Private Endpoint") >> redis
    aks >> Edge(label="Managed Identity", style="dashed") >> kv
    aks >> Edge(label="Managed Identity", style="dashed") >> blob
    aks >> Edge(label="Managed Identity", style="dashed") >> monitor
    aks >> Edge(label="Workload Identity", style="dashed") >> entra
    cicd >> Edge(label="Image push", style="dashed") >> aks
