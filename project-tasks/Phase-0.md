# Project: 🎵 Jamtrack Radio

## Phase 0: Environment Setup & GitHub Project Initialization
**Phase Description**:
Prepare the complete development workstation foundation for Jamtrack Radio, ensuring WSL Ubuntu, Git, SSH, VS Code, and essential extensions are installed entirely via command line. Additionally, set up the GitHub repository and project tracking infrastructure so you can track Phase 0 progress from the very beginning.

**Priority**: High
**Labels**: phase-0, setup, environment, github

---

### Task 0.0: Install Windows Terminal
- **Description**:
  Install Windows Terminal for better command-line experience with tabs, themes, and excellent WSL integration.
  **Commands (Windows PowerShell)**:
  ```powershell
  winget install --id Microsoft.WindowsTerminal --source winget
  ```
- **Labels**: setup, windows, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: None

---

### Task 0.1: Install WSL 2 with Ubuntu
- **Description**:
  Enable Windows Subsystem for Linux (WSL) and Virtual Machine Platform, set WSL 2 as default, install Ubuntu, and verify installation.
  **Commands (Windows PowerShell - Run as Administrator)**:
  ```powershell
  dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
  dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
  wsl --set-default-version 2
  wsl --install -d Ubuntu
  wsl --list --verbose
  ```
- **Labels**: setup, environment, windows, wsl, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.0

---

### Task 0.2: Update Ubuntu Packages
- **Description**:
  Update and upgrade package index inside WSL Ubuntu to ensure latest security patches and tools.
  **Commands (WSL Ubuntu)**:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
- **Labels**: setup, environment, wsl, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.1

---

### Task 0.3: Install Git inside WSL
- **Description**:
  Install Git CLI tools, configure global username and email for commits, and verify installation.
  **Commands (WSL Ubuntu)**:
  ```bash
  sudo apt install -y git
  git config --global user.name "Your Name"
  git config --global user.email "your_email@example.com"
  git --version
  ```
- **Labels**: setup, git, wsl, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.2

---

### Task 0.4: Install VS Code on Windows via Command Line
- **Description**:
  Install Visual Studio Code using Winget, verify CLI access for extensions and remote WSL usage.
  **Commands (Windows PowerShell)**:
  ```powershell
  winget install --id Microsoft.VisualStudioCode --source winget
  code --version
  ```
- **Labels**: setup, vscode, windows, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.1

---

### Task 0.5: Install VS Code Extensions via CLI
- **Description**:
  Install Remote WSL, C#, Docker, Kubernetes, Terraform, and PostgreSQL extensions using VS Code CLI.
  **Commands (Windows PowerShell)**:
  ```powershell
  code --install-extension ms-vscode-remote.remote-wsl
  code --install-extension ms-dotnettools.csharp
  code --install-extension ms-azuretools.vscode-docker
  code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
  code --install-extension hashicorp.terraform
  code --install-extension cweijan.vscode-postgresql-client2
  ```
- **Labels**: setup, vscode, extensions, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.4

---

### Task 0.6: Generate SSH Key in WSL
- **Description**:
  Generate an Ed25519 SSH key for GitHub authentication and add the private key to the SSH agent.
  **Commands (WSL Ubuntu)**:
  ```bash
  ssh-keygen -t ed25519 -C "your_email@example.com"
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_ed25519
  cat ~/.ssh/id_ed25519.pub
  ```
- **Labels**: setup, ssh, github, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.3

---

### Task 0.7: Add SSH Key to GitHub via CLI
- **Description**:
  Install GitHub CLI in WSL, authenticate, and add SSH public key to your GitHub account.
  **Commands (WSL Ubuntu)**:
  ```bash
  sudo apt install curl -y
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt update
  sudo apt install gh -y
  gh auth login
  gh ssh-key add ~/.ssh/id_ed25519.pub --title "Jamtrack Radio Dev Machine (WSL)"
  ```
- **Labels**: setup, ssh, github, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.6

---

### Task 0.8: Test SSH Connection to GitHub
- **Description**:
  Verify SSH authentication to GitHub works from WSL.
  **Commands (WSL Ubuntu)**:
  ```bash
  ssh -T git@github.com
  ```
  If prompted, type `yes` to trust the fingerprint.
