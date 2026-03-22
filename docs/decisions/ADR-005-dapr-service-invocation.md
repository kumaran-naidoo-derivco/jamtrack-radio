# ADR-005: Dapr for Service Invocation and Pub/Sub

**Status**: Accepted
**Date**: 2026-03-22

## Context

Services need to:
1. Call each other reliably with retries and circuit breaking
2. Publish and subscribe to domain events (e.g. `TrackUploaded` → Storage Service processes blob)

Without a framework, this requires hand-rolled retry logic, circuit breakers, dead-letter handling, and pub/sub infrastructure per service. Evaluated: Dapr, MassTransit + RabbitMQ, Azure Service Bus SDK direct, no framework (gRPC only).

## Decision

Use **Dapr (Distributed Application Runtime)** as a sidecar for:
- Service invocation with built-in retries, timeouts, and circuit breaking
- Pub/sub with a provider-agnostic API:
  - Phase 2–3 (local): Redis Streams as the pub/sub backing store
  - Phase 4 (Azure): Azure Service Bus as the pub/sub backing store
  - Phase 5 (AWS): AWS SNS/SQS via Dapr component swap (no application code change)

Dapr runs as a sidecar container alongside each service container. The application communicates with Dapr over localhost HTTP/gRPC.

## Consequences

**What becomes easier:**
- Provider portability: switching from Redis to Azure Service Bus to AWS SNS requires only a Dapr component YAML change — zero application code change. Critical for the multi-cloud Phase 5 objective.
- Observability: Dapr emits OpenTelemetry traces and metrics natively. Correlates with the ELK/ClickStack stack in Phase 6.
- Resilience out of the box: retries, circuit breaker, and timeout policies configured in Dapr resiliency YAML — not scattered across service code
- Actors model available if stateful workflows are needed (e.g. multi-step upload processing) — not required at Phase 2 but available

**What becomes harder:**
- Operational complexity: each service now has two containers (app + Dapr sidecar). Docker Compose and Helm charts are more verbose.
- Debugging: a failed pub/sub publish may appear as a Dapr sidecar error, not an application error. Requires understanding Dapr's own logs.
- Dapr version management: Dapr sidecar version must be compatible with the Dapr SDK version used in each service.

## Cost implication

£0 (self-hosted). Dapr itself is free. The backing infrastructure (Redis, Azure Service Bus) has a cost:
- Phase 2–3: Redis in Docker — £0
- Phase 4: Azure Service Bus Standard — ~£8/month for the namespace
- Phase 5: AWS SNS/SQS — ~£5/month at Jamtrack Radio message volumes
