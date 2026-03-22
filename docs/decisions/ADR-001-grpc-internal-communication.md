# ADR-001: gRPC for All Internal Service-to-Service Communication

**Status**: Accepted
**Date**: 2026-03-22

## Context

Jamtrack Radio is a microservices platform. Services must communicate reliably and efficiently over the internal network. The choices are: REST/JSON over HTTP, gRPC, GraphQL, or message-passing only.

At Phase 2 (local), services run in Docker Compose. At Phase 4+ they run in AKS. In both environments, the API Gateway is the only external-facing service — all other services communicate exclusively service-to-service.

## Decision

Use **gRPC** (via `Grpc.AspNetCore`) for all internal service-to-service communication.

The API Gateway (YARP) forwards external client requests inward and translates to gRPC. The Streaming Service retains REST (HTTP range requests) as its external protocol since HTTP range semantics are not idiomatic in gRPC.

## Consequences

**What becomes easier:**
- Strong typing: `.proto` contracts are the source of truth; code is generated, not written by hand
- Performance: HTTP/2 multiplexing, binary serialisation (Protocol Buffers) vs JSON — ~5–7× smaller payload, lower latency
- Contract-first design: changing a `.proto` file requires deliberate versioning, reducing accidental breaking changes
- Interoperability: any service can consume another's gRPC contract regardless of implementation language (future-proof)

**What becomes harder:**
- Browser clients cannot call gRPC directly without a translation layer (gRPC-Web or HTTP transcoding) — mitigated by the API Gateway absorbing all browser traffic
- Debugging raw gRPC requires tools like `grpcurl` or gRPC reflection; not as simple as `curl` for REST
- `.proto` contract changes must be backward-compatible (additive fields only; never remove or renumber fields)

## Cost implication

£0 — `Grpc.AspNetCore` is a first-party Microsoft library. No infrastructure cost.