- **Labels**: setup, ssh, github, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.7

---

### Task 0.9: Verify VS Code Remote WSL Setup
- **Description**:
  Launch VS Code from WSL and ensure VS Code Server installs for remote development.
  **Commands (WSL Ubuntu)**:
  ```bash
  code .
  ```
- **Labels**: setup, vscode, wsl, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.5

---

### Task 0.10: Create GitHub Repository via CLI
- **Description**:
  Use `gh repo create` to create the public repository `jamtrack-radio` with README, .gitignore (VisualStudio), MIT License, and enable issues directly from WSL.
  **Commands (WSL Ubuntu)**:
  ```bash
  # Navigate to your projects directory
  cd ~/training  # or your preferred location

  # Create the repository on GitHub (will prompt for clone location)
  gh repo create jamtrack-radio \
    --public \
    --description "🎵 A fun, music-themed full-stack cloud & DevOps training project using C#, Docker, Kubernetes, Terraform, Azure, AWS, and more." \
    --gitignore VisualStudio \
    --license MIT \
    --enable-issues

  # Clone the repository
  gh repo clone kumaran-naidoo-derivco/jamtrack-radio
  cd jamtrack-radio
  ```
  Note: If you already have a local git repo initialized, see Task 0.11 for how to connect it.
- **Labels**: setup, github, repo, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.8

---

### Task 0.11: Configure Git Remote and Push Initial Commit
- **Description**:
  If you already have a local repo initialized with commits, add the GitHub remote and push your initial content.
  **Commands (WSL Ubuntu)**:
  ```bash
  # Navigate to your existing local repo
  cd /mnt/c/training/jamtrack-radio  # or your repo location

  # If remote doesn't exist, add it
  git remote add origin git@github.com:kumaran-naidoo-derivco/jamtrack-radio.git

  # Or if origin exists but points to wrong URL
  git remote set-url origin git@github.com:kumaran-naidoo-derivco/jamtrack-radio.git

  # Stage and commit project files
  git add project-tasks/ CLAUDE.md
  git commit -m "Add project planning documents and phases"

  # Push to GitHub
  git branch -M main  # ensure branch is named 'main'
  git push -u origin main
  ```
- **Labels**: setup, git, github, phase-0
- **Estimated Effort**: Small
- **Status**: Todo
- **Dependencies**: Task 0.10

---

### Task 0.12: Create Labels via CLI
- **Description**:
  Add custom labels to the repo using GitHub CLI for organizing issues by phase and technology.
  **Commands (WSL Ubuntu)**:
  ```bash
  # Phase labels
  gh label create "phase-0" --description "Environment Setup" --color "5319e7"
  gh label create "phase-1" --description "Repo & Tracking Setup" --color "0e8a16"
  gh label create "phase-2" --description "Local Dev Environment" --color "fbca04"
  gh label create "phase-3" --description "Docker & Local K8s" --color "d93f0b"
  gh label create "phase-4" --description "Azure Deployment" --color "006b75"
  gh label create "phase-5" --description "AWS Deployment" --color "bfd4f2"
  gh label create "phase-6" --description "Monitoring" --color "f9d0c4"

  # Technology labels
  gh label create "setup" --description "Setup tasks" --color "c5def5"
  gh label create "environment" --description "Environment configuration" --color "1d76db"
  gh label create "docker" --description "Docker containers" --color "fef2c0"
  gh label create "kubernetes" --description "Kubernetes orchestration" --color "1d76db"
  gh label create "terraform" --description "Infrastructure as Code" --color "5319e7"
  gh label create "azure" --description "Azure cloud" --color "0e8a16"
  gh label create "aws" --description "AWS cloud" --color "fbca04"
  gh label create "postgres" --description "PostgreSQL database" --color "d93f0b"
  gh label create "grpc" --description "gRPC APIs" --color "006b75"
  gh label create "monitoring" --description "Monitoring & observability" --color "bfd4f2"
  gh label create "logging" --description "Logging" --color "f9d0c4"
  gh label create "github" --description "GitHub related" --color "000000"
  gh label create "vscode" --description "VS Code" --color "007acc"
  gh label create "wsl" --description "Windows Subsystem for Linux" --color "e95420"
  gh label create "git" --description "Git version control" --color "f05032"
  gh label create "ssh" --description "SSH configuration" --color "770f56"
  gh label create "windows" --description "Windows-specific tasks" --color "5319e7"
  ```
