# Contributing to Jamtrack Radio 🎵

Thank you for your interest in contributing to Jamtrack Radio! This document provides guidelines and best practices for contributing to this project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)

---

## Code of Conduct

While this is primarily a learning project, we strive to maintain a welcoming and respectful environment:

- Be respectful and constructive in feedback
- Focus on learning and improvement
- Help others learn and grow
- Share knowledge and best practices

---

## Getting Started

### Prerequisites

Before contributing, ensure you have completed Phase 0 setup:
- Windows 10/11 with WSL 2 (Ubuntu)
- Git configured with your name and email
- VS Code with required extensions
- GitHub account with SSH or HTTPS authentication

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/jamtrack-radio.git
   cd jamtrack-radio
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/kumaran-naidoo-derivco/jamtrack-radio.git
   ```
4. Verify remotes:
   ```bash
   git remote -v
   ```

---

## Development Workflow

### 1. Sync with Upstream

Before starting work, always sync with the latest changes:

```bash
# Fetch latest changes from upstream
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

### 2. Create a Branch

Create a new branch for your work (see [Branching Strategy](#branching-strategy)):

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write clean, readable code
- Follow the [Code Style Guidelines](#code-style-guidelines)
- Add tests for new functionality
- Update documentation as needed

### 4. Commit Changes

Follow the [Commit Message Guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: add user authentication service"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

- Go to your fork on GitHub
- Click "New Pull Request"
- Fill out the PR template completely
- Link related issues

---

## Branching Strategy

We follow a structured branching strategy to keep the repository organized:

### Branch Types

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Protected branch, requires PR reviews
- **Naming**: `main` (default branch)

#### Feature Branches
- **Purpose**: New features or enhancements
- **Naming**: `feature/<descriptive-name>`
- **Examples**:
  - `feature/user-authentication`
  - `feature/playlist-crud-api`
  - `feature/grpc-music-service`

#### Bugfix Branches
- **Purpose**: Non-critical bug fixes
- **Naming**: `bugfix/<issue-number>-<short-description>`
- **Examples**:
  - `bugfix/42-fix-playlist-delete`
  - `bugfix/89-null-reference-error`

#### Hotfix Branches
- **Purpose**: Critical production bugs (used in later phases)
- **Naming**: `hotfix/<issue-number>-<short-description>`
- **Examples**:
  - `hotfix/101-security-vulnerability`
  - `hotfix/102-database-connection-leak`

#### Documentation Branches
- **Purpose**: Documentation-only changes
- **Naming**: `docs/<description>`
- **Examples**:
  - `docs/update-readme`
  - `docs/api-documentation`

#### Chore Branches
- **Purpose**: Maintenance tasks (dependencies, config, etc.)
- **Naming**: `chore/<description>`
- **Examples**:
  - `chore/update-dependencies`
  - `chore/configure-docker`

### Branch Lifecycle

1. **Create**: Branch from `main`
2. **Develop**: Make commits following guidelines
3. **Push**: Push to your fork regularly
4. **PR**: Create pull request when ready
5. **Review**: Address feedback from code review
6. **Merge**: Merge into `main` after approval
7. **Delete**: Delete branch after merge

---

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for clear and structured commit history.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons, etc.)
- **refactor**: Code refactoring (no feature change or bug fix)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config, build)
- **ci**: CI/CD pipeline changes

### Examples

**Feature:**
```
feat(api): add user authentication endpoint

Implement JWT-based authentication for user login.
Includes token generation and validation middleware.

Closes #42
```

**Bug Fix:**
```
fix(playlist): resolve null reference on empty playlist

Fixed NullReferenceException when attempting to retrieve
an empty playlist. Added null check and appropriate error handling.

Fixes #89
```

**Documentation:**
```
docs(readme): update installation instructions

Updated setup steps to include .NET 8 SDK installation
and clarified PostgreSQL configuration.
```

**Chore:**
```
chore(deps): update Entity Framework Core to 8.0.1

Updated EF Core packages to latest stable version.
Includes migration compatibility updates.
```

### Best Practices

- **Use imperative mood**: "add" not "added" or "adds"
- **Be concise**: Subject line under 50 characters
- **Provide context**: Explain "why" in the body, not just "what"
- **Reference issues**: Use "Closes #123" or "Fixes #456"
- **Break up changes**: One logical change per commit

---

## Pull Request Process

### Before Submitting

- [ ] Code compiles without errors
- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines
- [ ] Branch is up to date with `main`

### PR Template

When creating a PR, fill out the template completely:

- **Description**: What changes does this PR introduce?
- **Related Issues**: Link to issue(s) this PR addresses
- **Type of Change**: Feature, bugfix, docs, etc.
- **Testing**: How was this tested?
- **Checklist**: Complete all checklist items

### Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
   - Build verification
   - Unit tests
   - Code quality checks
   - Security scans

2. **Code Review**: At least one approval required
   - Reviewers provide feedback
   - Address all comments
   - Request re-review after changes

3. **Merge**: After approval and passing checks
   - Squash and merge (preferred for feature branches)
   - Merge commit (for larger features with meaningful commit history)
   - Rebase and merge (for small, well-structured PRs)

### After Merge

- Delete your branch (GitHub will prompt)
- Update your local repository:
  ```bash
  git checkout main
  git pull upstream main
  git push origin main
  ```

---

## Code Style Guidelines

### C# / .NET

Follow Microsoft's official C# coding conventions:

#### Naming Conventions

- **PascalCase**: Classes, methods, properties, constants
  ```csharp
  public class MusicService
  public void PlayTrack()
  public string TrackName { get; set; }
  ```

- **camelCase**: Local variables, parameters
  ```csharp
  var trackId = 123;
  public void PlayTrack(string trackName)
  ```

- **_camelCase**: Private fields (with underscore prefix)
  ```csharp
  private readonly ILogger _logger;
  ```

#### Code Organization

```csharp
// 1. Using statements (sorted)
using System;
using System.Collections.Generic;
using JamtrackRadio.Core;

// 2. Namespace
namespace JamtrackRadio.Api.Controllers
{
    // 3. Class documentation
    /// <summary>
    /// Controller for managing music tracks.
    /// </summary>
    public class TracksController : ControllerBase
    {
        // 4. Private fields
        private readonly ITrackService _trackService;
        private readonly ILogger<TracksController> _logger;

        // 5. Constructor
        public TracksController(
            ITrackService trackService,
            ILogger<TracksController> logger)
        {
            _trackService = trackService;
            _logger = logger;
        }

        // 6. Public methods
        public async Task<IActionResult> GetTrack(int id)
        {
            // Implementation
        }

        // 7. Private methods
        private void ValidateTrack(Track track)
        {
            // Implementation
        }
    }
}
```

#### Best Practices

- **Use var**: When type is obvious from right side
  ```csharp
  var track = new Track(); // Good
  Track track = new Track(); // OK but verbose
  ```

- **Async/Await**: Use for I/O operations
  ```csharp
  public async Task<Track> GetTrackAsync(int id)
  {
      return await _repository.FindAsync(id);
  }
  ```

- **Null Checking**: Use null-conditional operators
  ```csharp
  var name = track?.Name ?? "Unknown";
  ```

- **LINQ**: Prefer LINQ for collections
  ```csharp
  var activeTracks = tracks.Where(t => t.IsActive).ToList();
  ```

- **Dependency Injection**: Use constructor injection
  ```csharp
  public TrackService(ITrackRepository repository)
  {
      _repository = repository ?? throw new ArgumentNullException(nameof(repository));
  }
  ```

### File Organization

```
src/
├── JamtrackRadio.Api/          # Web API project
│   ├── Controllers/            # API controllers
│   ├── Models/                 # Request/response models
│   └── Program.cs              # Application entry point
├── JamtrackRadio.Core/         # Business logic
│   ├── Entities/               # Domain entities
│   ├── Interfaces/             # Service interfaces
│   └── Services/               # Service implementations
└── JamtrackRadio.Infrastructure/ # Data access
    ├── Data/                   # DbContext, repositories
    └── Migrations/             # EF Core migrations
```

### EditorConfig

The project includes an `.editorconfig` file. Ensure your IDE respects these settings:
- Indentation: 4 spaces
- Line endings: LF (Unix-style)
- Charset: UTF-8
- Trim trailing whitespace

---

## Testing Requirements

### Test Structure

We follow the AAA pattern (Arrange, Act, Assert):

```csharp
[Fact]
public async Task GetTrack_WithValidId_ReturnsTrack()
{
    // Arrange
    var trackId = 1;
    var expectedTrack = new Track { Id = trackId, Name = "Test Track" };
    _mockRepository.Setup(r => r.FindAsync(trackId)).ReturnsAsync(expectedTrack);

    // Act
    var result = await _service.GetTrackAsync(trackId);

    // Assert
    Assert.NotNull(result);
    Assert.Equal(expectedTrack.Name, result.Name);
}
```

### Test Coverage

- **Unit Tests**: Required for all business logic
  - Service classes
  - Validators
  - Utility functions

- **Integration Tests**: Required for API endpoints
  - Controller actions
  - Database operations
  - External service integrations

- **E2E Tests**: Added in later phases
  - Critical user workflows
  - End-to-end scenarios

### Testing Tools

- **xUnit**: Test framework
- **Moq**: Mocking framework
- **FluentAssertions**: Assertion library
- **Testcontainers**: Integration testing with Docker

### Running Tests

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test /p:CollectCoverage=true

# Run specific test
dotnet test --filter "FullyQualifiedName~TracksControllerTests"
```

---

## Documentation

### Code Documentation

- **XML Comments**: Required for public APIs
  ```csharp
  /// <summary>
  /// Retrieves a track by its unique identifier.
  /// </summary>
  /// <param name="id">The track ID.</param>
  /// <returns>The track if found, null otherwise.</returns>
  public async Task<Track> GetTrackAsync(int id)
  ```

- **README**: Update when adding features
- **ARCHITECTURE**: Document design decisions
- **API Docs**: Will be auto-generated with Swagger (Phase 2)

### Markdown Files

- Use GitHub-flavored markdown
- Include code examples where helpful
- Add diagrams for complex concepts (Mermaid, ASCII art)
- Keep documentation up to date with code changes

---

## Questions or Need Help?

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Project Board**: Check the [project board](https://github.com/users/kumaran-naidoo-derivco/projects/3) for task status

---

## License

By contributing to Jamtrack Radio, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for contributing to Jamtrack Radio! 🎵**
