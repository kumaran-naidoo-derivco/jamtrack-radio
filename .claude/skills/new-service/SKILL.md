---
name: new-service
description: Scaffolds a new Clean Architecture microservice for Jamtrack Radio — Domain, Application, Infrastructure, and Api layers plus a test project. Wires up project references, adds standard packages, and removes placeholder files. Run this instead of repeating dotnet new + sln add + reference steps manually.
disable-model-invocation: true
argument-hint: [ServiceName] e.g. PlaylistService
---

You are scaffolding a new Jamtrack Radio microservice following Clean Architecture conventions.

If $ARGUMENTS is provided, use it as the service name (e.g. `PlaylistService`). Otherwise, ask:
- What is the service name? (PascalCase, e.g. `PlaylistService`)
- What is its primary responsibility? (one sentence — used for the README stub)

Use `$SERVICE` to represent the service name throughout.

---

## Step 1 — Scaffold Projects

```bash
# Class libraries for inner layers
dotnet new classlib -o src/$SERVICE/$SERVICE.Domain
dotnet new classlib -o src/$SERVICE/$SERVICE.Application
dotnet new classlib -o src/$SERVICE/$SERVICE.Infrastructure

# ASP.NET Core Web API for the outer layer
dotnet new webapi -o src/$SERVICE/$SERVICE.Api

# xUnit test project
dotnet new xunit -o tests/$SERVICE.Tests

# Add all four projects to the solution
dotnet sln add src/$SERVICE/$SERVICE.Domain/$SERVICE.Domain.csproj
dotnet sln add src/$SERVICE/$SERVICE.Application/$SERVICE.Application.csproj
dotnet sln add src/$SERVICE/$SERVICE.Infrastructure/$SERVICE.Infrastructure.csproj
dotnet sln add src/$SERVICE/$SERVICE.Api/$SERVICE.Api.csproj
dotnet sln add tests/$SERVICE.Tests/$SERVICE.Tests.csproj
```

---

## Step 2 — Wire Project References (Clean Architecture)

```bash
# Application depends on Domain
dotnet add src/$SERVICE/$SERVICE.Application reference \
  src/$SERVICE/$SERVICE.Domain

# Infrastructure depends on Application
dotnet add src/$SERVICE/$SERVICE.Infrastructure reference \
  src/$SERVICE/$SERVICE.Application

# Api depends on Application (business logic) and Infrastructure (DI wiring only)
dotnet add src/$SERVICE/$SERVICE.Api reference \
  src/$SERVICE/$SERVICE.Application
dotnet add src/$SERVICE/$SERVICE.Api reference \
  src/$SERVICE/$SERVICE.Infrastructure

# Tests reference the Api project (for WebApplicationFactory)
dotnet add tests/$SERVICE.Tests reference \
  src/$SERVICE/$SERVICE.Api
```

---

## Step 3 — Add Standard Packages

```bash
# Infrastructure — data access
dotnet add src/$SERVICE/$SERVICE.Infrastructure package Dapper
dotnet add src/$SERVICE/$SERVICE.Infrastructure package Npgsql
dotnet add src/$SERVICE/$SERVICE.Infrastructure package BCrypt.Net-Next

# Api — gRPC
dotnet add src/$SERVICE/$SERVICE.Api package Grpc.AspNetCore
dotnet add src/$SERVICE/$SERVICE.Api package Google.Protobuf
dotnet add src/$SERVICE/$SERVICE.Api package Grpc.Tools

# Api — logging
dotnet add src/$SERVICE/$SERVICE.Api package Serilog.AspNetCore
dotnet add src/$SERVICE/$SERVICE.Api package Serilog.Sinks.Console

# Api — health checks
dotnet add src/$SERVICE/$SERVICE.Api package Microsoft.Extensions.Diagnostics.HealthChecks

# Tests
dotnet add tests/$SERVICE.Tests package Microsoft.AspNetCore.Mvc.Testing
dotnet add tests/$SERVICE.Tests package Testcontainers.PostgreSql
dotnet add tests/$SERVICE.Tests package FluentAssertions
dotnet add tests/$SERVICE.Tests package Grpc.Net.Client
dotnet add tests/$SERVICE.Tests package Dapper
dotnet add tests/$SERVICE.Tests package Npgsql
```

---

## Step 4 — Remove Placeholder Files

```bash
rm src/$SERVICE/$SERVICE.Domain/Class1.cs
rm src/$SERVICE/$SERVICE.Application/Class1.cs
rm src/$SERVICE/$SERVICE.Infrastructure/Class1.cs
rm tests/$SERVICE.Tests/UnitTest1.cs

# Remove the default WeatherForecast scaffolding from the Api
rm src/$SERVICE/$SERVICE.Api/Controllers/WeatherForecastController.cs 2>/dev/null || true
rm src/$SERVICE/$SERVICE.Api/WeatherForecast.cs 2>/dev/null || true
```

---

## Step 5 — Scaffold Program.cs

Replace the generated `Program.cs` in `src/$SERVICE/$SERVICE.Api/` with this production-ready bootstrap:

```csharp
using Serilog;
using Serilog.Formatting.Json;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((ctx, cfg) =>
  cfg.ReadFrom.Configuration(ctx.Configuration)
     .Enrich.FromLogContext()
     .Enrich.WithProperty("Service", "$SERVICE")
     .WriteTo.Console(new JsonFormatter()));

builder.Services.AddGrpc();
builder.Services.AddHealthChecks();

// TODO: Register $SERVICE-specific services here
// builder.Services.AddScoped<I$SERVICERepository, $SERVICERepository>();

var app = builder.Build();

app.MapGrpcService</* TODO: $SERVICEGrpcService */>(); // add after creating the gRPC service
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");

app.Run();

public partial class Program { } // required for WebApplicationFactory in tests
```

---

## Step 6 — Scaffold appsettings.json

Ensure `src/$SERVICE/$SERVICE.Api/appsettings.json` includes:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    }
  },
  "ConnectionStrings": {
    "Default": ""
  }
}
```

Connection string value is always resolved from the environment — never committed.

---

## Step 7 — Verify

```bash
dotnet build
```

Expected: zero errors, zero warnings.

---

After scaffolding, ask:
- Ready to add the first gRPC endpoint? Run `/new-grpc-endpoint $SERVICE`
- Ready to add the first migration? Run `/new-migration`
- Ready to start implementing? Run `/design $SERVICE`
