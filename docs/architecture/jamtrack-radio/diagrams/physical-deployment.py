from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
from diagrams.azure.storage import BlobStorage
from diagrams.azure.security import KeyVaults
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.monitor import LogAnalyticsWorkspaces
from diagrams.azure.devops import Pipelines
from diagrams.k8s.compute import Pod
from diagrams.onprem.client import Users

DIAGRAMS_DIR = "/mnt/c/training/jamtrack-radio/docs/architecture/jamtrack-radio/diagrams"

with Diagram(
    "Jamtrack Radio — Physical Deployment (Azure Phase 4+)",
    show=False,
    filename=f"{DIAGRAMS_DIR}/physical-deployment",
    direction="TB",
    graph_attr={"bgcolor": "white", "pad": "0.8", "fontsize": "13", "fontname": "Helvetica"},
    node_attr={"fontsize": "10", "fontname": "Helvetica"},
    edge_attr={"fontsize": "9", "fontname": "Helvetica"},
):
    internet = Users("Internet")
    cicd = Pipelines("GitHub Actions\n→ ACR build & push")

    with Cluster("rg-jamtrack-prod  (UK South)"):
        with Cluster("Azure Virtual Network  10.0.0.0/16"):
            with Cluster("Ingress Subnet  10.0.3.0/24"):
                appgw = ApplicationGateway("Azure Application Gateway\n+ WAF v2  :443")

            with Cluster("AKS Subnet  10.0.1.0/24"):
                with Cluster("jamtrack-prod"):
                    apigw_pod = Pod("API Gateway\n(YARP :5000)")
                    identity_pod = Pod("Identity\nService :5001")
                    track_pod = Pod("Track\nService :5002")
                    playlist_pod = Pod("Playlist\nService :5003")
                    streaming_pod = Pod("Streaming\nService :5004")
                    storage_pod = Pod("Storage\nService :5005")

                with Cluster("jamtrack-staging"):
                    staging = KubernetesServices("Staging workloads\n(mirror of prod)")

                with Cluster("jamtrack-system"):
                    dapr = Pod("Dapr sidecars\n+ pub/sub")

            with Cluster("Data Subnet  10.0.2.0/24"):
                pg = DatabaseForPostgresqlServers("Azure Database for PostgreSQL\nFlexible Server (Private Endpoint)\nProd: D4s_v5 | Staging: B2ms")
                redis = CacheForRedis("Azure Cache for Redis\n(Private Endpoint)")

        kv = KeyVaults("Azure Key Vault\nkv-jamtrack-prod")
        blob = BlobStorage("Azure Blob Storage\nstjamtrack  Hot LRS")
        monitor = LogAnalyticsWorkspaces("Log Analytics\n+ Azure Monitor")
        entra = ActiveDirectory("Microsoft Entra ID\nManaged Identity")

    internet >> Edge(label="HTTPS :443 / TLS 1.3") >> appgw >> apigw_pod
    apigw_pod >> [identity_pod, track_pod, playlist_pod, streaming_pod, storage_pod]
    [identity_pod, track_pod, playlist_pod, storage_pod] >> Edge(label="SQL / Private Endpoint") >> pg
    storage_pod >> Edge(label="Managed Identity", style="dashed") >> blob
    dapr >> Edge(label="Pub/Sub") >> redis
    apigw_pod >> Edge(label="Managed Identity", style="dashed") >> kv
    apigw_pod >> Edge(label="Telemetry", style="dotted") >> monitor
    apigw_pod >> Edge(label="Workload Identity", style="dashed") >> entra
    cicd >> Edge(label="Image push", style="dashed") >> staging
