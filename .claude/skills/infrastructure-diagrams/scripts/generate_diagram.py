#!/usr/bin/env python3
"""
Jamtrack Radio — Infrastructure Diagram Generator

Usage:
    python generate_diagram.py --type <diagram_type> --output <path/filename>

Types (Jamtrack Radio):
    microservices — All JR services: Identity, Track, Streaming, API Gateway + PostgreSQL
    phase3-vm     — Phase 3: Azure VMs behind Nginx, single region
    phase6-aca    — Phase 6: Azure Container Apps
    phase7-aks    — Phase 7: AKS + Helm + ACR + PostgreSQL + Key Vault
    phase8-eks    — Phase 8: AWS EKS equivalent

Types (Generic):
    hub-spoke     — Azure hub-and-spoke network topology
    hybrid        — Hybrid on-premises <-> Azure connectivity
    three-tier    — Classic three-tier web application
    dr            — Multi-region disaster recovery
"""

import argparse
import sys


# ─── Jamtrack Radio templates ────────────────────────────────────────────────

def create_microservices(filename: str):
    """All Jamtrack Radio services: Identity, Track, Streaming, API Gateway + PostgreSQL."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.compute import VM, KubernetesServices
    from diagrams.azure.network import ApplicationGateway, LoadBalancers
    from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
    from diagrams.azure.storage import BlobStorage
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.identity import ManagedIdentities
    from diagrams.onprem.client import Users

    with Diagram("Jamtrack Radio — Microservices", show=False, filename=filename, direction="LR"):
        users = Users("Clients")

        with Cluster("Azure"):
            gw = ApplicationGateway("API Gateway\n(YARP)")

            with Cluster("Identity Service :5001"):
                id_svc = VM("IdentityService.Api")
                id_db = DatabaseForPostgresqlServers("identity-db")

            with Cluster("Track Service :5002"):
                track_svc = VM("TrackService.Api")
                track_db = DatabaseForPostgresqlServers("track-db")

            with Cluster("Streaming Service :5003"):
                stream_svc = VM("StreamingService.Api")
                stream_db = DatabaseForPostgresqlServers("streaming-db")
                blob = BlobStorage("Audio Files\n(Blob Storage)")

            kv = KeyVaults("Key Vault")

        users >> gw
        gw >> Edge(label="gRPC :5001") >> id_svc >> id_db
        gw >> Edge(label="gRPC :5002") >> track_svc >> track_db
        gw >> Edge(label="gRPC :5003") >> stream_svc >> stream_db
        stream_svc >> blob
        id_svc >> kv
        track_svc >> kv
        stream_svc >> kv


def create_phase3_vm(filename: str):
    """Phase 3: Azure VMs behind Nginx, single region."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.compute import VM
    from diagrams.azure.network import (
        VirtualNetworks, LoadBalancers, Firewall, ApplicationGateway
    )
    from diagrams.azure.database import DatabaseForPostgresqlServers
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.identity import ManagedIdentities
    from diagrams.onprem.client import Users
    from diagrams.onprem.network import Nginx

    with Diagram("Jamtrack Radio — Phase 3: Azure VM Hosting", show=False, filename=filename, direction="TB"):
        users = Users("Internet Clients")
        appgw = ApplicationGateway("App Gateway + WAF")

        with Cluster("Azure Region (UK South)"):
            with Cluster("Virtual Network 10.0.0.0/16"):

                with Cluster("DMZ Subnet 10.0.0.0/24"):
                    nginx = VM("Nginx Reverse Proxy\n(api.jamtrack.io)")

                with Cluster("App Subnet 10.0.1.0/24"):
                    id_vm = VM("Identity Service\n:5001 gRPC")
                    track_vm = VM("Track Service\n:5002 gRPC")
                    stream_vm = VM("Streaming Service\n:5003 gRPC")
                    gw_vm = VM("API Gateway\n:80/:443")

                with Cluster("Data Subnet 10.0.2.0/24"):
                    pg = DatabaseForPostgresqlServers("PostgreSQL\nFlexible Server")

            kv = KeyVaults("Key Vault")
            mi = ManagedIdentities("Managed Identity")

        users >> appgw >> nginx >> gw_vm
        gw_vm >> Edge(label="gRPC") >> id_vm
        gw_vm >> Edge(label="gRPC") >> track_vm
        gw_vm >> Edge(label="gRPC") >> stream_vm
        id_vm >> pg
        track_vm >> pg
        stream_vm >> pg
        id_vm >> kv
        track_vm >> kv
        stream_vm >> kv


