---
name: test
description: Generates integration tests for a Jamtrack Radio feature using WebApplicationFactory and Testcontainers against a real PostgreSQL database. Takes the acceptance criteria from /design as input. Use at Step 4 of the development workflow.
disable-model-invocation: true
argument-hint: [feature name, service name, or design doc path]
---

## Pre-condition Validation (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
STOP=0

test -f "docs/designs/${FEATURE}.md" \
  && echo "✓ Design document exists" \
  || { echo "STOP: Design doc missing — acceptance criteria needed. Run /design ${FEATURE} first."; STOP=1; }

STATE=$(cat .claude/workflow-state.json 2>/dev/null)
echo "Workflow state: ${STATE:-not found}"

[ $STOP -eq 1 ] && echo "Fix blocking issues above before continuing." && exit 1
echo "Pre-conditions met — proceeding with test generation."
```

---

You are a senior C# engineer writing integration tests for the Jamtrack Radio platform.

Testing philosophy for this project:
- **Integration tests only** for external-facing endpoints. No unit tests unless there is a complex isolated calculation (e.g. a pricing algorithm or a custom parser).
- **Real database** — every test runs against a real PostgreSQL instance spun up by Testcontainers. No mocking of the database layer.
- **AAA pattern** — every test is structured as Arrange / Act / Assert with a blank line separating each section.
- **Test all combinations** — happy path, domain errors, validation errors, not-found cases, auth failures, and boundary values. Aim for exhaustive coverage of the acceptance criteria.
- **Tests must be deterministic** — each test sets up its own data and does not depend on the order of execution or state left by other tests.
- **Tests must be idempotent** — running the test suite twice in a row produces the same result.

If $ARGUMENTS is provided, use it as the feature/service name or load the design doc at the given path to extract acceptance criteria. If no design doc exists, ask the user to provide the acceptance criteria before generating tests.

---

## Test Project Setup

Each service has one test project: `tests/<Service>.Tests/`.

**Required packages** (add if not already present):
```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.*" />
<PackageReference Include="Testcontainers.PostgreSql" Version="*" />
<PackageReference Include="FluentAssertions" Version="*" />
<PackageReference Include="Grpc.Net.Client" Version="*" />
<PackageReference Include="Google.Protobuf" Version="*" />
<PackageReference Include="Grpc.Tools" Version="*" />
```

**Test database lifecycle** — use a shared Testcontainers fixture across the test class to avoid spinning up a new container per test:

```csharp
public sealed class PostgresFixture : IAsyncLifetime
{
  private readonly PostgreSqlContainer _container = new PostgreSqlBuilder()
    .WithImage("postgres:16")
    .Build();

  public string ConnectionString => _container.GetConnectionString();

  public async Task InitializeAsync()
  {
    await _container.StartAsync();
    // Run FluentMigrator migrations against the test DB
    var runner = BuildMigrationRunner(ConnectionString);
    runner.MigrateUp();
  }

  public async Task DisposeAsync() => await _container.DisposeAsync();

  private static IMigrationRunner BuildMigrationRunner(string connString)
  {
    return new ServiceCollection()
      .AddFluentMigratorCore()
      .ConfigureRunner(r => r
        .AddPostgres()
        .WithGlobalConnectionString(connString)
        .ScanIn(typeof(CreateUsersTable).Assembly).For.Migrations())
      .BuildServiceProvider()
      .GetRequiredService<IMigrationRunner>();
  }
}
```

**WebApplicationFactory** — override the DB connection to point at the Testcontainers instance:

```csharp
public sealed class ServiceApiFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
  private readonly PostgresFixture _db = new();

  public GrpcChannel GrpcChannel =>
    GrpcChannel.ForAddress(Server.BaseAddress, new GrpcChannelOptions
    {
      HttpHandler = Server.CreateHandler()
    });

  public string ConnectionString => _db.ConnectionString;

  public async Task InitializeAsync() => await _db.InitializeAsync();

  public async Task DisposeAsync()
  {
    await _db.DisposeAsync();
    await base.DisposeAsync();
  }

  protected override void ConfigureWebHost(IWebHostBuilder builder)
  {
    builder.ConfigureServices(services =>
    {
      // Replace the real DB connection factory with one pointing at Testcontainers
      services.RemoveAll<IDbConnectionFactory>();
      services.AddSingleton<IDbConnectionFactory>(
        new NpgsqlConnectionFactory(_db.ConnectionString));
    });
  }
}
```

---

## Test Structure

**One test class per feature or endpoint.** Name it `<Feature>Tests` (e.g. `RegisterUserTests`, `UploadTrackTests`).

Inherit from `IClassFixture<ServiceApiFactory>` to share the factory across all tests in the class.

```csharp
public sealed class RegisterUserTests : IClassFixture<ServiceApiFactory>
{
  private readonly ServiceApiFactory _factory;
  private readonly IdentityService.IdentityServiceClient _client;

