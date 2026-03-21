---
name: new-grpc-endpoint
description: Scaffolds a new gRPC RPC endpoint for a Jamtrack Radio service — adds the RPC to the .proto file, creates the C# handler stub in the Api layer, and creates the Application command/query + handler stub. Wires everything up to DI in Program.cs.
disable-model-invocation: true
argument-hint: [ServiceName MethodName] e.g. TrackService GetTrack
---

You are scaffolding a new gRPC endpoint for a Jamtrack Radio service.

If $ARGUMENTS is provided, parse it as `$SERVICE $METHOD` (e.g. `TrackService GetTrack`). Otherwise, ask:
- Which service? (e.g. `IdentityService`, `TrackService`, `StreamingService`)
- What is the RPC method name? (PascalCase verb+noun, e.g. `GetTrack`, `UploadTrack`, `RegisterUser`)
- Is this a command (write) or a query (read)?
- What are the key request fields?
- What are the key response fields?

Use `$SERVICE`, `$METHOD`, `$PACKAGE` (lowercase service name, e.g. `trackservice`) throughout.

---

## Step 1 — Update the .proto File

File location: `src/$SERVICE/$SERVICE.Api/Protos/$PACKAGE.proto`

If the `.proto` file does not exist, create it first:

```protobuf
syntax = "proto3";

option csharp_namespace = "$SERVICE.Api";

package jamtrack.$PACKAGE.v1;

service $SERVICE {
}
```

Add the new RPC to the service definition and the request/response messages:

```protobuf
syntax = "proto3";

option csharp_namespace = "$SERVICE.Api";

package jamtrack.$PACKAGE.v1;

service $SERVICE {
  // Existing RPCs...

  rpc $METHOD ($METHODRequest) returns ($METHODResponse);
}

// --- $METHOD ---

message $METHODRequest {
  // TODO: add request fields
  // string track_id = 1;
}

message $METHODResponse {
  // TODO: add response fields
  // string track_id = 1;
  // string title = 2;
}
```

**Protobuf field rules**:
- Field numbers are immutable once published — never reuse or renumber existing fields
- Use `snake_case` for field names (C# code gen produces `PascalCase` automatically)
- Use `string` for IDs (UUIDs serialised as strings)
- Use `google.protobuf.Timestamp` for date/time fields
- Use `int64` for integer quantities; `double` for decimals
- Wrap optional fields in `optional` or use `oneof` — never rely on default zero values to mean "not set"

Ensure the `.csproj` includes the Protobuf item:

```xml
<ItemGroup>
  <Protobuf Include="Protos\$PACKAGE.proto" GrpcServices="Server" />
</ItemGroup>
```

---

## Step 2 — Application Layer: Command/Query + Handler

**For a command (write operation)**:

Create `src/$SERVICE/$SERVICE.Application/Commands/$METHODCommand.cs`:

```csharp
namespace $SERVICE.Application.Commands;

public sealed record $METHODCommand(
  // TODO: add command properties matching the request fields
  // Guid TrackId,
  // string Title
);
```

Create `src/$SERVICE/$SERVICE.Application/Commands/$METHODHandler.cs`:

```csharp
namespace $SERVICE.Application.Commands;

public sealed class $METHODHandler
{
  // TODO: inject required interfaces
  // private readonly I$SERVICERepository _repository;

  public $METHODHandler(/* TODO: inject interfaces */)
  {
    // _repository = repository;
  }

  public async Task</* TODO: return type */> HandleAsync($METHODCommand command, CancellationToken ct)
  {
    // TODO: implement use case
    // 1. Validate business rules (throw DomainException on violation)
    // 2. Call repository
    // 3. Return result
    throw new NotImplementedException();
  }
}
```

**For a query (read operation)**:

Create `src/$SERVICE/$SERVICE.Application/Queries/$METHODQuery.cs` and `$METHODHandler.cs` with the same pattern, returning a result DTO.

---

## Step 3 — Api Layer: gRPC Service Handler

In `src/$SERVICE/$SERVICE.Api/Services/$SERVICEGrpcService.cs`, add the new RPC method override:

```csharp
public override async Task<$METHODResponse> $METHOD(
  $METHODRequest request, ServerCallContext context)
{
  _logger.LogInformation("$METHOD called {@Request}", new { /* log safe fields only */ });

  try
  {
    var result = await _$METHODHandler.HandleAsync(
      new $METHODCommand(/* map request fields */),
      context.CancellationToken);

    return new $METHODResponse
    {
      // TODO: map result to response fields
    };
  }
  catch (DomainException ex) when (ex is NotFoundException)
  {
    throw new RpcException(new Status(StatusCode.NotFound, ex.Message));
  }
  catch (DomainException ex) when (ex is ValidationException)
  {
    throw new RpcException(new Status(StatusCode.InvalidArgument, ex.Message));
  }
  // TODO: add catches for other domain exceptions specific to this method
}
```

Add the handler field and constructor parameter:

```csharp
private readonly $METHODHandler _$METHODHandler;

public $SERVICEGrpcService(
  // existing params...
  $METHODHandler $METHODHandler,
  ILogger<$SERVICEGrpcService> logger)
{
  // existing assignments...
  _$METHODHandler = $METHODHandler;
  _logger = logger;
}
```

---

## Step 4 — Wire up DI in Program.cs

In `src/$SERVICE/$SERVICE.Api/Program.cs`, register the new handler:

```csharp
builder.Services.AddScoped<$METHODHandler>();
// Also register any new repository or service interfaces it depends on:
// builder.Services.AddScoped<INewInterface, NewImplementation>();
```

---

## Step 5 — Error Mapping Reference

| Domain Exception | gRPC Status Code |
|---|---|
| `NotFoundException` | `StatusCode.NotFound` (5) |
| `DuplicateException` / `AlreadyExistsException` | `StatusCode.AlreadyExists` (6) |
| `ValidationException` | `StatusCode.InvalidArgument` (3) |
| `UnauthorizedException` | `StatusCode.Unauthenticated` (16) |
| `ForbiddenException` | `StatusCode.PermissionDenied` (7) |
| Any unhandled infrastructure exception | `StatusCode.Internal` (13) — catch at top level, log, return generic message |

---

## Step 6 — Verify

```bash
dotnet build src/$SERVICE/$SERVICE.Api
```

Expected: zero errors, zero warnings. The proto code generation runs as part of the build.

---

After scaffolding the endpoint, ask:
- Should we run `/design $SERVICE $METHOD` to produce a full technical design before implementing the handler logic?
- Ready to implement the handler body? Run `/implement $SERVICE $METHOD`