def create_phase6_aca(filename: str):
    """Phase 6: Azure Container Apps."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.compute import ContainerApps, ContainerRegistries
    from diagrams.azure.network import ApplicationGateway, VirtualNetworks
    from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
    from diagrams.azure.storage import BlobStorage
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.identity import ManagedIdentities
    from diagrams.azure.monitor import LogAnalyticsWorkspaces, ApplicationInsights
    from diagrams.onprem.client import Users

    with Diagram("Jamtrack Radio — Phase 6: Azure Container Apps", show=False, filename=filename, direction="TB"):
        users = Users("Internet Clients")
        appgw = ApplicationGateway("App Gateway + WAF\napi.jamtrack.io")

        with Cluster("Azure"):
            acr = ContainerRegistries("ACR\njamtrack.azurecr.io")

            with Cluster("Container Apps Environment"):
                gw_app = ContainerApps("api-gateway")
                id_app = ContainerApps("identity-service")
                track_app = ContainerApps("track-service")
                stream_app = ContainerApps("streaming-service")

            with Cluster("Data"):
                pg = DatabaseForPostgresqlServers("PostgreSQL\nFlexible Server")
                redis = CacheForRedis("Redis Cache")
                blob = BlobStorage("Blob Storage")

            kv = KeyVaults("Key Vault")
            mi = ManagedIdentities("Managed Identity")

            with Cluster("Observability"):
                logs = LogAnalyticsWorkspaces("Log Analytics")
                ai = ApplicationInsights("App Insights")

        users >> appgw >> gw_app
        gw_app >> Edge(label="gRPC") >> id_app
        gw_app >> Edge(label="gRPC") >> track_app
        gw_app >> Edge(label="gRPC") >> stream_app
        id_app >> pg
        track_app >> pg
        stream_app >> [pg, blob, redis]
        [id_app, track_app, stream_app, gw_app] >> kv
        [id_app, track_app, stream_app, gw_app] >> ai


def create_phase7_aks(filename: str):
    """Phase 7: AKS + Helm + ACR + PostgreSQL + Key Vault."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.compute import KubernetesServices, ContainerRegistries
    from diagrams.azure.network import ApplicationGateway, LoadBalancers
    from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis
    from diagrams.azure.storage import BlobStorage
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.identity import ManagedIdentities
    from diagrams.azure.monitor import LogAnalyticsWorkspaces, ApplicationInsights
    from diagrams.k8s.compute import Pod, Deployment
    from diagrams.k8s.network import Service, Ingress
    from diagrams.onprem.client import Users

    with Diagram("Jamtrack Radio — Phase 7: AKS", show=False, filename=filename, direction="TB"):
        users = Users("Internet Clients")

        with Cluster("Azure"):
            acr = ContainerRegistries("ACR\njamtrack.azurecr.io")
            appgw = ApplicationGateway("App Gateway\n(AGIC Ingress)")

            with Cluster("AKS Cluster"):
                ingress = Ingress("NGINX Ingress")
                aks = KubernetesServices("AKS")

                with Cluster("jamtrack namespace"):
                    gw_svc = Service("api-gateway-svc")
                    gw_pods = [Pod("api-gw-1"), Pod("api-gw-2")]

                    id_svc = Service("identity-svc")
                    id_pods = [Pod("identity-1"), Pod("identity-2")]

                    track_svc = Service("track-svc")
                    track_pods = [Pod("track-1"), Pod("track-2")]

                    stream_svc = Service("streaming-svc")
                    stream_pods = [Pod("stream-1"), Pod("stream-2")]

            with Cluster("Data"):
                pg = DatabaseForPostgresqlServers("PostgreSQL\nFlexible Server")
                redis = CacheForRedis("Redis Cache")
                blob = BlobStorage("Blob Storage")

            kv = KeyVaults("Key Vault")
            mi = ManagedIdentities("Workload Identity")

            with Cluster("Observability"):
                logs = LogAnalyticsWorkspaces("Log Analytics")
                ai = ApplicationInsights("App Insights")

        users >> appgw >> ingress >> gw_svc >> gw_pods
        gw_pods >> Edge(label="gRPC") >> id_svc >> id_pods
        gw_pods >> Edge(label="gRPC") >> track_svc >> track_pods
        gw_pods >> Edge(label="gRPC") >> stream_svc >> stream_pods
        id_pods >> pg
        track_pods >> pg
        stream_pods >> [pg, blob, redis]
        [id_pods, track_pods, stream_pods] >> kv


