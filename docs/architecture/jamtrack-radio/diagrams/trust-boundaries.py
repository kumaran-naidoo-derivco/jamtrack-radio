from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.azure.identity import ActiveDirectory
from diagrams.onprem.client import Users

DIAGRAMS_DIR = "/mnt/c/training/jamtrack-radio/docs/architecture/jamtrack-radio/diagrams"

with Diagram(
    "Jamtrack Radio — Trust Boundaries & Security Zones",
    show=False,
    filename=f"{DIAGRAMS_DIR}/trust-boundaries",
    direction="TB",
    graph_attr={"bgcolor": "white", "pad": "0.8", "fontsize": "13", "fontname": "Helvetica"},
    node_attr={"fontsize": "11", "fontname": "Helvetica"},
    edge_attr={"fontsize": "10", "fontname": "Helvetica"},
):
    with Cluster("① Internet / Untrusted\n[STRIDE: Spoofing · Information Disclosure]"):
        browser = Users("Browser Client\n(JavaScript SPA)")

    with Cluster("② DMZ / TLS-Terminated\n[STRIDE: Spoofing · DoS]\nTLS 1.3 terminates here — no plain HTTP beyond"):
        appgw = ApplicationGateway("Azure App Gateway\n+ WAF v2 (OWASP ruleset)\nPhase 4+ / localhost Phase 2")

    with Cluster("③ Internal Service Network / Trusted\n[STRIDE: Spoofing · EoP · Tampering]\nJWT Bearer validated on every request — mTLS deferred to Phase 5"):
        aks = KubernetesServices("AKS Microservices\n(6 services + Dapr sidecars)")

    with Cluster("④ Data Zone / Most Trusted\n[STRIDE: Information Disclosure]\nSSL only · credentials from Key Vault (Phase 4+)"):
        pg = DatabaseForPostgresqlServers("PostgreSQL\n(per-service, isolated)\nEncrypted at rest")
        kv = KeyVaults("Azure Key Vault\nRS256 private key\nDB connection strings\nTOTP encryption key")
        blob = BlobStorage("Azure Blob Storage\nNo public URLs\nAuthenticated access only")
        entra = ActiveDirectory("Microsoft Entra ID\nManaged Identity\nWorkload Identity")

    browser >> Edge(label="HTTPS TLS 1.3\n[Spoofing, Info Disclosure]") >> appgw
    appgw >> Edge(label="gRPC + JWT Bearer validation\n[Spoofing, EoP]") >> aks
    aks >> Edge(label="SSL + credentials from Key Vault\n[Info Disclosure]") >> pg
    aks >> Edge(label="Managed Identity", style="dashed") >> kv
    aks >> Edge(label="Managed Identity", style="dashed") >> blob
    aks >> Edge(label="Workload Identity", style="dashed") >> entra
