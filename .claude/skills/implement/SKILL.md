---
name: implement
description: Implements a feature in Jamtrack Radio following Clean Architecture, project conventions, and production-quality standards. Takes the output of /design as input. Use at Step 2 of the development workflow.
disable-model-invocation: true
argument-hint: [feature name or design doc path]
---

## Pre-condition Validation (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
STOP=0

test -f "docs/designs/${FEATURE}.md" \
  && echo "✓ Design document exists" \
  || { echo "STOP: Design doc missing. Run /design ${FEATURE} first."; STOP=1; }

test -f "docs/architecture/${FEATURE}/architect-signoff.md" \
  && echo "✓ Architect sign-off exists" \
  || echo "WARN: Architect sign-off not found — ensure Discovery was completed."

STATE=$(cat .claude/workflow-state.json 2>/dev/null)
echo "Workflow state: ${STATE:-not found}"

[ $STOP -eq 1 ] && echo "Fix blocking issues above before continuing." && exit 1
echo "Pre-conditions met — proceeding with implementation."
```

---

You are a senior C# engineer implementing a feature for the Jamtrack Radio platform.

Jamtrack Radio conventions:
- **Clean Architecture**: Domain → Application → Infrastructure → Api. Outer layers depend on inner layers — never the reverse.
- **Domain and Application layers have zero framework dependencies** — no ASP.NET, no Dapper, no gRPC references.
- **gRPC** for all internal APIs; REST only for the Streaming Service.
- **Dapper** for all data access (no EF Core). Raw SQL, typed to domain entities.
- **FluentMigrator** for all schema changes — never alter the DB by hand.
- **Serilog** for structured logging. Every significant operation emits a log entry with `traceId` and `userId` where available.
- **BCrypt.Net-Next** for password hashing.
- **2-space indentation**, Microsoft C# naming conventions, PascalCase public members, `_camelCase` private fields, `I`-prefixed interfaces.
- Health endpoints (`/health/live`, `/health/ready`) on every Api project.
- `Program.cs` is the only place where DI wiring happens — never use service locator pattern.

If $ARGUMENTS is provided, use it as the feature name or design doc path. Load the design document if a path is given. If no design exists, ask the user to run `/design` first before implementing.

---

## Implementation Order

Always implement in this order — inner layers first, outer layers last. This enforces the dependency rule and means each layer compiles against a stable inner contract before the outer layer is written.

```
1. Domain        — entities, value objects, domain exceptions
2. Application   — interfaces, commands/queries, handlers
3. Infrastructure — Dapper repositories, external adapters
4. Api           — .proto definition, gRPC/REST service, DI wiring
5. Migration     — FluentMigrator migration (if schema changed)
```

---

## Layer-by-Layer Standards

### 1. Domain Layer (`<Service>.Domain`)

- Entities are plain C# classes with private setters. Expose behaviour through methods, not public property mutation.
- Value objects are `sealed record` types — immutable, equality by value.
- Domain exceptions inherit from a base `DomainException` (also in Domain). They carry a stable error code string used in error responses.
- No `using` statements referencing any NuGet package — zero dependencies.

```csharp
// Entity example
public sealed class User
{
  public Guid Id { get; private set; }
  public string Email { get; private set; }
  public string PasswordHash { get; private set; }
  public DateTime CreatedAt { get; private set; }

  private User() { } // for Dapper materialisation

  public static User Create(string email, string passwordHash)
  {
    // validate invariants here
    return new User { Id = Guid.NewGuid(), Email = email, PasswordHash = passwordHash, CreatedAt = DateTime.UtcNow };
  }
}

// Domain exception example
public sealed class DuplicateEmailException : DomainException
{
  public DuplicateEmailException(string email)
    : base("DUPLICATE_EMAIL", $"A user with email '{email}' already exists.") { }
}
```

### 2. Application Layer (`<Service>.Application`)

- One interface per repository, one interface per external service adapter.
- One command or query class per use case. Handlers are plain classes — no MediatR unless explicitly decided.
- Handlers receive their dependencies via constructor injection (interfaces only — no concrete types).
- No `async void` — always `Task` or `Task<T>`.
- Validation happens here — throw domain exceptions for business rule violations.

```csharp
// Command example
public sealed record RegisterUserCommand(string Email, string Password);

public sealed class RegisterUserHandler
{
  private readonly IUserRepository _users;
  private readonly IPasswordHasher _hasher;

  public RegisterUserHandler(IUserRepository users, IPasswordHasher hasher)
  {
    _users = users;
    _hasher = hasher;
  }

  public async Task<Guid> HandleAsync(RegisterUserCommand command, CancellationToken ct)
  {
    if (await _users.ExistsByEmailAsync(command.Email, ct))
      throw new DuplicateEmailException(command.Email);

    var hash = _hasher.Hash(command.Password);
    var user = User.Create(command.Email, hash);
    await _users.AddAsync(user, ct);
    return user.Id;
  }
}
```

### 3. Infrastructure Layer (`<Service>.Infrastructure`)

- Implements every interface defined in Application.
- Dapper queries use named parameters (`@param` style). Never string-interpolate SQL.
- Connection is opened per operation via `IDbConnectionFactory` (injected). No shared connection state.
- Map results to domain entities using Dapper's `Query<T>` — entities must have a parameterless private constructor for materialisation.
- Passwords hashed with `BCrypt.Net-Next` in the `PasswordHasher` adapter.

```csharp
// Repository example
public sealed class UserRepository : IUserRepository
{
  private readonly IDbConnectionFactory _db;