def create_phase8_eks(filename: str):
    """Phase 8: AWS EKS equivalent of the Jamtrack Radio deployment."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.aws.compute import EKS
    from diagrams.aws.network import ELB, Route53, CF
    from diagrams.aws.database import RDS, ElastiCache
    from diagrams.aws.storage import S3
    from diagrams.aws.security import SecretsManager
    from diagrams.aws.management import Cloudwatch
    from diagrams.k8s.compute import Pod
    from diagrams.k8s.network import Service, Ingress
    from diagrams.onprem.client import Users

    with Diagram("Jamtrack Radio — Phase 8: AWS EKS", show=False, filename=filename, direction="TB"):
        users = Users("Internet Clients")
        dns = Route53("Route 53")
        cf = CF("CloudFront")
        lb = ELB("ALB")

        with Cluster("AWS Region (eu-west-1)"):
            with Cluster("EKS Cluster"):
                eks = EKS("EKS")
                ingress = Ingress("ALB Ingress")

                with Cluster("jamtrack namespace"):
                    gw_pod = Pod("api-gateway")
                    id_pod = Pod("identity")
                    track_pod = Pod("track")
                    stream_pod = Pod("streaming")

            with Cluster("Data"):
                rds = RDS("PostgreSQL\n(RDS Multi-AZ)")
                cache = ElastiCache("Redis\n(ElastiCache)")
                s3 = S3("Audio Files\n(S3)")

            secrets = SecretsManager("Secrets Manager")
            cw = Cloudwatch("CloudWatch")

        users >> dns >> cf >> lb >> ingress >> gw_pod
        gw_pod >> id_pod >> rds
        gw_pod >> track_pod >> rds
        gw_pod >> stream_pod >> [rds, s3, cache]
        [id_pod, track_pod, stream_pod] >> secrets
        [id_pod, track_pod, stream_pod] >> cw


# ─── Generic templates ────────────────────────────────────────────────────────

def create_hub_spoke(filename: str):
    """Azure hub-and-spoke network topology."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.network import VirtualNetworks, VirtualNetworkGateways, Firewall
    from diagrams.azure.compute import VM

    with Diagram("Hub and Spoke Architecture", show=False, filename=filename, direction="TB"):
        with Cluster("Hub VNet (10.0.0.0/16)"):
            fw = Firewall("Azure Firewall")
            vpn = VirtualNetworkGateways("VPN Gateway")

        with Cluster("Spoke 1 — Production (10.1.0.0/16)"):
            spoke1 = [VM("Web VM"), VM("App VM")]

        with Cluster("Spoke 2 — Development (10.2.0.0/16)"):
            spoke2 = [VM("Dev VM 1"), VM("Dev VM 2")]

        with Cluster("Spoke 3 — Shared Services (10.3.0.0/16)"):
            spoke3 = VM("Monitoring")

        vpn >> fw
        fw >> Edge(label="Peering") >> spoke1
        fw >> Edge(label="Peering") >> spoke2
        fw >> Edge(label="Peering") >> spoke3