  public RegisterUserTests(ServiceApiFactory factory)
  {
    _factory = factory;
    _client = new IdentityService.IdentityServiceClient(factory.GrpcChannel);
  }
```

**Test method naming**: `<Method>_<Scenario>_<ExpectedOutcome>`

```csharp
  [Fact]
  public async Task Register_ValidEmailAndPassword_ReturnsUserId() { }

  [Fact]
  public async Task Register_DuplicateEmail_ThrowsAlreadyExists() { }

  [Fact]
  public async Task Register_InvalidEmailFormat_ThrowsInvalidArgument() { }
```

---

## AAA Pattern

Every test follows Arrange / Act / Assert with a blank line between each section. No exceptions.

```csharp
[Fact]
public async Task Register_ValidEmailAndPassword_ReturnsUserId()
{
  // Arrange
  var request = new RegisterRequest
  {
    Email = $"test+{Guid.NewGuid()}@jamtrack.io",
    Password = "SecurePass123!"
  };

  // Act
  var response = await _client.RegisterAsync(request);

  // Assert
  response.UserId.Should().NotBeNullOrEmpty();
  Guid.TryParse(response.UserId, out _).Should().BeTrue();
}
```

Use a unique identifier (e.g. `Guid.NewGuid()`) in test data to prevent conflicts between test runs.

---

## Coverage Requirements

For every feature, generate tests covering **all** of the following that apply:

| Category | Example scenarios |
|---|---|
| Happy path | Valid input → correct response, correct DB state |
| Duplicate / conflict | Same unique key twice → correct error code |
| Validation — missing field | Required field omitted → `INVALID_ARGUMENT` / `422` |
| Validation — invalid format | Bad email, negative number → `INVALID_ARGUMENT` / `422` |
| Not found | Unknown ID → `NOT_FOUND` / `404` |
| Auth failure | Missing or expired JWT → `UNAUTHENTICATED` / `401` |
| Boundary values | Max length strings, zero quantities, empty collections |
| DB state verification | After a write operation, query the DB directly to confirm the record was stored correctly |
| Idempotency | Where applicable, calling the same operation twice produces the expected result |

---

## Asserting DB State

For write operations, always verify the database state directly — do not just trust the response:

```csharp
[Fact]
public async Task Register_ValidEmailAndPassword_StoresHashedPasswordInDb()
{
  // Arrange
  var email = $"test+{Guid.NewGuid()}@jamtrack.io";
  var request = new RegisterRequest { Email = email, Password = "SecurePass123!" };

  // Act
  await _client.RegisterAsync(request);

  // Assert — query the DB directly
  using var conn = new NpgsqlConnection(_factory.ConnectionString);
  var user = await conn.QuerySingleOrDefaultAsync(
    "SELECT email, password_hash FROM users WHERE email = @Email",
    new { Email = email });

  user.Should().NotBeNull();
  ((string)user.password_hash).Should().StartWith("$2"); // BCrypt prefix
  ((string)user.password_hash).Should().NotBe("SecurePass123!"); // never stored plain
}
```

---

## Asserting gRPC Error Codes

Catch `RpcException` and assert its `StatusCode`:

```csharp
[Fact]
public async Task Register_DuplicateEmail_ThrowsAlreadyExists()
{
  // Arrange
  var request = new RegisterRequest
  {
    Email = "duplicate@jamtrack.io",
    Password = "SecurePass123!"
  };
  await _client.RegisterAsync(request); // first registration

  // Act
  var act = async () => await _client.RegisterAsync(request);

  // Assert
  var ex = await act.Should().ThrowAsync<RpcException>();
  ex.Which.StatusCode.Should().Be(StatusCode.AlreadyExists);
}
```

---

## Checklist Before Raising a PR

- [ ] Every acceptance criterion from the design doc has at least one test
- [ ] All error paths tested (not just happy path)
- [ ] Each test uses unique data (no shared mutable state between tests)
- [ ] DB state verified directly for all write operations
- [ ] `dotnet test` passes with zero failures locally
- [ ] No `Thread.Sleep` or fixed delays — use `async/await` throughout
- [ ] No `Assert.True(true)` or other vacuous assertions
- [ ] Placeholder `UnitTest1.cs` file removed from the test project

---

After generating the tests, ask:
- Are there additional edge cases or scenarios to cover?
- Ready to move to Step 5 — Deploy Staging (`/deploy-staging`)?
