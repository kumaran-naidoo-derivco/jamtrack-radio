# 🎵 Jamtrack Radio

A hands-on, music-themed full-stack cloud and DevOps training project that teaches modern software development practices from the ground up.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Status](https://img.shields.io/badge/Status-Phase%201-blue.svg)]()

---

## 📖 About The Project

**Jamtrack Radio** is a cloud-native music streaming and playlist management platform designed as a comprehensive learning project. It covers the entire software development lifecycle from local development to multi-cloud deployment, incorporating industry-standard tools and practices.

### What is Jamtrack Radio?

A real-world application that allows users to:
- 🎧 Stream music tracks (initially mock/sample audio files)
- 📝 Create and manage playlists (CRUD operations)
- 👥 Share playlists with other users
- 🔍 Discover music recommendations
- 📊 View listening statistics and history

### Why This Project?

This project serves as a hands-on learning platform to master modern software development skills including:
- Cloud-native application development
- Microservices architecture
- Container orchestration
- Infrastructure as Code (IaC)
- CI/CD pipelines
- Multi-cloud deployment
- Observability and monitoring

---

## 🎯 Learning Objectives

Through building Jamtrack Radio, you will gain practical experience in:

### Core Development
- **VS Code**: Modern IDE workflows and extensions
- **C# & ASP.NET Core**: Backend API development
- **PostgreSQL**: Relational database design and management
- **gRPC**: High-performance inter-service communication
- **Automated Testing**: Unit, integration, and end-to-end tests

### DevOps & Cloud
- **Docker**: Containerizing applications
- **Kubernetes**: Container orchestration and management
- **Helm Charts**: Kubernetes package management
- **Terraform**: Infrastructure as Code for cloud resources
- **GitHub & Git**: Version control and collaboration
- **CI/CD Pipelines**: Automated build, test, and deployment

### Cloud Platforms
- **Azure**: Deploy to Microsoft Azure cloud
- **AWS**: Deploy to Amazon Web Services
- **Networking**: Cloud network configuration and security

### Operations
- **Linux/WSL**: Command-line proficiency
- **Monitoring**: ELK stack (Elasticsearch, Logstash, Kibana)
- **Logging**: Structured logging with Serilog
- **Observability**: Metrics, logs, and distributed tracing

---

## 🛠️ Technology Stack

### Backend
- **Language**: C# (.NET 8+)
- **Framework**: ASP.NET Core Web API
- **API Protocols**: REST & gRPC
- **Database**: PostgreSQL
- **Data Access**: Dapper (micro-ORM)
- **Migrations**: FluentMigrator
- **Authentication**: JWT tokens
- **Logging**: Serilog with structured logging

### Infrastructure & DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes (local via Docker Desktop/Minikube, then AKS/EKS)
- **Package Manager**: Helm
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Version Control**: Git & GitHub

### Cloud Platforms
- **Azure**: Azure Kubernetes Service (AKS), Azure Container Registry (ACR), Azure Database for PostgreSQL
- **AWS**: Amazon Elastic Kubernetes Service (EKS), Amazon Elastic Container Registry (ECR), Amazon RDS for PostgreSQL

### Monitoring & Observability
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Metrics**: Prometheus & Grafana (optional future addition)
- **Tracing**: OpenTelemetry (optional future addition)

### Development Environment
- **OS**: Windows with WSL 2 (Ubuntu)
- **IDE**: Visual Studio Code
- **Terminal**: Windows Terminal
- **Package Manager**: NuGet (C#), npm (frontend if added)

---

## 🗺️ Project Phases

The project is structured into manageable phases, each focusing on specific skills:

### ✅ Phase 0: Environment Setup & GitHub Project Initialization
**Status**: Complete (100%)
- Development environment configuration (WSL, Git, VS Code)
- GitHub repository and project tracking setup
- Labels, milestones, and issue tracking

### 🚧 Phase 1: Repository Documentation & Templates (Current Phase)
**Status**: In Progress
- Comprehensive documentation (README, CONTRIBUTING, ARCHITECTURE)
- GitHub templates (PR and issue templates)
- Project board configuration

### 📋 Phase 2: Local Development Environment
- Install .NET SDK, PostgreSQL, and Docker Desktop
- Create basic C# Web API project structure
- Set up database with Dapper and FluentMigrator
- Implement basic CRUD operations for songs and playlists

### 🐳 Phase 3: Docker & Local Kubernetes
- Dockerize the application
- Write Kubernetes manifests (Deployments, Services, ConfigMaps)
- Create Helm charts
- Deploy to local Kubernetes cluster

### ☁️ Phase 4: Azure Deployment
- Set up Azure account and resources
- Create Terraform configurations for Azure
- Deploy to Azure Kubernetes Service (AKS)
- Configure Azure networking and security

### 🌩️ Phase 5: AWS Deployment
- Set up AWS account and resources
- Create Terraform configurations for AWS
- Deploy to Amazon Elastic Kubernetes Service (EKS)
- Configure AWS networking and security

### 📊 Phase 6: Monitoring & Observability
- Set up ELK stack for centralized logging
- Configure structured logging with Serilog
- Create monitoring dashboards
- Implement health checks and alerting

### 📦 Phase 7: Final Documentation & Packaging
- Complete all documentation
- Create deployment guides
- Record demo videos
- Prepare for production-readiness

---

## 🚀 Getting Started

### Prerequisites

- **Operating System**: Windows 10/11 with WSL 2
- **GitHub Account**: For version control and project tracking
- **Azure Account**: For Azure cloud deployment (Phase 4)
- **AWS Account**: For AWS cloud deployment (Phase 5) - will be created in Phase 5

### Quick Start

Detailed setup instructions are provided in each phase. To get started:

1. **Phase 0**: Environment Setup - See [Phase 0 Documentation](./project-tasks/Phase-0.md)
2. **Phase 1**: Repository Documentation - See [Phase 1 Documentation](./project-tasks/Phase-1.md)

For development workflow and contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md) (coming soon).

For architecture and design decisions, see [ARCHITECTURE.md](./ARCHITECTURE.md) (coming soon).

---

## 📂 Repository Structure

```
jamtrack-radio/
├── .github/                    # GitHub templates and workflows (Phase 1)
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   └── pull_request_template.md
├── project-tasks/             # Project planning and phase documentation
│   ├── brief.md               # Original project brief
│   ├── project-plan.md        # Complete project plan
│   ├── Phase-0.md             # Phase 0 tasks
│   ├── Phase-1.md             # Phase 1 tasks
│   └── session-progress.md    # Session progress log
├── src/                       # Source code (Phase 2+)
├── infrastructure/            # Terraform and infrastructure code (Phase 3+)
├── k8s/                       # Kubernetes manifests (Phase 3+)
├── helm/                      # Helm charts (Phase 3+)
├── docs/                      # Additional documentation
├── tests/                     # Automated tests (Phase 2+)
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # This file
├── CONTRIBUTING.md            # Contribution guidelines (Phase 1)
└── ARCHITECTURE.md            # Architecture documentation (Phase 1)
```

---

## 📚 Documentation

- **[Project Plan](./project-tasks/project-plan.md)**: Complete project roadmap with all phases and tasks
- **[Session Progress](./project-tasks/session-progress.md)**: Detailed session-by-session progress log
- **[Contributing Guidelines](./CONTRIBUTING.md)**: How to contribute to the project (coming in Phase 1)
- **[Architecture](./ARCHITECTURE.md)**: System architecture and design decisions (coming in Phase 1)

---

## 🤝 Contributing

This is a personal learning project, but contributions, suggestions, and feedback are welcome!

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines (coming soon).

---

## 📈 Project Tracking

- **GitHub Repository**: [kumaran-naidoo-derivco/jamtrack-radio](https://github.com/kumaran-naidoo-derivco/jamtrack-radio)
- **Project Board**: [Jamtrack Radio Agile Board](https://github.com/users/kumaran-naidoo-derivco/projects/3)
- **Milestones**: [View All Milestones](https://github.com/kumaran-naidoo-derivco/jamtrack-radio/milestones)
- **Issues**: [View All Issues](https://github.com/kumaran-naidoo-derivco/jamtrack-radio/issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎓 Acknowledgments

- Built as a comprehensive learning project covering modern cloud-native development
- Inspired by real-world enterprise application patterns
- Designed to teach from first principles with hands-on practice

---

## 📞 Contact

**Project Maintainer**: Kumaran Naidoo

**GitHub**: [@kumaran-naidoo-derivco](https://github.com/kumaran-naidoo-derivco)

---

**🎵 Happy Coding! Let's build something awesome together!**