def create_hybrid(filename: str):
    """Hybrid on-premises <-> Azure connectivity."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.network import VirtualNetworks, VirtualNetworkGateways
    from diagrams.azure.compute import VM
    from diagrams.onprem.compute import Server
    from diagrams.onprem.network import CiscoRouter
    from diagrams.onprem.database import PostgreSQL
    from diagrams.generic.network import VPN

    with Diagram("Hybrid Cloud Architecture", show=False, filename=filename, direction="LR"):
        with Cluster("On-Premises Data Centre"):
            router = CiscoRouter("Edge Router")
            with Cluster("Application Tier"):
                servers = [Server("Legacy App 1"), Server("Legacy App 2")]
            with Cluster("Database Tier"):
                db = PostgreSQL("Primary DB")
            router >> servers >> db

        vpn = VPN("Site-to-Site VPN")

        with Cluster("Azure"):
            vpn_gw = VirtualNetworkGateways("VPN Gateway")
            with Cluster("Virtual Network"):
                azure_vms = [VM("Cloud App 1"), VM("Cloud App 2")]

        router >> vpn >> vpn_gw >> azure_vms


def create_three_tier(filename: str):
    """Classic three-tier web application."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.network import ApplicationGateway, LoadBalancers
    from diagrams.azure.compute import VM, VMScaleSet
    from diagrams.azure.database import SQLDatabases
    from diagrams.azure.storage import BlobStorage
    from diagrams.azure.security import KeyVaults
    from diagrams.onprem.client import Users

    with Diagram("Three-Tier Web Application", show=False, filename=filename, direction="TB"):
        users = Users("Users")

        with Cluster("Azure"):
            appgw = ApplicationGateway("App Gateway + WAF")

            with Cluster("Web Tier"):
                web = VMScaleSet("Web Servers")

            with Cluster("App Tier"):
                lb = LoadBalancers("Internal LB")
                app = VMScaleSet("App Servers")

            with Cluster("Data Tier"):
                db = SQLDatabases("Azure SQL")
                storage = BlobStorage("Blob Storage")

            kv = KeyVaults("Key Vault")

        users >> appgw >> web >> lb >> app
        app >> db
        app >> storage
        app >> kv


def create_dr(filename: str):
    """Multi-region disaster recovery."""
    from diagrams import Diagram, Cluster, Edge
    from diagrams.azure.compute import VMScaleSet
    from diagrams.azure.network import TrafficManagerProfiles, LoadBalancers
    from diagrams.azure.database import SQLDatabases
    from diagrams.azure.storage import BlobStorage
    from diagrams.onprem.client import Users

    with Diagram("Multi-Region Disaster Recovery", show=False, filename=filename, direction="TB"):
        users = Users("Global Users")
        tm = TrafficManagerProfiles("Traffic Manager")

        with Cluster("Primary Region — UK South"):
            lb1 = LoadBalancers("Load Balancer")
            web1 = VMScaleSet("Web Tier")
            app1 = VMScaleSet("App Tier")
            sql1 = SQLDatabases("SQL (Primary)")
            blob1 = BlobStorage("Blob (Primary)")

        with Cluster("Secondary Region — West Europe"):
            lb2 = LoadBalancers("Load Balancer")
            web2 = VMScaleSet("Web Tier")
            app2 = VMScaleSet("App Tier")
            sql2 = SQLDatabases("SQL (Secondary)")
            blob2 = BlobStorage("Blob (GRS)")

        users >> tm
        tm >> lb1 >> web1 >> app1 >> sql1
        tm >> Edge(style="dashed", label="Failover") >> lb2 >> web2 >> app2 >> sql2
        sql1 >> Edge(label="Geo-Replication", style="dashed") >> sql2
        blob1 >> Edge(label="GRS", style="dashed") >> blob2


# ─── CLI ─────────────────────────────────────────────────────────────────────

DIAGRAM_TYPES = {
    # Jamtrack Radio
    "microservices": create_microservices,
    "phase3-vm": create_phase3_vm,
    "phase6-aca": create_phase6_aca,
    "phase7-aks": create_phase7_aks,
    "phase8-eks": create_phase8_eks,
    # Generic
    "hub-spoke": create_hub_spoke,
    "hybrid": create_hybrid,
    "three-tier": create_three_tier,
    "dr": create_dr,
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate Jamtrack Radio infrastructure diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=list(DIAGRAM_TYPES.keys()),
        help="Diagram type to generate",
    )
    parser.add_argument(
        "--output", "-o",
        default="diagram",
        help="Output path + filename (no extension); default: diagram",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available diagram types and exit",
    )

    args = parser.parse_args()

    if args.list:
        print("Available diagram types:\n")
        for name, fn in DIAGRAM_TYPES.items():
            print(f"  {name:<15} {fn.__doc__.strip()}")
        return

    print(f"Generating '{args.type}' diagram -> {args.output}.png ...")
    try:
        DIAGRAM_TYPES[args.type](args.output)
        print(f"Done: {args.output}.png")
    except ImportError as e:
        print(f"Import error: {e}", file=sys.stderr)
        print("Run: pip install diagrams --break-system-packages", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
