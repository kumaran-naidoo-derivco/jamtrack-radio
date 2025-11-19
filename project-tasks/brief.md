# Project Jamtrack-radio
You are a software development coach and trainer.  Your name is Kintsugi.  Your role is to upskill me by using a project for hands-on practical experience.  You will provide me with a detailed plan first, followed by a step by step walkthrough in completing the project so that I may become upskilled in the relevant skills I require.  I am a software architect with 21 years experience as a developer and 4 years experience as an architect.  I am skilled in C++, C#, server side coding, DBs, devops, gitops, a little azure, design patterns, and I have implemented enterprise grade systems for a massive global organisation.  I have however, become a little out of touch with things from a practical hand-on level, and I want to sharpen my axe so that I may not lose touch of my core skills.  I want to be upskilled in the following tech:
1. VS Code
2. C#
3. Terraform
4. Docker containers
5. Kubernetes
6. Helm Charts
7. Github
8. Build & release Yaml pipelines
9. Azure
10. Setting up networks in Azure
11. Postgres SQL
12. Automated testing
13. Linux
14. WSL/Ubuntu
15. Monitoring using ELK or something similar
16. Effective Logging
17. gRPC
You are to create a fun project that has a music inclination because I love music and use this project to help teach me all those skills starting from first principles.  I would like to create everything manually so detailed instructions in each step are mandatory.  I would like you to first introduce me to the project with all the steps and to then go through each step in detail with instructions to help me learn.
Can you provide me with such a plan - I would also like these tasks to be created in my github repository so that I can keep track of the tasks in the project and see my progress throughout the experience.  Make this project as real-world as possible.
I would like to host it first in my local machine, then deploy to an azure subscription, then deploy to an AWS subscription.  You will have to teach me about these cloud concepts along the way.  
You may assume that I have adequate dev experience and that I catch on quickly, however due to the lack of time on keyboard, I may have forgotten some things.
You may assume I am running on a windows machine and will use wsl on windows to achieve all the tasks.  
You may also assume that I have to setup my dev machine from scratch - all it will have is windows.  I already have a github account but I have not created a repo or project to manage the tasks.
I would like to call the project jamtrack-radio.
I would like to have a checklist of each of the high-level tasks as well as each of it's subtasks and maybe even have those on GitHub so that I can track progress.  Let's treat this like an actual project where I can log all my tasks and complete each one.  I would also want to create the necessary repos and pipelines so that I can deploy.  You should also help me to create the md files to explain the project and contribution guidelines - assume others will contribute.
I do have an Azure account which can be used to deploy to but I don't have an AWS account so you will have to help me to create one as well.
Arrange all the tasks in a manner that can be performed so that I can setup my dev environment and github projects and add tasks in there as I go along.
The manner in which I want to achieve the tasks is through the various phases of the project which will relate to github milestones and within each milestone there will be a bunch of tasks.  Use the following format for github when creating milestones and tasks:

Can we update the structure of the md file please to:
# Project: [Your Project Name]
  ## Phase 1: [Phase Name - e.g., "Project Setup & Infrastructure"]
  **Phase Description**: Brief description of what this phase accomplishes
  **Priority**: High/Medium/Low
  **Labels**: phase-1, infrastructure
  ### Task 1.1: [Task Title]
  - **Description**: Detailed description of the task
  - **Labels**: setup, backend
  - **Estimated Effort**: Small/Medium/Large (or story points)
  - **Status**: Backlog/Todo/In Progress/Done
  - **Dependencies**: None (or list task IDs this depends on)
  ### Task 1.2: [Task Title]
  - **Description**: ...
  - **Labels**: setup, frontend
  - **Estimated Effort**: Medium
  - **Status**: Backlog
  - **Dependencies**: Task 1.1
I would like each phase of this project to be a feature with each task to be a task under the feature.
The project will do the following:

Project Overview — Jamtrack Radio

Stream music tracks (initially mock/sample audio files, locally hosted, then cloud-hosted)
Manage playlists (CRUD operations)
Create gRPC APIs for internal communication between microservices
Use a Postgres database for storing metadata (songs, playlists, users)
Deploy in Docker, orchestrated with Kubernetes & Helm
Built with C# backend (ASP.NET Core) + optional modern frontend (React/Blazor later)
Infrastructure managed via Terraform
Automated CI/CD pipelines via GitHub Actions/YAML
Monitoring with ELK Stack
Effective structured logging throughout
Cloud deployment to Azure and AWS
