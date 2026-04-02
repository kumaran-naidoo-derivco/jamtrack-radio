# Error Envelope Specification

**Date**: 2026-04-01
**Status**: Accepted
**Applies to**: All Jamtrack Radio API surfaces

---

## Overview

This document defines the canonical error response format for all Jamtrack Radio APIs. Consistent error envelopes mean clients can write a single error handler rather than service-specific parsing logic.

---

## REST Error Envelope (RFC 9457 Problem Details)

Used by: **API Gateway** (external REST surface), **Streaming Service**.

```json
{
  "type": "https://jamtrack.io/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "One or more fields failed validation.",
  "traceId": "00-abc123def456-78901234-01",
  "errors": [
    {
      "field": "email",
      "message": "must be a valid email address"
    },
    {
      "field": "password",
      "message": "must be at least 8 characters"
    }
  ]
}
```

### Required fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string (URI) | Yes | Stable URI identifying the error type. Never changes between releases. |
| `title` | string | Yes | Short human-readable summary. Consistent for the same error type. |
| `status` | int | Yes | HTTP status code. Mirrors the response status line. |
| `detail` | string | Yes | Specific explanation for this occurrence. May vary. |
| `traceId` | string | Yes | W3C trace ID for correlation with logs. Always include. |
| `errors` | array | No | Field-level validation errors. Include when `status` is 422. |

### Error type registry

| `type` URI | `status` | When |
|------------|---------|------|
| `https://jamtrack.io/errors/validation-error` | 422 | Input failed validation |
| `https://jamtrack.io/errors/not-found` | 404 | Resource not found |
| `https://jamtrack.io/errors/conflict` | 409 | Duplicate resource (e.g. email already registered) |
| `https://jamtrack.io/errors/unauthorised` | 401 | Missing or invalid JWT |
| `https://jamtrack.io/errors/forbidden` | 403 | Valid JWT but insufficient permissions |
| `https://jamtrack.io/errors/rate-limited` | 429 | Request rate limit exceeded |
| `https://jamtrack.io/errors/internal-error` | 500 | Unexpected server error (do not leak details) |

---

## gRPC Error Mapping

Used by: **Identity Service**, **Track Service**, **Playlist Service**, **Storage Service**.

gRPC status codes are returned in the response `Status`. Rich error detail is carried in the `google.rpc.Status` trailing metadata where needed.

### Domain exception → gRPC status code mapping

| Domain Exception | gRPC Status Code | gRPC Code int |
|------------------|-----------------|---------------|
| `NotFoundException` | `NOT_FOUND` | 5 |
| `DuplicateException` | `ALREADY_EXISTS` | 6 |
| `ValidationException` | `INVALID_ARGUMENT` | 3 |
| `UnauthorizedException` | `UNAUTHENTICATED` | 16 |
| `ForbiddenException` | `PERMISSION_DENIED` | 7 |
| `DomainException` (base) | `FAILED_PRECONDITION` | 9 |
| Unhandled exception | `INTERNAL` | 13 |

### gRPC error detail in trailing metadata

For `INVALID_ARGUMENT` errors, include field-level detail using the `google.rpc.BadRequest` proto:

```protobuf
// google/rpc/error_details.proto
message BadRequest {
  message FieldViolation {
    string field = 1;
    string description = 2;
  }
  repeated FieldViolation field_violations = 1;
}
```

### C# interceptor pattern

All gRPC services use a server-side `ExceptionInterceptor` to map domain exceptions to gRPC status codes:

```csharp
public sealed class ExceptionInterceptor : Interceptor
{
    public override async Task<TResponse> UnaryServerHandler<TRequest, TResponse>(
        TRequest request, ServerCallContext context,
        UnaryServerMethod<TRequest, TResponse> continuation)
    {
        try
        {
            return await continuation(request, context);
        }
        catch (NotFoundException ex)
        {
            throw new RpcException(new Status(StatusCode.NotFound, ex.Message));
        }
        catch (DuplicateException ex)
        {
            throw new RpcException(new Status(StatusCode.AlreadyExists, ex.Message));
        }
        catch (ValidationException ex)
        {
            throw new RpcException(new Status(StatusCode.InvalidArgument, ex.Message));
        }
        catch (UnauthorizedException ex)
        {
            throw new RpcException(new Status(StatusCode.Unauthenticated, ex.Message));
        }
        catch (DomainException ex)
        {
            throw new RpcException(new Status(StatusCode.FailedPrecondition, ex.Message));
        }
        catch (Exception)
        {
            throw new RpcException(new Status(StatusCode.Internal, "An unexpected error occurred."));
        }
    }
}
```

Register in `Program.cs`:
```csharp
builder.Services.AddGrpc(options =>
{
    options.Interceptors.Add<ExceptionInterceptor>();
});
```

---

## API Gateway — gRPC to REST translation

The YARP API Gateway translates gRPC error codes to REST Problem Details responses before returning to external clients. The mapping follows the table above. The `traceId` is always propagated from the gRPC trailing metadata into the REST error envelope.

---

## Rules

1. **Never expose internal exception messages to external clients** — `INTERNAL` / `500` responses use a generic message; details go to the log only
2. **Always include `traceId`** in every error response (REST and gRPC)
3. **`type` URIs are stable** — once published, the URI is a contract; change the path only with a major version bump
4. **Log at `Error` level** for all `500`/`INTERNAL` responses; log at `Warning` for all `400`/`INVALID_ARGUMENT` responses
