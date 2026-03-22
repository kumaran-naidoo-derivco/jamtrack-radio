# ADR-004: YARP as the API Gateway

**Status**: Accepted
**Date**: 2026-03-22

## Context

The platform needs a single external-facing entry point that:
1. Terminates HTTPS and enforces JWT authentication
2. Routes requests to the appropriate microservice
3. Does not require a separately deployed, separately managed external service

Options evaluated: YARP (Microsoft), Ocelot, Kong, AWS API Gateway, Azure API Management.

## Decision

Use **YARP (Yet Another Reverse Proxy)** — Microsoft's open-source reverse proxy library — running as an ASP.NET Core middleware in a dedicated `ApiGateway` project.

YARP is configured via `appsettings.json` routes. JWT validation runs as ASP.NET Core authentication middleware before YARP forwards the request. The gateway translates REST → gRPC for downstream services.

## Consequences

**What becomes easier:**
- Native ASP.NET Core: YARP is a NuGet package, not an external service. No additional Docker container, no separate config management tool.
- Programmatic configuration: routes and clusters are strongly typed C# objects — refactorable, testable, and reviewable in the same codebase
- JWT integration: `UseAuthentication()` + `UseAuthorization()` middleware runs before YARP forwarding — consistent with any other ASP.NET Core app
- Phase 4: YARP runs in a K8s pod behind Azure Application Gateway WAF. No additional managed gateway service required (saving £20–50/month vs Azure APIM at this scale)

**What becomes harder:**
- Advanced API management: YARP has no built-in rate limiting dashboard, no API product tiers, no developer portal. If these are needed at Phase 5+, evaluate Azure APIM. Not needed for Jamtrack Radio.
- gRPC transcoding: YARP does not natively transcribe REST → gRPC. This requires a thin adapter in each downstream service or gRPC-Web. Accepted: the gateway calls gRPC clients directly using `Grpc.Net.Client`.

## Cost implication

£0. YARP is a free Microsoft OSS library. Saves ~£150+/month compared to Azure APIM Basic tier.
