# Project: Jamtrack Radio

A real-world music streaming application built to teach modern software development practices including C#, Docker, Kubernetes, Helm, Terraform, CI/CD, and cloud deployment (Azure & AWS).

---

## Phase 0: Environment Setup & GitHub Project Initialization
**Phase Description**: Set up Windows development machine from scratch AND initialize GitHub project tracking early so you can track your progress through Phase 0 itself! Includes Windows Terminal, WSL2, Ubuntu, Git, GitHub repo/project setup, VS Code, GitHub CLI, and SSH configuration.

**Priority**: High

**Labels**: phase-0, environment, setup, github

### Task 0.0: Install Windows Terminal
- **Description**: Install Windows Terminal for better command-line experience with tabs, themes, and excellent WSL integration. Windows Terminal is a modern, fast, and powerful terminal application that supports multiple tabs, Unicode characters, and extensive customization.

  **Step 1: Install Windows Terminal** (Windows PowerShell):
  ```powershell
  # Run PowerShell as Administrator (optional but recommended)
  winget install --id Microsoft.WindowsTerminal --source winget
  ```

  **Step 2: Verify installation**:
  ```powershell
  # Check if Windows Terminal is installed
  winget list --id Microsoft.WindowsTerminal

  # Or search for "Windows Terminal" in Start Menu
  ```

  **Step 3: Launch and configure**:
  - Open Windows Terminal from Start Menu or by typing `wt` in Run (Win+R)
  - Click the dropdown arrow (⌄) next to the tab
  - Click "Settings" or press `Ctrl+,`
  - Set your default profile (recommend PowerShell or will set to WSL after Task 0.1)
  - Explore themes, fonts, and color schemes

  **Step 4: Optional customization**:
  ```json
  // Settings.json example customizations:
  {
    "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",  // PowerShell
    "theme": "dark",
    "copyOnSelect": true,
    "copyFormatting": false
  }
  ```

  **Expected Outcome**:
  - Windows Terminal installed and appears in Start Menu
  - Can launch Windows Terminal successfully
  - Settings interface accessible via Ctrl+,
  - Default profile set
  - Terminal opens without errors

  **Common Issues & Solutions**:
  - **"winget not recognized"**:
    - Winget comes with Windows 11 and recent Windows 10 updates
    - Update Windows: Settings → Windows Update → Check for updates
    - Or download "App Installer" from Microsoft Store
    - Verify: Run `winget --version` in PowerShell

  - **"Multiple packages found"**:
    - Be specific: `winget install --id Microsoft.WindowsTerminal --exact`
    - Or accept the prompt to choose the correct package

  - **Installation fails with permissions error**:
    - Run PowerShell as Administrator (Right-click → "Run as administrator")
    - Or install via Microsoft Store as alternative

  - **Windows Terminal won't open after install**:
    - Restart your computer
    - Check if already running in background (Task Manager → End task)
    - Try launching from Start Menu directly

  - **Can't find Windows Terminal in Start Menu**:
    - Search for "wt" or "terminal"
    - Check: C:\Program Files\WindowsApps\ for installation
    - Reinstall if necessary

  💡 **Learning moment**: Windows Terminal is built on modern technology and supports features that the old Command Prompt and PowerShell console don't: GPU acceleration for text rendering, multiple tabs, split panes, true color support, and extensive customization via JSON settings. It's the foundation for a great developer experience on Windows!

  💡 **Why Windows Terminal?** Unlike the old Command Prompt or PowerShell console, Windows Terminal supports multiple tabs (PowerShell, CMD, WSL all in one window), beautiful themes, Ligature fonts (like Fira Code), and seamless WSL integration. Once you have WSL installed, you can open an Ubuntu tab right next to your PowerShell tab!

- **Labels**: setup, windows-terminal, windows, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: None