- **Labels**: setup, github, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.11

---

### Task 0.13: Create Milestones via CLI
- **Description**:
  Create milestones for each project phase using `gh milestone create`.
  **Commands (WSL Ubuntu)**:
  ```bash
  gh milestone create "Phase 0: Environment Setup" --description "Set up development environment, WSL, Git, VS Code, and GitHub project tracking"
  gh milestone create "Phase 1: Repo & Tracking Setup" --description "Repository documentation, templates, and project board configuration"
  gh milestone create "Phase 2: Local Dev Environment" --description "Local development setup for C# backend"
  gh milestone create "Phase 3: Docker & Local K8s" --description "Containerization and local Kubernetes orchestration"
  gh milestone create "Phase 4: Azure Deployment" --description "Deploy to Azure cloud"
  gh milestone create "Phase 5: AWS Deployment" --description "Deploy to AWS cloud"
  gh milestone create "Phase 6: Monitoring & Observability" --description "Set up ELK stack and monitoring"
  gh milestone create "Phase 7: Final Docs & Packaging" --description "Final documentation and project completion"
  ```
- **Labels**: setup, github, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.12

---

### Task 0.14: Create Project Board via CLI
- **Description**:
  Create a GitHub Project Board (Projects v2) for tracking all tasks across phases.
  **Commands (WSL Ubuntu)**:
  ```bash
  # Create the project (Projects v2)
  gh project create --owner kumaran-naidoo-derivco --title "Jamtrack Radio Agile Board 🎵"

  # Note the project number from the output
  # You can also list projects with: gh project list --owner kumaran-naidoo-derivco

  # Note: GitHub Projects v2 views and fields are best configured via web UI
  # Visit https://github.com/users/kumaran-naidoo-derivco/projects to configure columns
  ```
- **Labels**: setup, github, project-board, phase-0
- **Estimated Effort**: Medium
- **Status**: Todo
- **Dependencies**: Task 0.13

---

### Task 0.15: Populate Phase 0 Issues
- **Description**:
  Create GitHub issues for all Phase 0 tasks so progress can be tracked in the project board. Mark already-completed tasks as closed.
  **Commands (WSL Ubuntu)**:
  ```bash
  # You can create issues manually or use a script
  # Here's an example for a few tasks:

  gh issue create --title "Task 0.0: Install Windows Terminal" \
    --body "Install Windows Terminal for better command-line experience with tabs, themes, and excellent WSL integration." \
    --label "phase-0,setup,windows" \
    --milestone "Phase 0: Environment Setup"

  gh issue create --title "Task 0.1: Install WSL 2 with Ubuntu" \
    --body "Enable Windows Subsystem for Linux and install Ubuntu distribution." \
    --label "phase-0,setup,environment,wsl" \
    --milestone "Phase 0: Environment Setup"

  # Repeat for all Phase 0 tasks (0.0 through 0.15)
  # For tasks already completed, close them after creation:
  # gh issue close <issue-number> --comment "Completed during initial setup"
  ```

  Alternatively, you can use the comprehensive project-plan.md file to bulk-create issues programmatically.
- **Labels**: setup, github, issues, phase-0
- **Estimated Effort**: Large
- **Status**: Todo
- **Dependencies**: Task 0.14

---

## ✅ Phase 0 Summary

Phase 0 now includes **two major sections**:

### Section 1: Environment Setup (Tasks 0.0-0.9)
- Windows Terminal installation
- WSL 2 with Ubuntu
- Git configuration
- VS Code and extensions
- SSH key generation and GitHub authentication

### Section 2: GitHub Project Initialization (Tasks 0.10-0.15)
- GitHub repository creation
- Git remote configuration
- Custom labels for issue organization
- Milestones for each phase
- Project board creation
- Initial issue population

**This ensures you can track your entire Phase 0 progress in GitHub from the very beginning!**