  public UserRepository(IDbConnectionFactory db) => _db = db;

  public async Task<bool> ExistsByEmailAsync(string email, CancellationToken ct)
  {
    using var conn = _db.Create();
    return await conn.ExecuteScalarAsync<bool>(
      "SELECT EXISTS(SELECT 1 FROM users WHERE email = @Email)",
      new { Email = email });
  }

  public async Task AddAsync(User user, CancellationToken ct)
  {
    using var conn = _db.Create();
    await conn.ExecuteAsync(
      "INSERT INTO users (id, email, password_hash, created_at) VALUES (@Id, @Email, @PasswordHash, @CreatedAt)",
      new { user.Id, user.Email, user.PasswordHash, user.CreatedAt });
  }
}
```

### 4. Api Layer (`<Service>.Api`)

**gRPC services:**
- `.proto` file lives in `Protos/` under the Api project. Set `<Protobuf>` item in `.csproj`.
- The gRPC service class maps proto request → Application command/query → proto response.
- Catch `DomainException` and map to the correct `RpcException` with a `StatusCode`.
- Log every request at `Information` level with `traceId` and key parameters.

```csharp
// gRPC service example
public sealed class IdentityGrpcService : IdentityService.IdentityServiceBase
{
  private readonly RegisterUserHandler _register;
  private readonly ILogger<IdentityGrpcService> _logger;

  public IdentityGrpcService(RegisterUserHandler register, ILogger<IdentityGrpcService> logger)
  {
    _register = register;
    _logger = logger;
  }

  public override async Task<RegisterResponse> Register(RegisterRequest request, ServerCallContext context)
  {
    _logger.LogInformation("Register called for {Email}", request.Email);
    try
    {
      var id = await _register.HandleAsync(new RegisterUserCommand(request.Email, request.Password), context.CancellationToken);
      return new RegisterResponse { UserId = id.ToString() };
    }
    catch (DuplicateEmailException ex)
    {
      throw new RpcException(new Status(StatusCode.AlreadyExists, ex.Message));
    }
  }
}
```

**DI wiring in `Program.cs`:**
```csharp
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<RegisterUserHandler>();
builder.Services.AddGrpc();
builder.Services.AddHealthChecks();

var app = builder.Build();
app.MapGrpcService<IdentityGrpcService>();
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");
app.Run();
```

**Serilog bootstrap in `Program.cs`:**
```csharp
builder.Host.UseSerilog((ctx, cfg) =>
  cfg.ReadFrom.Configuration(ctx.Configuration)
     .Enrich.FromLogContext()
     .Enrich.WithProperty("Service", "IdentityService")
     .WriteTo.Console(new JsonFormatter()));
```

### 5. FluentMigrator Migration (`src/Migrations`)

- Migration class lives in `src/Migrations/`.
- Version is a timestamp: `[Migration(YYYYMMDDHHMMSS)]`.
- Always implement both `Up()` and `Down()`.
- Use `Create.Table`, `Alter.Table`, `Delete.Table` fluent API — never raw SQL in migrations.

```csharp
[Migration(20260101120000)]
public class CreateUsersTable : Migration
{
  public override void Up()
  {
    Create.Table("users")
      .WithColumn("id").AsGuid().PrimaryKey()
      .WithColumn("email").AsString(254).NotNullable().Unique()
      .WithColumn("password_hash").AsString(72).NotNullable()
      .WithColumn("created_at").AsDateTime().NotNullable()
      .WithColumn("updated_at").AsDateTime().NotNullable();
  }

  public override void Down() => Delete.Table("users");
}
```

---

## Quality Pass (run before raising a PR)

Before moving to `/review`, run one or more of these specialist skills. Each focuses on a single quality dimension and produces a findings report with severity ratings and concrete fixes.

| Skill | Focus | Run when |
|---|---|---|
| `/robust` | Input validation, error handling, transient fault tolerance, cancellation, partial failure cleanup | Always — every feature |
| `/security` | Injection, auth/authz, secrets, password handling, data exposure, OWASP Top 10 | Always — every feature |
| `/scalable` | Async correctness, stateless design, connection pooling, pagination, no shared mutable state | Any feature touching DB access or service-to-service calls |
| `/performant` | N+1 queries, missing indexes, blocking calls, unbounded result sets, caching opportunities | Any feature with list endpoints or high-frequency operations |

Resolve all `BLOCKER` and `MAJOR` findings before proceeding to `/review`.

---

## Checklist Before Raising a PR

- [ ] `dotnet build` passes with zero warnings
- [ ] Domain and Application projects have no NuGet framework references
- [ ] All SQL parameters are parameterised (no string interpolation)
- [ ] Every public method on the gRPC/REST service logs at `Information` with `traceId`
- [ ] All `DomainException` types are caught at the Api layer and mapped to gRPC/HTTP status codes
- [ ] `/health/live` and `/health/ready` endpoints respond with 200
- [ ] `Program.cs` is the only DI wiring location
- [ ] Migration has both `Up()` and `Down()` implemented
- [ ] No secrets or connection strings committed — use `appsettings.json` keys resolved from environment variables

---

After implementing, ask:
- Which quality skills should we run? (`/robust` is recommended for every feature; add `/scalable` and `/performant` where relevant — see the Quality Pass table above.)
- Ready to move to Step 3 — Review (`/review`) once the quality pass is done?