### Task 0.1: Install WSL 2 with Ubuntu
- **Description**: Enable Windows Subsystem for Linux (WSL) and Virtual Machine Platform, set WSL 2 as default, install Ubuntu, and verify installation. WSL 2 provides a real Linux kernel running in a lightweight virtual machine, offering better performance and full system call compatibility.

  **Step 1: Enable WSL and Virtual Machine Platform** (Windows PowerShell - Run as Administrator):
  ```powershell
  # Enable Windows Subsystem for Linux
  dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

  # Enable Virtual Machine Platform (required for WSL 2)
  dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

  # Verify features are enabled (optional)
  Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -like "*Linux*" -or $_.FeatureName -like "*VirtualMachine*"}
  ```

  **⚠️ Important**: You will need to **restart your computer** after enabling these features. Don't skip this step!

  **Step 2: Restart your computer**:
  ```powershell
  # Restart now or manually restart via Start Menu
  Restart-Computer
  ```

  **Step 3: Set WSL 2 as default** (After restart, in PowerShell as Administrator):
  ```powershell
  # Set WSL 2 as default version for new distributions
  wsl --set-default-version 2

  # Verify WSL is working
  wsl --status
  ```

  **Step 4: Install Ubuntu**:
  ```powershell
  # Install Ubuntu (latest LTS version)
  wsl --install -d Ubuntu

  # This will:
  # 1. Download Ubuntu (~500MB)
  # 2. Install it
  # 3. Launch it for first-time setup
  ```

  **Step 5: Complete Ubuntu first-time setup**:
  - Ubuntu will launch automatically and ask you to create a user
  - Enter a username (lowercase, no spaces): e.g., `yourname`
  - Enter a password (you won't see it as you type - this is normal)
  - Confirm password
  - Wait for setup to complete (~1-2 minutes)

  **Step 6: Verify installation**:
  ```powershell
  # List all WSL distributions
  wsl --list --verbose

  # Expected output:
  # NAME      STATE           VERSION
  # * Ubuntu    Running         2

  # Check WSL version
  wsl --version
  ```

  **Step 7: Test Ubuntu**:
  ```powershell
  # Launch Ubuntu
  wsl

  # Inside Ubuntu, run:
  whoami                    # Shows your username
  cat /etc/os-release       # Shows Ubuntu version info
  uname -r                  # Shows kernel version (should have "microsoft" in it)
  exit                      # Return to PowerShell
  ```

  **Expected Outcome**:
  - ✅ WSL and Virtual Machine Platform features enabled
  - ✅ Computer restarted successfully
  - ✅ WSL 2 set as default version
  - ✅ Ubuntu installed and running
  - ✅ `wsl --list --verbose` shows Ubuntu with VERSION 2
  - ✅ Can launch Ubuntu with `wsl` command
  - ✅ Created username and password successfully
  - ✅ Ubuntu responds to basic commands

  **Common Issues & Solutions**:
  - **"WSL 2 requires an update to its kernel component"**:
    - Download and install the WSL2 Linux kernel update package
    - Visit: https://aka.ms/wsl2kernel
    - Run the installer: `wsl_update_x64.msi`
    - Restart computer and try again
    - Verify with: `wsl --status`

  - **"Virtualization is not enabled"**:
    - You need to enable virtualization in BIOS/UEFI
    - Restart computer and enter BIOS (usually F2, F10, F12, or Delete during boot)
    - Look for "Virtualization Technology", "Intel VT-x", or "AMD-V"
    - Enable it and save changes
    - How to check if enabled: `systeminfo` in PowerShell, look for "Hyper-V Requirements"

  - **Ubuntu won't start after install**:
    - Run: `wsl --update` in PowerShell
    - Restart your computer
    - Try: `wsl --shutdown` then launch Ubuntu again
    - Check Windows Event Viewer for errors

  - **Installation hangs or freezes**:
    - Press Ctrl+C to cancel
    - Run: `wsl --unregister Ubuntu` to remove partial install
    - Restart computer
    - Try installation again
    - Ensure good internet connection (Ubuntu is downloaded from internet)

  - **"The requested operation requires elevation"**:
    - You must run PowerShell as Administrator
    - Right-click PowerShell → "Run as administrator"
    - Look for "Administrator" in the window title

  - **Ubuntu shows VERSION 1 instead of 2**:
    - Convert to WSL 2: `wsl --set-version Ubuntu 2`
    - Wait for conversion to complete (~5-10 mins)
    - Verify: `wsl --list --verbose`

  - **"WslRegisterDistribution failed with error: 0x80070003"**:
    - The install path has issues
    - Ensure Windows username doesn't have special characters
    - Try: `wsl --install -d Ubuntu --web-download`

  - **Can't set default version to 2**:
    - May need kernel update (see first issue above)
    - Check Windows version: Needs Windows 10 version 1903+ or Windows 11
    - Run: `winver` to check your Windows version

  💡 **Learning moment - WSL 1 vs WSL 2**:
  - **WSL 1**: Translation layer that converts Linux system calls to Windows calls. Fast file access to Windows files, but slower at Linux-to-Linux operations.
  - **WSL 2**: Real Linux kernel in a lightweight VM. Much faster for Linux operations, full system call compatibility, but slower accessing Windows files (/mnt/c/).
  - **Best practice**: Keep your project files inside WSL 2 filesystem (`~/projects/`) not on Windows (`/mnt/c/Users/...`) for best performance!

  💡 **Learning moment - What is WSL?**:
  Windows Subsystem for Linux lets you run Linux distributions directly on Windows without dual-booting or VMs. It's perfect for development because you get the power of Linux tools (bash, grep, awk, ssh) while still using Windows applications. Many developers use WSL because it provides a true Linux environment for running Docker, Kubernetes, and development tools!

  💡 **Security note**: The password you create during Ubuntu setup is for `sudo` commands (like administrator). You'll need it when installing packages or editing system files. Write it down! If you forget it, you'll need to reset the distribution.

- **Labels**: setup, environment, windows, wsl, phase-0
- **Estimated Effort**: Medium (30-45 mins including download and restart)
- **Status**: Backlog
- **Dependencies**: Task 0.0 (recommended but not required)

### Task 0.2: Update Ubuntu Packages
- **Description**: Update and upgrade package index inside WSL Ubuntu to ensure latest security patches and tools. This is essential after a fresh Ubuntu install to get the latest package versions and security updates.

  **Step 1: Launch Ubuntu**:
  ```powershell
  # From Windows PowerShell or Windows Terminal
  wsl
  ```

  **Step 2: Update package lists**:
  ```bash
  # Inside Ubuntu - this downloads the latest package information
  sudo apt update

  # You'll be prompted for your Ubuntu password (the one you created during setup)
  ```

  **Step 3: Upgrade installed packages**:
  ```bash
  # Upgrade all packages to their latest versions
  sudo apt upgrade -y

  # The -y flag automatically answers "yes" to prompts
  # This may take 5-10 minutes depending on how many packages need updating
  ```

  **Step 4: Optional - Clean up**:
  ```bash
  # Remove packages that are no longer needed
  sudo apt autoremove -y

  # Clear local package cache
  sudo apt clean
  ```

  **Step 5: Verify system is up to date**:
  ```bash
  # Check for any remaining updates
  sudo apt update
  sudo apt list --upgradable

  # If nothing listed, you're fully updated!
  ```

  **Expected Outcome**:
  - ✅ Package lists updated successfully
  - ✅ All packages upgraded to latest versions
  - ✅ No errors during update process
  - ✅ System shows "All packages are up to date" or "0 upgraded"
  - ✅ Optional cleanup completed

  **Common Issues & Solutions**:
  - **"sudo: command not found"**:
    - Very rare, but if it happens: `apt-get install sudo` as root
    - Or reinstall Ubuntu: `wsl --unregister Ubuntu` then `wsl --install -d Ubuntu`

  - **Password doesn't work or "Sorry, try again"**:
    - Make sure you're using the Ubuntu password you created during setup (not Windows password)
    - Password is case-sensitive
    - You won't see characters as you type - this is normal
    - If you forgot password, you'll need to reset it (see troubleshooting below)

  - **"Unable to lock directory /var/cache/apt/archives/"**:
    - Another apt process is running
    - Wait a few seconds and try again
    - Or check: `ps aux | grep apt`
    - Kill if stuck: `sudo killall apt apt-get`

  - **"Could not get lock /var/lib/dpkg/lock-frontend"**:
    - Another package manager is running
    - Wait for it to finish or reboot WSL: `wsl --shutdown` in PowerShell, then relaunch
    - If persistent: `sudo rm /var/lib/dpkg/lock-frontend` then try again

  - **404 errors or "Failed to fetch"**:
    - Internet connection issue or Ubuntu repository is temporarily down
    - Check internet connection
    - Try again in a few minutes
    - Or change repository mirror (advanced)

  - **"E: Unable to locate package"**:
    - Run `sudo apt update` first to refresh package lists
    - Package might not exist for your Ubuntu version
    - Check package name spelling

  - **Slow download speeds**:
    - Ubuntu downloads from archive.ubuntu.com by default
    - Can change to faster mirror (advanced)
    - Or just wait - first update after install is usually largest

  - **Forgot Ubuntu password**:
    - In PowerShell: `wsl -u root` (login as root, no password needed)
    - Inside Ubuntu as root: `passwd yourusername` (replace with your actual username)
    - Enter new password twice
    - Exit and login normally

  💡 **Learning moment - apt vs apt-get**:
  `apt` is the newer, more user-friendly command that combines functionality from `apt-get`, `apt-cache`, and other tools. Use `apt` for interactive use and `apt-get` in scripts. Both do the same thing for basic operations like update/upgrade/install!

  💡 **Learning moment - sudo explained**:
  `sudo` (Super User DO) lets you run commands as administrator (root). Linux requires explicit permission for system changes (unlike Windows where Admin permissions can be automatic). The password prompt is your Ubuntu password, and `sudo` remembers it for 15 minutes so you don't have to re-enter constantly.

  💡 **Best practice**: Run `sudo apt update && sudo apt upgrade -y` regularly (weekly or monthly) to keep your system secure and up-to-date. You can also run `sudo apt update && sudo apt upgrade -y` as a single command - the `&&` means "run second command only if first succeeds".

- **Labels**: setup, environment, wsl, ubuntu, phase-0
- **Estimated Effort**: Small (10-20 mins including download time)
- **Status**: Backlog
- **Dependencies**: Task 0.1

### Task 0.3: Install and Configure Git inside WSL
- **Description**: Install Git CLI tools, configure global username, email, and best practices settings for commits. Git is essential for version control and will be used throughout the project.

  **Step 1: Install Git** (WSL Ubuntu):
  ```bash
  # Update package lists first (if not done recently)
  sudo apt update

  # Install Git
  sudo apt install -y git

  # The -y flag automatically confirms installation
  ```

  **Step 2: Verify Git installation**:
  ```bash
  # Check Git version (should be 2.x.x)
  git --version

  # Check where Git is installed
  which git
  # Should show: /usr/bin/git
  ```

  **Step 3: Configure your identity** (IMPORTANT - required for commits):
  ```bash
  # Set your name (will appear in commits)
  git config --global user.name "Your Full Name"

  # Set your email (will appear in commits - use your GitHub email)
  git config --global user.email "your_email@example.com"
  ```

  **Step 4: Configure Git best practices**:
  ```bash
  # Set default branch name to 'main' (GitHub standard)
  git config --global init.defaultBranch main

  # Configure line endings (important for Windows/Linux compatibility)
  git config --global core.autocrlf input

  # Configure pull behavior (merge instead of rebase)
  git config --global pull.rebase false

  # Use VS Code as default editor (optional, requires VS Code installed)
  git config --global core.editor "code --wait"
  ```

  **Step 5: Verify configuration**:
  ```bash
  # List all Git configuration
  git config --list

  # Or check specific settings
  git config user.name
  git config user.email
  git config init.defaultBranch
  ```

  **Step 6: (Optional) Set up useful Git aliases**:
  ```bash
  # Shortcut for 'git status'
  git config --global alias.st status

  # Shortcut for 'git checkout'
  git config --global alias.co checkout

  # Shortcut for 'git branch'
  git config --global alias.br branch

  # Shortcut for 'git commit'
  git config --global alias.ci commit

  # Beautiful log view
  git config --global alias.lg "log --oneline --graph --decorate --all"

  # Show last commit
  git config --global alias.last "log -1 HEAD"

  # Undo last commit (keeps changes)
  git config --global alias.undo "reset HEAD~1 --mixed"
  ```

  **Step 7: Test Git configuration**:
  ```bash
  # Create a test repository
  mkdir ~/git-test
  cd ~/git-test
  git init
  # Should create .git directory and show "Initialized empty Git repository"

  # Create a test file
  echo "# Test" > README.md
  git add README.md
  git commit -m "Initial commit"
  # Should succeed with your configured name and email

  # View the commit
  git log
  # Should show your commit with your name and email

  # Clean up test
  cd ~
  rm -rf ~/git-test
  ```

  **Expected Outcome**:
  - ✅ Git installed successfully (version 2.x.x or higher)
  - ✅ `user.name` configured with your name
  - ✅ `user.email` configured with your email
  - ✅ Default branch set to `main`
  - ✅ Line ending behavior configured
  - ✅ Pull behavior configured
  - ✅ `git config --list` shows all your settings
  - ✅ Test repository created and committed successfully
  - ✅ Optional aliases configured

  **Common Issues & Solutions**:
  - **"git: command not found" after installation**:
    - Close and reopen your WSL terminal
    - Or run: `source ~/.bashrc`
    - Verify: `sudo apt list --installed | grep git`

  - **"Please tell me who you are" error when committing**:
    - You forgot to configure user.name and user.email
    - Run the configuration commands from Step 3
    - Must be done before first commit

  - **Wrong name or email configured**:
    - Just run the config command again with correct values
    - It will overwrite the previous setting
    - Or edit directly: `nano ~/.gitconfig`

  - **Commits showing wrong name on GitHub**:
    - Your Git email must match your GitHub email
    - Check GitHub email: Settings → Emails on github.com
    - Update Git email: `git config --global user.email "correct@email.com"`
    - For existing commits, you'll need to rewrite history (advanced)

  - **"fatal: not a git repository"**:
    - You're not inside a Git repository
    - Need to `git init` first or `cd` into an existing repo
    - Check with: `ls -la` and look for `.git` directory

  - **VS Code editor not working**:
    - VS Code not installed yet (we'll install in Task 0.10)
    - Or use nano instead: `git config --global core.editor "nano"`
    - Or leave default (usually vim)

  - **Aliases not working**:
    - Make sure you used the exact syntax shown
    - Test with: `git st` (should run `git status`)
    - View aliases: `git config --get-regexp alias`

  💡 **Learning moment - Global vs Local config**:
  - **`--global`**: Settings apply to all repositories for your user (stored in `~/.gitconfig`)
  - **`--local`**: Settings apply only to current repository (stored in `.git/config`)
  - **`--system`**: Settings apply to all users on the system (rarely used)
  - Global settings are perfect for identity (name/email) since they're the same across all your projects!

  💡 **Learning moment - Why configure line endings?**:
  Windows uses `CRLF` (Carriage Return + Line Feed) for line endings, while Linux/Mac use just `LF`. Setting `core.autocrlf input` means Git will convert CRLF to LF when committing (important when working with Windows files), but won't convert LF to CRLF when checking out. This keeps your repository clean!

  💡 **Learning moment - Why 'main' instead of 'master'?**:
  GitHub changed the default branch name from 'master' to 'main' in 2020 for inclusive language. Setting `init.defaultBranch main` ensures your new repositories match GitHub's convention, avoiding confusion when pushing for the first time.

  💡 **Best practice - Email privacy**:
  GitHub provides a private email address (username@users.noreply.github.com) if you want to keep your real email private. You can find it at GitHub → Settings → Emails → "Keep my email addresses private". Use that email in your Git config!

- **Labels**: setup, git, wsl, version-control, phase-0
- **Estimated Effort**: Small (15-20 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.2

---

**✅ Checkpoint #1**: Basic Development Environment
**Progress**: [████░░░░░░░░░░░░] 25% through Phase 0
**Time elapsed**: ~30-60 mins
**What you have**: WSL2 with Ubuntu, Git configured
**Next**: Set up GitHub project tracking

---

### 🎯 **GitHub Project Setup** (Start tracking your progress early!)

### Task 0.4: Install GitHub CLI on Windows
- **Description**: Install GitHub CLI (gh) on Windows for managing GitHub repositories, issues, pull requests, and projects. This is the primary method since Claude Code runs on Windows. The GitHub CLI is a powerful command-line tool that brings GitHub functionality to your terminal.

  **Step 1: Install GitHub CLI** (Windows PowerShell):
  ```powershell
  # Install via winget
  winget install --id GitHub.cli --source winget
  ```

  **Step 2: Verify installation**:
  ```powershell
  # Check version (should be 2.x.x)
  gh --version

  # Check where gh is installed
  where.exe gh
  # Should show: C:\Program Files\GitHub CLI\gh.exe
  ```

  **Step 3: Authenticate with GitHub**:
  ```powershell
  # Start authentication flow
  gh auth login

  # You'll be prompted with questions:
  # 1. "What account do you want to log into?" → Choose: GitHub.com
  # 2. "What is your preferred protocol?" → Choose: HTTPS
  # 3. "Authenticate Git with your GitHub credentials?" → Choose: Yes
  # 4. "How would you like to authenticate?" → Choose: Login with a web browser

  # A code will be displayed - copy it
  # Press Enter to open browser
  # Paste the code in browser and authorize
  ```

  **Step 4: Verify authentication**:
  ```powershell
  # Check authentication status
  gh auth status

  # Expected output shows:
  # ✓ Logged in to github.com as YOUR_USERNAME
  # ✓ Git operations for github.com configured to use https protocol
  # ✓ Token: *******************
  ```

  **Step 5: Test GitHub CLI**:
  ```powershell
  # List your repositories (may be empty if you're new to GitHub)
  gh repo list

  # View your GitHub profile
  gh api user

  # Check available commands
  gh help
  ```

  **Expected Outcome**:
  - ✅ GitHub CLI installed (version 2.x.x or higher)
  - ✅ `gh --version` works
  - ✅ Successfully authenticated with GitHub
  - ✅ `gh auth status` shows logged in status
  - ✅ Git is configured to use GitHub credentials
  - ✅ `gh repo list` works (even if empty)

  **Common Issues & Solutions**:
  - **"winget not recognized"**:
    - Update Windows or install App Installer from Microsoft Store
    - Verify: `winget --version` in PowerShell

  - **gh command not found after install**:
    - Close and reopen PowerShell (need to refresh PATH)
    - Or restart computer
    - Verify PATH: `echo $env:PATH` should contain GitHub CLI directory

  - **Authentication browser doesn't open**:
    - Manually open browser and go to: https://github.com/login/device
    - Enter the code shown in terminal
    - Alternative: Use token instead: `gh auth login --with-token`

  - **"Failed to authenticate"**:
    - Check internet connection
    - Try again: `gh auth logout` then `gh auth login`
    - Ensure you're logged into GitHub in your browser

  - **"Permission denied" when using gh**:
    - Your authentication expired
    - Re-authenticate: `gh auth login`
    - Check status: `gh auth status`

  - **"Could not resolve host: github.com"**:
    - Internet connection issue
    - Check firewall/proxy settings
    - Try: `ping github.com` to test connectivity

  💡 **Learning moment - Why GitHub CLI?**:
  The GitHub CLI (`gh`) brings GitHub functionality to your terminal, letting you create repos, manage issues, create PRs, run workflows, and more without leaving the command line. It's especially powerful for automation and scripting. Many developers use it daily to speed up their workflow!

  💡 **Learning moment - HTTPS vs SSH**:
  When gh CLI asks for protocol preference:
  - **HTTPS**: Easier setup, uses tokens, works through firewalls. Recommended for beginners.
  - **SSH**: More secure long-term, uses SSH keys, requires SSH setup (Task 0.13). Better for advanced users.
  For this project, HTTPS is fine! You can switch to SSH later if you want.

  💡 **Security note**: When you authenticate, gh CLI creates a token and stores it securely in your system's credential manager. This token has permissions you grant during auth. You can view/revoke tokens at: GitHub → Settings → Developer settings → Personal access tokens.

- **Labels**: setup, github, windows, cli, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.3

### Task 0.5: Create GitHub Repository
- **Description**: Create a new public repository named `jamtrack-radio` on GitHub with a basic README using GitHub CLI. This will be your project's home base where all code, documentation, and collaboration happens.

  **Step 1: Navigate to your projects folder** (Windows PowerShell):
  ```powershell
  # Create a training folder if it doesn't exist
  cd C:\
  mkdir training -ErrorAction SilentlyContinue

  # Navigate into it
  cd C:\training

  # Verify you're in the right place
  pwd
  # Should show: C:\training
  ```

  **Step 2: Create project directory**:
  ```powershell
  # Create the jamtrack-radio folder
  mkdir jamtrack-radio -ErrorAction SilentlyContinue

  # Navigate into it
  cd jamtrack-radio

  # Verify
  pwd
  # Should show: C:\training\jamtrack-radio
  ```

  **Step 3: Initialize local Git repository**:
  ```powershell
  # Initialize Git
  git init

  # Verify .git folder was created
  Get-ChildItem -Hidden -Filter .git
  # Should show a .git directory

  # Set main as default branch
  git branch -M main
  ```

  **Step 4: Create GitHub repository**:
  ```powershell
  # Create public repo on GitHub
  gh repo create jamtrack-radio --public --source=. --remote=origin --clone=false

  # This creates the repo and adds it as the 'origin' remote
  # Verify remote was added
  git remote -v
  # Should show:
  # origin  https://github.com/YOUR_USERNAME/jamtrack-radio.git (fetch)
  # origin  https://github.com/YOUR_USERNAME/jamtrack-radio.git (push)
  ```

  **Step 5: Create initial README file**:
  ```powershell
  # Create README with content
  @"
# Jamtrack Radio

A music streaming application for learning modern software development.

## Project Overview

This project is a learning journey through:
- C# backend development (ASP.NET Core)
- gRPC microservices
- PostgreSQL database
- Docker containerization
- Kubernetes orchestration
- Terraform infrastructure
- CI/CD pipelines
- Azure & AWS cloud deployment
- Monitoring with ELK stack

## Getting Started

Documentation and setup instructions coming soon!

## Status

🚧 Project in early development
"@ | Out-File -FilePath README.md -Encoding utf8

  # Verify file was created
  Get-Content README.md
  ```

  **Step 6: Make initial commit**:
  ```powershell
  # Stage the README
  git add README.md

  # Check status
  git status
  # Should show README.md as "new file" in staging area

  # Create initial commit
  git commit -m "Initial commit: Add README"

  # Verify commit was created
  git log --oneline
  # Should show one commit with your message
  ```

  **Step 7: Push to GitHub**:
  ```powershell
  # Push to GitHub (sets upstream tracking)
  git push -u origin main

  # Verify it worked
  git status
  # Should show: "Your branch is up to date with 'origin/main'"
  ```

  **Step 8: Verify repository on GitHub**:
  ```powershell
  # View the repository in your browser
  gh repo view --web

  # Or manually visit: https://github.com/YOUR_USERNAME/jamtrack-radio
  ```

  **Expected Outcome**:
  - ✅ Local directory `C:\training\jamtrack-radio` exists
  - ✅ Git repository initialized (`.git` folder present)
  - ✅ Default branch is `main`
  - ✅ GitHub repository created at `https://github.com/YOUR_USERNAME/jamtrack-radio`
  - ✅ Remote `origin` configured correctly
  - ✅ README.md file created and committed
  - ✅ Initial commit pushed to GitHub
  - ✅ Repository visible on github.com with README displayed

  **Common Issues & Solutions**:
  - **"gh: command not found"**:
    - GitHub CLI not installed or not in PATH
    - Close and reopen PowerShell to refresh PATH
    - Verify with: `gh --version`
    - Reinstall if needed: `winget install GitHub.cli`

  - **"To create a repository, you must authenticate first"**:
    - You're not authenticated with GitHub
    - Run: `gh auth login` and follow prompts
    - Verify with: `gh auth status`

  - **"Repository already exists"**:
    - You or someone else already created this repo name
    - Either delete the existing repo on GitHub or choose a different name
    - To use different name: `gh repo create jamtrack-radio-yourname --public --source=. --remote=origin`

  - **"fatal: not a git repository"**:
    - You forgot to run `git init`
    - Or you're in the wrong directory
    - Check with `pwd` and ensure you see `.git` folder with `Get-ChildItem -Hidden`

  - **"Permission denied" when pushing**:
    - Authentication issue
    - Re-authenticate: `gh auth login`
    - Or try: `gh auth refresh -h github.com -s repo`

  - **"git push" fails with "failed to push some refs"**:
    - Remote might have content that local doesn't (shouldn't happen on brand new repo)
    - If this happens: `git pull origin main --allow-unrelated-histories` then push again
    - Or force push (ONLY for brand new repo): `git push -u origin main --force`

  - **README not displaying on GitHub**:
    - Wait a few seconds and refresh the page
    - Verify file is named exactly `README.md` (case sensitive)
    - Check file was actually committed: `git log --name-only`

  - **"-ErrorAction SilentlyContinue" explanation**:
    - This PowerShell flag prevents errors if the folder already exists
    - It's safer than letting mkdir fail
    - Ensures the command completes successfully

  💡 **Learning moment - Local vs Remote repositories**:
  A Git repository has two parts:
  - **Local repository**: The `.git` folder on your machine containing full project history
  - **Remote repository**: The copy on GitHub (or other Git host) that others can access

  The `origin` remote is the conventional name for the primary remote repository. When you `git push`, you're sending your local commits to the remote. When you `git pull`, you're fetching updates from remote to local.

  💡 **Learning moment - Why initialize Git locally first?**:
  You could use `gh repo create --clone` to let GitHub CLI create everything, but doing it manually teaches you the fundamental workflow: init → add → commit → push. This is the same process you'll use hundreds of times when making changes!

  💡 **Learning moment - Public vs Private repositories**:
  - **Public repositories**: Anyone can see the code (but only collaborators can push changes)
  - **Private repositories**: Only you and invited collaborators can see or access

  We're using public for this learning project. In production, you'd typically use private repos for proprietary code. GitHub Free accounts get unlimited private repos!

  💡 **Learning moment - Markdown README**:
  The `.md` extension stands for Markdown, a lightweight markup language. GitHub automatically renders README.md files on the repository homepage, making it the first thing visitors see. Markdown uses simple syntax like `#` for headers, `**bold**` for bold text, etc.

- **Labels**: github, repository, setup, git, phase-0
- **Estimated Effort**: Small (15-20 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.4

### Task 0.6: Create GitHub Project Board
- **Description**: Set up a GitHub Project (Projects v2) board for tracking all tasks and milestones throughout the entire project. This gives you a kanban-style board to visualize your progress!

  **Step 1: Create the project** (Windows PowerShell):
  ```powershell
  # Navigate to your repository
  cd C:\training\jamtrack-radio

  # Create a new project (Projects v2)
  gh project create --owner @me --title "Jamtrack Radio Development"

  # Output will show:
  # https://github.com/users/YOUR_USERNAME/projects/NUMBER
  ```

  **Step 2: Save the project number**:
  ```powershell
  # List your projects to see the number
  gh project list --owner @me

  # You'll see something like:
  # NUMBER  TITLE                         STATE  ID
  # 2       Jamtrack Radio Development    OPEN   PVT_...

  # Note the NUMBER (e.g., 2) - you'll use this later to add issues!
  # Save it in a variable for convenience:
  $projectNumber = 2  # Replace with your actual project number
  ```

  **Step 3: View your project in browser**:
  ```powershell
  # Open the project in your browser
  # (Replace NUMBER with your project number)
  Start-Process "https://github.com/users/$(gh api user -q .login)/projects/2"

  # Or manually navigate to: github.com → Your profile → Projects tab
  ```

  **Step 4: Configure project views** (Web UI):
  - In your browser, go to your project
  - You'll see the default "Table" and "Board" views
  - Click on the **Board** view (this is your kanban board)

  **Step 5: Customize the Board view**:
  - Click **"..."** next to "Board" → **"Settings"**
  - Under "Column field", select **"Status"**
  - You'll see default columns: Todo, In Progress, Done
  - These are perfect for tracking tasks!

  **Step 6: Add a "By Phase" view (optional but recommended)**:
  - Click **"+"** to add a new view
  - Name it: **"By Phase"**
  - Select layout: **Board**
  - Under "Column field", select **"Milestone"**
  - Click **"Save"**
  - Now you can view tasks grouped by phase/milestone!

  **Step 7: Customize fields (optional)**:
  - Click **"+ New field"** in the table view
  - Add useful fields like:
    - **Priority**: Single select (High, Medium, Low)
    - **Effort**: Single select (Small, Medium, Large)
  - These help with planning and estimation

  **Expected Outcome**:
  - ✅ GitHub Project created successfully
  - ✅ Project number noted for future use
  - ✅ Project accessible via browser
  - ✅ Board view configured with Status columns
  - ✅ "By Phase" view created (optional)
  - ✅ Project appears in your GitHub profile → Projects tab
  - ✅ Project is ready to receive issues

  **Common Issues & Solutions**:
  - **"gh project: command not supported on this version"**:
    - Your GitHub CLI is outdated
    - Update: `winget upgrade GitHub.cli`
    - Minimum version needed: gh 2.4.0+

  - **"Could not resolve to a User or Organization"**:
    - Authentication issue
    - Re-authenticate: `gh auth refresh`
    - Verify: `gh auth status`

  - **"Project not appearing in list"**:
    - Wait a few seconds and try again: `gh project list --owner @me`
    - Refresh your browser if checking on github.com

  - **Can't find project number**:
    - Run: `gh project list --owner @me --format json`
    - Look for `"number": 2` in the output
    - Or check the URL when viewing project in browser

  - **"Field 'Milestone' not available"**:
    - Milestones must be created first (we'll do this in Task 0.7)
    - You can create the "By Phase" view later after milestones exist
    - For now, just use the Status board view

  - **Browser doesn't open**:
    - Copy the URL manually and paste in browser
    - URL format: `https://github.com/users/YOUR_USERNAME/projects/NUMBER`

  💡 **Learning moment - GitHub Projects v1 vs v2**:
  GitHub has two project systems:
  - **Projects v1** (Classic): Repository-level, simpler, being phased out
  - **Projects v2** (New): User/org-level, more powerful, with custom fields and views

  We're using Projects v2 (accessed via `gh project` command). Projects v2 can span multiple repositories and offers much more flexibility for tracking work!

  💡 **Learning moment - Kanban boards**:
  Kanban is a visual workflow management method using columns to represent stages of work (e.g., Todo → In Progress → Done). Tasks move across the board as they progress. This helps you:
  - Visualize your workload
  - Limit work-in-progress
  - Identify bottlenecks
  - Track completion

  💡 **Learning moment - Why project boards matter**:
  For learning projects like this, having a project board serves multiple purposes:
  - **Tracks progress**: See what you've accomplished
  - **Maintains focus**: Know what to work on next
  - **Portfolio value**: Shows your project management skills to potential employers
  - **Motivation**: Watching tasks move to "Done" is satisfying!

- **Labels**: github, project-management, kanban, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.5

### Task 0.7: Create Initial GitHub Milestones
- **Description**: Create GitHub milestones for the first three phases (Phase 0, 1, and 2A). Milestones group related issues together and help track progress toward major goals. You'll create more milestones as you progress through the project.

  **Step 1: Navigate to repository** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio

  # Verify you're in the right repo
  git remote -v
  # Should show your jamtrack-radio repository
  ```

  **Step 2: Create Phase 0 milestone**:
  ```powershell
  # Create milestone using GitHub API
  gh api repos/:owner/:repo/milestones `
    -f title="Phase 0: Environment Setup & GitHub Init" `
    -f description="Setup development environment (WSL, Git, VS Code) and GitHub project tracking (repository, project board, issues)" `
    -f state="open"

  # The output shows the milestone details including its number
  ```

  **Step 3: Create Phase 1 milestone**:
  ```powershell
  gh api repos/:owner/:repo/milestones `
    -f title="Phase 1: Documentation" `
    -f description="Create comprehensive project documentation including README, contribution guidelines, issue/PR templates, and first GitHub Actions workflow" `
    -f state="open"
  ```

  **Step 4: Create Phase 2A milestone**:
  ```powershell
  gh api repos/:owner/:repo/milestones `
    -f title="Phase 2A: Basic Backend Development" `
    -f description="Build C# backend with ASP.NET Core, PostgreSQL database, basic REST API, and Dapper ORM" `
    -f state="open"
  ```

  **Step 5: List and verify milestones**:
  ```powershell
  # Get all milestones
  gh api repos/:owner/:repo/milestones | ConvertFrom-Json | Select-Object number, title, state, open_issues, closed_issues

  # You should see:
  # number  title                                        state  open_issues  closed_issues
  # ------  -----                                        -----  -----------  -------------
  # 1       Phase 0: Environment Setup & GitHub Init     open   0            0
  # 2       Phase 1: Documentation                       open   0            0
  # 3       Phase 2A: Basic Backend Development          open   0            0
  ```

  **Step 6: Save milestone numbers** (you'll need these!):
  ```powershell
  # Store milestone numbers in variables for convenience
  $milestonePhase0 = 1
  $milestonePhase1 = 2
  $milestonePhase2A = 3

  # Or save them in a text file for reference
  @"
  Phase 0: Milestone 1
  Phase 1: Milestone 2
  Phase 2A: Milestone 3
  "@ | Out-File -FilePath milestones.txt

  Get-Content milestones.txt
  ```

  **Step 7: View milestones in browser (optional)**:
  ```powershell
  # Open milestones page
  Start-Process "https://github.com/$(gh api user -q .login)/jamtrack-radio/milestones"

  # You should see all three milestones listed!
  ```

  **Expected Outcome**:
  - ✅ Three milestones created successfully
  - ✅ Milestone 1: Phase 0 (Environment Setup)
  - ✅ Milestone 2: Phase 1 (Documentation)
  - ✅ Milestone 3: Phase 2A (Basic Backend Development)
  - ✅ All milestones in "open" state
  - ✅ Milestone numbers noted for later use
  - ✅ Milestones visible on GitHub website
  - ✅ Each milestone has descriptive title and description

  **Common Issues & Solutions**:
  - **"Not Found" or 404 error**:
    - Repository name or owner is wrong
    - Verify your repo exists: `gh repo view`
    - The `:owner` and `:repo` placeholders should auto-fill from your current directory

  - **"Resource not accessible by personal access token"**:
    - Permission issue with GitHub authentication
    - Re-authenticate with proper scopes: `gh auth refresh -h github.com -s repo`

  - **Line continuation character (backtick) not working**:
    - PowerShell uses backtick (`) for line continuation
    - Make sure backtick is at END of line with no spaces after it
    - Or put entire command on one line

  - **"milestone already exists" error**:
    - Milestone with that title already created
    - List existing: `gh api repos/:owner/:repo/milestones`
    - Either use existing milestone or choose different title

  - **Can't find milestone numbers**:
    - Run: `gh api repos/:owner/:repo/milestones | ConvertFrom-Json | Select-Object number, title`
    - Numbers are auto-assigned sequentially (1, 2, 3...)
    - Or check on GitHub web UI: Repository → Issues → Milestones

  - **ConvertFrom-Json error**:
    - Old PowerShell version
    - Try without formatting: `gh api repos/:owner/:repo/milestones`
    - Or view in browser instead

  💡 **Learning moment - What are Milestones?**:
  Milestones are a GitHub feature for grouping related issues and pull requests toward a common goal or deadline. They help you:
  - **Track progress**: See percentage of issues completed
  - **Organize work**: Group tasks by feature, sprint, or release
  - **Set deadlines**: Optional due dates for accountability
  - **Communicate**: Show stakeholders what's in each release

  In our project, each Phase is a milestone!

  💡 **Learning moment - GitHub API via CLI**:
  The `gh api` command lets you interact directly with the GitHub REST API. The `:owner` and `:repo` are special placeholders that auto-fill based on your current repository. This is incredibly powerful - anything GitHub can do via web UI, you can automate via API!

  Format: `gh api <endpoint> -f <field>=<value>`
  - `-f` = field (string value)
  - `-F` = file
  - `GET` is default, use `-X POST` for other methods

  💡 **Learning moment - Progressive milestone creation**:
  We're only creating milestones for Phase 0-2A now instead of all phases upfront. This is an Agile practice called "just-in-time planning":
  - Reduces upfront overhead
  - Allows flexibility based on learnings
  - Keeps focus on near-term goals
  - You can always add more milestones later!

- **Labels**: github, milestones, project-management, api, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.6

### Task 0.8: Create Repository Labels
- **Description**: Create a comprehensive set of custom labels for categorizing and filtering issues throughout the project. Labels help you quickly identify task types, phases, and technologies at a glance!

  **Step 1: Navigate to repository** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio

  # Verify you're in correct repo
  gh repo view --json name,owner -q ".owner.login + \"/\" + .name"
  ```

  **Step 2: Create phase labels** (color-coded for visual organization):
  ```powershell
  # Blue theme for Phase 0 (setup/foundation)
  gh label create "phase-0" --description "Phase 0 tasks" --color "1d76db"

  # Green for Phase 1 (documentation)
  gh label create "phase-1" --description "Phase 1 tasks" --color "0e8a16"

  # Yellow for Phase 2A (initial backend)
  gh label create "phase-2a" --description "Phase 2A tasks" --color "fbca04"

  # Orange for Phase 2B (enhanced backend)
  gh label create "phase-2b" --description "Phase 2B tasks" --color "d93f0b"

  # Teal for Phase 3 (Docker)
  gh label create "phase-3" --description "Phase 3 tasks" --color "006b75"
  ```

  **Step 3: Create category/technology labels**:
  ```powershell
  # Environment & setup
  gh label create "setup" --description "Initial setup tasks" --color "1d76db"
  gh label create "environment" --description "Environment configuration" --color "1d76db"

  # Development categories
  gh label create "backend" --description "Backend development" --color "0e8a16"
  gh label create "frontend" --description "Frontend development" --color "5319e7"
  gh label create "database" --description "Database tasks" --color "0e8a16"
  gh label create "api" --description "API development" --color "0e8a16"

  # Cloud & Infrastructure
  gh label create "docker" --description "Docker containerization" --color "006b75"
  gh label create "kubernetes" --description "Kubernetes orchestration" --color "326ce5"
  gh label create "terraform" --description "Infrastructure as Code" --color "5319e7"
  gh label create "azure" --description "Azure deployment" --color "0089d6"
  gh label create "aws" --description "AWS deployment" --color "ff9900"

  # DevOps & Operations
  gh label create "ci-cd" --description "CI/CD pipelines" --color "fbca04"
  gh label create "monitoring" --description "Monitoring and logging" --color "d93f0b"
  gh label create "testing" --description "Testing tasks" --color "0e8a16"

  # Documentation & Planning
  gh label create "documentation" --description "Documentation updates" --color "0075ca"

  # Special categories
  gh label create "optional" --description "Optional task" --color "ededed"
  gh label create "learning" --description "Learning resource or concept" --color "fef2c0"
  ```

  **Step 4: Create tool/technology-specific labels**:
  ```powershell
  # Tools & technologies
  gh label create "git" --description "Git version control" --color "f34f29"
  gh label create "github" --description "GitHub features" --color "000000"
  gh label create "vscode" --description "VS Code editor" --color "007acc"
  gh label create "wsl" --description "Windows Subsystem for Linux" --color "1d76db"
  gh label create "windows" --description "Windows-specific tasks" --color "5319e7"
  gh label create "linux" --description "Linux-specific tasks" --color "fcc624"
  ```

  **Step 5: Verify all labels created**:
  ```powershell
  # List all labels with color display
  gh label list

  # Count total labels
  (gh label list | Measure-Object).Count
  # Should show 26+ labels

  # Export labels to file for reference
  gh label list | Out-File -FilePath labels.txt
  ```

  **Step 6: View labels in browser (optional)**:
  ```powershell
  # Open labels page on GitHub
  Start-Process "https://github.com/$(gh api user -q .login)/jamtrack-radio/labels"

  # You'll see all your color-coded labels!
  ```

  **Expected Outcome**:
  - ✅ Phase labels created (phase-0, phase-1, phase-2a, phase-2b, phase-3)
  - ✅ Category labels created (setup, backend, docker, kubernetes, etc.)
  - ✅ Technology labels created (git, github, vscode, wsl, etc.)
  - ✅ Special labels created (optional, learning)
  - ✅ All labels have descriptions
  - ✅ Color-coded for easy visual identification
  - ✅ Approximately 26+ labels total
  - ✅ Labels visible on GitHub labels page

  **Common Issues & Solutions**:
  - **"label already exists"**:
    - Label with that name already created (maybe GitHub defaults)
    - Skip it or delete first: `gh label delete "labelname" --yes`
    - Or edit existing: `gh label edit "labelname" --description "new desc" --color "newcolor"`

  - **"Invalid color format"**:
    - Colors must be 6-digit hex codes WITHOUT the `#`
    - Valid: `1d76db`
    - Invalid: `#1d76db`
    - Invalid: `blue`

  - **Labels not showing up**:
    - Wait a few seconds and refresh: `gh label list`
    - Check browser page (may need refresh)
    - Verify authentication: `gh auth status`

  - **"Resource not accessible"**:
    - Permission issue
    - Re-authenticate: `gh auth refresh -h github.com -s repo`

  - **Want to delete all labels and start over?**:
    ```powershell
    # CAREFUL: This deletes ALL custom labels
    gh label list --json name -q ".[].name" | ForEach-Object { gh label delete $_ --yes }
    ```

  - **Want to bulk create labels from a file?**:
    - You can script label creation from CSV or JSON
    - Useful for maintaining consistency across multiple repos

  💡 **Learning moment - Why use labels?**:
  Labels are essential for project organization:
  - **Filter issues**: Find all "backend" or "azure" tasks quickly
  - **Triage**: Identify priority, status, or type at a glance
  - **Automation**: Trigger GitHub Actions based on labels
  - **Communication**: Show what kind of work an issue involves
  - **Metrics**: Track how much work is "documentation" vs "development"

  Real-world teams often have 20-50 labels for complex projects!

  💡 **Learning moment - Label color psychology**:
  Our label colors follow common conventions:
  - **Blue** (1d76db): Foundation/setup work
  - **Green** (0e8a16): Active development, positive progress
  - **Yellow** (fbca04): Caution, in-progress, needs attention
  - **Orange/Red** (d93f0b): Critical, infrastructure, monitoring
  - **Purple** (5319e7): Advanced features, frontend
  - **Gray** (ededed): Optional, low priority

  Consistent coloring helps your brain quickly identify task types!

  💡 **Learning moment - Multi-label strategy**:
  Issues can (and should!) have multiple labels:
  - **Phase label**: Which phase is this? (e.g., phase-2a)
  - **Category label**: What type of work? (e.g., backend, docker)
  - **Technology label**: What tool/platform? (e.g., azure, kubernetes)
  - **Status label**: Special status? (e.g., optional, learning)

  Example: A task might be labeled: `phase-3`, `docker`, `backend`, `azure`

- **Labels**: github, labels, project-management, organization, phase-0
- **Estimated Effort**: Small (15-20 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.7

### Task 0.9: Create GitHub Issues for Remaining Phase 0 Tasks
- **Description**: Create GitHub issues for the remaining Phase 0 tasks (VS Code, SSH setup, environment testing) and add them to your project board! This is where your GitHub project tracking really comes to life - you'll be able to see and manage all remaining setup tasks.

  **Step 1: Navigate to repository** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio

  # Verify repo
  gh repo view --json nameWithOwner -q ".nameWithOwner"
  ```

  **Step 2: Get your Phase 0 milestone number**:
  ```powershell
  # Query milestones and filter for Phase 0
  $milestone = gh api repos/:owner/:repo/milestones | ConvertFrom-Json | Where-Object {$_.title -like "*Phase 0*"} | Select-Object -ExpandProperty number

  # Verify milestone number (should be 1)
  echo "Phase 0 Milestone: $milestone"
  ```

  **Step 3: Get your project number** (from Task 0.6):
  ```powershell
  # List your projects
  gh project list --owner @me

  # Save the project number (likely 2 or whatever you noted in Task 0.6)
  $projectNumber = 2  # Replace with YOUR project number
  ```

  **Step 4: Create issues for remaining Phase 0 tasks**:
  ```powershell
  # Task 0.10: Install VS Code
  gh issue create `
    --title "Task 0.10: Install VS Code on Windows" `
    --body "Install Visual Studio Code using Winget for code editing and remote WSL development. Verify CLI access works." `
    --label "setup,vscode,windows,phase-0" `
    --milestone $milestone

  # Task 0.11: Install Remote-WSL Extension
  gh issue create `
    --title "Task 0.11: Install VS Code Remote - WSL Extension" `
    --body "Install the Remote-WSL extension to enable VS Code to work seamlessly with WSL Ubuntu environment." `
    --label "setup,vscode,wsl,phase-0" `
    --milestone $milestone

  # Task 0.12: GitHub CLI in WSL (Optional)
  gh issue create `
    --title "Task 0.12: Install GitHub CLI in WSL (Optional)" `
    --body "**OPTIONAL**: Install GitHub CLI in WSL for gh commands directly from Ubuntu. Windows gh CLI is sufficient for most workflows." `
    --label "setup,github,wsl,optional,phase-0" `
    --milestone $milestone

  # Task 0.13: Generate SSH Key
  gh issue create `
    --title "Task 0.13: Generate SSH Key for GitHub" `
    --body "Create SSH key pair in WSL for secure authentication to GitHub. Add public key to GitHub account." `
    --label "setup,git,github,wsl,phase-0" `
    --milestone $milestone

  # Task 0.14: Test SSH Connection
  gh issue create `
    --title "Task 0.14: Test SSH Connection to GitHub" `
    --body "Verify SSH authentication to GitHub works correctly from WSL." `
    --label "setup,git,github,phase-0" `
    --milestone $milestone

  # Task 0.15: Test Complete Environment
  gh issue create `
    --title "Task 0.15: Test Complete Development Environment" `
    --body "Perform end-to-end verification that entire dev environment (WSL, Git, GitHub, VS Code, SSH) is working correctly." `
    --label "setup,testing,phase-0" `
    --milestone $milestone
  ```

  **Step 5: Verify issues were created**:
  ```powershell
  # List all Phase 0 issues
  gh issue list --milestone $milestone

  # You should see 6 new issues (Tasks 0.10-0.15)

  # Count issues in milestone
  (gh issue list --milestone $milestone).Count
  ```

  **Step 6: Add issues to your project board**:
  ```powershell
  # Get all Phase 0 issue numbers
  $issues = gh issue list --milestone $milestone --json number --jq '.[].number'

  # Add each issue to your project
  # (Replace 2 with your project number if different)
  foreach ($issue in $issues) {
    gh project item-add $projectNumber --owner @me --url "https://github.com/$(gh api user -q .login)/jamtrack-radio/issues/$issue"
    echo "Added issue #$issue to project"
  }
  ```

  **Step 7: View your project board**:
  ```powershell
  # Open project in browser
  Start-Process "https://github.com/users/$(gh api user -q .login)/projects/$projectNumber"

  # You'll see all your Phase 0 issues on the board!
  ```

  **Expected Outcome**:
  - ✅ 6 new issues created (Tasks 0.10 through 0.15)
  - ✅ All issues assigned to Phase 0 milestone
  - ✅ Issues have appropriate labels (setup, vscode, wsl, etc.)
  - ✅ Issues have descriptive bodies explaining the task
  - ✅ All issues added to your project board
  - ✅ Issues visible on GitHub Issues page
  - ✅ Issues visible on project board
  - ✅ Can now track remaining Phase 0 progress in GitHub!

  **Common Issues & Solutions**:
  - **"$milestone" is empty or null**:
    - Milestone query didn't work
    - Manually set: `$milestone = 1` (or whatever your Phase 0 milestone number is)
    - Verify: `gh api repos/:owner/:repo/milestones | ConvertFrom-Json | Select-Object number,title`

  - **"--milestone" flag not working**:
    - Milestone might not exist
    - Check: `gh api repos/:owner/:repo/milestones`
    - Or create milestone first (Task 0.7)

  - **"project not found" when adding items**:
    - Wrong project number
    - List projects: `gh project list --owner @me`
    - Update `$projectNumber` variable

  - **"gh project item-add" command fails**:
    - Old gh CLI version (need 2.4.0+)
    - Update: `winget upgrade GitHub.cli`
    - Or skip project-add step and add manually via web UI

  - **Rate limiting errors**:
    - Creating issues too fast
    - Add small delays: `Start-Sleep -Seconds 2` between issue creations

  - **Want to close an issue?**:
    ```powershell
    gh issue close ISSUE_NUMBER --comment "Completed!"
    ```

  - **Want to edit an issue?**:
    ```powershell
    gh issue edit ISSUE_NUMBER --title "New Title" --body "New body"
    ```

  💡 **Learning moment - Issues are work tracking units**:
  GitHub Issues are the fundamental unit of work tracking:
  - **Title**: Short summary (like a task name)
  - **Body**: Detailed description (can include markdown, checklists, code blocks)
  - **Labels**: Categorize and filter
  - **Milestone**: Group related issues
  - **Assignees**: Who's responsible
  - **Projects**: Visual organization on boards

  Issues can also have comments, linked PRs, and activity history!

  💡 **Learning moment - Why create issues programmatically?**:
  We're using `gh issue create` via CLI instead of manually clicking on GitHub because:
  - **Speed**: Create 6 issues in seconds vs minutes
  - **Consistency**: Ensure all issues follow same format
  - **Reproducibility**: Could run same script on another project
  - **Automation**: Part of DevOps culture - automate repetitive tasks!

  In real projects, teams often generate issues from templates, spreadsheets, or project management tools.

  💡 **Learning moment - Issue-to-Project linking**:
  GitHub Projects v2 and Issues are separate entities that link together. An issue can be in multiple projects, and a project can contain issues from multiple repositories. The `gh project item-add` command creates this linkage, making issues appear on your project board!

  💡 **Real-world tip - Issue templates**:
  Production repositories usually have issue templates (we'll create these in Phase 1!) that provide a consistent structure for bugs, features, and tasks. They guide contributors to provide all necessary information, improving collaboration quality.

- **Labels**: github, issues, project-management, automation, phase-0
- **Estimated Effort**: Medium (20-25 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.8

---

**✅ Checkpoint #2**: GitHub Project Tracking Active!
**Progress**: [████████░░░░░░░░] 56% through Phase 0
**Time elapsed**: ~2-3 hours
**What you have**: WSL, Git, GitHub repo, project board, milestones, labels, and issues created!
**Achievement unlocked**: 🎉 You're now tracking your progress in GitHub!
**Next**: Complete VS Code and SSH setup

---

### 🛠️ **Complete Development Environment Setup**

### Task 0.10: Install VS Code on Windows via Command Line
- **Description**: Install Visual Studio Code using Winget for powerful code editing, remote WSL development, and integrated terminal. VS Code will be your primary development environment throughout this project!

  **Step 1: Install VS Code** (Windows PowerShell):
  ```powershell
  # Install Visual Studio Code
  winget install --id Microsoft.VisualStudioCode --source winget

  # This installs VS Code and automatically adds 'code' to your PATH
  # Installation takes 1-2 minutes
  ```

  **Step 2: Close and reopen PowerShell**:
  ```powershell
  # IMPORTANT: Close your PowerShell window completely and open a new one
  # This refreshes the PATH so 'code' command is available
  # Or alternatively, you can restart your terminal
  ```

  **Step 3: Verify installation** (in new PowerShell window):
  ```powershell
  # Check VS Code version
  code --version
  # Should show version 1.x.x, commit hash, and architecture

  # Check where code.exe is installed
  where.exe code
  # Should show: C:\Users\YourName\AppData\Local\Programs\Microsoft VS Code\bin\code
  ```

  **Step 4: Verify VS Code can launch**:
  ```powershell
  # Launch VS Code (should open the application)
  code

  # After verifying it opens, close VS Code
  # (We'll configure it more in Task 0.11)
  ```

  **Step 5: Test code command with a file**:
  ```powershell
  # Navigate to your project
  cd C:\training\jamtrack-radio

  # Open current directory in VS Code
  code .

  # VS Code should open with your jamtrack-radio folder
  # You'll see README.md in the explorer sidebar
  # Close VS Code after verifying
  ```

  **Step 6: Verify VS Code extensions command works**:
  ```powershell
  # List installed extensions (will be empty initially)
  code --list-extensions

  # This should run without errors
  # (Even if output is empty, that's expected)
  ```

  **Expected Outcome**:
  - ✅ VS Code installed successfully
  - ✅ `code --version` shows version 1.x.x
  - ✅ VS Code launches when running `code`
  - ✅ `code .` opens current folder in VS Code
  - ✅ `code --list-extensions` command works
  - ✅ VS Code appears in Windows Start Menu
  - ✅ VS Code CLI accessible from PowerShell

  **Common Issues & Solutions**:
  - **"winget not recognized"**:
    - Update Windows to latest version
    - Or install App Installer from Microsoft Store
    - Minimum Windows version: Windows 10 1809 or Windows 11

  - **"code: command not found" after install**:
    - **Most common issue**: You need to close and reopen PowerShell
    - PATH isn't refreshed until you open new terminal
    - Or restart your computer if still not working
    - Manually add to PATH: System → Advanced → Environment Variables

  - **VS Code installs but doesn't launch**:
    - Check if antivirus is blocking it
    - Try running as Administrator
    - Check Windows Event Viewer for errors

  - **"Multiple packages found"**:
    - Use `--exact` flag: `winget install --exact --id Microsoft.VisualStudioCode`

  - **Installation hangs or fails**:
    - Check internet connection
    - Try again: `winget install --id Microsoft.VisualStudioCode --force`
    - Or download manually from code.visualstudio.com

  - **Want to install specific VS Code version?**:
    ```powershell
    winget install --id Microsoft.VisualStudioCode --version 1.85.0
    ```

  - **Already have VS Code installed?**:
    - That's fine! Just verify `code --version` works
    - Update if needed: `winget upgrade Microsoft.VisualStudioCode`

  💡 **Learning moment - Why VS Code?**:
  Visual Studio Code is the most popular code editor for modern development:
  - **Lightweight**: Starts quickly, doesn't hog resources
  - **Extensible**: Thousands of extensions for every language and framework
  - **Integrated Terminal**: Run commands without leaving editor
  - **Git Integration**: Built-in source control
  - **Remote Development**: Edit files in WSL, containers, or remote servers seamlessly
  - **IntelliSense**: Smart code completion and navigation
  - **Free & Open Source**: Backed by Microsoft, used by millions

  For our project, we'll use extensions for C#, Docker, Kubernetes, and more!

  💡 **Learning moment - CLI-first installation**:
  We're using `winget` (Windows Package Manager) instead of downloading installers because:
  - **Automation**: Can script and reproduce installations
  - **Speed**: No need to navigate websites and click through wizards
  - **Consistency**: Same installation method across different machines
  - **Updates**: Easy to update: `winget upgrade --all`
  - **DevOps mindset**: Command-line tools are essential for automation

  This is how infrastructure-as-code and configuration management work!

  💡 **Learning moment - The 'code' command**:
  The `code` command is incredibly powerful:
  - `code .` - Open current directory
  - `code file.txt` - Open specific file
  - `code --new-window` - Open new window
  - `code --diff file1 file2` - Compare two files
  - `code --install-extension` - Install extensions
  - `code --goto file:line:column` - Jump to specific location

  You'll use `code .` constantly to open projects!

  💡 **Real-world tip - VS Code Settings Sync**:
  VS Code has built-in Settings Sync (Sign in → Account icon → Turn on Settings Sync). This syncs your settings, extensions, keybindings, and snippets across multiple machines via your GitHub/Microsoft account. Incredibly useful when working on multiple computers!

- **Labels**: setup, vscode, windows, editor, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.9

### Task 0.11: Install VS Code Remote - WSL Extension
- **Description**: Install the Remote - WSL extension to enable VS Code to work seamlessly with your WSL Ubuntu environment. This is a game-changer - you'll be able to edit files in WSL using VS Code's GUI while the code actually runs in Linux!

  **Step 1: Install the extension** (Windows PowerShell):
  ```powershell
  # Install Remote - WSL extension
  code --install-extension ms-vscode-remote.remote-wsl

  # This installs the bridge between Windows VS Code and WSL
  ```

  **Step 2: Verify extension installed**:
  ```powershell
  # List installed extensions
  code --list-extensions

  # Should show: ms-vscode-remote.remote-wsl

  # Or search for it specifically
  code --list-extensions | Select-String "remote-wsl"
  ```

  **Step 3: Launch WSL** (Windows PowerShell or Terminal):
  ```powershell
  # Start Ubuntu WSL
  wsl

  # You're now in your WSL Ubuntu environment
  # Your prompt should change to show username@hostname
  ```

  **Step 4: Test opening VS Code from WSL** (WSL Ubuntu terminal):
  ```bash
  # Navigate to home directory
  cd ~

  # Verify you're in WSL
  pwd
  # Should show: /home/your-username

  # Try to open VS Code from WSL
  code .

  # First time will install VS Code Server in WSL (takes 30-60 seconds)
  # You'll see messages like:
  # "Installing VS Code Server for x64"
  # "Downloading: 100%"
  ```

  **Step 5: Verify VS Code opened in WSL mode**:
  - VS Code should open in a new window
  - Look at the **bottom-left corner** of VS Code
  - You should see a **green indicator** that says: **WSL: Ubuntu**
  - This confirms you're connected to WSL!

  **Step 6: Test creating a file in WSL**:
  In VS Code (connected to WSL):
  ```plaintext
  1. Click "New File" or press Ctrl+N
  2. Type: echo "Hello from WSL!"
  3. Save as: test-wsl.sh (File → Save)
  4. Save location: /home/yourusername/test-wsl.sh
  ```

  **Step 7: Verify file exists in WSL**:
  Back in WSL terminal:
  ```bash
  # List files
  ls -la ~/test-wsl.sh

  # Should show the file you just created

  # View contents
  cat ~/test-wsl.sh
  # Should show: echo "Hello from WSL!"

  # Make it executable and run it
  chmod +x ~/test-wsl.sh
  ./test-wsl.sh
  # Should output: Hello from WSL!

  # Clean up test file
  rm ~/test-wsl.sh
  ```

  **Step 8: Test opening project folder from WSL**:
  ```bash
  # Create a test directory
  mkdir -p ~/projects/test-vscode-wsl
  cd ~/projects/test-vscode-wsl

  # Create a sample file
  echo "# WSL Test Project" > README.md

  # Open this directory in VS Code
  code .

  # VS Code should open showing the test-vscode-wsl folder
  # Still connected to WSL (green indicator in bottom-left)

  # Exit VS Code and clean up
  cd ~
  rm -rf ~/projects/test-vscode-wsl
  ```

  **Expected Outcome**:
  - ✅ Remote - WSL extension installed
  - ✅ `code .` command works from WSL terminal
  - ✅ VS Code shows "WSL: Ubuntu" in bottom-left green indicator
  - ✅ VS Code Server installed in WSL (~/.vscode-server/ directory exists)
  - ✅ Can create and edit files in WSL from VS Code
  - ✅ Files created in VS Code appear in WSL filesystem
  - ✅ Can open WSL directories in VS Code
  - ✅ Integrated terminal in VS Code runs in WSL

  **Common Issues & Solutions**:
  - **"code: command not found" in WSL**:
    - The `code` command should work after installing Remote-WSL
    - If not, close WSL terminal completely and reopen
    - Or try: `export PATH="$PATH:/mnt/c/Users/YourName/AppData/Local/Programs/Microsoft VS Code/bin"`
    - Add to ~/.bashrc if needed (but shouldn't be necessary)

  - **VS Code opens but doesn't show "WSL: Ubuntu"**:
    - The extension didn't activate
    - Check extensions in VS Code: View → Extensions → Search "WSL"
    - Enable the Remote - WSL extension
    - Restart VS Code and try again

  - **"Installing VS Code Server" hangs**:
    - Internet connection issue
    - Or Windows Firewall blocking
    - Cancel and try again
    - Check: ~/.vscode-server/bin/ directory in WSL

  - **Permission denied errors**:
    - Don't run `code` with `sudo` in WSL
    - Make sure you own the files: `ls -la` to check
    - Fix permissions: `sudo chown -R $USER:$USER ~/`

  - **VS Code shows "disconnected" or fails to connect**:
    - WSL might be stopped
    - Restart WSL: Exit all WSL terminals, run `wsl --shutdown` from PowerShell, then `wsl` again
    - Or restart computer

  - **Want to reconnect to WSL from Windows VS Code?**:
    - Open VS Code on Windows
    - Click green indicator in bottom-left (or F1)
    - Select: "Remote-WSL: New Window" or "Remote-WSL: Reopen Folder in WSL"

  - **Extensions not working in WSL**:
    - Some extensions need to be installed separately in WSL
    - When connected to WSL, go to Extensions view
    - Extensions show "Install in WSL: Ubuntu" button
    - Install C#, Docker, etc. extensions in WSL when needed

  💡 **Learning moment - How Remote - WSL works**:
  The Remote - WSL extension uses a client-server architecture:
  - **VS Code GUI**: Runs on Windows (the "client")
  - **VS Code Server**: Runs in WSL (the "server")
  - **Connection**: They communicate via local socket/pipe

  Benefits:
  - Edit files with Windows GUI while code runs in Linux
  - Linux tools (compilers, runtimes) work natively
  - No file sync issues between Windows and WSL
  - Full Linux environment while using Windows applications

  **Step 9: Open integrated terminal** (in VS Code connected to WSL):
  ```plaintext
  1. Press Ctrl+` (backtick) or View → Terminal
  2. Terminal should open at bottom
  3. Notice it's a bash shell (not PowerShell!)
  4. Run: uname -a
  5. Should show Linux kernel version
  6. This terminal is running inside WSL!
  ```

  💡 **Learning moment - Why this matters for development**:
  Most production servers run Linux, so developing in Linux (via WSL) means:
  - **Consistent environment**: Dev matches production
  - **Native tools**: Use Linux package managers, bash scripts
  - **Docker compatibility**: Docker runs better on Linux
  - **Path differences**: Learn Linux path structure (/home vs C:\)
  - **Line endings**: Linux uses LF, Windows uses CRLF - WSL uses LF natively

  With Remote-WSL, you get best of both worlds: Windows desktop + Linux development!

  💡 **Learning moment - VS Code Server**:
  When you run `code .` from WSL, VS Code installs a headless server in `~/.vscode-server/` that:
  - Handles file operations
  - Runs language servers (IntelliSense)
  - Executes terminal commands
  - Manages extensions

  The Windows VS Code GUI is just a "remote control" for this server. This same architecture powers Remote-SSH (edit files on remote servers) and Remote-Containers (edit inside Docker containers)!

  💡 **Real-world tip - Multiple WSL distros**:
  You can install multiple WSL distributions (Ubuntu, Debian, Fedora, etc.) and VS Code can connect to any of them. Use `Remote-WSL: New Window using Distro...` to choose. Great for testing across different Linux versions!

- **Labels**: setup, vscode, wsl, remote-development, phase-0
- **Estimated Effort**: Small (15-20 mins including first-time VS Code Server install)
- **Status**: Backlog
- **Dependencies**: Task 0.10

### Task 0.12: Install GitHub CLI in WSL (Optional)
- **Description**: **(OPTIONAL)** Install GitHub CLI inside WSL Ubuntu if you prefer to run `gh` commands directly from Linux. Since you already have GitHub CLI on Windows (Task 0.4), this is completely optional. Only do this if you want gh available in your WSL environment.

  **Note**: You can skip this task! The Windows gh CLI is sufficient for most workflows.

  **Step 1: Add GitHub CLI repository** (WSL Ubuntu):
  ```bash
  # Launch WSL if not already in it
  # (From Windows: wsl)

  # Download and add GitHub CLI GPG key
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

  # Verify key was added
  ls -la /usr/share/keyrings/githubcli-archive-keyring.gpg
  ```

  **Step 2: Add GitHub CLI package repository**:
  ```bash
  # Add repository to sources list
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

  # Verify repository was added
  cat /etc/apt/sources.list.d/github-cli.list
  # Should show the deb line
  ```

  **Step 3: Install GitHub CLI**:
  ```bash
  # Update package list
  sudo apt update

  # Install gh
  sudo apt install -y gh

  # This will download and install GitHub CLI
  ```

  **Step 4: Verify installation**:
  ```bash
  # Check version
  gh --version
  # Should show: gh version 2.x.x

  # Check where gh is installed
  which gh
  # Should show: /usr/bin/gh
  ```

  **Step 5: Authenticate with GitHub**:
  ```bash
  # Start authentication
  gh auth login

  # Follow prompts:
  # 1. "What account?" → Choose: GitHub.com
  # 2. "Protocol?" → Choose: HTTPS (or SSH if you prefer)
  # 3. "Authenticate Git?" → Choose: Yes
  # 4. "How to authenticate?" → Choose: Login with a web browser

  # Copy the code shown, press Enter
  # Browser opens → paste code → authorize
  ```

  **Step 6: Verify authentication**:
  ```bash
  # Check auth status
  gh auth status

  # Should show: ✓ Logged in to github.com as YOUR_USERNAME

  # Test gh command
  gh repo list
  # Should show your repositories
  ```

  **Expected Outcome** (if you choose to do this optional task):
  - ✅ GitHub CLI repository added to apt sources
  - ✅ gh installed in WSL
  - ✅ `gh --version` works in WSL
  - ✅ Authenticated with GitHub from WSL
  - ✅ `gh auth status` shows logged in
  - ✅ Can run gh commands from WSL terminal

  **Common Issues & Solutions**:
  - **curl command fails**:
    - Internet connection issue
    - Or proxy/firewall blocking
    - Verify curl works: `curl -I https://github.com`

  - **"sudo: dd: command not found"**:
    - Unlikely but possible
    - Try alternative: `curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /usr/share/keyrings/githubcli-archive-keyring.gpg > /dev/null`

  - **apt update fails with GPG error**:
    - GPG key not added correctly
    - Remove and re-add: `sudo rm /usr/share/keyrings/githubcli-archive-keyring.gpg`
    - Then repeat Step 1

  - **"gh: command not found" after install**:
    - Close and reopen WSL terminal
    - Or run: `hash -r` to refresh command cache

  - **Authentication browser doesn't open**:
    - WSL can't open Windows browsers directly
    - Copy the URL shown and paste in Windows browser manually
    - Or use: `gh auth login --web`

  - **Already authenticated on Windows, need to auth in WSL too?**:
    - Yes, Windows and WSL are separate environments
    - Each needs its own authentication
    - But it's quick - just `gh auth login`

  💡 **Learning moment - Why is this optional?**:
  Since you have gh CLI on Windows (from Task 0.4), you can run GitHub commands from PowerShell or Windows Terminal. The Windows gh CLI can interact with your GitHub account perfectly fine.

  Installing gh in WSL is only useful if:
  - You prefer working entirely in the Linux terminal
  - You're writing bash scripts that use gh commands
  - You want to keep Windows and Linux environments completely separate

  For this learning project, the Windows gh CLI is sufficient!

  💡 **Learning moment - Package repositories**:
  Unlike Windows (where you download .exe files), Linux uses **package repositories**:
  1. **Repository**: A server hosting software packages
  2. **Sources list**: Configuration telling apt where to find packages (/etc/apt/sources.list.d/)
  3. **GPG key**: Cryptographic signature verifying packages are authentic
  4. **apt update**: Downloads package lists from repositories
  5. **apt install**: Downloads and installs packages

  This is how all software is installed on Linux servers - no downloading random executables from websites!

  💡 **Learning moment - Windows vs WSL binaries**:
  The gh.exe on Windows and gh in WSL are completely different binaries:
  - **Windows gh.exe**: Compiled for Windows, runs on Windows kernel
  - **WSL gh**: Compiled for Linux, runs on Linux kernel (inside WSL)

  They can't share authentication tokens or configuration because they're in different environments with different file systems. This is why we need to authenticate separately!

- **Labels**: setup, github, wsl, optional, linux, phase-0
- **Estimated Effort**: Small (10-15 mins) - **But you can skip this entirely!**
- **Status**: Backlog
- **Dependencies**: Task 0.3

### Task 0.13: Generate SSH Key for GitHub
- **Description**: Create an SSH key pair in WSL for secure, password-less authentication to GitHub. SSH keys are more secure than passwords and essential for modern Git workflows. You'll generate a private key (stays on your machine) and a public key (uploaded to GitHub).

  **Step 1: Check for existing SSH keys** (WSL Ubuntu):
  ```bash
  # Launch WSL if not already in it
  # (From Windows: wsl)

  # Check if SSH keys already exist
  ls -la ~/.ssh/

  # If you see id_ed25519 and id_ed25519.pub, you already have keys!
  # You can either use them or generate new ones (Step 2)
  ```

  **Step 2: Generate new SSH key pair**:
  ```bash
  # Generate ED25519 SSH key (modern, secure algorithm)
  ssh-keygen -t ed25519 -C "your_email@example.com"

  # Replace "your_email@example.com" with YOUR actual email
  # (Use the same email as your GitHub account)

  # You'll be prompted:
  # 1. "Enter file in which to save the key" → Press Enter (use default: ~/.ssh/id_ed25519)
  # 2. "Enter passphrase" → Press Enter for no passphrase (or enter one for extra security)
  # 3. "Enter same passphrase again" → Press Enter again (or repeat your passphrase)

  # Output shows:
  # "Your identification has been saved in /home/username/.ssh/id_ed25519"
  # "Your public key has been saved in /home/username/.ssh/id_ed25519.pub"
  # Plus a key fingerprint and randomart image
  ```

  **Step 3: Start SSH agent**:
  ```bash
  # Start the ssh-agent in the background
  eval "$(ssh-agent -s)"

  # Output shows: Agent pid XXXXX
  # This means ssh-agent is now running
  ```

  **Step 4: Add your SSH private key to the agent**:
  ```bash
  # Add your private key to ssh-agent
  ssh-add ~/.ssh/id_ed25519

  # Output: "Identity added: /home/username/.ssh/id_ed25519 (your_email@example.com)"
  ```

  **Step 5: Display your public key**:
  ```bash
  # View your public key
  cat ~/.ssh/id_ed25519.pub

  # Output starts with: ssh-ed25519 AAAA...lots of characters...== your_email@example.com
  # Copy this ENTIRE line (including ssh-ed25519 at the start and email at the end)
  ```

  **Step 6: Copy public key to clipboard** (easier method):
  ```bash
  # Linux doesn't have direct clipboard access, so copy output manually
  # Or use this trick to copy via Windows clipboard:
  cat ~/.ssh/id_ed25519.pub | clip.exe

  # The public key is now in your Windows clipboard!
  # (clip.exe is a Windows tool accessible from WSL)
  ```

  **Step 7: Add SSH key to GitHub** (Web UI):
  - Open GitHub in your browser
  - Click your profile picture (top-right) → **Settings**
  - In left sidebar, click **SSH and GPG keys**
  - Click green **"New SSH key"** button
  - **Title**: Enter a descriptive name (e.g., "WSL Ubuntu - Laptop")
  - **Key type**: Select "Authentication Key"
  - **Key**: Paste your public key (the ssh-ed25519 AAAA... line)
  - Click **"Add SSH key"**
  - You may need to confirm with your GitHub password

  **Step 8: Verify key was added**:
  - You should see your new key listed on the SSH keys page
  - It shows the title, key fingerprint, and "Added" date
  - If you added it just now, it will say "Added X seconds ago"

  **Expected Outcome**:
  - ✅ SSH key pair generated in ~/.ssh/
  - ✅ Private key: ~/.ssh/id_ed25519 (never share this!)
  - ✅ Public key: ~/.ssh/id_ed25519.pub
  - ✅ ssh-agent running
  - ✅ Private key added to ssh-agent
  - ✅ Public key copied
  - ✅ Public key added to GitHub account
  - ✅ Key visible on GitHub → Settings → SSH and GPG keys

  **Common Issues & Solutions**:
  - **"ssh-keygen: command not found"**:
    - OpenSSH not installed (very rare on Ubuntu)
    - Install: `sudo apt install openssh-client`

  - **Already have a key and don't want to overwrite?**:
    - When prompted for filename, use different name: `~/.ssh/id_ed25519_github`
    - Then add it: `ssh-add ~/.ssh/id_ed25519_github`
    - And configure Git to use it in ~/.ssh/config (advanced)

  - **Forgot passphrase?**:
    - Unfortunately, you'll need to generate a new key pair
    - Passphrases protect your private key and are unrecoverable

  - **clip.exe doesn't work**:
    - Just manually copy the output of `cat ~/.ssh/id_ed25519.pub`
    - Triple-click to select entire line, Ctrl+C to copy
    - Or use: `cat ~/.ssh/id_ed25519.pub` and copy from terminal

  - **"Key is already in use" error on GitHub**:
    - That public key is already associated with another GitHub account
    - Generate a new key pair with different email
    - Or remove it from the other account first

  - **Want to see your key fingerprint?**:
    ```bash
    ssh-keygen -lf ~/.ssh/id_ed25519.pub
    ```

  - **Why ED25519 instead of RSA?**:
    - ED25519 is newer, faster, and more secure
    - Smaller key size (but more secure than 2048-bit RSA)
    - If you need RSA for compatibility: `ssh-keygen -t rsa -b 4096 -C "email@example.com"`

  💡 **Learning moment - Public/Private Key Cryptography**:
  SSH keys use **asymmetric encryption**:
  - **Private key** (id_ed25519): Secret, stays on your machine, never share!
  - **Public key** (id_ed25519.pub): Can be shared freely, uploaded to GitHub

  How it works:
  1. You connect to GitHub
  2. GitHub sends a challenge encrypted with your public key
  3. Only your private key can decrypt it
  4. You send back the decrypted answer
  5. GitHub knows it's you!

  This is more secure than passwords because:
  - Private key never leaves your machine
  - Can't be phished
  - Can't be brute-forced
  - Each machine can have its own key

  💡 **Learning moment - SSH Agent**:
  The ssh-agent is a background program that holds your private keys in memory so you don't need to enter the passphrase every time. Benefits:
  - Convenience: Enter passphrase once per session
  - Security: Keys stored in memory, not on disk
  - Multiple keys: Agent can manage multiple keys

  The `eval "$(ssh-agent -s)"` command starts the agent and sets environment variables so SSH knows how to talk to it.

  💡 **Learning moment - Why use SSH for Git?**:
  GitHub supports two protocols for Git operations:
  - **HTTPS**: Username/password or token, works everywhere
  - **SSH**: Key-based, more secure, no password prompts

  SSH is preferred for:
  - **Security**: No passwords to steal or forget
  - **Convenience**: No authentication prompts after initial setup
  - **Performance**: Slightly faster connection
  - **Git operations**: Essential for advanced workflows

  You'll use SSH URLs like: `git@github.com:username/repo.git`

  💡 **Real-world tip - Multiple SSH keys**:
  Many developers have multiple SSH keys:
  - Different keys for work vs personal
  - Different keys per machine (laptop, desktop, server)
  - Different keys per GitHub account

  GitHub shows which key was used for each commit, helping audit access. You can manage this with ~/.ssh/config to specify which key to use for which host!

- **Labels**: setup, ssh, github, security, cryptography, phase-0
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.11

### Task 0.14: Test SSH Connection to GitHub
- **Description**: Verify that SSH authentication to GitHub works correctly from WSL. This test confirms your SSH key is properly configured and GitHub recognizes your identity!

  **Step 1: Test SSH connection** (WSL Ubuntu):
  ```bash
  # Launch WSL if not already in it
  # (From Windows: wsl)

  # Test SSH connection to GitHub
  ssh -T git@github.com

  # The -T flag disables pseudo-terminal allocation (not needed for test)
  ```

  **Step 2: Handle host verification (first time only)**:
  - First time connecting, you'll see:
    ```
    The authenticity of host 'github.com (IP_ADDRESS)' can't be established.
    ED25519 key fingerprint is SHA256:...
    Are you sure you want to continue connecting (yes/no/[fingerprint])?
    ```
  - **Type: `yes`** and press Enter
  - This adds GitHub to your known_hosts file (~/.ssh/known_hosts)
  - You'll see: `Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.`

  **Step 3: Verify success message**:
  - You should see:
    ```
    Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
    ```
  - **This is SUCCESS!** Despite saying "no shell access", it confirms authentication worked!

  **Step 4: Verify known_hosts file was created**:
  ```bash
  # Check known_hosts file exists
  ls -la ~/.ssh/known_hosts

  # View its contents (GitHub's host key)
  cat ~/.ssh/known_hosts

  # Should show github.com with public key
  ```

  **Step 5: Test again (should be instant now)**:
  ```bash
  # Run test again - no prompt this time!
  ssh -T git@github.com

  # Should immediately show:
  # Hi YOUR_USERNAME! You've successfully authenticated...
  ```

  **Step 6: Configure Git to use SSH**:
  ```bash
  # Check current remote URL (if in a repo)
  cd ~/  # Not in a repo yet, this is just for future reference

  # When you clone a repo, use SSH URL format:
  # git clone git@github.com:username/repo.git
  # Instead of: https://github.com/username/repo.git
  ```

  **Expected Outcome**:
  - ✅ SSH connection to GitHub successful
  - ✅ GitHub recognizes your username
  - ✅ "Successfully authenticated" message appears
  - ✅ known_hosts file created with GitHub's host key
  - ✅ Subsequent SSH tests work instantly (no prompt)
  - ✅ Ready to use Git with SSH URLs

  **Common Issues & Solutions**:
  - **"Permission denied (publickey)"**:
    - **Most common issue**: SSH key not added to GitHub
    - Verify key exists: `ls -la ~/.ssh/id_ed25519.pub`
    - Re-check Task 0.13 - make sure you uploaded public key to GitHub
    - Verify key is in ssh-agent: `ssh-add -l`
    - If not listed, add it: `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519`

  - **"ssh: connect to host github.com port 22: Connection refused"**:
    - Firewall or network blocking SSH (port 22)
    - Try GitHub's HTTPS port for SSH: `ssh -T -p 443 git@ssh.github.com`
    - If this works, configure permanently in ~/.ssh/config

  - **"Could not resolve hostname github.com"**:
    - DNS issue
    - Test internet: `ping github.com`
    - Check /etc/resolv.conf for nameservers

  - **"Host key verification failed"**:
    - known_hosts file corrupted or GitHub's key changed
    - Remove old entry: `ssh-keygen -R github.com`
    - Try again and accept new key

  - **Stuck at "connecting..." or hangs**:
    - Network timeout
    - Press Ctrl+C to cancel
    - Check firewall settings
    - Try with verbose output: `ssh -Tv git@github.com`

  - **"Are you sure you want to continue?" - typed 'yes' but still fails**:
    - You typed "y" instead of "yes"
    - Must type full word: "yes"
    - Run command again

  - **Want to verify which SSH key is being used?**:
    ```bash
    ssh -Tv git@github.com 2>&1 | grep "Offering public key"
    # Shows path to key being offered
    ```

  - **Want to test with specific key?**:
    ```bash
    ssh -T -i ~/.ssh/id_ed25519 git@github.com
    ```

  💡 **Learning moment - What is SSH doing?**:
  When you run `ssh -T git@github.com`, here's what happens:
  1. **SSH connects** to github.com on port 22
  2. **Host verification**: Check if github.com is in known_hosts
  3. **Key exchange**: GitHub sends its public key, you send yours
  4. **Authentication**: GitHub challenges you to prove you have the private key
  5. **Success**: GitHub responds with your username

  The `-T` flag tells SSH "don't allocate a terminal" because we're just testing, not getting a shell.

  💡 **Learning moment - Why "no shell access"?**:
  GitHub's message says "does not provide shell access" because:
  - You CAN'T run commands on GitHub's servers (for security!)
  - SSH is ONLY for Git operations (clone, push, pull, fetch)
  - GitHub isn't giving you a Linux shell to hack around in

  If authentication failed, you'd see "Permission denied" instead of this message. So this "no shell access" message is actually **good news** - it means auth worked!

  💡 **Learning moment - known_hosts file**:
  The `~/.ssh/known_hosts` file stores fingerprints of servers you've connected to. This protects against **man-in-the-middle attacks**:
  - First connection: SSH asks you to verify the fingerprint
  - Subsequent connections: SSH checks if fingerprint matches
  - If fingerprint changes: SSH warns you (might be an attack!)

  You can verify GitHub's current fingerprints at: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints

  💡 **Real-world tip - SSH verbose mode**:
  If SSH connection fails, use verbose mode to debug:
  ```bash
  ssh -Tvvv git@github.com
  # -v = verbose, -vv = very verbose, -vvv = extremely verbose
  # Shows every step: key loading, connection, authentication, etc.
  ```

  This is incredibly useful for troubleshooting SSH issues in production!

- **Labels**: setup, ssh, github, testing, authentication, phase-0
- **Estimated Effort**: Small (5-10 mins)
- **Status**: Backlog
- **Dependencies**: Task 0.13

---

**✅ Checkpoint #3**: Full Development Environment Ready
**Progress**: [██████████████░░] 94% through Phase 0
**Time elapsed**: ~4-6 hours
**What you have**: Complete dev environment - WSL, Git, GitHub (with tracking!), VS Code with Remote-WSL, and SSH authentication!
**Next**: Final verification and celebration!

---

### Task 0.15: Test Complete Development Environment
- **Description**: Perform comprehensive end-to-end testing of your entire development environment to verify everything works together. This is your final checkpoint before moving to Phase 1 - let's make sure every component is ready!

  **Part A: Test Windows Environment**

  **Step 1: Test WSL** (Windows PowerShell):
  ```powershell
  # Verify WSL is installed and running
  wsl --list --verbose

  # Expected output:
  # NAME      STATE    VERSION
  # Ubuntu    Running  2

  # Check WSL version (should be 2)
  wsl --status
  ```

  **Step 2: Test VS Code**:
  ```powershell
  # Verify VS Code version
  code --version

  # Should show version 1.x.x

  # Verify extensions
  code --list-extensions
  # Should include: ms-vscode-remote.remote-wsl
  ```

  **Step 3: Test GitHub CLI on Windows**:
  ```powershell
  # Verify gh installed
  gh --version

  # Verify authenticated
  gh auth status

  # Should show: ✓ Logged in to github.com as YOUR_USERNAME
  ```

  **Part B: Test WSL/Linux Environment**

  **Step 4: Launch WSL and test Git** (WSL Ubuntu):
  ```bash
  # Launch WSL
  # (From PowerShell: wsl)

  # Verify you're in WSL
  uname -a
  # Should show Linux kernel info

  # Test Git version
  git --version

  # Verify Git configuration
  git config user.name
  git config user.email
  # Should show your configured name and email
  ```

  **Step 5: Test SSH to GitHub**:
  ```bash
  # Test SSH connection
  ssh -T git@github.com

  # Should show: Hi YOUR_USERNAME! You've successfully authenticated...
  ```

  **Part C: Test VS Code + WSL Integration**

  **Step 6: Create test workspace in WSL**:
  ```bash
  # Create test directory
  mkdir -p ~/test-env-verification
  cd ~/test-env-verification

  # Create test files
  echo "# Test Environment" > README.md
  echo "console.log('Hello from WSL!');" > test.js
  echo "#!/bin/bash" > test.sh
  echo "echo 'WSL Test Script'" >> test.sh
  chmod +x test.sh

  # Verify files created
  ls -la
  ```

  **Step 7: Open in VS Code from WSL**:
  ```bash
  # Open current directory in VS Code
  code .

  # VS Code should open with:
  # - Green "WSL: Ubuntu" indicator in bottom-left
  # - Files visible in Explorer sidebar
  # - README.md, test.js, test.sh shown
  ```

  **Step 8: Test integrated terminal in VS Code**:
  In VS Code (while connected to WSL):
  1. Press **Ctrl+`** (backtick) to open terminal
  2. Terminal should be bash (not PowerShell)
  3. Run: `pwd` - should show `/home/yourusername/test-env-verification`
  4. Run: `./test.sh` - should output "WSL Test Script"
  5. Run: `node test.js` - should output "Hello from WSL!" (if node installed, otherwise skip)

  **Step 9: Test file editing in VS Code**:
  1. Open README.md in VS Code
  2. Add a new line: `## Environment Verification Successful!`
  3. Save file (Ctrl+S)
  4. In terminal, run: `cat README.md`
  5. Should show the new line you added

  **Step 10: Clean up test environment**:
  ```bash
  # Exit VS Code (Ctrl+Q or close window)

  # Remove test directory
  cd ~
  rm -rf ~/test-env-verification

  # Verify removed
  ls -la ~/ | grep test-env-verification
  # Should show nothing
  ```

  **Part D: Test GitHub Project Tracking**

  **Step 11: Test GitHub repository** (Windows PowerShell):
  ```powershell
  # Navigate to your project
  cd C:\training\jamtrack-radio

  # Verify Git repo
  git status

  # Verify remote
  git remote -v
  # Should show your GitHub repository

  # Test GitHub CLI with your repo
  gh repo view

  # Should show your jamtrack-radio repository info
  ```

  **Step 12: Test GitHub issues**:
  ```powershell
  # List Phase 0 milestone issues
  gh issue list --milestone 1

  # Should show 6 issues (Tasks 0.10-0.15) if you created them in Task 0.9

  # List all issues
  gh issue list
  ```

  **Step 13: Test GitHub project board**:
  ```powershell
  # List your projects
  gh project list --owner @me

  # Should show "Jamtrack Radio Development"

  # View project URL
  gh project list --owner @me

  # You can manually open the URL in browser to see your project board
  ```

  **Part E: Final Integration Test**

  **Step 14: Test complete Git workflow** (Windows PowerShell):
  ```powershell
  # In your jamtrack-radio directory
  cd C:\training\jamtrack-radio

  # Create a test file
  echo "# Phase 0 Complete!" > phase0-complete.md

  # Check status
  git status
  # Should show phase0-complete.md as untracked

  # Stage file
  git add phase0-complete.md

  # Commit
  git commit -m "Test: Verify complete development environment"

  # Push to GitHub
  git push origin main

  # Verify push succeeded
  git log --oneline -n 1
  # Should show your commit

  # View on GitHub
  gh repo view --web
  # Browser opens to your repo - you should see the new file!

  # Clean up test file
  git rm phase0-complete.md
  git commit -m "Test: Remove verification test file"
  git push origin main
  ```

  **Expected Outcome - Master Checklist**:

  **Windows Environment:**
  - ✅ WSL 2 running with Ubuntu
  - ✅ VS Code installed and accessible via `code` command
  - ✅ GitHub CLI authenticated
  - ✅ Windows Terminal available

  **WSL/Linux Environment:**
  - ✅ Git installed and configured (name/email set)
  - ✅ SSH key generated and working
  - ✅ SSH authentication to GitHub successful
  - ✅ Can run Linux commands (bash, ls, cat, etc.)

  **VS Code Integration:**
  - ✅ Remote-WSL extension installed
  - ✅ Can open WSL folders in VS Code
  - ✅ "WSL: Ubuntu" indicator shows in VS Code
  - ✅ Integrated terminal runs bash from WSL
  - ✅ Can edit files in WSL from VS Code
  - ✅ Files saved in VS Code appear in WSL

  **GitHub Integration:**
  - ✅ Repository created and accessible
  - ✅ Can push/pull to GitHub
  - ✅ GitHub CLI works with repository
  - ✅ Issues created and visible
  - ✅ Project board set up
  - ✅ Milestones created

  **Complete Workflow:**
  - ✅ Can create files in WSL
  - ✅ Can edit in VS Code (connected to WSL)
  - ✅ Can commit with Git
  - ✅ Can push to GitHub
  - ✅ Can view changes on GitHub
  - ✅ Can track work via GitHub issues/projects

  **Common Issues & Solutions**:
  - **Any command fails**:
    - Review the specific task where that component was set up
    - Re-run the installation/configuration steps
    - Check the "Common Issues" section of that task

  - **VS Code doesn't show "WSL: Ubuntu"**:
    - Restart VS Code
    - In WSL, run: `code .` again
    - Check Remote-WSL extension is enabled

  - **Git push fails**:
    - Check authentication: `gh auth status`
    - Verify remote: `git remote -v`
    - Check SSH: `ssh -T git@github.com`

  - **Can't find test files created in WSL**:
    - Windows path: `\\wsl$\Ubuntu\home\yourusername\`
    - Or in File Explorer: Type `\\wsl$` in address bar

  - **Something still not working?**:
    - Document which step failed
    - Go back to that specific task (0.1-0.14)
    - Re-read instructions and troubleshooting
    - Verify each prerequisite

  💡 **Learning moment - Why this comprehensive test?**:
  This test verifies **integration** between all components:
  - Windows ↔ WSL communication
  - VS Code ↔ WSL connection
  - WSL ↔ GitHub authentication
  - Local Git ↔ Remote GitHub
  - GitHub CLI ↔ GitHub API

  In real projects, this is called **integration testing** - making sure components work together, not just individually. You've built a complex system and now verified it works end-to-end!

  💡 **Learning moment - Development environment as infrastructure**:
  What you've built is essentially **infrastructure** for development:
  - **Compute**: WSL provides Linux environment
  - **Storage**: File systems (Windows + Linux)
  - **Networking**: SSH to GitHub, HTTPS for gh CLI
  - **Tools**: Git, VS Code, GitHub CLI
  - **Project Management**: Issues, milestones, project board

  This is **Infrastructure as Code** thinking applied to your dev machine!

  💡 **Celebrate!** 🎉
  You've completed Phase 0! You now have:
  - A professional development environment
  - Git and GitHub expertise
  - VS Code with remote development
  - Project tracking system
  - Skills that professional developers use daily

  **This is exactly how modern software teams work!**

  You're ready to start building the Jamtrack Radio application in Phase 1!

- **Labels**: setup, testing, verification, integration-testing, phase-0
- **Estimated Effort**: Medium (30-40 mins for comprehensive testing)
- **Status**: Backlog
- **Dependencies**: Tasks 0.11 AND 0.14

---

## Phase 1: Project Documentation
**Phase Description**: Create comprehensive project documentation including expanded README, contribution guidelines, issue/PR templates, and a simple GitHub Actions workflow to learn CI/CD basics. The GitHub repo and project tracking are already set up in Phase 0!

**Priority**: Medium

**Labels**: phase-1, documentation

### Task 1.1: Create Issue and Pull Request Templates
- **Description**: Create GitHub issue templates for bugs and features, plus a pull request template to establish good contribution practices.

  **Step 1: Create directory structure** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio
  mkdir .github\ISSUE_TEMPLATE -Force
  ```

  **Step 2: Create Bug Report Template**

  File: `.github/ISSUE_TEMPLATE/bug_report.md`
  ```markdown
  ---
  name: Bug Report
  about: Create a report to help us improve
  title: '[BUG] '
  labels: bug
  assignees: ''
  ---

  ## Bug Description
  A clear and concise description of what the bug is.

  ## Steps To Reproduce
  1. Go to '...'
  2. Click on '...'
  3. See error

  ## Expected Behavior
  A clear description of what you expected to happen.

  ## Actual Behavior
  What actually happened.

  ## Environment
  - OS: [e.g., Windows 11, WSL Ubuntu 22.04]
  - .NET Version: [e.g., 8.0]
  - Docker Version: [if applicable]

  ## Additional Context
  Add any other context about the problem here.
  ```

  **Step 3: Create Feature Request Template**

  File: `.github/ISSUE_TEMPLATE/feature_request.md`
  ```markdown
  ---
  name: Feature Request
  about: Suggest an idea for this project
  title: '[FEATURE] '
  labels: enhancement
  assignees: ''
  ---

  ## Feature Description
  A clear and concise description of the feature you'd like to see.

  ## Problem Statement
  What problem does this feature solve? Why is it needed?

  ## Proposed Solution
  Describe how you envision this feature working.

  ## Alternatives Considered
  Describe any alternative solutions or features you've considered.

  ## Additional Context
  Add any other context or screenshots about the feature request here.
  ```

  **Step 4: Create Pull Request Template**

  File: `.github/PULL_REQUEST_TEMPLATE.md`
  ```markdown
  ## Description
  Brief description of what this PR does.

  ## Related Issue
  Fixes #(issue number)

  ## Type of Change
  - [ ] Bug fix (non-breaking change which fixes an issue)
  - [ ] New feature (non-breaking change which adds functionality)
  - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
  - [ ] Documentation update

  ## Testing Checklist
  - [ ] I have tested this code locally
  - [ ] I have added/updated unit tests
  - [ ] All tests pass locally
  - [ ] I have updated documentation (if needed)

  ## Screenshots (if applicable)
  Add screenshots to help explain your changes.
  ```

  **Step 5: Commit and push**:
  ```powershell
  git add .github/
  git commit -m "Add issue and PR templates"
  git push
  ```

  **Expected Outcome**:
  - `.github/ISSUE_TEMPLATE/` directory contains bug_report.md and feature_request.md
  - `.github/PULL_REQUEST_TEMPLATE.md` exists
  - When creating a new issue on GitHub, you see template options
  - When creating a PR on GitHub, the template auto-populates

  💡 **Can I do this in parallel?** Yes! Tasks 1.1, 1.2, and 1.3 can be done in any order or simultaneously.
- **Labels**: github, templates, documentation, phase-1
- **Estimated Effort**: Medium (30-45 mins)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.15)

### Task 1.2: Expand README.md
- **Description**: Expand the basic README created in Phase 0 with more project information.

  **Commands** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio
  code README.md
  ```

  **Expand with these sections**:

  ```markdown
  # Jamtrack Radio

  A music streaming application built for learning modern software development practices.

  ## 🎯 Project Overview
  This project is a hands-on learning journey covering:
  - Backend development with C# and ASP.NET Core
  - Database management with PostgreSQL
  - Containerization with Docker
  - Orchestration with Kubernetes & Helm
  - Cloud deployment (Azure & AWS)
  - CI/CD with GitHub Actions
  - Infrastructure as Code with Terraform
  - Monitoring with ELK stack

  ## 🛠️ Tech Stack
  - **Backend**: C# (.NET 8), ASP.NET Core, gRPC
  - **Database**: PostgreSQL
  - **Containerization**: Docker, Docker Compose
  - **Orchestration**: Kubernetes, Helm
  - **CI/CD**: GitHub Actions
  - **Infrastructure**: Terraform
  - **Monitoring**: ELK Stack (Elasticsearch, Logstash, Kibana)
  - **Cloud**: Azure (AKS), AWS (EKS)

  ## 📋 Prerequisites
  - Windows 11 with WSL 2 (Ubuntu)
  - .NET 8 SDK
  - Docker Desktop
  - Git
  - GitHub account
  - VS Code with Remote-WSL extension

  ## 📊 Project Status
  🚧 **Under Active Development**

  Current Phase: [Phase name here]

  [Link to GitHub Project Board](https://github.com/users/YOUR_USERNAME/projects/PROJECT_NUMBER)

  ## 🤝 Contributing
  See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

  ## 📄 License
  This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
  ```

  **Note**: Update the project board link with your actual GitHub username and project number.

  **Expected Outcome**:
  - README has all sections filled in
  - Tech stack clearly documented
  - Link to project board works
  - Professional appearance for potential contributors

  💡 **Can I do this in parallel?** Yes! Tasks 1.1, 1.2, and 1.3 can be done in any order or simultaneously.
- **Labels**: documentation, readme, phase-1
- **Estimated Effort**: Small (20-30 mins)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.15)

### Task 1.3: Create CONTRIBUTING.md and LICENSE
- **Description**: Create CONTRIBUTING.md with guidelines for contributors, and add MIT LICENSE file.

  **Step 1: Create LICENSE** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio

  # Create LICENSE using gh CLI
  gh api -X GET /licenses/mit | ConvertFrom-Json | Select-Object -ExpandProperty body | Out-File -FilePath LICENSE -Encoding UTF8
  ```

  **Step 2: Create CONTRIBUTING.md**:

  File: `CONTRIBUTING.md`
  ```markdown
  # Contributing to Jamtrack Radio

  Thank you for your interest in contributing! This project is a learning journey, and contributions are welcome.

  ## 🐛 Reporting Bugs

  Found a bug? Please create an issue using our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md).

  Make sure to include:
  - Clear description of the issue
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, .NET version, etc.)

  ## 💡 Suggesting Features

  Have an idea? Create an issue using our [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md).

  ## 🔧 Development Workflow

  1. **Fork the repository**
  2. **Clone your fork**:
     ```bash
     git clone https://github.com/YOUR_USERNAME/jamtrack-radio.git
     cd jamtrack-radio
     ```
  3. **Create a feature branch**:
     ```bash
     git checkout -b feature/your-feature-name
     ```
  4. **Make your changes** and commit:
     ```bash
     git add .
     git commit -m "Description of your changes"
     ```
  5. **Push to your fork**:
     ```bash
     git push origin feature/your-feature-name
     ```
  6. **Open a Pull Request** on GitHub

  ## 📝 Pull Request Process

  1. Ensure your code follows the project's coding standards
  2. Update documentation if you're changing functionality
  3. Add or update tests as needed
  4. Ensure all tests pass locally
  5. Fill out the PR template completely
  6. Link related issues in your PR description

  ## 🎨 Coding Standards

  - **C#**: Follow Microsoft's C# coding conventions
  - **Naming**: Use descriptive names for variables, methods, and classes
  - **Comments**: Add comments for complex logic
  - **Testing**: Write unit tests for new features

  ## ❓ Questions?

  Feel free to open an issue with your question or reach out via GitHub Discussions.

  ## 📄 Code of Conduct

  Be respectful, inclusive, and constructive in all interactions.
  ```

  **Step 3: Commit and push**:
  ```powershell
  git add CONTRIBUTING.md LICENSE
  git commit -m "Add CONTRIBUTING.md and LICENSE"
  git push
  ```

  **Expected Outcome**:
  - `LICENSE` file exists with MIT license text
  - `CONTRIBUTING.md` exists with clear contribution guidelines
  - Both files visible in repository root on GitHub

  💡 **Can I do this in parallel?** Yes! Tasks 1.1, 1.2, and 1.3 can be done in any order or simultaneously.
- **Labels**: documentation, contributing, license, phase-1
- **Estimated Effort**: Small (15-25 mins)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.15)

### Task 1.4: Create Hello World GitHub Action
- **Description**: Create a simple "Hello World" GitHub Actions workflow to get familiar with CI/CD early, before diving into complex pipelines in Phase 5.

  **Commands** (Windows PowerShell):
  ```powershell
  cd C:\training\jamtrack-radio
  mkdir .github\workflows -Force
  code .github\workflows\hello.yml
  ```

  **Create .github/workflows/hello.yml**:
  ```yaml
  name: Hello World

  on:
    push:
      branches: [ main ]
    pull_request:
      branches: [ main ]

  jobs:
    greet:
      runs-on: ubuntu-latest
      steps:
        - name: Checkout code
          uses: actions/checkout@v4

        - name: Say hello
          run: |
            echo "Hello from Jamtrack Radio!"
            echo "Triggered by: ${{ github.event_name }}"
            echo "Branch: ${{ github.ref }}"
  ```

  **Commit and push**:
  ```powershell
  git add .github/workflows/
  git commit -m "Add Hello World GitHub Action"
  git push
  ```

  **Verify the workflow runs**:
  1. Go to your repository on GitHub
  2. Click the "Actions" tab
  3. You should see "Hello World" workflow running or completed
  4. Click on the workflow run to see output

  **Expected Outcome**:
  - Workflow file exists at `.github/workflows/hello.yml`
  - Workflow appears in Actions tab on GitHub
  - Workflow runs successfully (green checkmark)
  - Output shows "Hello from Jamtrack Radio!" message

  **Common Issues & Solutions**:
  - **Workflow doesn't appear**: Wait 1-2 minutes for GitHub to detect the new workflow
  - **Workflow fails with "actions/checkout@v4 not found"**: Ensure you have internet connection; GitHub needs to download the action
  - **YAML syntax error**: Check indentation (use spaces, not tabs) and ensure colons have spaces after them
  - **Workflow doesn't trigger**: Ensure you pushed to the `main` branch
  - **To manually trigger**: Go to Actions tab → Click workflow → "Run workflow" button

  💡 **Learning moment**: You've just created your first CI/CD pipeline! This is the foundation for automated testing and deployment in Phase 5.
- **Labels**: github-actions, ci-cd, learning, phase-1
- **Estimated Effort**: Small (15-20 mins)
- **Status**: Backlog
- **Dependencies**: Tasks 1.1, 1.2, AND 1.3

---

**✅ Phase 1 Complete!** 🎉

**Progress**: [████████████████] 100% through Phase 1
**Time elapsed**: ~1.5-2.5 hours
**What you've accomplished**:
- ✅ Professional issue and PR templates
- ✅ Comprehensive README with tech stack
- ✅ CONTRIBUTING.md and LICENSE for open source
- ✅ First GitHub Actions workflow (CI/CD basics!)

**Achievement unlocked**: 📚 **Documentation Master** - Your project now looks professional and welcoming to contributors!

**Next**: Phase 2A - Build your first working C# API with Postgres!

---

## Phase 2A: Basic Backend Development (Local)
**Phase Description**: Build a **minimal working backend** with ASP.NET Core, Postgres database, and basic REST API. Focus on getting a simple API running quickly without complex patterns. You'll add advanced patterns in Phase 2B.

**Priority**: High

**Labels**: phase-2a, backend, csharp, database

**Goal**: Get to a working API with basic CRUD operations ASAP to build confidence and momentum!

### Task 2.1: Install .NET SDK in WSL
- **Description**: Install .NET 8 SDK in WSL Ubuntu for C# development.

  **Commands (WSL Ubuntu)**:
  ```bash
  wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
  sudo dpkg -i packages-microsoft-prod.deb
  rm packages-microsoft-prod.deb
  sudo apt update
  sudo apt install -y dotnet-sdk-8.0
  dotnet --version
  ```

  **Expected Outcome**: Running `dotnet --version` shows `8.0.xxx`

  **Common Issues & Solutions**:
  - **"Package 'dotnet-sdk-8.0' has no installation candidate"**: Run `sudo apt update` again and ensure the Microsoft repository was added correctly
  - **404 errors during wget**: Your Ubuntu version might not be supported. Check [Microsoft's .NET install guide](https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu)
  - **Permission denied errors**: Ensure you're using `sudo` for installation commands
  - **Old .NET version showing**: Run `sudo apt remove dotnet*` then reinstall

  💡 **Can I do this in parallel?** Yes! Tasks 2.1 and 2.2 are independent and can be done simultaneously.
- **Labels**: setup, dotnet, csharp, wsl, phase-2a
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.2)

### Task 2.2: Install Postgres in WSL
- **Description**: Install PostgreSQL database server in WSL Ubuntu for local development.

  **Commands (WSL Ubuntu)**:
  ```bash
  sudo apt install -y postgresql postgresql-contrib
  sudo service postgresql start
  sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"

  # Verify installation
  sudo service postgresql status
  sudo -u postgres psql -c "SELECT version();"
  ```

  **Expected Outcome**:
  - PostgreSQL service is running
  - `SELECT version();` shows PostgreSQL 14.x or higher
  - Postgres user password is set to 'postgres'

  **Common Issues & Solutions**:
  - **"Service postgresql not found"**: Installation may have failed. Run `sudo apt install postgresql postgresql-contrib` again
  - **"Could not connect to database"**: Start the service with `sudo service postgresql start`
  - **Service stops after WSL restart**: WSL doesn't auto-start services. Create a startup script or start manually each session
  - **Password change fails**: Run `sudo service postgresql restart` and try again

  💡 **Can I do this in parallel?** Yes! Tasks 2.1 and 2.2 are independent and can be done simultaneously.
- **Labels**: setup, database, postgres, wsl, phase-2a
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.2)

### Task 2.3: Create Simple Solution and Project Structure
- **Description**: Create a **simple .NET solution** with just API and Domain projects to start. Keep it minimal - you'll add Infrastructure and gRPC projects in Phase 2B.

  **Commands (WSL Ubuntu)**:
  ```bash
  # Create project directory structure
  mkdir -p ~/projects/jamtrack-radio
  cd ~/projects/jamtrack-radio

  # Create solution and projects
  dotnet new sln -n JamtrackRadio
  dotnet new webapi -n JamtrackRadio.Api -o src/JamtrackRadio.Api
  dotnet new classlib -n JamtrackRadio.Domain -o src/JamtrackRadio.Domain

  # Add projects to solution
  dotnet sln add src/JamtrackRadio.Api/JamtrackRadio.Api.csproj
  dotnet sln add src/JamtrackRadio.Domain/JamtrackRadio.Domain.csproj

  # Add reference from Api to Domain
  dotnet add src/JamtrackRadio.Api/JamtrackRadio.Api.csproj reference src/JamtrackRadio.Domain/JamtrackRadio.Domain.csproj

  # Verify structure
  dotnet sln list
  ```

  **Expected Outcome**:
  - Directory structure: `~/projects/jamtrack-radio/src/{Api, Domain}`
  - Solution file: `JamtrackRadio.sln`
  - `dotnet sln list` shows both projects
  - Projects build successfully: `dotnet build`

  **Project Structure**:
  ```
  jamtrack-radio/
  ├── JamtrackRadio.sln
  └── src/
      ├── JamtrackRadio.Api/          # REST API project
      │   ├── Controllers/
      │   ├── Program.cs
      │   └── JamtrackRadio.Api.csproj
      └── JamtrackRadio.Domain/       # Domain models
          └── JamtrackRadio.Domain.csproj
  ```

  **Common Issues & Solutions**:
  - **"src/**/*.csproj" not working**: Use explicit paths as shown above instead of wildcard
  - **Reference not added**: Use full .csproj paths, not just project names
  - **Permission denied**: Ensure you have write permissions in ~/projects/
  - **"Solution already exists"**: Delete `JamtrackRadio.sln` and try again

  **Note**: We're keeping it simple! No separate Infrastructure or gRPC projects yet. DbContext will live in the API project for now.
- **Labels**: backend, csharp, project-structure, phase-2a
- **Estimated Effort**: Small (15-20 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.1

### Task 2.4: Design and Implement Domain Models
- **Description**: Create domain entities for Track, Playlist, User, and related models with proper relationships.

  **Create the following model files in `src/JamtrackRadio.Domain/Entities/`**:

  **File: `Track.cs`**
  ```csharp
  namespace JamtrackRadio.Domain.Entities;

  public class Track
  {
      public Guid Id { get; set; }
      public string Title { get; set; } = string.Empty;
      public string Artist { get; set; } = string.Empty;
      public string? Album { get; set; }
      public int DurationSeconds { get; set; }
      public string? FilePath { get; set; }
      public DateTime CreatedAt { get; set; }

      // Navigation property
      public ICollection<PlaylistTrack> PlaylistTracks { get; set; } = new List<PlaylistTrack>();
  }
  ```

  **File: `Playlist.cs`**
  ```csharp
  namespace JamtrackRadio.Domain.Entities;

  public class Playlist
  {
      public Guid Id { get; set; }
      public string Name { get; set; } = string.Empty;
      public string? Description { get; set; }
      public Guid CreatedBy { get; set; }
      public DateTime CreatedAt { get; set; }
      public DateTime UpdatedAt { get; set; }

      // Navigation properties
      public User User { get; set; } = null!;
      public ICollection<PlaylistTrack> PlaylistTracks { get; set; } = new List<PlaylistTrack>();
  }
  ```

  **File: `PlaylistTrack.cs`** (Many-to-many junction)
  ```csharp
  namespace JamtrackRadio.Domain.Entities;

  public class PlaylistTrack
  {
      public Guid PlaylistId { get; set; }
      public Guid TrackId { get; set; }
      public int Order { get; set; }
      public DateTime AddedAt { get; set; }

      // Navigation properties
      public Playlist Playlist { get; set; } = null!;
      public Track Track { get; set; } = null!;
  }
  ```

  **File: `User.cs`**
  ```csharp
  namespace JamtrackRadio.Domain.Entities;

  public class User
  {
      public Guid Id { get; set; }
      public string Username { get; set; } = string.Empty;
      public string Email { get; set; } = string.Empty;
      public DateTime CreatedAt { get; set; }

      // Navigation property
      public ICollection<Playlist> Playlists { get; set; } = new List<Playlist>();
  }
  ```

  **Expected Outcome**:
  - Four model files created in `src/JamtrackRadio.Domain/Entities/`
  - Solution builds successfully: `dotnet build`
  - Models have proper relationships defined

  **Common Issues & Solutions**:
  - **Nullable reference warnings**: Add `#nullable disable` at top of file if you prefer, or keep nullable annotations
  - **"Entities namespace not found"**: Ensure you created the Entities folder
  - **Build warnings about navigation properties**: These are expected - EF Core will configure them

  💡 **Learning moment**: Notice the many-to-many relationship between Playlist and Track using the junction table PlaylistTrack. This allows tracks to be in multiple playlists and playlists to contain multiple tracks.
- **Labels**: backend, csharp, domain-model, phase-2a
- **Estimated Effort**: Medium (30-40 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.3

### Task 2.5: Set Up Dapper with Postgres and Stored Procedures
- **Description**: Install Dapper packages, create database schema initialization scripts, create stored procedures for all CRUD operations, and configure Dapper for database access.

  **Step 1: Install Dapper packages**:
  ```bash
  cd ~/projects/jamtrack-radio/src/JamtrackRadio.Api
  dotnet add package Dapper
  dotnet add package Npgsql
  ```

  **Step 2: Create database connection factory**

  File: `Data/IDbConnectionFactory.cs`
  ```csharp
  using System.Data;

  namespace JamtrackRadio.Api.Data;

  public interface IDbConnectionFactory
  {
      IDbConnection CreateConnection();
  }
  ```

  File: `Data/DbConnectionFactory.cs`
  ```csharp
  using Npgsql;
  using System.Data;

  namespace JamtrackRadio.Api.Data;

  public class DbConnectionFactory : IDbConnectionFactory
  {
      private readonly string _connectionString;

      public DbConnectionFactory(string connectionString)
      {
          _connectionString = connectionString;
      }

      public IDbConnection CreateConnection()
      {
          return new NpgsqlConnection(_connectionString);
      }
  }
  ```

  **Step 3: Create database initialization SQL script**

  Create directory and file:
  ```bash
  mkdir -p ~/projects/jamtrack-radio/src/JamtrackRadio.Api/Data/Scripts
  ```

  File: `Data/Scripts/001_InitialSchema.sql`
  ```sql
  -- ================================
  -- Drop existing objects if they exist
  -- ================================
  DROP TABLE IF EXISTS "PlaylistTracks" CASCADE;
  DROP TABLE IF EXISTS "Playlists" CASCADE;
  DROP TABLE IF EXISTS "Tracks" CASCADE;
  DROP TABLE IF EXISTS "Users" CASCADE;

  -- ================================
  -- Create Tables
  -- ================================

  -- Users table
  CREATE TABLE "Users" (
      "Id" UUID PRIMARY KEY,
      "Username" VARCHAR(100) NOT NULL UNIQUE,
      "Email" VARCHAR(200) NOT NULL UNIQUE,
      "CreatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX "IX_Users_Username" ON "Users"("Username");
  CREATE INDEX "IX_Users_Email" ON "Users"("Email");

  -- Tracks table
  CREATE TABLE "Tracks" (
      "Id" UUID PRIMARY KEY,
      "Title" VARCHAR(200) NOT NULL,
      "Artist" VARCHAR(200) NOT NULL,
      "Album" VARCHAR(200),
      "DurationSeconds" INTEGER NOT NULL,
      "FilePath" VARCHAR(500),
      "CreatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  );

  CREATE INDEX "IX_Tracks_Artist" ON "Tracks"("Artist");
  CREATE INDEX "IX_Tracks_Title" ON "Tracks"("Title");

  -- Playlists table
  CREATE TABLE "Playlists" (
      "Id" UUID PRIMARY KEY,
      "Name" VARCHAR(200) NOT NULL,
      "Description" TEXT,
      "CreatedBy" UUID NOT NULL,
      "CreatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      "UpdatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY ("CreatedBy") REFERENCES "Users"("Id") ON DELETE CASCADE
  );

  CREATE INDEX "IX_Playlists_CreatedBy" ON "Playlists"("CreatedBy");

  -- PlaylistTracks junction table (many-to-many)
  CREATE TABLE "PlaylistTracks" (
      "PlaylistId" UUID NOT NULL,
      "TrackId" UUID NOT NULL,
      "Order" INTEGER NOT NULL,
      "AddedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY ("PlaylistId", "TrackId"),
      FOREIGN KEY ("PlaylistId") REFERENCES "Playlists"("Id") ON DELETE CASCADE,
      FOREIGN KEY ("TrackId") REFERENCES "Tracks"("Id") ON DELETE CASCADE
  );

  CREATE INDEX "IX_PlaylistTracks_PlaylistId" ON "PlaylistTracks"("PlaylistId");
  CREATE INDEX "IX_PlaylistTracks_TrackId" ON "PlaylistTracks"("TrackId");
  ```

  **Step 4: Create stored procedures for Track CRUD operations**

  File: `Data/Scripts/002_TrackStoredProcedures.sql`
  ```sql
  -- ================================
  -- Track Stored Procedures
  -- ================================

  -- Get all tracks
  CREATE OR REPLACE FUNCTION sp_get_all_tracks()
  RETURNS TABLE (
      "Id" UUID,
      "Title" VARCHAR,
      "Artist" VARCHAR,
      "Album" VARCHAR,
      "DurationSeconds" INTEGER,
      "FilePath" VARCHAR,
      "CreatedAt" TIMESTAMP
  ) AS $$
  BEGIN
      RETURN QUERY
      SELECT t."Id", t."Title", t."Artist", t."Album", t."DurationSeconds", t."FilePath", t."CreatedAt"
      FROM "Tracks" t
      ORDER BY t."Artist", t."Title";
  END;
  $$ LANGUAGE plpgsql;

  -- Get track by ID
  CREATE OR REPLACE FUNCTION sp_get_track_by_id(p_id UUID)
  RETURNS TABLE (
      "Id" UUID,
      "Title" VARCHAR,
      "Artist" VARCHAR,
      "Album" VARCHAR,
      "DurationSeconds" INTEGER,
      "FilePath" VARCHAR,
      "CreatedAt" TIMESTAMP
  ) AS $$
  BEGIN
      RETURN QUERY
      SELECT t."Id", t."Title", t."Artist", t."Album", t."DurationSeconds", t."FilePath", t."CreatedAt"
      FROM "Tracks" t
      WHERE t."Id" = p_id;
  END;
  $$ LANGUAGE plpgsql;

  -- Search tracks by title, artist, or album
  CREATE OR REPLACE FUNCTION sp_search_tracks(p_search_term VARCHAR)
  RETURNS TABLE (
      "Id" UUID,
      "Title" VARCHAR,
      "Artist" VARCHAR,
      "Album" VARCHAR,
      "DurationSeconds" INTEGER,
      "FilePath" VARCHAR,
      "CreatedAt" TIMESTAMP
  ) AS $$
  BEGIN
      RETURN QUERY
      SELECT t."Id", t."Title", t."Artist", t."Album", t."DurationSeconds", t."FilePath", t."CreatedAt"
      FROM "Tracks" t
      WHERE LOWER(t."Title") LIKE '%' || LOWER(p_search_term) || '%'
         OR LOWER(t."Artist") LIKE '%' || LOWER(p_search_term) || '%'
         OR LOWER(COALESCE(t."Album", '')) LIKE '%' || LOWER(p_search_term) || '%'
      ORDER BY t."Artist", t."Title";
  END;
  $$ LANGUAGE plpgsql;

  -- Create new track
  CREATE OR REPLACE FUNCTION sp_create_track(
      p_id UUID,
      p_title VARCHAR,
      p_artist VARCHAR,
      p_album VARCHAR,
      p_duration_seconds INTEGER,
      p_file_path VARCHAR
  )
  RETURNS UUID AS $$
  BEGIN
      INSERT INTO "Tracks" ("Id", "Title", "Artist", "Album", "DurationSeconds", "FilePath", "CreatedAt")
      VALUES (p_id, p_title, p_artist, p_album, p_duration_seconds, p_file_path, CURRENT_TIMESTAMP);

      RETURN p_id;
  END;
  $$ LANGUAGE plpgsql;

  -- Update track
  CREATE OR REPLACE FUNCTION sp_update_track(
      p_id UUID,
      p_title VARCHAR,
      p_artist VARCHAR,
      p_album VARCHAR,
      p_duration_seconds INTEGER,
      p_file_path VARCHAR
  )
  RETURNS BOOLEAN AS $$
  DECLARE
      v_rows_affected INTEGER;
  BEGIN
      UPDATE "Tracks"
      SET "Title" = p_title,
          "Artist" = p_artist,
          "Album" = p_album,
          "DurationSeconds" = p_duration_seconds,
          "FilePath" = p_file_path
      WHERE "Id" = p_id;

      GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
      RETURN v_rows_affected > 0;
  END;
  $$ LANGUAGE plpgsql;

  -- Delete track
  CREATE OR REPLACE FUNCTION sp_delete_track(p_id UUID)
  RETURNS BOOLEAN AS $$
  DECLARE
      v_rows_affected INTEGER;
  BEGIN
      DELETE FROM "Tracks"
      WHERE "Id" = p_id;

      GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
      RETURN v_rows_affected > 0;
  END;
  $$ LANGUAGE plpgsql;
  ```

  **Step 5: Create database initializer**

  File: `Data/DatabaseInitializer.cs`
  ```csharp
  using Npgsql;
  using Dapper;

  namespace JamtrackRadio.Api.Data;

  public class DatabaseInitializer
  {
      private readonly IDbConnectionFactory _connectionFactory;
      private readonly ILogger<DatabaseInitializer> _logger;

      public DatabaseInitializer(IDbConnectionFactory connectionFactory, ILogger<DatabaseInitializer> logger)
      {
          _connectionFactory = connectionFactory;
          _logger = logger;
      }

      public async Task InitializeAsync()
      {
          try
          {
              using var connection = _connectionFactory.CreateConnection();

              // Execute schema creation
              _logger.LogInformation("Creating database schema...");
              await ExecuteSqlFileAsync(connection, "001_InitialSchema.sql");

              // Execute stored procedures
              _logger.LogInformation("Creating stored procedures...");
              await ExecuteSqlFileAsync(connection, "002_TrackStoredProcedures.sql");

              _logger.LogInformation("Database initialization completed successfully");
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error initializing database");
              throw;
          }
      }

      private async Task ExecuteSqlFileAsync(IDbConnection connection, string fileName)
      {
          var scriptPath = Path.Combine(AppContext.BaseDirectory, "Data", "Scripts", fileName);

          if (!File.Exists(scriptPath))
          {
              throw new FileNotFoundException($"SQL script not found: {scriptPath}");
          }

          var sql = await File.ReadAllTextAsync(scriptPath);
          await connection.ExecuteAsync(sql);

          _logger.LogInformation($"Executed SQL script: {fileName}");
      }
  }
  ```

  **Step 6: Configure connection string in appsettings.json**:
  ```json
  {
    "ConnectionStrings": {
      "DefaultConnection": "Host=localhost;Database=jamtrackradio;Username=postgres;Password=postgres"
    },
    "Logging": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft.AspNetCore": "Warning"
      }
    },
    "AllowedHosts": "*"
  }
  ```

  **Step 7: Register services in Program.cs**:
  ```csharp
  using JamtrackRadio.Api.Data;

  var builder = WebApplication.CreateBuilder(args);

  // Add services to the container.
  builder.Services.AddControllers();
  builder.Services.AddEndpointsApiExplorer();
  builder.Services.AddSwaggerGen();

  // Register database services
  var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")!;
  builder.Services.AddSingleton<IDbConnectionFactory>(new DbConnectionFactory(connectionString));
  builder.Services.AddScoped<DatabaseInitializer>();

  var app = builder.Build();

  // Initialize database
  using (var scope = app.Services.CreateScope())
  {
      var initializer = scope.ServiceProvider.GetRequiredService<DatabaseInitializer>();
      await initializer.InitializeAsync();
  }

  // Configure the HTTP request pipeline.
  if (app.Environment.IsDevelopment())
  {
      app.UseSwagger();
      app.UseSwaggerUI();
  }

  app.UseHttpsRedirection();
  app.UseAuthorization();
  app.MapControllers();

  app.Run();
  ```

  **Step 8: Update .csproj to include SQL scripts**

  Edit `src/JamtrackRadio.Api/JamtrackRadio.Api.csproj` and add:
  ```xml
  <ItemGroup>
    <None Update="Data\Scripts\*.sql">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </None>
  </ItemGroup>
  ```

  **Step 9: Verify database initialization**:
  ```bash
  cd ~/projects/jamtrack-radio/src/JamtrackRadio.Api

  # Build the project
  dotnet build

  # Run the application (it will create tables and stored procedures)
  dotnet run

  # In another terminal, verify tables were created
  sudo -u postgres psql -d jamtrackradio -c "\dt"

  # Verify stored procedures were created
  sudo -u postgres psql -d jamtrackradio -c "\df sp_*"
  ```

  **Expected Outcome**:
  - `Data/IDbConnectionFactory.cs` and `DbConnectionFactory.cs` created
  - SQL scripts created in `Data/Scripts/` folder
  - `DatabaseInitializer.cs` created
  - Database `jamtrackradio` created in Postgres
  - Tables created: Users, Tracks, Playlists, PlaylistTracks
  - Stored procedures created: sp_get_all_tracks, sp_get_track_by_id, sp_search_tracks, sp_create_track, sp_update_track, sp_delete_track
  - Application starts without errors
  - SQL scripts are copied to output directory

  **Common Issues & Solutions**:
  - **"Unable to connect to database"**: Ensure Postgres is running: `sudo service postgresql status`
  - **"Password authentication failed"**: Verify postgres user password was set correctly in Task 2.2
  - **"SQL script not found"**: Ensure scripts are in `Data/Scripts/` and .csproj includes them
  - **"Syntax error in SQL"**: Check Postgres version supports the syntax (need 9.3+ for `CREATE OR REPLACE FUNCTION`)
  - **"Function already exists"**: Use `CREATE OR REPLACE FUNCTION` or drop functions first
  - **"Permission denied"**: Ensure postgres user has CREATE rights on the database

  💡 **Learning moment - Dapper vs EF Core**:
  - **Dapper** is a micro-ORM. You write the SQL, Dapper just maps results to objects. Lightning fast!
  - **EF Core** is a full ORM. It generates SQL for you. Easier for complex relationships, but slower.
  - Dapper gives you full control over SQL and stored procedures, perfect for performance-critical applications.

  💡 **Learning moment - Stored procedures benefits**:
  - **Performance**: Compiled and cached in the database
  - **Security**: Prevents SQL injection, can control permissions at procedure level
  - **Maintainability**: Database logic stays in the database
  - **Reusability**: Can be called from multiple applications
  - **Transaction control**: Better control over complex transactions

  💡 **Learning moment - Postgres functions**: In Postgres, what other databases call "stored procedures" are called "functions". They can return tables, scalars, or void. `RETURNS TABLE` makes them work like SELECT statements!

- **Labels**: backend, csharp, database, dapper, stored-procedures, phase-2a
- **Estimated Effort**: Large (75-90 mins)
- **Status**: Backlog
- **Dependencies**: Tasks 2.2 AND 2.4

### Task 2.5.5: Create Sample Data Seeder
- **Description**: Create a SQL seed script and seeder class using Dapper to add sample tracks and playlists for testing. Makes manual testing much easier!

  **Step 1: Create seed data SQL script**

  File: `Data/Scripts/003_SeedData.sql`
  ```sql
  -- ================================
  -- Seed Data Script
  -- ================================

  -- Check if data already exists
  DO $$
  DECLARE
      v_user_count INTEGER;
  BEGIN
      SELECT COUNT(*) INTO v_user_count FROM "Users";

      IF v_user_count > 0 THEN
          RAISE NOTICE 'Database already seeded. Skipping...';
          RETURN;
      END IF;

      -- Insert sample user
      INSERT INTO "Users" ("Id", "Username", "Email", "CreatedAt")
      VALUES (
          'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
          'demo_user',
          'demo@jamtrackradio.com',
          CURRENT_TIMESTAMP
      );

      -- Insert sample tracks
      INSERT INTO "Tracks" ("Id", "Title", "Artist", "Album", "DurationSeconds", "FilePath", "CreatedAt")
      VALUES
          (
              'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Bohemian Rhapsody',
              'Queen',
              'A Night at the Opera',
              354,
              '/music/queen/bohemian-rhapsody.mp3',
              CURRENT_TIMESTAMP
          ),
          (
              'b2eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Stairway to Heaven',
              'Led Zeppelin',
              'Led Zeppelin IV',
              482,
              '/music/led-zeppelin/stairway-to-heaven.mp3',
              CURRENT_TIMESTAMP
          ),
          (
              'b3eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Hotel California',
              'Eagles',
              'Hotel California',
              391,
              '/music/eagles/hotel-california.mp3',
              CURRENT_TIMESTAMP
          ),
          (
              'b4eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Imagine',
              'John Lennon',
              'Imagine',
              183,
              '/music/john-lennon/imagine.mp3',
              CURRENT_TIMESTAMP
          ),
          (
              'b5eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Sweet Child O'' Mine',
              'Guns N'' Roses',
              'Appetite for Destruction',
              356,
              '/music/guns-n-roses/sweet-child-o-mine.mp3',
              CURRENT_TIMESTAMP
          );

      -- Insert sample playlists
      INSERT INTO "Playlists" ("Id", "Name", "Description", "CreatedBy", "CreatedAt", "UpdatedAt")
      VALUES
          (
              'c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Rock Classics',
              'Timeless rock anthems from the 70s and 80s',
              'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              CURRENT_TIMESTAMP,
              CURRENT_TIMESTAMP
          ),
          (
              'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              'Chill Vibes',
              'Relaxing tunes for a peaceful evening',
              'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
              CURRENT_TIMESTAMP,
              CURRENT_TIMESTAMP
          );

      -- Insert tracks into playlists
      INSERT INTO "PlaylistTracks" ("PlaylistId", "TrackId", "Order", "AddedAt")
      VALUES
          -- Rock Classics playlist
          ('c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 1, CURRENT_TIMESTAMP),
          ('c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b2eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 2, CURRENT_TIMESTAMP),
          ('c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b3eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 3, CURRENT_TIMESTAMP),
          ('c1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b5eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 4, CURRENT_TIMESTAMP),
          -- Chill Vibes playlist
          ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b4eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 1, CURRENT_TIMESTAMP),
          ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 'b3eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID, 2, CURRENT_TIMESTAMP);

      RAISE NOTICE 'Sample data seeded successfully';
  END $$;
  ```

  **Step 2: Update DatabaseInitializer to include seed script**

  Update the `InitializeAsync` method in `Data/DatabaseInitializer.cs`:
  ```csharp
  public async Task InitializeAsync()
  {
      try
      {
          using var connection = _connectionFactory.CreateConnection();

          // Execute schema creation
          _logger.LogInformation("Creating database schema...");
          await ExecuteSqlFileAsync(connection, "001_InitialSchema.sql");

          // Execute stored procedures
          _logger.LogInformation("Creating stored procedures...");
          await ExecuteSqlFileAsync(connection, "002_TrackStoredProcedures.sql");

          // Seed sample data
          _logger.LogInformation("Seeding sample data...");
          await ExecuteSqlFileAsync(connection, "003_SeedData.sql");

          _logger.LogInformation("Database initialization completed successfully");
      }
      catch (Exception ex)
      {
          _logger.LogError(ex, "Error initializing database");
          throw;
      }
  }
  ```

  **Expected Outcome**:
  - `Data/Scripts/003_SeedData.sql` created with sample data
  - When app starts, database is automatically seeded (only once)
  - Database contains:
    - 1 demo user (username: demo_user)
    - 5 sample tracks (Queen, Led Zeppelin, Eagles, John Lennon, Guns N' Roses)
    - 2 playlists with tracks assigned (Rock Classics with 4 tracks, Chill Vibes with 2 tracks)
  - Running app multiple times doesn't duplicate data (due to check in SQL)

  **Common Issues & Solutions**:
  - **Seeder runs every time**: The SQL script checks if users exist before seeding
  - **"Duplicate key" errors**: Drop the database and recreate: `sudo -u postgres psql -c "DROP DATABASE jamtrackradio;"`
  - **Foreign key errors**: Ensure UUIDs match exactly between inserts
  - **Seeder doesn't run**: Check logs for errors, ensure 003_SeedData.sql is included in .csproj

  💡 **Learning moment**: Notice how we use fixed UUIDs in the seed script? This makes the seed data predictable and reproducible. In production, you'd generate new UUIDs, but for testing it's helpful to have consistent IDs you can use in curl commands!

  💡 **Learning moment - DO blocks**: Postgres `DO $$` blocks allow you to write procedural code (like checking if data exists) directly in SQL scripts. The `$$` is a delimiter (like quote marks but for larger blocks of text).

  💡 **Why seed data?** Seeding gives you sample data to test your API immediately without manually creating records. Essential for rapid development!

- **Labels**: backend, csharp, database, seed-data, dapper, phase-2a
- **Estimated Effort**: Small (20-30 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.5

### Task 2.6: Implement Basic REST API Controllers with Dapper
- **Description**: Create a **simple TracksController** with basic CRUD endpoints using Dapper to call stored procedures. Controllers use `IDbConnectionFactory` to get connections and call the stored procedures we created.

  **Step 1: Create `Controllers/TracksController.cs`** in API project:
  ```csharp
  using JamtrackRadio.Api.Data;
  using JamtrackRadio.Domain.Entities;
  using Microsoft.AspNetCore.Mvc;
  using Dapper;

  namespace JamtrackRadio.Api.Controllers;

  [ApiController]
  [Route("api/[controller]")]
  public class TracksController : ControllerBase
  {
      private readonly IDbConnectionFactory _connectionFactory;
      private readonly ILogger<TracksController> _logger;

      public TracksController(IDbConnectionFactory connectionFactory, ILogger<TracksController> logger)
      {
          _connectionFactory = connectionFactory;
          _logger = logger;
      }

      // GET: api/tracks
      [HttpGet]
      public async Task<ActionResult<IEnumerable<Track>>> GetTracks([FromQuery] string? search = null)
      {
          try
          {
              using var connection = _connectionFactory.CreateConnection();

              if (string.IsNullOrWhiteSpace(search))
              {
                  _logger.LogInformation("Getting all tracks");
                  var tracks = await connection.QueryAsync<Track>("SELECT * FROM sp_get_all_tracks()");
                  return Ok(tracks);
              }
              else
              {
                  _logger.LogInformation("Searching tracks with term: {SearchTerm}", search);
                  var tracks = await connection.QueryAsync<Track>(
                      "SELECT * FROM sp_search_tracks(@SearchTerm)",
                      new { SearchTerm = search }
                  );
                  return Ok(tracks);
              }
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error retrieving tracks");
              return StatusCode(500, new { message = "An error occurred while retrieving tracks" });
          }
      }

      // GET: api/tracks/{id}
      [HttpGet("{id}")]
      public async Task<ActionResult<Track>> GetTrack(Guid id)
      {
          try
          {
              _logger.LogInformation("Getting track with ID: {TrackId}", id);

              using var connection = _connectionFactory.CreateConnection();
              var track = await connection.QueryFirstOrDefaultAsync<Track>(
                  "SELECT * FROM sp_get_track_by_id(@TrackId)",
                  new { TrackId = id }
              );

              if (track == null)
              {
                  _logger.LogWarning("Track with ID {TrackId} not found", id);
                  return NotFound(new { message = $"Track with ID {id} not found" });
              }

              return Ok(track);
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error retrieving track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while retrieving the track" });
          }
      }

      // POST: api/tracks
      [HttpPost]
      public async Task<ActionResult<Track>> CreateTrack(Track track)
      {
          try
          {
              _logger.LogInformation("Creating new track: {Title} by {Artist}", track.Title, track.Artist);

              // Validate required fields
              if (string.IsNullOrWhiteSpace(track.Title) || string.IsNullOrWhiteSpace(track.Artist))
              {
                  return BadRequest(new { message = "Title and Artist are required" });
              }

              // Generate new ID
              track.Id = Guid.NewGuid();

              using var connection = _connectionFactory.CreateConnection();
              var createdId = await connection.ExecuteScalarAsync<Guid>(
                  "SELECT sp_create_track(@Id, @Title, @Artist, @Album, @DurationSeconds, @FilePath)",
                  new
                  {
                      Id = track.Id,
                      Title = track.Title,
                      Artist = track.Artist,
                      Album = track.Album,
                      DurationSeconds = track.DurationSeconds,
                      FilePath = track.FilePath
                  }
              );

              _logger.LogInformation("Track created successfully with ID: {TrackId}", createdId);

              // Fetch the created track to return
              var createdTrack = await connection.QueryFirstOrDefaultAsync<Track>(
                  "SELECT * FROM sp_get_track_by_id(@TrackId)",
                  new { TrackId = createdId }
              );

              return CreatedAtAction(nameof(GetTrack), new { id = createdId }, createdTrack);
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error creating track");
              return StatusCode(500, new { message = "An error occurred while creating the track" });
          }
      }

      // PUT: api/tracks/{id}
      [HttpPut("{id}")]
      public async Task<ActionResult<Track>> UpdateTrack(Guid id, Track track)
      {
          try
          {
              _logger.LogInformation("Updating track with ID: {TrackId}", id);

              // Validate required fields
              if (string.IsNullOrWhiteSpace(track.Title) || string.IsNullOrWhiteSpace(track.Artist))
              {
                  return BadRequest(new { message = "Title and Artist are required" });
              }

              using var connection = _connectionFactory.CreateConnection();
              var updated = await connection.ExecuteScalarAsync<bool>(
                  "SELECT sp_update_track(@Id, @Title, @Artist, @Album, @DurationSeconds, @FilePath)",
                  new
                  {
                      Id = id,
                      Title = track.Title,
                      Artist = track.Artist,
                      Album = track.Album,
                      DurationSeconds = track.DurationSeconds,
                      FilePath = track.FilePath
                  }
              );

              if (!updated)
              {
                  _logger.LogWarning("Track with ID {TrackId} not found", id);
                  return NotFound(new { message = $"Track with ID {id} not found" });
              }

              _logger.LogInformation("Track updated successfully: {TrackId}", id);

              // Fetch the updated track to return
              var updatedTrack = await connection.QueryFirstOrDefaultAsync<Track>(
                  "SELECT * FROM sp_get_track_by_id(@TrackId)",
                  new { TrackId = id }
              );

              return Ok(updatedTrack);
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error updating track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while updating the track" });
          }
      }

      // DELETE: api/tracks/{id}
      [HttpDelete("{id}")]
      public async Task<IActionResult> DeleteTrack(Guid id)
      {
          try
          {
              _logger.LogInformation("Deleting track with ID: {TrackId}", id);

              using var connection = _connectionFactory.CreateConnection();
              var deleted = await connection.ExecuteScalarAsync<bool>(
                  "SELECT sp_delete_track(@TrackId)",
                  new { TrackId = id }
              );

              if (!deleted)
              {
                  _logger.LogWarning("Track with ID {TrackId} not found", id);
                  return NotFound(new { message = $"Track with ID {id} not found" });
              }

              _logger.LogInformation("Track deleted successfully: {TrackId}", id);
              return NoContent();
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error deleting track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while deleting the track" });
          }
      }
  }
  ```

  **Step 2: Verify the controller builds and runs**
  ```bash
  cd ~/projects/jamtrack-radio/src/JamtrackRadio.Api
  dotnet build
  dotnet run
  ```

  **Expected Outcome**:
  - `Controllers/TracksController.cs` created using Dapper
  - Swagger UI shows five endpoints:
    - GET /api/tracks (with optional search query parameter)
    - GET /api/tracks/{id}
    - POST /api/tracks
    - PUT /api/tracks/{id}
    - DELETE /api/tracks/{id}
  - All endpoints call stored procedures via Dapper
  - Solution builds successfully: `dotnet build`
  - Controller opens and closes connections properly (using statements)

  **Common Issues & Solutions**:
  - **"Stored procedure not found" error**:
    - Ensure DatabaseInitializer ran successfully - check startup logs
    - Verify SQL scripts are in `Data/Scripts/` folder
    - Check .csproj includes SQL scripts with `<CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>`
    - Manually verify in psql: `\df sp_*` to list stored procedures
    - If missing, manually run: `psql -U postgres -d jamtrackradio -f Data/Scripts/002_TrackStoredProcedures.sql`

  - **"Cannot connect to database" from Dapper**:
    - Verify Postgres is running: `sudo service postgresql status`
    - Check connection string in appsettings.json
    - Test connection manually: `psql -U postgres -d jamtrackradio`
    - Check firewall isn't blocking port 5432

  - **Dapper mapping errors (property not found)**:
    - Ensure property names in C# Track class match column names in SQL (case-sensitive!)
    - Postgres uses case-sensitive quoted identifiers: `"Title"` vs `title`
    - Our stored procedures return quoted identifiers: `"Id"`, `"Title"`, etc.
    - Dapper maps by name, so C# properties must match exactly

  - **Parameters not binding correctly**:
    - Use `@` prefix in SQL: `@SearchTerm`, `@TrackId`
    - Anonymous object property names must match: `new { SearchTerm = search }`
    - Case-sensitive: `SearchTerm` in C# must match `@SearchTerm` in SQL

  - **500 errors on all endpoints**:
    - Check logs: `dotnet run` output or check console
    - Look for exceptions in try-catch blocks
    - Common causes: SQL syntax errors, missing stored procedures, parameter mismatches
    - Test stored procedure directly in psql first

  - **Controller not discovered**:
    - Ensure class has `[ApiController]` and `[Route("api/[controller]")]` attributes
    - Ensure namespace is `JamtrackRadio.Api.Controllers`
    - Verify `AddControllers()` is called in Program.cs

  - **Swagger not showing endpoints**:
    - Ensure `AddSwaggerGen()` and `UseSwagger()` in Program.cs
    - Check ASPNETCORE_ENVIRONMENT is set to Development
    - Try accessing: `http://localhost:5000/swagger/index.html`

  💡 **Learning moment - Dapper patterns used**:
  - **`connection.QueryAsync<Track>(sql)`** - For SELECT queries returning multiple rows. Returns `IEnumerable<Track>`.
  - **`connection.QueryFirstOrDefaultAsync<Track>(sql, params)`** - For SELECT returning single row or null. Returns `Track?`.
  - **`connection.ExecuteScalarAsync<Guid>(sql, params)`** - For functions returning scalar values like UUIDs or integers.
  - **`connection.ExecuteScalarAsync<bool>(sql, params)`** - For functions returning boolean success indicators.
  - **Anonymous objects for parameters** - `new { TrackId = id }` automatically binds to `@TrackId` in SQL.
  - **`using var connection`** - Ensures connection is disposed after use. Critical for connection pool management!

  💡 **Learning moment - Why Dapper + Stored Procedures?**:
  - **Performance**: Stored procedures are compiled and cached by Postgres. Dapper adds minimal overhead.
  - **Control**: You write the exact SQL that runs - no surprises from ORM-generated queries.
  - **Security**: Stored procedures can limit database permissions. Dapper prevents SQL injection via parameterization.
  - **Maintainability**: Database logic stays in the database. C# code is clean and focused on HTTP concerns.
  - **Trade-off**: More code to write (SQL + C#) vs EF Core's automatic CRUD. But you get full control!

  💡 **Learning moment - Connection management**:
  Notice we use `using var connection = _connectionFactory.CreateConnection()` in every method. This ensures connections are returned to the pool immediately after use. Dapper doesn't maintain state like DbContext - each operation opens and closes its own connection. This is lightweight and scales well!

- **Labels**: backend, csharp, rest-api, dapper, stored-procedures, phase-2a
- **Estimated Effort**: Medium (40-50 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.5.5

---

**✅ Checkpoint #1**: Database and Models Ready
**Progress**: [████████░░░░░░░░] 50% through Phase 2A
**Time elapsed**: ~3-4 hours
**What you have**: .NET installed, Postgres running, project structure, domain models, Dapper configured with connection factory, database schema created, 6 stored procedures implemented, sample data seeded, and API controller with full CRUD created!
**Next**: Run and test your first working API with stored procedures!

---

### Task 2.7: Run and Test Your API
- **Description**: Test stored procedures directly in Postgres, then start your application and test all API endpoints using Swagger UI and curl.

  **Step 1: Test stored procedures directly in Postgres** (before starting the API):
  ```bash
  # Connect to database
  sudo -u postgres psql -d jamtrackradio

  # Inside psql, test each stored procedure:

  # 1. List all stored procedures
  \df sp_*

  # 2. Test get all tracks
  SELECT * FROM sp_get_all_tracks();
  -- Should return 5 seeded tracks

  # 3. Test get track by ID (use a real UUID from seeded data)
  SELECT * FROM sp_get_track_by_id('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID);
  -- Should return "Bohemian Rhapsody" by Queen

  # 4. Test search
  SELECT * FROM sp_search_tracks('queen');
  SELECT * FROM sp_search_tracks('heaven');
  -- Should return matching tracks

  # 5. Test create track
  SELECT sp_create_track(
    'b6eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
    'Test Track',
    'Test Artist',
    'Test Album',
    180,
    '/music/test.mp3'
  );
  -- Should return the UUID

  # 6. Verify it was created
  SELECT * FROM sp_get_all_tracks();
  -- Should now show 6 tracks

  # 7. Test update
  SELECT sp_update_track(
    'b6eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID,
    'Updated Track',
    'Updated Artist',
    'Updated Album',
    200,
    '/music/updated.mp3'
  );
  -- Should return true

  # 8. Verify update
  SELECT * FROM sp_get_track_by_id('b6eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID);
  -- Should show updated values

  # 9. Test delete
  SELECT sp_delete_track('b6eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'::UUID);
  -- Should return true

  # 10. Verify deletion
  SELECT * FROM sp_get_all_tracks();
  -- Should be back to 5 tracks

  # Exit psql
  \q
  ```

  **Step 2: Start the application**:
  ```bash
  cd ~/projects/jamtrack-radio/src/JamtrackRadio.Api

  # Run the application
  dotnet run

  # Or run with watch (auto-restart on file changes)
  dotnet watch run
  ```

  **Step 3: Access Swagger UI**:
  - Open browser: `http://localhost:5000/swagger` or `https://localhost:5001/swagger`
  - You should see the Swagger UI with your TracksController endpoints (5 endpoints total)

  **Step 4: Test API endpoints via Swagger**:

  1. **GET /api/tracks** - Click "Try it out" → "Execute"
     - Should return 5 seeded tracks
     - Status code: 200 OK
     - Response shows all track properties

  2. **GET /api/tracks?search=queen** - Click "Try it out"
     - Enter "queen" in search parameter → "Execute"
     - Should return 1 track (Bohemian Rhapsody)
     - Status code: 200 OK
     - Test with other search terms: "heaven", "hotel", "led"

  3. **GET /api/tracks/{id}** - Click "Try it out"
     - Copy an ID from GET all tracks response
     - Paste into id field → "Execute"
     - Should return that specific track
     - Status code: 200 OK

  4. **POST /api/tracks** - Click "Try it out"
     - Enter new track data in JSON:
       ```json
       {
         "title": "Thunderstruck",
         "artist": "AC/DC",
         "album": "The Razors Edge",
         "durationSeconds": 292,
         "filePath": "/music/acdc/thunderstruck.mp3"
       }
       ```
     - Click "Execute"
     - Should return created track with new ID
     - Status code: 201 Created
     - Location header should point to the new track

  5. **PUT /api/tracks/{id}** - Click "Try it out"
     - Copy the ID from the track you just created
     - Paste into id field
     - Modify the JSON body (change title to "Thunderstruck (Live)")
     - Click "Execute"
     - Should return updated track
     - Status code: 200 OK

  6. **DELETE /api/tracks/{id}** - Click "Try it out"
     - Use the same ID
     - Click "Execute"
     - Should return empty response
     - Status code: 204 No Content
     - GET /api/tracks should no longer show this track

  **Step 5: Test API endpoints via curl** (optional but recommended):
  ```bash
  # GET all tracks
  curl http://localhost:5000/api/tracks

  # GET with search
  curl "http://localhost:5000/api/tracks?search=queen"

  # GET by ID (replace with actual ID)
  curl http://localhost:5000/api/tracks/b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a11

  # POST new track
  curl -X POST http://localhost:5000/api/tracks \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Back in Black",
      "artist": "AC/DC",
      "album": "Back in Black",
      "durationSeconds": 255,
      "filePath": "/music/acdc/back-in-black.mp3"
    }'

  # PUT (update) - replace ID with the one from POST response
  curl -X PUT http://localhost:5000/api/tracks/<ID> \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Back in Black (Remastered)",
      "artist": "AC/DC",
      "album": "Back in Black",
      "durationSeconds": 255,
      "filePath": "/music/acdc/back-in-black-remastered.mp3"
    }'

  # DELETE - replace ID
  curl -X DELETE http://localhost:5000/api/tracks/<ID>

  # Verify deletion
  curl http://localhost:5000/api/tracks
  ```

  **Step 6: Verify in database**:
  ```bash
  # Check database directly to verify API operations
  sudo -u postgres psql -d jamtrackradio -c "SELECT \"Id\", \"Title\", \"Artist\" FROM \"Tracks\" ORDER BY \"CreatedAt\" DESC LIMIT 10;"

  # Count tracks
  sudo -u postgres psql -d jamtrackradio -c "SELECT COUNT(*) FROM \"Tracks\";"
  ```

  **Expected Outcome**:
  - All stored procedures work correctly when tested in psql
  - Application starts without errors
  - Swagger UI is accessible and shows 5 endpoints
  - All five endpoints work correctly:
    - GET /api/tracks returns seeded data
    - GET /api/tracks?search=X filters results correctly
    - GET /api/tracks/{id} returns single track
    - POST /api/tracks creates new tracks
    - PUT /api/tracks/{id} updates existing tracks
    - DELETE /api/tracks/{id} removes tracks
  - Status codes are correct (200, 201, 204, 404, 400, 500)
  - Logs show request information and SQL calls
  - Database reflects all operations (inserts, updates, deletes)

  **Common Issues & Solutions**:
  - **Stored procedures not found in psql**:
    - Check if DatabaseInitializer ran: look for "Creating stored procedures..." in startup logs
    - Manually run script: `psql -U postgres -d jamtrackradio -f src/JamtrackRadio.Api/Data/Scripts/002_TrackStoredProcedures.sql`
    - Verify with `\df sp_*` in psql

  - **Stored procedure returns no data**:
    - Check if seeder ran: look for "Seeding sample data..." in logs
    - Manually run: `psql -U postgres -d jamtrackradio -f src/JamtrackRadio.Api/Data/Scripts/003_SeedData.sql`
    - Or verify: `SELECT COUNT(*) FROM "Tracks";` in psql

  - **Port already in use**:
    - Another process is using port 5000
    - Find process: `lsof -i :5000` or `netstat -ano | findstr :5000` (Windows)
    - Kill it or change port in launchSettings.json

  - **"Unable to connect to database" when starting API**:
    - Ensure Postgres is running: `sudo service postgresql status`
    - Start it: `sudo service postgresql start`
    - Test connection: `psql -U postgres -d jamtrackradio`

  - **Swagger not loading**:
    - Check browser console for errors
    - Ensure you're using HTTP not HTTPS if certificate issues
    - Try direct URL: `http://localhost:5000/swagger/index.html`
    - Verify `UseSwagger()` and `UseSwaggerUI()` are in Program.cs

  - **404 Not Found on API calls**:
    - Verify route: should be `/api/tracks` not `/tracks`
    - Check controller has `[Route("api/[controller]")]`
    - Check controller is in `Controllers` folder

  - **500 errors on endpoints**:
    - Check application logs for exceptions
    - Common causes: stored procedure doesn't exist, parameter mismatch, SQL syntax error
    - Test stored procedure directly in psql first
    - Check Dapper mapping (C# property names must match SQL column names)

  - **Search returns nothing**:
    - Search is case-insensitive and uses LIKE with wildcards
    - Try broader terms: "q" instead of "queen"
    - Check stored procedure: `sp_search_tracks` should use LOWER() and wildcards

  - **PUT/DELETE returns 404 but track exists**:
    - UUID format issue - ensure you're using the exact UUID (including hyphens)
    - Test in psql first: `SELECT * FROM sp_get_track_by_id('your-uuid'::UUID);`

  💡 **Learning moment - Testing workflow**:
  Always test your database layer (stored procedures) BEFORE testing your API layer. This isolates issues:
  - If stored procedures work but API doesn't → Problem is in C# code or Dapper mapping
  - If stored procedures don't work → Problem is in SQL logic
  This bottom-up testing approach saves debugging time!

  💡 **Learning moment - Swagger UI**:
  Swagger UI (OpenAPI) is automatically generated from your controller code! It reads your `[HttpGet]`, `[HttpPost]` attributes and method signatures to create interactive documentation. Every ASP.NET Core API should have Swagger - it's perfect for development, testing, and API documentation.

  💡 **Learning moment - Status codes**:
  - **200 OK** - Successful GET, PUT (resource returned)
  - **201 Created** - Successful POST (new resource created)
  - **204 No Content** - Successful DELETE (no response body needed)
  - **400 Bad Request** - Invalid input (missing required fields)
  - **404 Not Found** - Resource doesn't exist
  - **500 Internal Server Error** - Server-side exception
  Using correct status codes helps clients handle responses properly!

- **Labels**: backend, testing, swagger, dapper, stored-procedures, phase-2a
- **Estimated Effort**: Medium (40-50 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.6

### Task 2.8: Create GitHub Issue to Track Phase 2A Progress
- **Description**: Create a GitHub issue in your jamtrack-radio repository to track Phase 2A completion and document what you've built.

  **Commands (Windows PowerShell)**:
  ```powershell
  cd C:\training\jamtrack-radio

  # Get Phase 2A milestone number
  $milestone = gh api repos/:owner/:repo/milestones | ConvertFrom-Json | Where-Object {$_.title -like "*Phase 2A*"} | Select-Object -ExpandProperty number

  # Create completion issue
  gh issue create --title "Phase 2A Complete: Basic Backend API with Dapper" --body "## Phase 2A Achievements

  Successfully completed Phase 2A with the following:

  ### ✅ Environment Setup
  - .NET 8 SDK installed in WSL
  - PostgreSQL installed and configured
  - Database user and permissions set up

  ### ✅ Project Structure
  - Solution created: JamtrackRadio.sln
  - API project: JamtrackRadio.Api
  - Domain project: JamtrackRadio.Domain

  ### ✅ Domain Models
  - Track entity with properties
  - Playlist entity with properties
  - User entity
  - PlaylistTrack junction table (many-to-many)

  ### ✅ Database Configuration
  - Dapper micro-ORM configured with Npgsql
  - Connection factory pattern implemented
  - Database schema created with SQL scripts
  - 6 Postgres stored procedures for CRUD operations:
    - sp_get_all_tracks() - Retrieve all tracks
    - sp_get_track_by_id() - Get single track
    - sp_search_tracks() - Search functionality
    - sp_create_track() - Insert new track
    - sp_update_track() - Update existing track
    - sp_delete_track() - Delete track
  - DatabaseInitializer for automatic script execution
  - Sample data seeder with 5 tracks, 2 playlists, 1 user

  ### ✅ REST API
  - TracksController with complete CRUD (5 endpoints):
    - GET /api/tracks - List all tracks
    - GET /api/tracks?search=X - Search tracks
    - GET /api/tracks/{id} - Get by ID
    - POST /api/tracks - Create new track
    - PUT /api/tracks/{id} - Update track
    - DELETE /api/tracks/{id} - Delete track
  - All endpoints call stored procedures via Dapper
  - Proper HTTP status codes (200, 201, 204, 404, 400, 500)
  - Input validation and error handling
  - Swagger UI configured and tested
  - All endpoints working correctly

  ### 📊 Statistics
  - Time spent: ~6-8 hours
  - Files created: ~15 files (includes SQL scripts)
  - Lines of code: ~800 lines (C# + SQL)
  - SQL Scripts: 3 files (~300 lines)
  - C# Code: ~500 lines
  - Stored Procedures: 6 functions

  ### 🎯 Key Technical Decisions
  - **Dapper over EF Core**: Chose Dapper for performance and full SQL control
  - **Stored Procedures**: Database logic in Postgres for security and maintainability
  - **Connection Factory**: Clean connection management without DbContext overhead
  - **SQL Script Execution**: Automated database initialization on startup

  ### 🎯 Next Steps
  Options:
  1. **Phase 2B**: Add Repository pattern, Service layer, gRPC (optional - can defer)
  2. **Phase 3**: Dockerize the application (recommended - maintain momentum!)
  3. **Take a break!** You earned it!

  " --label "phase-2a,milestone,backend,dapper" --milestone $milestone

  # Close the issue immediately (since Phase 2A is complete)
  # gh issue close <issue-number> --comment "Phase 2A completed successfully with Dapper and stored procedures!"
  ```

  **Expected Outcome**:
  - Issue created in your GitHub repository
  - Issue includes comprehensive summary of Phase 2A achievements
  - Documents Dapper + stored procedure implementation
  - Milestone tracking updated

  💡 **Why document this?** Tracking your progress in GitHub creates a portfolio of your learning journey that you can reference later! This issue shows you learned both Dapper and Postgres stored procedures!
- **Labels**: github, documentation, milestone, phase-2a, dapper
- **Estimated Effort**: Small (10 mins)
- **Status**: Backlog
- **Dependencies**: Task 2.7

---

**✅ Phase 2A Complete!** 🎉

**Progress**: [████████████████] 100% through Phase 2A
**Time elapsed**: ~6-8 hours total
**What you've accomplished**:
- ✅ .NET 8 SDK installed in WSL
- ✅ PostgreSQL database set up and running
- ✅ Clean project structure (Domain + API)
- ✅ Domain models with proper relationships
- ✅ **Dapper micro-ORM with Postgres** (lightweight and fast!)
- ✅ **6 stored procedures for complete CRUD operations**
- ✅ Connection factory pattern for clean database access
- ✅ Database schema initialization with SQL scripts
- ✅ Automatic seeding with sample data
- ✅ **Working REST API with 5 endpoints** (full CRUD + search)
- ✅ Swagger UI for testing
- ✅ Proper logging, validation, and error handling
- ✅ Tested stored procedures directly in Postgres
- ✅ Tested all API endpoints via Swagger and curl

**Achievement unlocked**: 🚀 **Backend Developer + Database Pro** - You built a production-ready API from scratch using Dapper and stored procedures!

**Key learnings**:
- **Dapper**: Lightweight micro-ORM that gives you full SQL control with minimal overhead
- **Stored Procedures**: Database logic stays in the database for performance, security, and maintainability
- **Connection Factory**: Clean pattern for managing database connections without DbContext
- **Bottom-up testing**: Test database layer before API layer to isolate issues

**What's next?** You have options:

1. **Phase 2B** (Optional - Advanced Patterns):
   - Add Repository pattern for cleaner data access
   - Implement Service layer for business logic
   - Add gRPC services for microservice communication
   - **Time**: 2-3 weeks
   - **Best for**: Learning enterprise architecture patterns
   - **Note**: You already have complete CRUD with Dapper, so Phase 2B focuses on architectural patterns

2. **Phase 3** (Docker - Recommended):
   - Containerize your application
   - Learn Docker fundamentals
   - Set up Docker Compose for multi-container orchestration
   - **Time**: 1 week
   - **Best for**: Maintaining momentum and getting to deployment faster

3. **Take a break!**
   - You've earned it! Building a working API with Dapper and stored procedures is a significant achievement.
   - Come back refreshed and choose your path.

**Recommendation**: Skip to Phase 3 (Docker) to keep momentum! Your API is fully functional with complete CRUD operations. You can always return to Phase 2B later when you need more advanced architectural patterns like Repository or Service layers.

---

---

## Phase 2B: Advanced Backend Patterns (Optional - Can defer to later)
**Phase Description**: Refactor the basic backend to add professional patterns: Repository pattern, Service layer, complete CRUD operations, and gRPC services. This phase is **optional** and can be done later - you can skip to Phase 3 (Docker) if you want to keep momentum!

**Priority**: Medium

**Labels**: phase-2b, backend, refactoring, patterns

**Note**: This phase adds complexity. Consider skipping it initially and returning after Phase 3-4 when you understand Docker/Kubernetes better.

### Task 2B.1: Create Infrastructure Project
- **Description**: Add a separate Infrastructure project for data access concerns, moving DbContext out of the API project for better separation of concerns.

  **Step 1: Create Infrastructure project**:
  ```bash
  cd ~/projects/jamtrack-radio
  dotnet new classlib -n JamtrackRadio.Infrastructure -o src/JamtrackRadio.Infrastructure
  dotnet sln add src/JamtrackRadio.Infrastructure/JamtrackRadio.Infrastructure.csproj

  # Add project references
  dotnet add src/JamtrackRadio.Infrastructure/JamtrackRadio.Infrastructure.csproj reference src/JamtrackRadio.Domain/JamtrackRadio.Domain.csproj
  dotnet add src/JamtrackRadio.Api/JamtrackRadio.Api.csproj reference src/JamtrackRadio.Infrastructure/JamtrackRadio.Infrastructure.csproj
  ```

  **Step 2: Copy EF Core packages to Infrastructure project**:
  ```bash
  cd src/JamtrackRadio.Infrastructure
  dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
  dotnet add package Microsoft.EntityFrameworkCore.Design
  ```

  **Step 3: Move DbContext from API to Infrastructure**:
  ```bash
  # Create Data folder in Infrastructure
  mkdir -p ~/projects/jamtrack-radio/src/JamtrackRadio.Infrastructure/Data

  # Move JamtrackDbContext.cs from API/Data to Infrastructure/Data
  mv ~/projects/jamtrack-radio/src/JamtrackRadio.Api/Data/JamtrackDbContext.cs ~/projects/jamtrack-radio/src/JamtrackRadio.Infrastructure/Data/

  # Also move DbSeeder.cs
  mv ~/projects/jamtrack-radio/src/JamtrackRadio.Api/Data/DbSeeder.cs ~/projects/jamtrack-radio/src/JamtrackRadio.Infrastructure/Data/
  ```

  **Step 4: Update namespace in JamtrackDbContext.cs**:
  Change from:
  ```csharp
  namespace JamtrackRadio.Api.Data;
  ```
  To:
  ```csharp
  namespace JamtrackRadio.Infrastructure.Data;
  ```

  Do the same for `DbSeeder.cs`.

  **Step 5: Update Program.cs in API project**:
  Change the using statement:
  ```csharp
  using JamtrackRadio.Infrastructure.Data;  // Changed from Api.Data
  ```

  **Step 6: Verify and build**:
  ```bash
  cd ~/projects/jamtrack-radio
  dotnet build
  ```

  **Expected Outcome**:
  - Infrastructure project created with Data folder
  - DbContext and DbSeeder moved to Infrastructure
  - Solution builds successfully
  - Clean separation: Domain (models) → Infrastructure (data access) → API (HTTP)

  **Common Issues & Solutions**:
  - **Build errors after moving files**: Check namespace updates in all files
  - **"Type not found" errors**: Ensure using statements are updated in Program.cs
  - **Migration errors**: Migrations folder stays in API project - that's OK for now
  - **DbContext not found**: Check project references are correct

  💡 **Why separate Infrastructure?** This follows Clean Architecture principles: the API layer shouldn't know about database implementation details. Infrastructure can be swapped (e.g., from Postgres to SQL Server) without changing API code!
- **Labels**: backend, csharp, refactoring, infrastructure, phase-2b
- **Estimated Effort**: Small (20-30 mins)
- **Status**: Backlog
- **Dependencies**: Phase 2A (Task 2.8)

### Task 2B.2: Implement Repository Pattern
- **Description**: Create generic repository and unit of work patterns for data access abstraction.

  **Step 1: Create `Repositories/IRepository.cs`** in Infrastructure:
  ```csharp
  namespace JamtrackRadio.Infrastructure.Repositories;

  public interface IRepository<T> where T : class
  {
      Task<T?> GetByIdAsync(Guid id);
      Task<IEnumerable<T>> GetAllAsync();
      Task<IEnumerable<T>> FindAsync(System.Linq.Expressions.Expression<Func<T, bool>> predicate);
      Task<T> AddAsync(T entity);
      Task UpdateAsync(T entity);
      Task DeleteAsync(T entity);
      Task<bool> ExistsAsync(Guid id);
  }
  ```

  **Step 2: Create `Repositories/Repository.cs`** (base implementation):
  ```csharp
  using JamtrackRadio.Infrastructure.Data;
  using Microsoft.EntityFrameworkCore;
  using System.Linq.Expressions;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public class Repository<T> : IRepository<T> where T : class
  {
      protected readonly JamtrackDbContext _context;
      protected readonly DbSet<T> _dbSet;

      public Repository(JamtrackDbContext context)
      {
          _context = context;
          _dbSet = context.Set<T>();
      }

      public virtual async Task<T?> GetByIdAsync(Guid id)
      {
          return await _dbSet.FindAsync(id);
      }

      public virtual async Task<IEnumerable<T>> GetAllAsync()
      {
          return await _dbSet.ToListAsync();
      }

      public virtual async Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate)
      {
          return await _dbSet.Where(predicate).ToListAsync();
      }

      public virtual async Task<T> AddAsync(T entity)
      {
          await _dbSet.AddAsync(entity);
          return entity;
      }

      public virtual async Task UpdateAsync(T entity)
      {
          _dbSet.Update(entity);
          await Task.CompletedTask;
      }

      public virtual async Task DeleteAsync(T entity)
      {
          _dbSet.Remove(entity);
          await Task.CompletedTask;
      }

      public virtual async Task<bool> ExistsAsync(Guid id)
      {
          return await _dbSet.FindAsync(id) != null;
      }
  }
  ```

  **Step 3: Create `Repositories/ITrackRepository.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public interface ITrackRepository : IRepository<Track>
  {
      Task<IEnumerable<Track>> GetTracksByArtistAsync(string artist);
      Task<IEnumerable<Track>> SearchTracksAsync(string searchTerm);
  }
  ```

  **Step 4: Create `Repositories/TrackRepository.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;
  using JamtrackRadio.Infrastructure.Data;
  using Microsoft.EntityFrameworkCore;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public class TrackRepository : Repository<Track>, ITrackRepository
  {
      public TrackRepository(JamtrackDbContext context) : base(context)
      {
      }

      public async Task<IEnumerable<Track>> GetTracksByArtistAsync(string artist)
      {
          return await _dbSet
              .Where(t => t.Artist.ToLower().Contains(artist.ToLower()))
              .OrderBy(t => t.Title)
              .ToListAsync();
      }

      public async Task<IEnumerable<Track>> SearchTracksAsync(string searchTerm)
      {
          searchTerm = searchTerm.ToLower();
          return await _dbSet
              .Where(t => t.Title.ToLower().Contains(searchTerm) ||
                         t.Artist.ToLower().Contains(searchTerm) ||
                         (t.Album != null && t.Album.ToLower().Contains(searchTerm)))
              .ToListAsync();
      }
  }
  ```

  **Step 5: Create `Repositories/IPlaylistRepository.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public interface IPlaylistRepository : IRepository<Playlist>
  {
      Task<IEnumerable<Playlist>> GetPlaylistsByUserAsync(Guid userId);
      Task<Playlist?> GetPlaylistWithTracksAsync(Guid playlistId);
  }
  ```

  **Step 6: Create `Repositories/PlaylistRepository.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;
  using JamtrackRadio.Infrastructure.Data;
  using Microsoft.EntityFrameworkCore;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public class PlaylistRepository : Repository<Playlist>, IPlaylistRepository
  {
      public PlaylistRepository(JamtrackDbContext context) : base(context)
      {
      }

      public async Task<IEnumerable<Playlist>> GetPlaylistsByUserAsync(Guid userId)
      {
          return await _dbSet
              .Where(p => p.CreatedBy == userId)
              .OrderByDescending(p => p.UpdatedAt)
              .ToListAsync();
      }

      public async Task<Playlist?> GetPlaylistWithTracksAsync(Guid playlistId)
      {
          return await _dbSet
              .Include(p => p.PlaylistTracks)
              .ThenInclude(pt => pt.Track)
              .FirstOrDefaultAsync(p => p.Id == playlistId);
      }
  }
  ```

  **Step 7: Create `IUnitOfWork.cs`**:
  ```csharp
  namespace JamtrackRadio.Infrastructure.Repositories;

  public interface IUnitOfWork : IDisposable
  {
      ITrackRepository Tracks { get; }
      IPlaylistRepository Playlists { get; }
      Task<int> SaveChangesAsync();
  }
  ```

  **Step 8: Create `UnitOfWork.cs`**:
  ```csharp
  using JamtrackRadio.Infrastructure.Data;

  namespace JamtrackRadio.Infrastructure.Repositories;

  public class UnitOfWork : IUnitOfWork
  {
      private readonly JamtrackDbContext _context;
      private ITrackRepository? _trackRepository;
      private IPlaylistRepository? _playlistRepository;

      public UnitOfWork(JamtrackDbContext context)
      {
          _context = context;
      }

      public ITrackRepository Tracks => _trackRepository ??= new TrackRepository(_context);
      public IPlaylistRepository Playlists => _playlistRepository ??= new PlaylistRepository(_context);

      public async Task<int> SaveChangesAsync()
      {
          return await _context.SaveChangesAsync();
      }

      public void Dispose()
      {
          _context.Dispose();
      }
  }
  ```

  **Expected Outcome**:
  - 8 new files created in Infrastructure/Repositories/
  - Generic repository pattern implemented
  - Specific repositories for Track and Playlist
  - Unit of Work pattern for transaction management
  - Solution builds successfully

  **Common Issues & Solutions**:
  - **Namespace errors**: Ensure all using statements are correct
  - **Build warnings about nullable**: Add `?` for nullable return types
  - **Repository not found**: Check namespace and file location

  💡 **Learning moment**: The Repository pattern abstracts data access, making your code testable. You can mock repositories in unit tests without needing a real database! Unit of Work ensures multiple operations happen in a single transaction.

  **Benefits**: Testability, separation of concerns, reusability, transaction management
- **Labels**: backend, csharp, repository-pattern, phase-2b
- **Estimated Effort**: Medium (60-75 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.1

### Task 2B.3: Implement Service Layer
- **Description**: Create service layer to move business logic out of controllers.

  **Step 1: Create new Services project** (recommended for larger applications):
  ```bash
  cd ~/projects/jamtrack-radio
  dotnet new classlib -n JamtrackRadio.Services -o src/JamtrackRadio.Services
  dotnet sln add src/JamtrackRadio.Services/JamtrackRadio.Services.csproj
  dotnet add src/JamtrackRadio.Services/JamtrackRadio.Services.csproj reference src/JamtrackRadio.Domain/JamtrackRadio.Domain.csproj
  dotnet add src/JamtrackRadio.Services/JamtrackRadio.Services.csproj reference src/JamtrackRadio.Infrastructure/JamtrackRadio.Infrastructure.csproj
  dotnet add src/JamtrackRadio.Api/JamtrackRadio.Api.csproj reference src/JamtrackRadio.Services/JamtrackRadio.Services.csproj
  ```

  **Step 2: Create `Services/ITrackService.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;

  namespace JamtrackRadio.Services;

  public interface ITrackService
  {
      Task<IEnumerable<Track>> GetAllTracksAsync();
      Task<Track?> GetTrackByIdAsync(Guid id);
      Task<Track> CreateTrackAsync(Track track);
      Task<Track> UpdateTrackAsync(Guid id, Track track);
      Task DeleteTrackAsync(Guid id);
      Task<IEnumerable<Track>> SearchTracksAsync(string searchTerm);
      Task<IEnumerable<Track>> GetTracksByArtistAsync(string artist);
  }
  ```

  **Step 3: Create `Services/TrackService.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;
  using JamtrackRadio.Infrastructure.Repositories;

  namespace JamtrackRadio.Services;

  public class TrackService : ITrackService
  {
      private readonly IUnitOfWork _unitOfWork;

      public TrackService(IUnitOfWork unitOfWork)
      {
          _unitOfWork = unitOfWork;
      }

      public async Task<IEnumerable<Track>> GetAllTracksAsync()
      {
          return await _unitOfWork.Tracks.GetAllAsync();
      }

      public async Task<Track?> GetTrackByIdAsync(Guid id)
      {
          return await _unitOfWork.Tracks.GetByIdAsync(id);
      }

      public async Task<Track> CreateTrackAsync(Track track)
      {
          if (string.IsNullOrWhiteSpace(track.Title))
              throw new ArgumentException("Track title is required");

          if (string.IsNullOrWhiteSpace(track.Artist))
              throw new ArgumentException("Track artist is required");

          track.Id = Guid.NewGuid();
          track.CreatedAt = DateTime.UtcNow;

          await _unitOfWork.Tracks.AddAsync(track);
          await _unitOfWork.SaveChangesAsync();

          return track;
      }

      public async Task<Track> UpdateTrackAsync(Guid id, Track track)
      {
          var existingTrack = await _unitOfWork.Tracks.GetByIdAsync(id);
          if (existingTrack == null)
              throw new KeyNotFoundException($"Track with ID {id} not found");

          existingTrack.Title = track.Title;
          existingTrack.Artist = track.Artist;
          existingTrack.Album = track.Album;
          existingTrack.DurationSeconds = track.DurationSeconds;
          existingTrack.FilePath = track.FilePath;

          await _unitOfWork.Tracks.UpdateAsync(existingTrack);
          await _unitOfWork.SaveChangesAsync();

          return existingTrack;
      }

      public async Task DeleteTrackAsync(Guid id)
      {
          var track = await _unitOfWork.Tracks.GetByIdAsync(id);
          if (track == null)
              throw new KeyNotFoundException($"Track with ID {id} not found");

          await _unitOfWork.Tracks.DeleteAsync(track);
          await _unitOfWork.SaveChangesAsync();
      }

      public async Task<IEnumerable<Track>> SearchTracksAsync(string searchTerm)
      {
          if (string.IsNullOrWhiteSpace(searchTerm))
              return await GetAllTracksAsync();

          return await _unitOfWork.Tracks.SearchTracksAsync(searchTerm);
      }

      public async Task<IEnumerable<Track>> GetTracksByArtistAsync(string artist)
      {
          if (string.IsNullOrWhiteSpace(artist))
              throw new ArgumentException("Artist name is required");

          return await _unitOfWork.Tracks.GetTracksByArtistAsync(artist);
      }
  }
  ```

  **Step 4: Create `Services/IPlaylistService.cs`** and `Services/PlaylistService.cs`** (similar pattern - implement full CRUD + add/remove tracks).

  **Expected Outcome**:
  - New Services project created
  - TrackService and PlaylistService implemented
  - Business logic moved out of controllers
  - Services use Unit of Work pattern
  - Solution builds successfully

  **Common Issues & Solutions**:
  - **Circular dependency**: Ensure project references flow one direction: Domain ← Infrastructure ← Services ← API
  - **UnitOfWork not found**: Check Infrastructure project reference in Services
  - **ArgumentException not caught**: Controllers will need to catch and return appropriate HTTP status codes

  💡 **Learning moment**: The Service layer contains business logic and validation. Controllers should be "thin" - just handling HTTP concerns. This makes logic reusable (e.g., you could call TrackService from both REST API and gRPC service).

  **Benefits**: Separation of concerns, easier testing, reusable business logic, single source of truth for validation
- **Labels**: backend, csharp, service-layer, phase-2b
- **Estimated Effort**: Large (90-120 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.2

### Task 2B.4: Refactor Controllers to Use Services
- **Description**: Update TracksController to use TrackService instead of DbContext directly, making controllers thin and focused only on HTTP concerns.

  **Update `Controllers/TracksController.cs`**:
  ```csharp
  using JamtrackRadio.Domain.Entities;
  using JamtrackRadio.Services;
  using Microsoft.AspNetCore.Mvc;

  namespace JamtrackRadio.Api.Controllers;

  [ApiController]
  [Route("api/[controller]")]
  public class TracksController : ControllerBase
  {
      private readonly ITrackService _trackService;
      private readonly ILogger<TracksController> _logger;

      public TracksController(ITrackService trackService, ILogger<TracksController> logger)
      {
          _trackService = trackService;
          _logger = logger;
      }

      [HttpGet]
      public async Task<ActionResult<IEnumerable<Track>>> GetTracks([FromQuery] string? search = null)
      {
          try
          {
              var tracks = string.IsNullOrWhiteSpace(search)
                  ? await _trackService.GetAllTracksAsync()
                  : await _trackService.SearchTracksAsync(search);

              return Ok(tracks);
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error retrieving tracks");
              return StatusCode(500, new { message = "An error occurred while retrieving tracks" });
          }
      }

      [HttpGet("{id}")]
      public async Task<ActionResult<Track>> GetTrack(Guid id)
      {
          try
          {
              var track = await _trackService.GetTrackByIdAsync(id);
              if (track == null)
                  return NotFound(new { message = $"Track with ID {id} not found" });

              return Ok(track);
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error retrieving track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while retrieving the track" });
          }
      }

      [HttpPost]
      public async Task<ActionResult<Track>> CreateTrack(Track track)
      {
          try
          {
              var createdTrack = await _trackService.CreateTrackAsync(track);
              return CreatedAtAction(nameof(GetTrack), new { id = createdTrack.Id }, createdTrack);
          }
          catch (ArgumentException ex)
          {
              return BadRequest(new { message = ex.Message });
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error creating track");
              return StatusCode(500, new { message = "An error occurred while creating the track" });
          }
      }

      [HttpPut("{id}")]
      public async Task<ActionResult<Track>> UpdateTrack(Guid id, Track track)
      {
          try
          {
              var updatedTrack = await _trackService.UpdateTrackAsync(id, track);
              return Ok(updatedTrack);
          }
          catch (KeyNotFoundException ex)
          {
              return NotFound(new { message = ex.Message });
          }
          catch (ArgumentException ex)
          {
              return BadRequest(new { message = ex.Message });
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error updating track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while updating the track" });
          }
      }

      [HttpDelete("{id}")]
      public async Task<IActionResult> DeleteTrack(Guid id)
      {
          try
          {
              await _trackService.DeleteTrackAsync(id);
              return NoContent();
          }
          catch (KeyNotFoundException ex)
          {
              return NotFound(new { message = ex.Message });
          }
          catch (Exception ex)
          {
              _logger.LogError(ex, "Error deleting track {TrackId}", id);
              return StatusCode(500, new { message = "An error occurred while deleting the track" });
          }
      }
  }
  ```

  **Update Program.cs to register services**:
  ```csharp
  using JamtrackRadio.Infrastructure.Data;
  using JamtrackRadio.Infrastructure.Repositories;
  using JamtrackRadio.Services;
  using Microsoft.EntityFrameworkCore;

  var builder = WebApplication.CreateBuilder(args);

  builder.Services.AddControllers();
  builder.Services.AddEndpointsApiExplorer();
  builder.Services.AddSwaggerGen();

  // Register DbContext
  builder.Services.AddDbContext<JamtrackDbContext>(options =>
      options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

  // Register UnitOfWork and Services
  builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
  builder.Services.AddScoped<ITrackService, TrackService>();
  // Add PlaylistService when implemented

  var app = builder.Build();

  // Rest of Program.cs...
  ```

  **Expected Outcome**:
  - Controller is now "thin" - only handles HTTP concerns
  - All business logic is in TrackService
  - Proper exception handling with appropriate HTTP status codes
  - PUT and DELETE endpoints now available
  - Search functionality added via query parameter

  **Common Issues & Solutions**:
  - **Service not injected**: Ensure services are registered in Program.cs
  - **500 errors on all requests**: Check that UnitOfWork and services are registered with correct lifetimes (Scoped)
  - **Old controller code conflicts**: Remove old DbContext injection completely

  💡 **Learning moment**: Notice how thin the controller is now! It just translates HTTP requests into service calls and service results into HTTP responses. All validation and business logic lives in the service layer.
- **Labels**: backend, csharp, refactoring, controllers, phase-2b
- **Estimated Effort**: Small (30-40 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.3

### Task 2B.5: Implement Complete CRUD for Tracks and Playlists
- **Description**: PUT/DELETE are already in TracksController from Task 2B.4. Now create full PlaylistsController with playlist management and track assignment endpoints.

  **Create `Controllers/PlaylistsController.cs`** with endpoints:
  - GET /api/playlists - List all playlists
  - GET /api/playlists/{id} - Get playlist with tracks
  - POST /api/playlists - Create playlist
  - PUT /api/playlists/{id} - Update playlist
  - DELETE /api/playlists/{id} - Delete playlist
  - POST /api/playlists/{id}/tracks/{trackId} - Add track to playlist
  - DELETE /api/playlists/{id}/tracks/{trackId} - Remove track from playlist

  **Note**: Implement PlaylistService first (similar to TrackService pattern), then create controller.

  **Expected Outcome**: Full CRUD for both Tracks and Playlists, including playlist-track management

  **Time estimate**: Large (60-90 mins)
- **Labels**: backend, csharp, rest-api, crud, phase-2b
- **Estimated Effort**: Large (60-90 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.4

### Task 2B.6: Create gRPC Service Project
- **Description**: Add gRPC project for internal microservice communication (advanced - optional for learning purposes).

  **Commands**:
  ```bash
  cd ~/projects/jamtrack-radio
  dotnet new grpc -n JamtrackRadio.GrpcService -o src/JamtrackRadio.GrpcService
  dotnet sln add src/JamtrackRadio.GrpcService/JamtrackRadio.GrpcService.csproj
  dotnet add src/JamtrackRadio.GrpcService/JamtrackRadio.GrpcService.csproj reference src/JamtrackRadio.Services/JamtrackRadio.Services.csproj
  ```

  **Expected Outcome**: gRPC project created, can reuse Services layer for business logic

  💡 **Why gRPC?** gRPC is faster and more efficient than REST for service-to-service communication in microservices architectures.
- **Labels**: backend, csharp, grpc, phase-2b
- **Estimated Effort**: Small (20-30 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.5

### Task 2B.7: Implement gRPC Services
- **Description**: Create gRPC proto files and implement gRPC services using the existing service layer.

  **Create `Protos/track.proto`**:
  ```protobuf
  syntax = "proto3";
  option csharp_namespace = "JamtrackRadio.GrpcService";

  service TrackService {
    rpc GetAllTracks (Empty) returns (TrackList);
    rpc GetTrackById (TrackRequest) returns (TrackResponse);
    rpc CreateTrack (CreateTrackRequest) returns (TrackResponse);
  }

  message Empty {}
  message TrackRequest { string id = 1; }
  message TrackList { repeated TrackResponse tracks = 1; }
  message TrackResponse {
    string id = 1;
    string title = 2;
    string artist = 3;
    string album = 4;
    int32 durationSeconds = 5;
  }
  message CreateTrackRequest {
    string title = 1;
    string artist = 2;
    string album = 3;
    int32 durationSeconds = 4;
  }
  ```

  **Implement service** - Call existing TrackService methods from gRPC implementations.

  **Expected Outcome**: gRPC endpoints callable via tools like BloomRPC or Postman
- **Labels**: backend, csharp, grpc, phase-2b
- **Estimated Effort**: Large (90-120 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.6

### Task 2B.8: Update Dependency Injection and Test
- **Description**: Finalize DI configuration and test both REST and gRPC endpoints.

  **Update Program.cs** in gRPC project to register all services (same as API project).

  **Test scenarios**:
  1. Test all REST endpoints via Swagger
  2. Test gRPC endpoints via BloomRPC/Postman
  3. Verify CRUD operations work end-to-end
  4. Check database for correct data

  **Expected Outcome**:
  - All patterns working together
  - Both REST and gRPC functional
  - Clean architecture maintained
- **Labels**: backend, csharp, dependency-injection, testing, phase-2b
- **Estimated Effort**: Medium (45-60 mins)
- **Status**: Backlog
- **Dependencies**: Task 2B.7

---

**✅ Phase 2B Complete!** (if you chose to do it) 🎉

**Progress**: [████████████████] 100% through Phase 2B
**Time elapsed**: ~10-15 hours total (Phase 2A + 2B combined)
**What you've accomplished**:
- ✅ Clean Architecture: Domain → Infrastructure → Services → API
- ✅ Repository pattern for data access abstraction
- ✅ Unit of Work pattern for transaction management
- ✅ Service layer with business logic and validation
- ✅ Thin controllers focused on HTTP concerns
- ✅ Complete CRUD for Tracks and Playlists
- ✅ gRPC services (if completed)
- ✅ Professional enterprise patterns

**Achievement unlocked**: 🏗️ **Software Architect** - You've built an enterprise-grade backend with best practices!

**What's next**: Phase 3 (Docker) - Time to containerize your application!

---

---

## Phase 3: Containerization with Docker
**Phase Description**: Dockerize the backend services, create Dockerfiles with multi-stage builds, set up Docker Compose for local multi-container orchestration.

**Priority**: High

**Labels**: phase-3, docker, containerization

### Task 3.0: Docker Basics Exploration
- **Description**: Before dockerizing your own application, get comfortable with Docker by running and exploring existing containers. This hands-on exploration will teach you container fundamentals.

  **Learning exercises (WSL Ubuntu or Windows Terminal)**:

  **Exercise 1: Hello World**
  ```bash
  # Run your first container
  docker run hello-world
  ```
  **What happened?** Docker downloaded the hello-world image and ran it. The container printed a message and exited. This demonstrates the basic container lifecycle.

  **Exercise 2: Interactive Container**
  ```bash
  # Run an interactive Ubuntu container
  docker run -it ubuntu bash

  # Inside the container, explore:
  whoami              # You're root!
  cat /etc/os-release # Check OS
  apt update          # Update packages
  apt install -y curl # Install software
  curl --version      # Verify installation
  exit                # Leave container

  # Try running it again
  docker run -it ubuntu bash
  curl --version      # curl is gone! Containers are ephemeral
  exit
  ```
  **What happened?** Each `docker run` creates a NEW container. Changes aren't persisted unless you commit them or use volumes.

  **Exercise 3: Background Web Server**
  ```bash
  # Run nginx web server in detached mode
  docker run -d -p 8080:80 --name my-nginx nginx

  # Visit http://localhost:8080 in browser
  # You should see "Welcome to nginx!"

  # View running containers
  docker ps

  # View logs
  docker logs my-nginx

  # View live logs (Ctrl+C to exit)
  docker logs -f my-nginx

  # Execute command inside running container
  docker exec -it my-nginx bash
  ls /usr/share/nginx/html/  # See nginx files
  exit
  ```
  **What happened?** The `-d` flag ran the container in the background. The `-p 8080:80` mapped port 8080 on your machine to port 80 in the container.

  **Exercise 4: Container Management**
  ```bash
  # List all containers (running and stopped)
  docker ps -a

  # Stop the nginx container
  docker stop my-nginx

  # Verify it's stopped
  docker ps

  # Start it again
  docker start my-nginx

  # Remove the container (must stop first)
  docker stop my-nginx
  docker rm my-nginx

  # Remove with force (stops and removes)
  docker rm -f my-nginx
  ```

  **Exercise 5: Image Management**
  ```bash
  # List downloaded images
  docker images

  # Pull an image without running it
  docker pull alpine

  # See image details
  docker inspect alpine

  # Remove an image
  docker rmi alpine

  # Pull a specific version
  docker pull nginx:1.25-alpine
  ```

  **Exercise 6: Run a .NET Application**
  ```bash
  # Run Microsoft's sample ASP.NET app
  docker run -it --rm -p 8000:80 mcr.microsoft.com/dotnet/samples:aspnetapp

  # Visit http://localhost:8000
  # You should see a .NET sample page

  # Press Ctrl+C to stop
  ```
  **What happened?** The `--rm` flag automatically removes the container when it stops. Perfect for testing!

  **Exercise 7: Cleanup**
  ```bash
  # Remove all stopped containers
  docker container prune

  # Remove all unused images
  docker image prune -a

  # Remove everything (containers, images, networks, volumes)
  # WARNING: Only do this if you're sure!
  docker system prune -a --volumes
  ```

  **Expected Outcome**:
  - You understand containers are isolated, ephemeral environments
  - You can run containers interactively (`-it`) or in background (`-d`)
  - You understand port mapping (`-p host:container`)
  - You know how to inspect logs, execute commands, and manage lifecycle
  - You've seen a working .NET containerized application
  - Docker Desktop is running smoothly

  **Common Issues & Solutions**:
  - **"Cannot connect to Docker daemon"**: Docker Desktop not running - start it from Windows
  - **"port is already allocated"**: Another service using port 8080 - use different port: `-p 8081:80`
  - **"Permission denied" in WSL**: Add user to docker group: `sudo usermod -aG docker $USER` then logout/login
  - **Image pull fails**: Check internet connection, try `docker pull nginx` to test
  - **Container immediately exits**: Check logs: `docker logs <container-id>` for errors
  - **"Cannot remove container"**: Container is running - stop it first: `docker stop <container-id>`

  💡 **Learning moment**: Containers vs VMs - Containers share the host OS kernel (lightweight, fast), while VMs run a full OS (heavy, slower). Containers start in milliseconds!

  💡 **Best practices learned**:
  - Use `--name` to give containers meaningful names instead of random IDs
  - Use `--rm` for temporary containers to auto-cleanup
  - Use `-p` to expose only necessary ports
  - Always check logs when things don't work: `docker logs <container>`

- **Labels**: docker, learning, exploration, phase-3
- **Estimated Effort**: Small (30-45 mins)
- **Status**: Backlog
- **Dependencies**: Task 3.1

**Note**: Install Docker Desktop (Task 3.1) first, then do this exploration before creating your own Dockerfiles.

### Task 3.1: Install Docker Desktop on Windows
- **Description**: Install Docker Desktop for Windows with WSL 2 backend integration. Docker Desktop provides Docker Engine, Docker CLI, Docker Compose, and a nice GUI for managing containers.

  **Step 1: Download Docker Desktop**
  1. Open your browser and go to: https://www.docker.com/products/docker-desktop
  2. Click "Download for Windows"
  3. Save the installer: `Docker Desktop Installer.exe` (~500 MB)

  **Step 2: Run the Installer** (Windows PowerShell as Administrator)
  ```powershell
  # Navigate to your Downloads folder
  cd $env:USERPROFILE\Downloads

  # Run the installer
  .\Docker` Desktop` Installer.exe install

  # Or just double-click the installer from File Explorer
  ```

  **During installation**:
  - ✅ **IMPORTANT**: Ensure "Use WSL 2 instead of Hyper-V" is **CHECKED**
  - ✅ Ensure "Add shortcut to desktop" is checked (optional but helpful)
  - Click "Ok" and let it install (~5-10 minutes)
  - When prompted, click "Close and restart" to restart your computer

  **Step 3: Start Docker Desktop** (After restart)
  1. Docker Desktop should start automatically after restart
  2. If not, search for "Docker Desktop" in Windows Start menu and launch it
  3. Accept the Docker Subscription Service Agreement
  4. You can skip the tutorial or complete it (optional)
  5. Wait for "Docker Desktop is running" in the system tray

  **Step 4: Configure WSL Integration**
  1. Click the Docker icon in system tray (bottom-right, near clock)
  2. Click the gear icon (⚙️) to open Settings
  3. Navigate to: **Resources → WSL Integration**
  4. Toggle ON: "Enable integration with my default WSL distro"
  5. Toggle ON: "Ubuntu" (or your WSL distro name)
  6. Click "Apply & Restart"
  7. Wait for Docker to restart (~30 seconds)

  **Step 5: Verify Installation** (WSL Ubuntu)
  ```bash
  # Check Docker version
  docker --version
  # Expected: Docker version 24.x.x or higher

  # Check Docker Compose version
  docker compose version
  # Expected: Docker Compose version v2.x.x or higher

  # Verify Docker daemon is running
  docker info

  # Run a test container
  docker run hello-world

  # Check Docker Desktop is connected to WSL
  docker context ls
  # Should show "desktop-linux" as current context
  ```

  **Step 6: Optional - Configure Docker Settings**

  Open Docker Desktop Settings and configure:

  **Resources**:
  - **Memory**: Allocate 4-8 GB (default is usually 2 GB)
  - **CPUs**: Allocate 2-4 CPUs
  - **Swap**: 1-2 GB
  - **Disk image size**: 60+ GB

  **Docker Engine** (optional - for advanced users):
  ```json
  {
    "builder": {
      "gc": {
        "defaultKeepStorage": "20GB",
        "enabled": true
      }
    },
    "features": {
      "buildkit": true
    }
  }
  ```
  This enables BuildKit for faster builds.

  **Expected Outcome**:
  - Docker Desktop running in Windows system tray
  - `docker --version` shows Docker 24.x or higher
  - `docker compose version` shows v2.x or higher
  - `docker run hello-world` completes successfully
  - `docker info` shows system information without errors
  - WSL integration enabled and working
  - You can access Docker commands from both Windows and WSL

  **Common Issues & Solutions**:
  - **"WSL 2 installation is incomplete"**:
    - Run in PowerShell as Admin: `wsl --update`
    - Restart computer
    - If still failing, download WSL2 kernel update from Microsoft: https://aka.ms/wsl2kernel

  - **"Docker Desktop requires Windows 10/11"**:
    - Ensure you have Windows 10 version 19041 or higher, or Windows 11
    - Check version: Run `winver` in Windows
    - Update Windows if needed

  - **"Hyper-V is not enabled"**:
    - We're using WSL 2, not Hyper-V
    - In installer, ensure "Use WSL 2 instead of Hyper-V" is checked
    - If Hyper-V is enabled, that's OK - Docker can use both

  - **"Docker Desktop is starting..." (stuck forever)**:
    - Open Task Manager, end "Docker Desktop" process
    - Restart Docker Desktop
    - Check Windows Event Viewer for errors
    - Try: Settings → Reset → Reset to factory defaults

  - **"docker: command not found" in WSL**:
    - Verify WSL integration is enabled (Step 4)
    - Restart WSL: `wsl --shutdown` in PowerShell, then reopen Ubuntu
    - Check Docker Desktop is running in Windows

  - **"Cannot connect to Docker daemon"**:
    - Docker Desktop not running - start it from Windows Start menu
    - In WSL, run: `docker context use desktop-linux`
    - Check Docker Desktop → Settings → General → "Use the WSL 2 based engine" is checked

  - **Very slow performance**:
    - Increase memory allocation (Settings → Resources)
    - Store project files in WSL filesystem (`~/projects/`), not Windows (`/mnt/c/`)
    - Disable Windows Defender real-time scanning for WSL folders

  - **Port conflicts (can't start Docker)**:
    - Another service might be using Docker's ports
    - Stop other virtualization software (VirtualBox, VMware)
    - In cmd as Admin: `net stop winnat` then restart Docker, then `net start winnat`

  💡 **Learning moment**: Docker Desktop bundles Docker Engine (daemon), Docker CLI (commands), and Docker Compose (orchestration). When you run `docker` in WSL, it talks to the Docker Engine running in Windows via a socket.

  💡 **Important**: Always work with your project files **inside WSL filesystem** (`~/projects/`) rather than Windows filesystem (`/mnt/c/`). Docker performance is 10-20x faster with files in WSL!

  💡 **Resource usage**: Docker Desktop can consume significant resources. You can quit Docker Desktop when not using it - just remember to start it before running Docker commands.

- **Labels**: setup, docker, windows, phase-3
- **Estimated Effort**: Medium (30-45 mins including download time)
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.1 - WSL 2 must be installed)

### Task 3.2: Create Dockerfile for API Service
- **Description**: Create a multi-stage Dockerfile for the ASP.NET Core API service with optimized build and runtime stages. Multi-stage builds keep the final image small by separating build dependencies from runtime dependencies.

  **Step 1: Navigate to your project root** (WSL Ubuntu)
  ```bash
  cd ~/projects/jamtrack-radio
  ```

  **Step 2: Create `Dockerfile` in the API project**

  File: `src/JamtrackRadio.Api/Dockerfile`
  ```dockerfile
  # ================================
  # Build Stage
  # ================================
  FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
  WORKDIR /src

  # Copy solution file
  COPY ["JamtrackRadio.sln", "./"]

  # Copy project files for restore (layer caching optimization)
  # This way, NuGet packages are only restored when .csproj files change
  COPY ["src/JamtrackRadio.Api/JamtrackRadio.Api.csproj", "src/JamtrackRadio.Api/"]
  COPY ["src/JamtrackRadio.Domain/JamtrackRadio.Domain.csproj", "src/JamtrackRadio.Domain/"]

  # If you completed Phase 2B, uncomment these lines:
  # COPY ["src/JamtrackRadio.Infrastructure/JamtrackRadio.Infrastructure.csproj", "src/JamtrackRadio.Infrastructure/"]
  # COPY ["src/JamtrackRadio.Services/JamtrackRadio.Services.csproj", "src/JamtrackRadio.Services/"]

  # Restore dependencies
  RUN dotnet restore "src/JamtrackRadio.Api/JamtrackRadio.Api.csproj"

  # Copy all source code
  COPY . .

  # Build the application
  WORKDIR "/src/src/JamtrackRadio.Api"
  RUN dotnet build "JamtrackRadio.Api.csproj" -c Release -o /app/build

  # ================================
  # Publish Stage
  # ================================
  FROM build AS publish
  RUN dotnet publish "JamtrackRadio.Api.csproj" -c Release -o /app/publish /p:UseAppHost=false

  # ================================
  # Runtime Stage
  # ================================
  FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
  WORKDIR /app

  # Install curl for health checks (optional but useful)
  RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

  # Create non-root user for security
  RUN addgroup --system --gid 1001 appgroup && \
      adduser --system --uid 1001 --ingroup appgroup appuser

  # Copy published output from publish stage
  COPY --from=publish /app/publish .

  # Change ownership to non-root user
  RUN chown -R appuser:appgroup /app

  # Switch to non-root user
  USER appuser

  # Expose port
  EXPOSE 8080
  EXPOSE 8081

  # Set environment variables
  ENV ASPNETCORE_URLS=http://+:8080
  ENV ASPNETCORE_ENVIRONMENT=Production

  # Health check
  HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

  # Run the application
  ENTRYPOINT ["dotnet", "JamtrackRadio.Api.dll"]
  ```

  **Step 3: Create a simple health endpoint** (if you don't have one yet)

  Update `Program.cs` to add a health check endpoint:
  ```csharp
  // Add this before app.MapControllers();
  app.MapGet("/health", () => Results.Ok(new { status = "healthy", timestamp = DateTime.UtcNow }));
  ```

  **Step 4: Build the Docker image** (from project root)
  ```bash
  cd ~/projects/jamtrack-radio

  # Build the image (this will take a few minutes the first time)
  docker build -f src/JamtrackRadio.Api/Dockerfile -t jamtrack-api:latest .

  # Watch the build process - you'll see each layer being built
  ```

  **Step 5: Verify the image was created**
  ```bash
  # List Docker images
  docker images | grep jamtrack-api

  # Check image size (should be ~200-250 MB)
  docker images jamtrack-api:latest

  # Inspect the image
  docker inspect jamtrack-api:latest
  ```

  **Step 6: Test run the container**
  ```bash
  # Run the container (note: database connection will fail without Postgres)
  docker run -d -p 5000:8080 --name jamtrack-api-test jamtrack-api:latest

  # Check if it's running
  docker ps

  # View logs
  docker logs jamtrack-api-test

  # Test health endpoint
  curl http://localhost:5000/health

  # Stop and remove test container
  docker stop jamtrack-api-test
  docker rm jamtrack-api-test
  ```

  **Expected Outcome**:
  - `Dockerfile` created in `src/JamtrackRadio.Api/`
  - Docker image built successfully: `jamtrack-api:latest`
  - Image size is ~200-250 MB (much smaller than the SDK image which is ~1.2 GB)
  - Image appears in `docker images` list
  - Test container runs and responds to health check
  - Application logs show startup messages

  **Common Issues & Solutions**:
  - **"COPY failed: no such file or directory"**:
    - Ensure you're running `docker build` from the project root (`~/projects/jamtrack-radio`)
    - The build context (`.`) must include the solution file and all projects
    - Check the `-f` path points to the correct Dockerfile location

  - **"error: The current .NET SDK does not support targeting .NET 8.0"**:
    - Update the base image to a newer version: `mcr.microsoft.com/dotnet/sdk:8.0-alpine`
    - Or change to the SDK version you have installed

  - **Build is very slow**:
    - First build always takes longer (downloading base images and NuGet packages)
    - Subsequent builds should be faster due to layer caching
    - Ensure Docker Desktop has enough memory allocated (4+ GB)

  - **"Unable to load project" errors during build**:
    - Check that all COPY paths in Dockerfile match your actual project structure
    - If you completed Phase 2B, uncomment the Infrastructure and Services project lines
    - Verify solution file includes all necessary projects: `dotnet sln list`

  - **Image size is huge (> 1 GB)**:
    - Ensure you're using multi-stage build correctly
    - Final stage should use `aspnet:8.0` (runtime) not `sdk:8.0` (build tools)
    - Check you're copying from the `publish` stage, not the `build` stage

  - **Health check always failing**:
    - Verify `/health` endpoint exists in your API
    - Check logs: `docker logs <container-id>`
    - The health check runs inside the container, so it uses `localhost:8080` not the exposed port
    - You might need to wait for the app to fully start (--start-period)

  - **"Permission denied" errors in container**:
    - This can happen with volume mounts
    - Ensure the non-root user (appuser) has necessary permissions
    - For now (without volumes), this shouldn't be an issue

  - **Build context is too large (slow upload to Docker daemon)**:
    - Create a `.dockerignore` file (Task 3.4)
    - Exclude `bin/`, `obj/`, `node_modules/`, `.git/`

  💡 **Learning moment - Multi-stage builds**:
  - **Build stage** uses the full SDK (~1.2 GB) with compilers and build tools
  - **Publish stage** creates optimized output
  - **Runtime stage** uses only the lightweight runtime (~200 MB) - doesn't include SDK
  - Final image only contains the runtime stage = small, fast, secure!

  💡 **Learning moment - Layer caching**:
  Notice how we COPY .csproj files before COPY everything? This is intentional! Docker caches each layer. If only source code changes (not project files), Docker reuses the cached restore layer instead of re-downloading all NuGet packages. This makes builds much faster!

  💡 **Learning moment - Non-root user**:
  Running as root in containers is a security risk. If an attacker compromises your app, they'd have root access. By creating and switching to a non-root user (`appuser`), we limit the damage potential.

  💡 **Learning moment - ASPNETCORE_URLS**:
  In .NET 8+, the default is HTTPS on 8081 and HTTP on 8080. By setting `ASPNETCORE_URLS=http://+:8080`, we tell the app to listen on HTTP port 8080. In production, you'd typically put a reverse proxy (nginx, ingress) in front that handles HTTPS.

  **Dockerfile breakdown**:
  - **Line 1-5**: Build stage - starts with SDK image, sets working directory
  - **Line 7-15**: Copy project files for layer caching optimization
  - **Line 17-18**: Restore NuGet packages (cached if .csproj unchanged)
  - **Line 20-24**: Copy all code and build
  - **Line 27-29**: Publish stage - creates optimized publish output
  - **Line 32-34**: Runtime stage - starts fresh with lightweight runtime image
  - **Line 36-37**: Install curl for health checks
  - **Line 39-43**: Create non-root user and switch to it
  - **Line 45-46**: Copy only the published output (not source code!)
  - **Line 51-54**: Expose ports and set environment
  - **Line 56-58**: Configure health check
  - **Line 60-61**: Define startup command

- **Labels**: docker, backend, dockerfile, phase-3
- **Estimated Effort**: Medium (45-60 mins)
- **Status**: Backlog
- **Dependencies**: Task 3.0

### Task 3.3: Create Dockerfile for gRPC Service (Optional)
- **Description**: **(OPTIONAL)** Create multi-stage Dockerfile for the gRPC service if you completed Phase 2B. Skip this if you only completed Phase 2A.

  **Dockerfile features**:
  - Multi-stage build
  - gRPC port exposure (5001, 5002)
  - Health check for gRPC
  - Production-ready configuration
- **Labels**: docker, backend, grpc, dockerfile, phase-3, optional
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Phase 2B (Task 2B.9) OR skip if only completed Phase 2A

### Task 3.4: Create .dockerignore File
- **Description**: Create `.dockerignore` file to exclude unnecessary files from the Docker build context. This significantly speeds up builds and reduces image size by preventing unnecessary files from being sent to the Docker daemon.

  **Step 1: Create `.dockerignore` in project root** (WSL Ubuntu)
  ```bash
  cd ~/projects/jamtrack-radio
  ```

  File: `.dockerignore`
  ```gitignore
  # Git
  .git
  .gitignore
  .gitattributes

  # Documentation
  *.md
  README.md
  LICENSE
  CONTRIBUTING.md
  docs/

  # IDE and editor files
  .vs/
  .vscode/
  .idea/
  *.suo
  *.user
  *.userosscache
  *.sln.docstates

  # Build outputs
  **/bin/
  **/obj/
  **/out/
  **/publish/

  # Test projects and coverage
  **/tests/
  **/test/
  **/*.Tests/
  **/*.Test/
  coverage/
  TestResults/
  *.trx
  *.coverage

  # NuGet packages (will be restored during build)
  **/packages/
  *.nupkg
  *.snupkg

  # Docker files (don't need these in build context)
  **/*.md
  **/Dockerfile*
  **/.dockerignore
  **/docker-compose*

  # CI/CD
  .github/
  azure-pipelines.yml
  .gitlab-ci.yml

  # Logs and databases
  *.log
  *.sqlite
  *.db

  # OS files
  .DS_Store
  Thumbs.db
  desktop.ini

  # Environment and secrets
  .env
  .env.*
  *.pfx
  *.p12
  *.key
  *.pem
  appsettings.Development.json
  appsettings.*.json
  !appsettings.json
  !appsettings.Production.json

  # Node (if you add frontend later)
  node_modules/
  npm-debug.log
  yarn-error.log

  # Temporary files
  *.tmp
  *.temp
  *.swp
  *~

  # Project-specific (optional)
  project-tasks/
  CLAUDE.md
  ```

  **Step 2: Verify the .dockerignore is working**
  ```bash
  # Rebuild the Docker image
  docker build -f src/JamtrackRadio.Api/Dockerfile -t jamtrack-api:latest .

  # The build should be faster now, especially the "Sending build context" step
  # Watch the first line: "Sending build context to Docker daemon: XXX kB"
  # It should be much smaller than before
  ```

  **Step 3: Test the difference (optional)**
  ```bash
  # See what files are included in build context
  # This command shows files Docker would send (but doesn't actually build)
  docker build -f src/JamtrackRadio.Api/Dockerfile --no-cache -t jamtrack-api:test . 2>&1 | head -20

  # Check build context size
  # Before .dockerignore: might be 50-100 MB+
  # After .dockerignore: should be < 10 MB
  ```

  **Expected Outcome**:
  - `.dockerignore` file created in project root
  - Docker build is faster (especially "Sending build context" step)
  - Build context size reduced from 50-100 MB to < 10 MB
  - Unnecessary files (bin, obj, .git, docs) excluded from image
  - Sensitive files (.env, *.pfx) never sent to Docker daemon

  **Common Issues & Solutions**:
  - **".dockerignore not being applied"**:
    - Ensure `.dockerignore` is in the same directory as your build context (project root)
    - When you run `docker build ... .`, the `.dockerignore` must be in that `.` directory
    - File must be named exactly `.dockerignore` (with the dot, no extension)

  - **"Still seeing large build context"**:
    - Check for large files in your project: `du -sh ./* | sort -h`
    - Add specific large directories to .dockerignore
    - On Windows, use Git Bash or WSL to create the file (not Notepad)

  - **"Build fails after adding .dockerignore"**:
    - You might have excluded something Docker needs
    - Temporarily remove .dockerignore and rebuild to verify
    - Add back patterns one by one to find the culprit
    - Common mistake: excluding the `src/` directory itself

  - **".dockerignore file not found" (on Windows)**:
    - Use WSL or Git Bash to create the file
    - Windows Explorer might not let you create files starting with `.`
    - In PowerShell: `New-Item -Name ".dockerignore" -ItemType File`

  - **"Patterns not working as expected"**:
    - Use `**/pattern` to match at any level (e.g., `**/bin/`)
    - Use `!pattern` to negate (include) a pattern that was excluded
    - `.dockerignore` uses Go's filepath.Match, not regex

  💡 **Learning moment**: The `.dockerignore` file works like `.gitignore` but for Docker. When you run `docker build`, Docker first sends ALL files in the build context to the Docker daemon. Without `.dockerignore`, this includes `bin/`, `obj/`, `.git/`, which can be hundreds of MBs! With `.dockerignore`, you send only what's needed (~10 MB), making builds much faster.

  💡 **Why exclude bin/ and obj/?**: These are build artifacts that will be regenerated during the Docker build anyway. Including them wastes time and space. They also might contain builds for a different platform (Windows vs Linux).

  💡 **Security note**: The `.dockerignore` prevents sensitive files (`.env`, `*.pfx`, appsettings.Development.json) from being accidentally included in your image. Even if they're not COPY'd in the Dockerfile, they're still sent to the Docker daemon, which could be a security risk in some environments.

  💡 **Best practice**: The pattern `!appsettings.json` is a negation - it means "exclude all appsettings.*.json except appsettings.json and appsettings.Production.json". This way, local dev settings never make it into your production images.

  **What each section excludes**:
  - **Git files**: Version control history (not needed in container)
  - **Documentation**: README, markdown files (container doesn't need these)
  - **IDE files**: Visual Studio, VS Code configs (developer-specific)
  - **Build outputs**: bin/, obj/ folders (will be rebuilt in container)
  - **Test projects**: Unit tests don't run in production containers
  - **Secrets**: .env files, certificates, local settings
  - **CI/CD files**: GitHub workflows, pipelines (not needed in runtime)
  - **OS files**: Windows/Mac system files

- **Labels**: docker, configuration, optimization, phase-3
- **Estimated Effort**: Small (10-15 mins)
- **Status**: Backlog
- **Dependencies**: Task 3.2

### Task 3.5: Create Docker Compose Configuration
- **Description**: Create `docker-compose.yml` to orchestrate all services locally (API, Postgres, and optionally gRPC). Docker Compose lets you define and run multi-container applications with a single command.

  **Step 1: Create docker-compose.yml in project root** (WSL Ubuntu)
  ```bash
  cd ~/projects/jamtrack-radio
  ```

  File: `docker-compose.yml`
  ```yaml
  version: '3.8'

  services:
    # ================================
    # PostgreSQL Database
    # ================================
    postgres:
      image: postgres:16-alpine
      container_name: jamtrack-postgres
      restart: unless-stopped
      environment:
        POSTGRES_DB: jamtrackradio
        POSTGRES_USER: postgres
        POSTGRES_PASSWORD: postgres
        PGDATA: /var/lib/postgresql/data/pgdata
      ports:
        - "5432:5432"
      volumes:
        - postgres-data:/var/lib/postgresql/data
      networks:
        - jamtrack-network
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U postgres"]
        interval: 10s
        timeout: 5s
        retries: 5

    # ================================
    # Jamtrack Radio API (REST)
    # ================================
    jamtrack-api:
      build:
        context: .
        dockerfile: src/JamtrackRadio.Api/Dockerfile
      image: jamtrack-api:latest
      container_name: jamtrack-api
      restart: unless-stopped
      environment:
        ASPNETCORE_ENVIRONMENT: Development
        ASPNETCORE_URLS: http://+:8080
        ConnectionStrings__DefaultConnection: "Host=postgres;Port=5432;Database=jamtrackradio;Username=postgres;Password=postgres"
      ports:
        - "5000:8080"
      depends_on:
        postgres:
          condition: service_healthy
      networks:
        - jamtrack-network
      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
        interval: 30s
        timeout: 3s
        retries: 3
        start_period: 10s

    # ================================
    # Jamtrack Radio gRPC (Optional)
    # ================================
    # Uncomment this section if you completed Phase 2B and want to run gRPC service
    # jamtrack-grpc:
    #   build:
    #     context: .
    #     dockerfile: src/JamtrackRadio.GrpcService/Dockerfile
    #   image: jamtrack-grpc:latest
    #   container_name: jamtrack-grpc
    #   restart: unless-stopped
    #   environment:
    #     ASPNETCORE_ENVIRONMENT: Development
    #     ASPNETCORE_URLS: http://+:5001
    #     ConnectionStrings__DefaultConnection: "Host=postgres;Port=5432;Database=jamtrackradio;Username=postgres;Password=postgres"
    #   ports:
    #     - "5001:5001"
    #   depends_on:
    #     postgres:
    #       condition: service_healthy
    #   networks:
    #     - jamtrack-network
    #   healthcheck:
    #     test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
    #     interval: 30s
    #     timeout: 3s
    #     retries: 3
    #     start_period: 10s

  # ================================
  # Networks
  # ================================
  networks:
    jamtrack-network:
      driver: bridge
      name: jamtrack-network

  # ================================
  # Volumes
  # ================================
  volumes:
    postgres-data:
      driver: local
      name: jamtrack-postgres-data
  ```

  **Step 2: Create .env file for environment variables** (optional but recommended)

  File: `.env`
  ```bash
  # Database configuration
  POSTGRES_DB=jamtrackradio
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres

  # API configuration
  ASPNETCORE_ENVIRONMENT=Development

  # Ports
  API_PORT=5000
  GRPC_PORT=5001
  POSTGRES_PORT=5432
  ```

  **Update docker-compose.yml to use .env** (if created):
  ```yaml
  # In postgres service, replace hardcoded values with:
  environment:
    POSTGRES_DB: ${POSTGRES_DB:-jamtrackradio}
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}

  # In ports section:
  ports:
    - "${POSTGRES_PORT:-5432}:5432"
  ```

  **Step 3: Add .env to .gitignore** (IMPORTANT for security)
  ```bash
  echo ".env" >> .gitignore
  echo ".env.local" >> .gitignore
  ```

  **Step 4: Create .env.example** (template for other developers)

  File: `.env.example`
  ```bash
  # Copy this file to .env and update with your values

  # Database configuration
  POSTGRES_DB=jamtrackradio
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=postgres

  # API configuration
  ASPNETCORE_ENVIRONMENT=Development

  # Ports
  API_PORT=5000
  GRPC_PORT=5001
  POSTGRES_PORT=5432
  ```

  **Step 5: Update ConnectionString in appsettings.json**

  Edit `src/JamtrackRadio.Api/appsettings.json`:
  ```json
  {
    "ConnectionStrings": {
      "DefaultConnection": "Host=localhost;Port=5432;Database=jamtrackradio;Username=postgres;Password=postgres"
    },
    "Logging": {
      "LogLevel": {
        "Default": "Information",
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore.Database.Command": "Information"
      }
    },
    "AllowedHosts": "*"
  }
  ```

  **Note**: When running via Docker Compose, the connection string in the environment variable (using `Host=postgres`) will override this. When running locally without Docker, it will use `Host=localhost`.

  **Expected Outcome**:
  - `docker-compose.yml` created in project root
  - `.env` file created with configuration (optional)
  - `.env.example` committed to Git as a template
  - `.env` added to `.gitignore` (secrets protected)
  - Three services defined: postgres, jamtrack-api, (optionally jamtrack-grpc)
  - Network created for inter-container communication
  - Volume created for Postgres data persistence
  - Health checks configured for all services
  - Dependencies properly defined (API waits for healthy database)

  **Common Issues & Solutions**:
  - **"version is obsolete" warning**:
    - Compose v3.8 is fine, but you can remove the `version:` line entirely for newer Docker Compose
    - This warning is harmless - your compose file will still work

  - **"Build failed" errors**:
    - Ensure Dockerfile paths are correct: `dockerfile: src/JamtrackRadio.Api/Dockerfile`
    - Ensure build context is project root: `context: .`
    - Run `docker compose build` to see detailed error messages

  - **"Cannot connect to database" from API**:
    - Check the connection string uses `Host=postgres` (container name), not `Host=localhost`
    - Verify postgres service is healthy: `docker compose ps`
    - Check logs: `docker compose logs postgres`
    - Wait a bit - sometimes the API starts before Postgres is ready (though `depends_on` should prevent this)

  - **"Port is already allocated"**:
    - Another service is using the port (e.g., local Postgres using 5432)
    - Change the external port in docker-compose.yml: `"5433:5432"` instead of `"5432:5432"`
    - Stop the conflicting service first

  - **"Network jamtrack-network declared as external, but could not be found"**:
    - Remove `external: true` from networks section
    - Docker Compose will create the network automatically

  - **"No such file or directory: .env"**:
    - The .env file is optional
    - Either create it or remove `env_file:` directives from docker-compose.yml
    - Docker Compose will use inline `environment:` values if no .env file exists

  - **Volumes not persisting data**:
    - Check volume is defined in `volumes:` section at bottom
    - Verify volume is mounted correctly: `volumes: - postgres-data:/var/lib/postgresql/data`
    - View volumes: `docker volume ls`
    - Inspect volume: `docker volume inspect jamtrack-postgres-data`

  - **Services can't communicate**:
    - All services must be on the same network
    - Use container names as hostnames (e.g., `postgres`, `jamtrack-api`)
    - Don't use `localhost` or `127.0.0.1` between containers

  💡 **Learning moment - Service discovery**: In Docker Compose, containers can reach each other using service names as hostnames. The `postgres` service is accessible at `postgres:5432` from the API container. Docker Compose creates DNS entries automatically!

  💡 **Learning moment - Depends_on with health checks**: The `depends_on` with `condition: service_healthy` ensures the API won't start until Postgres is ready. Without this, the API might start first and fail to connect. Health checks make this reliable!

  💡 **Learning moment - Volumes vs bind mounts**:
  - **Volumes** (what we're using): Managed by Docker, stored in Docker's area, work across Windows/Linux/Mac
  - **Bind mounts**: Map to a specific host path, good for development (mounting source code)
  - For databases, always use volumes (better performance and portability)

  💡 **Learning moment - Bridge networks**: The `bridge` driver creates an isolated network. Containers on this network can talk to each other but are isolated from other Docker networks. This is perfect for a multi-service application!

  💡 **Learning moment - Restart policies**:
  - `unless-stopped`: Container always restarts unless you explicitly stop it
  - `always`: Always restarts, even after you stop it manually
  - `on-failure`: Only restarts if container exits with error
  - `no`: Never auto-restart
  For development, `unless-stopped` is usually best.

  💡 **Security best practice**: Never commit `.env` files to Git! They often contain passwords and secrets. Instead, commit `.env.example` as a template. Each developer copies it to `.env` and fills in their own values.

  **Docker Compose file breakdown**:
  - **postgres service**: Official Postgres 16 Alpine image (lightweight)
  - **jamtrack-api service**: Builds from our Dockerfile, connects to postgres
  - **networks**: Creates isolated bridge network for inter-container communication
  - **volumes**: Creates named volume for Postgres data persistence
  - **ports**: Maps host:container ports (e.g., `5000:8080` = localhost:5000 → container:8080)
  - **environment**: Sets environment variables inside containers
  - **depends_on**: Defines startup order and health check dependencies
  - **healthcheck**: Defines how Docker checks if service is healthy
  - **restart**: Defines restart behavior if container crashes

- **Labels**: docker, docker-compose, orchestration, phase-3
- **Estimated Effort**: Large (60-90 mins)
- **Status**: Backlog
- **Dependencies**: Task 3.4

### Task 3.6: Test Docker Compose Setup Locally
- **Description**: Build and run all containers using Docker Compose, verify inter-service communication, and test the complete stack. This validates everything works together!

  **Step 1: Build all images** (WSL Ubuntu)
  ```bash
  cd ~/projects/jamtrack-radio

  # Build all services (this might take 5-10 minutes first time)
  docker compose build

  # Or build with no cache (if you want fresh build)
  docker compose build --no-cache

  # Watch the build progress - you'll see each stage
  ```

  **Step 2: Start all services**
  ```bash
  # Start all services in detached mode (background)
  docker compose up -d

  # Watch logs in real-time (Ctrl+C to stop watching)
  docker compose logs -f

  # Or watch logs for specific service
  docker compose logs -f jamtrack-api
  ```

  **Step 3: Verify all containers are running**
  ```bash
  # List running containers with status
  docker compose ps

  # Expected output:
  # NAME                 STATUS              PORTS
  # jamtrack-postgres    Up (healthy)        0.0.0.0:5432->5432/tcp
  # jamtrack-api         Up (healthy)        0.0.0.0:5000->8080/tcp

  # Check individual service status
  docker compose ps postgres
  docker compose ps jamtrack-api

  # View detailed info
  docker compose ps --format json
  ```

  **Step 4: Check health status**
  ```bash
  # All services should show "healthy" status
  docker compose ps

  # Check logs for health check failures
  docker compose logs postgres | grep -i health
  docker compose logs jamtrack-api | grep -i health

  # Manually test health endpoint
  curl http://localhost:5000/health
  # Expected: {"status":"healthy","timestamp":"2025-01-XX..."}
  ```

  **Step 5: Test database connectivity**
  ```bash
  # Connect to Postgres from host
  docker compose exec postgres psql -U postgres -d jamtrackradio

  # Inside psql, run:
  \dt                           # List tables (should see Tracks, Playlists, Users, etc.)
  SELECT COUNT(*) FROM "Tracks";  # Check if seeded data exists
  SELECT * FROM "Tracks" LIMIT 3; # View sample tracks
  \q                            # Quit psql

  # Or run query directly from host
  docker compose exec postgres psql -U postgres -d jamtrackradio -c '\dt'
  ```

  **Step 6: Test API endpoints**
  ```bash
  # Test health endpoint
  curl http://localhost:5000/health

  # Open Swagger UI in browser
  # Visit: http://localhost:5000/swagger

  # Test GET /api/tracks (should return seeded tracks)
  curl http://localhost:5000/api/tracks

  # Test GET /api/tracks/{id} - copy an ID from previous response
  curl http://localhost:5000/api/tracks/{paste-id-here}

  # Test POST /api/tracks
  curl -X POST http://localhost:5000/api/tracks \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Smoke on the Water",
      "artist": "Deep Purple",
      "album": "Machine Head",
      "durationSeconds": 340
    }'

  # If you have jq installed (for pretty JSON)
  curl http://localhost:5000/api/tracks | jq
  ```

  **Step 7: Test inter-service communication**
  ```bash
  # Verify API can connect to database
  docker compose logs jamtrack-api | grep -i "database"
  docker compose logs jamtrack-api | grep -i "postgres"

  # Should see logs like:
  # "Successfully connected to database"
  # "Executed DbCommand"

  # Test from inside API container
  docker compose exec jamtrack-api curl http://postgres:5432
  # (Will fail but proves network connectivity)
  ```

  **Step 8: Check volumes and persistence**
  ```bash
  # List Docker volumes
  docker volume ls | grep jamtrack

  # Inspect Postgres volume
  docker volume inspect jamtrack-postgres-data

  # Test data persistence:
  # 1. Add a track via API (Step 6)
  # 2. Stop all services
  docker compose down

  # 3. Start services again
  docker compose up -d

  # 4. Verify your track still exists
  curl http://localhost:5000/api/tracks

  # The track you added should still be there!
  ```

  **Step 9: Check logs for errors**
  ```bash
  # View all logs
  docker compose logs

  # View logs for specific service
  docker compose logs postgres
  docker compose logs jamtrack-api

  # Follow logs in real-time
  docker compose logs -f --tail=100

  # Search for errors
  docker compose logs | grep -i error
  docker compose logs | grep -i exception
  docker compose logs | grep -i fail
  ```

  **Step 10: Cleanup (when done testing)**
  ```bash
  # Stop all services
  docker compose stop

  # Stop and remove containers (keeps volumes/data)
  docker compose down

  # Stop, remove containers AND volumes (fresh start)
  docker compose down -v

  # Remove images as well
  docker compose down --rmi all

  # Full cleanup (everything)
  docker compose down -v --rmi all --remove-orphans
  ```

  **Expected Outcome**:
  - All containers built successfully without errors
  - All services running with "healthy" status
  - Postgres database created with tables and seeded data
  - API accessible at http://localhost:5000
  - Swagger UI working at http://localhost:5000/swagger
  - All API endpoints responding correctly
  - Database queries working (GET /api/tracks returns data)
  - Can create new tracks (POST /api/tracks)
  - Data persists after restart (`docker compose down` then `up`)
  - No error messages in logs
  - Inter-service communication working (API → Postgres)

  **Common Issues & Solutions**:
  - **"network jamtrack-network not found"**:
    - Run `docker compose up` (without `-d` first) to see detailed errors
    - Try: `docker network create jamtrack-network`
    - Or let Docker Compose create it automatically on first run

  - **"Container is unhealthy"**:
    - Check logs: `docker compose logs <service-name>`
    - Check health check command in docker-compose.yml
    - Wait longer - health checks run on intervals (10-30 seconds)
    - Verify the health endpoint exists: `curl http://localhost:5000/health`

  - **API can't connect to database**:
    - Verify connection string uses `Host=postgres`, not `Host=localhost`
    - Check both containers are on same network: `docker network inspect jamtrack-network`
    - Check postgres is healthy: `docker compose ps postgres`
    - View postgres logs: `docker compose logs postgres | grep "ready to accept connections"`

  - **"bind: address already in use"**:
    - Port 5000, 5432, or 5001 is already in use
    - Find what's using the port: `lsof -i :5000` or `netstat -tulpn | grep 5000`
    - Stop the conflicting service, or change ports in docker-compose.yml

  - **"404 Not Found" on Swagger**:
    - Ensure `AddSwaggerGen()` and `UseSwagger()` are in Program.cs
    - Check ASPNETCORE_ENVIRONMENT is set to Development
    - Try: `http://localhost:5000/swagger/index.html`

  - **No seeded data (empty tracks)**:
    - Check if database seeder ran: `docker compose logs jamtrack-api | grep -i "seed"`
    - Verify seeder is called in Program.cs
    - Manually run seeder (might need to add a seed endpoint)
    - Or run migrations: `docker compose exec jamtrack-api dotnet ef database update`

  - **"Cannot connect to Docker daemon"**:
    - Docker Desktop not running - start it
    - In WSL, verify: `docker ps` works
    - Check Docker Desktop → Settings → Resources → WSL Integration

  - **Build fails with "no such file or directory"**:
    - Verify you're in project root: `~/projects/jamtrack-radio`
    - Check Dockerfile paths in docker-compose.yml
    - Ensure .dockerignore isn't excluding necessary files

  - **Very slow performance**:
    - Ensure project files are in WSL filesystem (`~/projects/`), not `/mnt/c/`
    - Increase Docker Desktop memory (Settings → Resources)
    - Use BuildKit: `DOCKER_BUILDKIT=1 docker compose build`

  💡 **Learning moment - Docker Compose commands**:
  - `docker compose up`: Start services (Ctrl+C stops them)
  - `docker compose up -d`: Start in detached/background mode
  - `docker compose down`: Stop and remove containers (keeps volumes)
  - `docker compose ps`: List services status
  - `docker compose logs`: View logs from all services
  - `docker compose exec <service> <command>`: Run command in running container
  - `docker compose build`: Build/rebuild images
  - `docker compose restart`: Restart services

  💡 **Learning moment - Debugging workflow**:
  1. `docker compose ps` - check status
  2. `docker compose logs <service>` - read logs
  3. `docker compose exec <service> sh` - get shell inside container
  4. Test connectivity, check files, debug issue
  5. Fix code/config, rebuild: `docker compose build`
  6. Restart: `docker compose up -d --force-recreate`

  💡 **Learning moment - Data persistence**:
  Notice how data survives `docker compose down`? That's because volumes are separate from containers! Volume data persists until you explicitly remove it with `-v` flag. This is crucial for databases in production!

  💡 **Best practice - Logs**: Always check logs when something doesn't work. Logs tell you:
  - Is the service starting correctly?
  - Are there connection errors?
  - Are health checks passing?
  - Are there exceptions or warnings?
  Start with `docker compose logs` and drill down to specific services.

  💡 **Best practice - Testing workflow**:
  1. Make code changes
  2. Rebuild image: `docker compose build <service>`
  3. Recreate container: `docker compose up -d --force-recreate <service>`
  4. Check logs: `docker compose logs -f <service>`
  5. Test endpoint
  Don't restart all services if only one changed!

  **Success criteria checklist**:
  - [ ] All containers show "healthy" status in `docker compose ps`
  - [ ] Swagger UI loads at http://localhost:5000/swagger
  - [ ] GET /api/tracks returns seeded tracks (5 tracks)
  - [ ] POST /api/tracks creates new track successfully
  - [ ] New track appears in subsequent GET requests
  - [ ] Data persists after `docker compose down` then `up`
  - [ ] No error messages in logs
  - [ ] Can connect to Postgres via `docker compose exec`
  - [ ] Health endpoint returns 200 OK
  - [ ] All database tables exist (\dt in psql shows tables)

- **Labels**: docker, testing, verification, local, phase-3
- **Estimated Effort**: Medium (45-60 mins including troubleshooting)
- **Status**: Backlog
- **Dependencies**: Task 3.5

---

**✅ Phase 3 Complete!** 🎉

**Progress**: [████████████████] 100% through Phase 3
**Time elapsed**: ~5-7 hours total
**What you've accomplished**:
- ✅ Docker Desktop installed and configured with WSL 2
- ✅ Hands-on Docker exploration with 7 practical exercises
- ✅ Production-ready multi-stage Dockerfile for API (~200-250 MB image)
- ✅ .dockerignore optimized (build context reduced from 50-100 MB to < 10 MB)
- ✅ Complete Docker Compose orchestration (API + Postgres + optional gRPC)
- ✅ Network isolation with bridge networking
- ✅ Data persistence with Docker volumes
- ✅ Health checks for all services
- ✅ Full testing and verification of containerized stack
- ✅ Working multi-container application with single command: `docker compose up`

**Achievement unlocked**: 🐳 **Container Master** - You've successfully containerized your entire application!

**Key skills gained**:
- Docker fundamentals (images, containers, volumes, networks)
- Multi-stage Dockerfile optimization
- Docker Compose orchestration
- Container networking and service discovery
- Volume management and data persistence
- Health checks and container monitoring
- Debugging containerized applications

**Statistics**:
- Image size: ~200-250 MB (API) + ~170 MB (Postgres)
- Build time: 5-10 minutes first build, 1-2 minutes subsequent
- Startup time: ~10-20 seconds for full stack
- Services running: 2 containers (3 if including gRPC)
- Lines of Docker code: ~150 (Dockerfile + docker-compose.yml)

**What's next?** You have options:

1. **Phase 4** (Kubernetes & Helm - Recommended):
   - Deploy to local Kubernetes cluster (Minikube)
   - Learn Kubernetes fundamentals
   - Create Helm charts for deployment
   - **Time**: 1-2 weeks
   - **Best for**: Learning container orchestration before cloud deployment

2. **Phase 5** (CI/CD):
   - Set up GitHub Actions workflows
   - Automate builds and tests
   - Learn CI/CD fundamentals
   - **Time**: 1-2 weeks
   - **Best for**: Automating your workflow

3. **Phase 6** (Monitoring):
   - Add ELK stack for logging
   - Implement structured logging
   - Create dashboards
   - **Time**: 1 week
   - **Best for**: Understanding observability

**Recommendation**: Continue to Phase 4 (Kubernetes) to learn orchestration concepts before jumping to cloud deployment. Kubernetes skills are essential for modern cloud deployments!

**Quick commands reference**:
```bash
# Start the entire stack
docker compose up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down

# Rebuild after code changes
docker compose build
docker compose up -d --force-recreate

# Fresh start (removes volumes)
docker compose down -v
docker compose up -d

# Access database
docker compose exec postgres psql -U postgres -d jamtrackradio

# Test API
curl http://localhost:5000/api/tracks
```

**Your containerized application is production-ready for deployment!** 🚢

---

## Phase 4: Local Kubernetes & Helm
**Phase Description**: Deploy containerized application to local Kubernetes cluster (Minikube or kind), create Helm charts for service deployment and configuration management.

**Priority**: High

**Labels**: phase-4, kubernetes, helm, orchestration

### Task 4.1: Install Minikube and kubectl in WSL
- **Description**: Install Minikube for local Kubernetes cluster and kubectl CLI tool.

  **Commands (WSL Ubuntu)**:
  ```bash
  # Install kubectl
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

  # Install Minikube
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube

  # Start Minikube with Docker driver
  minikube start --driver=docker
  kubectl cluster-info
  ```
- **Labels**: setup, kubernetes, minikube, wsl
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 3.1

### Task 4.2: Install Helm in WSL
- **Description**: Install Helm package manager for Kubernetes.

  **Commands (WSL Ubuntu)**:
  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  helm version
  ```
- **Labels**: setup, helm, wsl
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 4.1

### Task 4.3: Create Kubernetes Manifests
- **Description**: Create basic Kubernetes manifests (Deployment, Service, ConfigMap, Secret) for each service before Helm.

  **Manifests to create**:
  - Namespace: jamtrack-radio
  - Deployment: jamtrack-api-deployment.yaml
  - Service: jamtrack-api-service.yaml
  - Deployment: jamtrack-grpc-deployment.yaml
  - Service: jamtrack-grpc-service.yaml
  - StatefulSet: postgres-statefulset.yaml
  - Service: postgres-service.yaml
  - ConfigMap: app-config.yaml
  - Secret: app-secrets.yaml
- **Labels**: kubernetes, manifests, yaml
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 4.2

### Task 4.4: Create Helm Chart Structure
- **Description**: Initialize Helm chart for Jamtrack Radio with proper directory structure.

  **Commands**:
  ```bash
  helm create jamtrack-radio
  ```

  **Structure**:
  - Chart.yaml - Chart metadata
  - values.yaml - Default configuration values
  - templates/ - Kubernetes manifest templates
  - charts/ - Dependency charts
- **Labels**: helm, chart, structure
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 4.3

### Task 4.5: Implement Helm Templates
- **Description**: Convert Kubernetes manifests to Helm templates with parameterized values.

  **Templates to create**:
  - deployment.yaml for API
  - deployment.yaml for gRPC
  - service.yaml for API
  - service.yaml for gRPC
  - statefulset.yaml for Postgres
  - configmap.yaml
  - secret.yaml
  - ingress.yaml (optional)

  **Use Helm templating**:
  - {{ .Values.* }} for parameterization
  - {{ .Release.* }} for release info
  - Conditional logic with {{ if }}
- **Labels**: helm, templates, yaml
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 4.4

### Task 4.6: Configure Helm Values Files
- **Description**: Create values.yaml files for different environments (dev, staging, prod).

  **Values to configure**:
  - Image repositories and tags
  - Resource limits and requests
  - Replica counts
  - Environment variables
  - Database connection strings
  - Service ports
- **Labels**: helm, configuration, values
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 4.5

### Task 4.7: Deploy to Minikube using Helm
- **Description**: Deploy Jamtrack Radio to local Minikube cluster using Helm chart and verify all services.

  **Commands**:
  ```bash
  # Build and load images to Minikube
  eval $(minikube docker-env)
  docker build -t jamtrack-api:local ./src/JamtrackRadio.Api
  docker build -t jamtrack-grpc:local ./src/JamtrackRadio.GrpcService

  # Install Helm chart
  helm install jamtrack-radio ./helm/jamtrack-radio

  # Verify deployment
  kubectl get pods -n jamtrack-radio
  kubectl get services -n jamtrack-radio
  helm list
  ```

  **Test**:
  - Port-forward to access services locally
  - Verify API endpoints
  - Verify gRPC connectivity
- **Labels**: helm, kubernetes, deployment, local
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 4.6

---

## Phase 5: CI/CD Pipeline with GitHub Actions
**Phase Description**: Create automated CI/CD pipelines using GitHub Actions for building, testing, and deploying the application.

**Priority**: High

**Labels**: phase-5, ci-cd, github-actions, automation

### Task 5.1: Create GitHub Actions Workflow for Build
- **Description**: Create workflow to build .NET application on every push and pull request.

  **Workflow file**: .github/workflows/build.yml

  **Steps**:
  - Checkout code
  - Setup .NET SDK
  - Restore dependencies
  - Build solution
  - Upload build artifacts
- **Labels**: ci-cd, github-actions, build
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.12)

### Task 5.2: Create GitHub Actions Workflow for Testing
- **Description**: Create workflow to run unit tests and integration tests.

  **Workflow file**: .github/workflows/test.yml

  **Steps**:
  - Setup test environment
  - Run unit tests
  - Run integration tests (with test database)
  - Generate code coverage report
  - Upload coverage to Codecov or similar
- **Labels**: ci-cd, github-actions, testing
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 5.1

### Task 5.3: Create Unit Tests
- **Description**: Implement unit tests for domain models, services, and repositories using xUnit.

  **Create test projects**:
  ```bash
  dotnet new xunit -n JamtrackRadio.Tests -o tests/JamtrackRadio.Tests
  dotnet add tests/JamtrackRadio.Tests package Moq
  dotnet add tests/JamtrackRadio.Tests package FluentAssertions
  ```

  **Test coverage for**:
  - TrackService
  - PlaylistService
  - Repository operations
  - Domain model validation
- **Labels**: testing, unit-tests, csharp
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.8)

### Task 5.4: Create Integration Tests
- **Description**: Implement integration tests for API endpoints and database operations using WebApplicationFactory.

  **Test scenarios**:
  - API endpoint tests
  - Database integration tests
  - gRPC service tests
  - End-to-end workflows

  **Use**:
  - TestContainers for Postgres
  - WebApplicationFactory for API testing
- **Labels**: testing, integration-tests, csharp
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 5.3

### Task 5.5: Create Docker Build and Push Workflow
- **Description**: Create workflow to build Docker images and push to GitHub Container Registry (GHCR).

  **Workflow file**: .github/workflows/docker-publish.yml

  **Steps**:
  - Checkout code
  - Setup Docker Buildx
  - Login to GHCR
  - Build and tag images
  - Push images to GHCR
  - Tag with git SHA and latest
- **Labels**: ci-cd, github-actions, docker
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 3.6

### Task 5.6: Create Helm Chart Linting Workflow
- **Description**: Create workflow to validate and lint Helm charts.

  **Workflow file**: .github/workflows/helm-lint.yml

  **Steps**:
  - Checkout code
  - Setup Helm
  - Run helm lint
  - Run helm template (dry-run)
  - Validate generated manifests
- **Labels**: ci-cd, github-actions, helm
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 4.7

### Task 5.7: Create Deployment Workflow
- **Description**: Create reusable workflow for deploying to different environments (dev, staging, prod).

  **Workflow file**: .github/workflows/deploy.yml

  **Features**:
  - Manual trigger with environment selection
  - Environment-specific secrets
  - Helm upgrade/install
  - Deployment verification
  - Rollback capability
- **Labels**: ci-cd, github-actions, deployment
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 5.5

### Task 5.8: Set Up Branch Protection and Required Checks
- **Description**: Configure branch protection rules for main branch requiring CI checks to pass.

  **Configure**:
  - Require pull request reviews
  - Require status checks (build, test, lint)
  - Require branches to be up to date
  - Restrict force pushes
  - Require signed commits (optional)
- **Labels**: github, ci-cd, branch-protection
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 5.7

---

## Phase 6: Monitoring & Observability with ELK
**Phase Description**: Set up the ELK (Elasticsearch, Logstash, Kibana) stack for centralized logging, implement structured logging in the application, and create monitoring dashboards.

**Priority**: Medium

**Labels**: phase-6, monitoring, elk, logging, observability

### Task 6.1: Implement Structured Logging with Serilog
- **Description**: Add Serilog to the application with structured logging to JSON format.

  **Install packages**:
  ```bash
  dotnet add package Serilog.AspNetCore
  dotnet add package Serilog.Sinks.Console
  dotnet add package Serilog.Sinks.File
  dotnet add package Serilog.Sinks.Elasticsearch
  ```

  **Configure**:
  - Log enrichment (timestamp, machine name, environment)
  - Contextual logging with correlation IDs
  - Log levels per environment
  - Sensitive data masking
- **Labels**: logging, serilog, backend
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.11)

### Task 6.2: Add Request/Response Logging Middleware
- **Description**: Create middleware to log HTTP requests and responses with performance metrics.

  **Log information**:
  - Request method, path, query parameters
  - Request/response headers (sanitized)
  - Response status code
  - Request duration
  - User context (if authenticated)
- **Labels**: logging, middleware, backend
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 6.1

### Task 6.3: Set Up ELK Stack with Docker Compose
- **Description**: Add Elasticsearch, Logstash, and Kibana services to Docker Compose for local development.

  **Add services**:
  - Elasticsearch (single node for dev)
  - Logstash (with config for ingesting logs)
  - Kibana (for visualization)
  - Configure volumes for persistence
  - Configure networks for service communication
- **Labels**: elk, docker, monitoring
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 3.6

### Task 6.4: Configure Logstash Pipeline
- **Description**: Create Logstash configuration to ingest logs from application and parse JSON logs.

  **Logstash config**:
  - Input: HTTP or file input from application
  - Filter: JSON parsing, field extraction, grok patterns
  - Output: Elasticsearch with index patterns
- **Labels**: elk, logstash, configuration
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 6.3

### Task 6.5: Create Kibana Dashboards
- **Description**: Create Kibana dashboards for monitoring application health, performance, and errors.

  **Dashboards**:
  - Application overview (request rate, error rate, latency)
  - Error tracking and analysis
  - Performance metrics (response times, slow queries)
  - User activity tracking
  - Custom searches and visualizations
- **Labels**: elk, kibana, dashboards, monitoring
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 6.4

### Task 6.6: Add Health Check Endpoints
- **Description**: Implement health check endpoints for Kubernetes liveness and readiness probes.

  **Endpoints**:
  - /health/live - Liveness probe (application is alive)
  - /health/ready - Readiness probe (ready to accept traffic)
  - /health/startup - Startup probe (application has started)

  **Checks**:
  - Database connectivity
  - External service availability
  - Memory and CPU thresholds
- **Labels**: monitoring, health-checks, backend
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 6.2

---

## Phase 7: Azure Infrastructure with Terraform
**Phase Description**: Use Terraform to provision Azure infrastructure including AKS cluster, Azure Database for PostgreSQL, Azure Container Registry, networking (VNet, subnets), and storage.

**Priority**: High

**Labels**: phase-7, azure, terraform, infrastructure

### Task 7.1: Install Azure CLI and Terraform in WSL
- **Description**: Install Azure CLI and Terraform CLI tools in WSL Ubuntu.

  **Commands (WSL Ubuntu)**:
  ```bash
  # Install Azure CLI
  curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
  az --version
  az login

  # Install Terraform
  wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
  sudo apt update && sudo apt install -y terraform
  terraform --version
  ```
- **Labels**: setup, azure, terraform, wsl
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Phase 0 (Task 0.2)

### Task 7.2: Create Terraform Project Structure
- **Description**: Set up Terraform project structure with modules for reusability.

  **Structure**:
  ```
  terraform/
  ├── azure/
  │   ├── main.tf
  │   ├── variables.tf
  │   ├── outputs.tf
  │   ├── terraform.tfvars
  │   ├── backend.tf
  │   └── modules/
  │       ├── networking/
  │       ├── aks/
  │       ├── acr/
  │       ├── database/
  │       └── storage/
  ```
- **Labels**: terraform, infrastructure, project-structure
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 7.1

### Task 7.3: Create Azure Networking Module
- **Description**: Create Terraform module for Azure VNet, subnets, NSGs, and security rules.

  **Resources**:
  - Resource Group
  - Virtual Network (VNet)
  - Subnets (AKS, database, application gateway)
  - Network Security Groups (NSGs)
  - Route tables
  - Service endpoints
- **Labels**: terraform, azure, networking
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 7.2

### Task 7.4: Create Azure Container Registry (ACR) Module
- **Description**: Create Terraform module for Azure Container Registry to store Docker images.

  **Resources**:
  - ACR with appropriate SKU (Basic/Standard/Premium)
  - Admin access configuration
  - Network rules and private endpoint (optional)
  - Geo-replication (for Premium SKU)
- **Labels**: terraform, azure, acr, docker
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 7.3

### Task 7.5: Create Azure Kubernetes Service (AKS) Module
- **Description**: Create Terraform module for AKS cluster with node pools and configurations.

  **Resources**:
  - AKS cluster
  - System node pool
  - User node pool (for application workloads)
  - Managed identity
  - Network plugin (Azure CNI)
  - Network policy (Calico/Azure)
  - RBAC configuration
  - Integration with ACR
- **Labels**: terraform, azure, aks, kubernetes
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 7.4

### Task 7.6: Create Azure Database for PostgreSQL Module
- **Description**: Create Terraform module for managed PostgreSQL database.

  **Resources**:
  - Azure Database for PostgreSQL Flexible Server
  - Firewall rules
  - VNet integration
  - Backup configuration
  - High availability settings (optional)
  - Database and user creation
- **Labels**: terraform, azure, database, postgres
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 7.3

### Task 7.7: Create Azure Storage Module
- **Description**: Create Terraform module for Azure Storage Account for music file storage.

  **Resources**:
  - Storage Account
  - Blob container for music files
  - Access policies and SAS tokens
  - Network rules
  - Lifecycle management policies
- **Labels**: terraform, azure, storage
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 7.3

### Task 7.8: Configure Terraform Backend with Azure Storage
- **Description**: Set up Terraform remote backend using Azure Storage Account for state management.

  **Steps**:
  1. Create storage account for Terraform state
  2. Create blob container
  3. Configure backend.tf with Azure storage
  4. Initialize Terraform with backend
  5. Verify state is stored remotely
- **Labels**: terraform, azure, backend, state
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 7.2

### Task 7.9: Apply Terraform Configuration to Azure
- **Description**: Run Terraform plan and apply to provision all Azure infrastructure.

  **Commands**:
  ```bash
  cd terraform/azure
  terraform init
  terraform validate
  terraform plan -out=tfplan
  terraform apply tfplan
  ```

  **Verify**:
  - All resources created successfully
  - AKS cluster accessible via kubectl
  - ACR can be logged into
  - Database accessible
  - Document outputs (endpoints, connection strings)
- **Labels**: terraform, azure, deployment, infrastructure
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 7.8

---

## Phase 8: Azure Deployment
**Phase Description**: Deploy Jamtrack Radio application to Azure Kubernetes Service, configure ingress, SSL certificates, and connect to Azure services.

**Priority**: High

**Labels**: phase-8, azure, deployment, kubernetes

### Task 8.1: Configure kubectl for AKS
- **Description**: Get AKS credentials and configure kubectl to connect to Azure cluster.

  **Commands**:
  ```bash
  az aks get-credentials --resource-group jamtrack-rg --name jamtrack-aks
  kubectl config get-contexts
  kubectl config use-context jamtrack-aks
  kubectl get nodes
  ```
- **Labels**: azure, aks, kubectl, setup
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 7.9

### Task 8.2: Push Docker Images to Azure Container Registry
- **Description**: Build and push Docker images to ACR for deployment.

  **Commands**:
  ```bash
  # Login to ACR
  az acr login --name jamtrackacr

  # Tag images
  docker tag jamtrack-api:latest jamtrackacr.azurecr.io/jamtrack-api:v1.0.0
  docker tag jamtrack-grpc:latest jamtrackacr.azurecr.io/jamtrack-grpc:v1.0.0

  # Push images
  docker push jamtrackacr.azurecr.io/jamtrack-api:v1.0.0
  docker push jamtrackacr.azurecr.io/jamtrack-grpc:v1.0.0
  ```
- **Labels**: azure, acr, docker, deployment
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 8.1

### Task 8.3: Create Azure-Specific Helm Values
- **Description**: Create values-azure.yaml file with Azure-specific configurations.

  **Configure**:
  - ACR image repository URLs
  - Azure Database for PostgreSQL connection string
  - Azure Storage connection for music files
  - Resource requests and limits for Azure
  - Ingress configuration
  - Service type (LoadBalancer for Azure)
- **Labels**: azure, helm, configuration
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 8.2

### Task 8.4: Deploy Application to AKS using Helm
- **Description**: Deploy Jamtrack Radio to AKS cluster using Helm chart with Azure values.

  **Commands**:
  ```bash
  # Create namespace
  kubectl create namespace jamtrack-radio

  # Install Helm chart
  helm install jamtrack-radio ./helm/jamtrack-radio \
    -f ./helm/jamtrack-radio/values-azure.yaml \
    -n jamtrack-radio

  # Verify deployment
  kubectl get pods -n jamtrack-radio
  kubectl get services -n jamtrack-radio
  ```
- **Labels**: azure, aks, helm, deployment
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 8.3

### Task 8.5: Configure Ingress Controller and SSL
- **Description**: Install NGINX Ingress Controller on AKS and configure SSL with Let's Encrypt.

  **Steps**:
  1. Install NGINX Ingress Controller via Helm
  2. Install cert-manager for SSL certificates
  3. Create ClusterIssuer for Let's Encrypt
  4. Create Ingress resource with TLS configuration
  5. Configure DNS to point to ingress IP

  **Commands**:
  ```bash
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
  helm install nginx-ingress ingress-nginx/ingress-nginx

  helm repo add jetstack https://charts.jetstack.io
  helm install cert-manager jetstack/cert-manager --set installCRDs=true
  ```
- **Labels**: azure, aks, ingress, ssl, networking
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 8.4

### Task 8.6: Configure Application Insights
- **Description**: Set up Azure Application Insights for monitoring and telemetry.

  **Steps**:
  1. Create Application Insights resource in Azure
  2. Install Application Insights SDK in .NET application
  3. Configure instrumentation key
  4. Enable automatic telemetry collection
  5. Create custom metrics and events
- **Labels**: azure, monitoring, application-insights
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 8.5

### Task 8.7: Verify and Test Azure Deployment
- **Description**: Perform end-to-end testing of Azure deployment and verify all services.

  **Verify**:
  - Application accessible via public URL
  - SSL certificate working
  - API endpoints responding correctly
  - gRPC services accessible
  - Database connectivity working
  - File upload to Azure Storage working
  - Logging to Application Insights working
  - Load balancing across pods
- **Labels**: azure, testing, deployment, verification
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 8.6

---

## Phase 9: AWS Infrastructure with Terraform
**Phase Description**: Create AWS account, use Terraform to provision AWS infrastructure including EKS cluster, RDS PostgreSQL, ECR, VPC networking, and S3 storage.

**Priority**: Medium

**Labels**: phase-9, aws, terraform, infrastructure

### Task 9.1: Create AWS Account
- **Description**: Create AWS account, set up billing alerts, and configure IAM user with appropriate permissions.

  **Steps**:
  1. Sign up at aws.amazon.com
  2. Set up billing alerts and budget
  3. Enable MFA for root account
  4. Create IAM user with administrative access
  5. Generate access key for programmatic access
  6. Document account ID and access keys securely
- **Labels**: setup, aws, account, iam
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: None

### Task 9.2: Install and Configure AWS CLI in WSL
- **Description**: Install AWS CLI v2 in WSL and configure credentials.

  **Commands (WSL Ubuntu)**:
  ```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
  aws --version

  # Configure AWS credentials
  aws configure
  # Enter access key, secret key, region (us-east-1), output format (json)
  ```
- **Labels**: setup, aws, cli, wsl
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 9.1

### Task 9.3: Create Terraform Project Structure for AWS
- **Description**: Set up Terraform project structure for AWS with modules.

  **Structure**:
  ```
  terraform/
  ├── aws/
  │   ├── main.tf
  │   ├── variables.tf
  │   ├── outputs.tf
  │   ├── terraform.tfvars
  │   ├── backend.tf
  │   └── modules/
  │       ├── vpc/
  │       ├── eks/
  │       ├── ecr/
  │       ├── rds/
  │       └── s3/
  ```
- **Labels**: terraform, aws, infrastructure, project-structure
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 9.2

### Task 9.4: Create AWS VPC Networking Module
- **Description**: Create Terraform module for VPC, subnets, route tables, internet gateway, and NAT gateways.

  **Resources**:
  - VPC with CIDR block
  - Public subnets (for load balancers, NAT gateways)
  - Private subnets (for EKS nodes, RDS)
  - Internet Gateway
  - NAT Gateways (for private subnet internet access)
  - Route tables and associations
  - Security groups
- **Labels**: terraform, aws, vpc, networking
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 9.3

### Task 9.5: Create AWS ECR (Elastic Container Registry) Module
- **Description**: Create Terraform module for ECR repositories to store Docker images.

  **Resources**:
  - ECR repositories for each service
  - Repository policies
  - Lifecycle policies (image retention)
  - Scan on push configuration
- **Labels**: terraform, aws, ecr, docker
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 9.4

### Task 9.6: Create AWS EKS (Elastic Kubernetes Service) Module
- **Description**: Create Terraform module for EKS cluster with managed node groups.

  **Resources**:
  - EKS cluster
  - Cluster IAM role and policies
  - Managed node group
  - Node IAM role and policies
  - Cluster security group
  - OIDC provider for IRSA (IAM Roles for Service Accounts)
  - Add-ons (VPC CNI, CoreDNS, kube-proxy)
- **Labels**: terraform, aws, eks, kubernetes
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 9.5

### Task 9.7: Create AWS RDS PostgreSQL Module
- **Description**: Create Terraform module for managed PostgreSQL database using RDS.

  **Resources**:
  - RDS PostgreSQL instance
  - DB subnet group
  - DB parameter group
  - DB security group
  - Automated backups configuration
  - Multi-AZ deployment (optional)
  - Read replicas (optional)
- **Labels**: terraform, aws, rds, postgres, database
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 9.4

### Task 9.8: Create AWS S3 Module
- **Description**: Create Terraform module for S3 bucket for music file storage.

  **Resources**:
  - S3 bucket with versioning
  - Bucket policy
  - CORS configuration
  - Lifecycle rules
  - Encryption configuration
  - Access logging
- **Labels**: terraform, aws, s3, storage
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 9.4

### Task 9.9: Configure Terraform Backend with S3
- **Description**: Set up Terraform remote backend using S3 bucket and DynamoDB for state locking.

  **Steps**:
  1. Create S3 bucket for Terraform state
  2. Create DynamoDB table for state locking
  3. Configure backend.tf with S3 backend
  4. Initialize Terraform with backend
  5. Verify state is stored remotely
- **Labels**: terraform, aws, backend, state
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 9.3

### Task 9.10: Apply Terraform Configuration to AWS
- **Description**: Run Terraform plan and apply to provision all AWS infrastructure.

  **Commands**:
  ```bash
  cd terraform/aws
  terraform init
  terraform validate
  terraform plan -out=tfplan
  terraform apply tfplan
  ```

  **Verify**:
  - All resources created successfully
  - EKS cluster accessible via kubectl
  - ECR repositories created
  - RDS instance running
  - S3 bucket created
  - Document outputs (endpoints, ARNs)
- **Labels**: terraform, aws, deployment, infrastructure
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 9.9

---

## Phase 10: AWS Deployment
**Phase Description**: Deploy Jamtrack Radio application to Amazon EKS, configure ALB Ingress Controller, SSL certificates, and connect to AWS services.

**Priority**: Medium

**Labels**: phase-10, aws, deployment, kubernetes

### Task 10.1: Configure kubectl for EKS
- **Description**: Update kubeconfig to connect to EKS cluster.

  **Commands**:
  ```bash
  aws eks update-kubeconfig --region us-east-1 --name jamtrack-eks
  kubectl config get-contexts
  kubectl config use-context jamtrack-eks
  kubectl get nodes
  ```
- **Labels**: aws, eks, kubectl, setup
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 9.10

### Task 10.2: Push Docker Images to AWS ECR
- **Description**: Build and push Docker images to ECR for deployment.

  **Commands**:
  ```bash
  # Login to ECR
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

  # Tag images
  docker tag jamtrack-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/jamtrack-api:v1.0.0
  docker tag jamtrack-grpc:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/jamtrack-grpc:v1.0.0

  # Push images
  docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/jamtrack-api:v1.0.0
  docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/jamtrack-grpc:v1.0.0
  ```
- **Labels**: aws, ecr, docker, deployment
- **Estimated Effort**: Small
- **Status**: Backlog
- **Dependencies**: Task 10.1

### Task 10.3: Create AWS-Specific Helm Values
- **Description**: Create values-aws.yaml file with AWS-specific configurations.

  **Configure**:
  - ECR image repository URLs
  - RDS PostgreSQL connection string
  - S3 bucket configuration for music files
  - IAM roles for service accounts (IRSA)
  - Resource requests and limits for AWS
  - Ingress configuration for ALB
  - Service annotations for AWS
- **Labels**: aws, helm, configuration
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 10.2

### Task 10.4: Install AWS Load Balancer Controller
- **Description**: Install AWS Load Balancer Controller for managing ALB and NLB from Kubernetes.

  **Steps**:
  1. Create IAM policy for Load Balancer Controller
  2. Create IAM role with IRSA
  3. Install cert-manager (prerequisite)
  4. Install AWS Load Balancer Controller via Helm
  5. Verify controller is running

  **Commands**:
  ```bash
  helm repo add eks https://aws.github.io/eks-charts
  helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    -n kube-system \
    --set clusterName=jamtrack-eks \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller
  ```
- **Labels**: aws, eks, alb, ingress, networking
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 10.3

### Task 10.5: Deploy Application to EKS using Helm
- **Description**: Deploy Jamtrack Radio to EKS cluster using Helm chart with AWS values.

  **Commands**:
  ```bash
  # Create namespace
  kubectl create namespace jamtrack-radio

  # Install Helm chart
  helm install jamtrack-radio ./helm/jamtrack-radio \
    -f ./helm/jamtrack-radio/values-aws.yaml \
    -n jamtrack-radio

  # Verify deployment
  kubectl get pods -n jamtrack-radio
  kubectl get services -n jamtrack-radio
  kubectl get ingress -n jamtrack-radio
  ```
- **Labels**: aws, eks, helm, deployment
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 10.4

### Task 10.6: Configure SSL with AWS Certificate Manager
- **Description**: Create SSL certificate using ACM and configure ALB Ingress to use it.

  **Steps**:
  1. Request certificate in ACM for domain
  2. Validate domain ownership (DNS or email)
  3. Update Ingress with ACM certificate ARN annotation
  4. Configure Route 53 for DNS (if using)
  5. Verify HTTPS access
- **Labels**: aws, acm, ssl, ingress, networking
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Task 10.5

### Task 10.7: Verify and Test AWS Deployment
- **Description**: Perform end-to-end testing of AWS deployment and verify all services.

  **Verify**:
  - Application accessible via ALB URL
  - SSL certificate working
  - API endpoints responding correctly
  - gRPC services accessible
  - RDS connectivity working
  - S3 file operations working
  - CloudWatch logging working
  - Auto-scaling configuration
  - Load balancing across pods
- **Labels**: aws, testing, deployment, verification
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Task 10.6

---

## Phase 11: Advanced Features & Production Hardening
**Phase Description**: Add advanced streaming features, optional frontend UI, implement security best practices, performance optimization, and production readiness improvements.

**Priority**: Low

**Labels**: phase-11, advanced, security, optimization, frontend

### Task 11.1: Implement Music Streaming Functionality
- **Description**: Add actual music streaming capability with support for different audio formats.

  **Features**:
  - Stream audio files from Azure Blob / S3
  - Support multiple formats (MP3, FLAC, WAV)
  - Implement HTTP range requests for seeking
  - Add buffering and chunked streaming
  - Implement streaming quality selection
- **Labels**: backend, streaming, audio
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 8 or Phase 10

### Task 11.2: Create Frontend UI (Optional)
- **Description**: Build a simple frontend using React or Blazor for interacting with the API.

  **Features**:
  - Music library browser
  - Playlist management UI
  - Audio player component
  - Search functionality
  - User authentication UI

  **Tech choices**:
  - React + TypeScript, or
  - Blazor WebAssembly
- **Labels**: frontend, react, blazor, ui
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.12)

### Task 11.3: Implement Authentication and Authorization
- **Description**: Add JWT-based authentication and role-based authorization.

  **Features**:
  - User registration and login
  - JWT token generation and validation
  - Role-based access control (Admin, User)
  - Refresh token mechanism
  - OAuth2 integration (optional: Google, GitHub)
- **Labels**: backend, security, authentication, jwt
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.11)

### Task 11.4: Implement Rate Limiting and Throttling
- **Description**: Add rate limiting middleware to prevent API abuse.

  **Features**:
  - Rate limiting per IP address
  - Rate limiting per authenticated user
  - Configurable limits for different endpoints
  - Response headers showing rate limit status
  - Integration with Redis for distributed rate limiting
- **Labels**: backend, security, rate-limiting
- **Estimated Effort**: Medium
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.11)

### Task 11.5: Implement Caching Strategy
- **Description**: Add caching using Redis for improved performance.

  **Caching layers**:
  - Response caching for GET endpoints
  - Database query result caching
  - Distributed caching across instances
  - Cache invalidation strategies
  - Cache warming for popular content
- **Labels**: backend, performance, caching, redis
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 2 (Task 2.11)

### Task 11.6: Security Hardening
- **Description**: Implement security best practices and conduct security audit.

  **Security measures**:
  - HTTPS enforcement
  - CORS policy configuration
  - SQL injection prevention (parameterized queries)
  - XSS protection headers
  - CSRF protection
  - Secrets management (Azure Key Vault / AWS Secrets Manager)
  - Network policies in Kubernetes
  - Pod security policies
  - Vulnerability scanning in CI/CD
- **Labels**: security, hardening, best-practices
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 8 or Phase 10

### Task 11.7: Performance Optimization
- **Description**: Optimize application performance through profiling and tuning.

  **Optimization areas**:
  - Database query optimization and indexing
  - N+1 query prevention
  - Connection pooling tuning
  - Memory usage optimization
  - CPU profiling and optimization
  - Load testing and benchmarking
  - CDN integration for static assets
  - Lazy loading and pagination
- **Labels**: performance, optimization, profiling
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 8 or Phase 10

### Task 11.8: Documentation and Knowledge Transfer
- **Description**: Create comprehensive documentation for the entire project.

  **Documentation**:
  - API documentation (Swagger/OpenAPI)
  - Architecture decision records (ADRs)
  - Deployment runbooks
  - Troubleshooting guides
  - Developer onboarding guide
  - Infrastructure diagrams
  - Monitoring and alerting playbooks
  - Disaster recovery procedures
- **Labels**: documentation, knowledge-transfer
- **Estimated Effort**: Large
- **Status**: Backlog
- **Dependencies**: Phase 11 (Tasks 11.1-11.7)

---

**Total Tasks**: ~97 tasks across 12 phases (Phase 2 split into 2A and 2B)

**Core Path** (if skipping optional Phase 2B): ~88 tasks

**Task Breakdown by Phase**:
- Phase 0: Environment Setup & GitHub Init - 16 tasks
- Phase 1: Documentation - 4 tasks
- Phase 2A: Basic Backend - 9 tasks
- Phase 2B: Advanced Patterns (Optional) - 9 tasks
- Phase 3-11: ~59 tasks

**Estimated Timeline**:
- Phase 0: Environment Setup & GitHub Init - 1-1.5 weeks ⭐ **Start tracking early!**
- Phase 1: Documentation - 2-3 days
- Phase 2A: Basic Backend - 2-3 weeks ⭐ **Quick win to working API!**
- Phase 2B: Advanced Patterns (Optional) - 2-3 weeks (can defer or skip)
- Phase 3: Docker - 1 week
- Phase 4: Kubernetes - 1-2 weeks
- Phase 5-6: CI/CD & Monitoring - 2-3 weeks
- Phase 7-8: Azure - 2-3 weeks
- Phase 9-10: AWS - 2-3 weeks
- Phase 11: Advanced Features (Optional) - 2-4 weeks

**Total Estimated Time**:
- **Fast Track** (Phase 2A, skip 2B): 12-17 weeks (3-4 months)
- **Complete** (all phases): 15-22 weeks (4-5.5 months)

**Key Advantages of This Structure**:
✅ **Early Tracking**: GitHub project set up in Phase 0 - track your progress from day one!
✅ **Quick Wins**: Working API in ~4 weeks (Phase 0 + 1 + 2A)
✅ **Flexible Learning**: Can skip Phase 2B and return later
✅ **Momentum Building**: Documentation tasks are light, keeping energy high before backend work

**Recommended Approach**: Complete Phase 0 and start tracking everything in GitHub immediately. Phase 1 is light (documentation), then Phase 2A gets you to a working API quickly. Decide after Phase 2A whether to continue to Phase 3 (Docker) or return to Phase 2B (patterns) later. Building momentum is more important than perfection!
