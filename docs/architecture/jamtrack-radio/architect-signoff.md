# Architect Sign-off: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Solutions Architect)
**Status**: ✅ Signed Off
**Skill**: `/architect jamtrack-radio` — DISCOVERY Step 6

---

## Cross-View Consistency Check

### 1. Service Boundaries (Software) ↔ K8s Namespaces (Cloud)

| Service (software-arch.md) | Namespace (cloud-arch.md) | Match? |
|---------------------------|--------------------------|--------|
| Identity Service | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| Track Service | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| Playlist Service | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| Streaming Service | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| Storage Service | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| API Gateway (YARP) | `jamtrack-prod` / `jamtrack-staging` | ✅ |
| Dapr control plane | `jamtrack-system` | ✅ |

All 6 application services deploy into the same AKS namespace pair, consistent with the single-user/single-tenant design. No namespace mismatch.

---

### 2. Data Ownership (Data) ↔ Service Responsibilities (Software)

| Table(s) | Owning service (data-arch.md) | Service that owns it (software-arch.md) | Match? |
|----------|------------------------------|----------------------------------------|--------|
| `users`, `refresh_tokens` | Identity Service | Identity — `IUserRepository`, `UserRepository` | ✅ |
| `tracks`, `tags`, `track_tags` | Track Service | Track — `ITrackRepository`, `TrackRepository` | ✅ |
| `playlists`, `playlist_tracks` | Playlist Service | Playlist — `IPlaylistRepository`, `PlaylistRepository` | ✅ |
| `storage_objects` | Storage Service | Storage — `IStorageService`, `AzureBlobStorageService` | ✅ |

No cross-service DB reads. Cross-service references use UUID values only (no relational FK across service boundaries). Consistent with the distributed monolith anti-pattern check.

---

### 3. Security Controls ↔ Data Classification (Security) ↔ Data Layer

| Data (data-arch.md) | Classification (security-arch.md) | Control (security-arch.md) | Applied in (software-arch.md) |
|--------------------|----------------------------------|--------------------------|------------------------------|
| `password_hash` | Secret | BCrypt cost 12 | `PasswordHash` value object in Identity Domain |
| `totp_seed_enc` | Secret | AES-256-GCM, Key in Key Vault | `TotpSeed` value object; `TotpService` in Identity Application |
| `token_hash` | Secret | SHA-256 hash — raw token never stored | `RefreshToken` entity; `RefreshTokenCommand` |
| `email` | PII — Restricted | Hashed in logs; GDPR right to erasure | Serilog destructuring; soft-delete + hard-delete pipeline |
| `storage_ref`, `artwork_ref` | Confidential | Authenticated blob access; no public URLs | `Streaming Service` validates ownership via gRPC before streaming |
| RS256 private key | Secret | Key Vault + Managed Identity (Phase 3+), Workload Identity (Phase 7) | `LoginCommand` — `IdentityGrpcService` |

All classified data has a corresponding control. No secret data is unprotected. ✅

---

### 4. Security Controls ↔ Every Service Boundary

| Boundary | Authentication | Authorisation | Encryption |
|----------|---------------|--------------|------------|
| Internet → API Gateway | HTTPS TLS 1.3 | n/a (public entry) | TLS termination at App Gateway |
| API Gateway → Services | JWT Bearer validation middleware | Route-level role check | gRPC TLS (Phase 3+ over VNet) |
| API Gateway → Streaming | JWT Bearer validation | Track ownership validation | HTTPS |
| Services → PostgreSQL | SSL connection | DB credentials from Key Vault (Phase 3+) | Encrypted at rest (Azure-managed) |
| Services → Azure Key Vault | Managed Identity | RBAC: `Key Vault Secrets User` role | HTTPS |
| Services → Azure Blob | Managed Identity | RBAC: `Storage Blob Data Contributor` | HTTPS |
| Dapr sidecar ↔ Service | localhost (same pod) | — | mTLS between sidecars (Phase 5) |

Every boundary has authentication + encryption defined. ✅

---

## Total Cost of Ownership (TCO) — Aggregated

### Development (Phase 2): £0/month
All services run locally. No cloud infrastructure cost.

### Azure VMs (Phase 3–5): ~£37–50/month
Services deploy to Azure VMs with managed PostgreSQL and Key Vault. Use `terraform destroy` when not actively developing to minimise cost.

### Azure Container Apps (Phase 6): ~£55–70/month
Services move to ACA with scale-to-zero. VMs decommissioned.

### AKS Staging (Phase 7+): ~£197–256/month

| Source | Monthly |
|--------|---------|
| Cloud (cloud-arch.md §5) | £197 |
| Data (data-arch.md §8 — Log Analytics staging) | Included in cloud total |
| Security controls (security-arch.md §4) | £0 (Phase 4 controls: Key Vault £1, Dependabot £0) |
| **Staging total (base)** | **~£198/month** |
| + 30% buffer | **~£258/month** |

### Production — Baseline (Phase 7+): ~£1,143/month

| Source | Monthly |
|--------|---------|
| Compute + DB + App Gateway (cloud-arch.md §5) | £797 |
| Log Analytics 5 GB/day prod (data-arch.md §8) | £345 |
| WAF (security-arch.md §7) | Included in App Gateway above |
| Azure Service Bus (cloud-arch.md §5) | £8 |
| Key Vault + ACR + Blob + DNS | £8.60 |
| **Production baseline total** | **~£1,159/month** |

### Full TCO Table

| Scenario | Monthly | Annual |
|----------|---------|--------|
| Development (Phase 2) | £0 | £0 |
| Azure VMs (Phase 3–5) | ~£37–50 | ~£450–600 |
| ACA (Phase 6) | ~£55–70 | ~£660–840 |
| AKS Staging (Phase 7+) | ~£198–258 | ~£2,376–3,096 |
| AKS Production baseline (Phase 7+) | ~£1,159 | ~£13,908 |
| Production 2× load | ~£1,316 | ~£15,792 |
| Production 10× load | ~£1,727 | ~£20,724 |

**Budget note**: Phases 3–6 comfortably fit within the £50–100/month budget. AKS (Phase 7+) requires cost optimisation (spot nodes, auto-shutdown — see cloud-arch §7) to stay near the upper bound.

---

## Architectural Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Dapr adds complexity in Phase 2 before value is evident | High | Low | Implement gRPC direct calls first; introduce Dapr at Phase 3 (VM) |
| Budget overrun in Phase 7 (prod vs staging sizing confusion) | Medium | Medium | Auto-shutdown staging; burstable SKUs; Azure Cost Management budget alert from day one |
| ACA → AKS migration complexity | Medium | Medium | Ensure service mesh and networking behaviour is equivalent between ACA and AKS; test Dapr component portability before decommissioning ACA |
| `storage_ref` set asynchronously — track upload appears incomplete to user | Medium | Medium | Return upload status as `pending` until `StorageObjectCreated` event received; poll endpoint or webhook |
| Key rotation complexity — RS256 private key | Low | High | JWKS endpoint from day one; never hardcode key in application |
| pg_trgm full-text search insufficient at 10,000+ tracks | Low | Low | Evaluate at Phase 6; Elasticsearch already in ELK stack as fallback |

---

## Sign-off

All four architecture views are consistent. No contradictions between service boundaries, data ownership, K8s namespaces, or security controls. TCO accepted.

**Gate**: ✅ Proceed to `/project-plan` — GitHub milestones and issues creation.

| View | Author | Status |
|------|--------|--------|
| Software Architecture (`software-arch.md`) | Kintsugi | ✅ Accepted |
| Cloud Architecture (`cloud-arch.md`) | Kintsugi | ✅ Accepted |
| Data Architecture (`data-arch.md`) | Kintsugi | ✅ Accepted |
| Security Architecture (`security-arch.md`) | Kintsugi | ✅ Accepted |
| ADR-001 through ADR-005 (`docs/decisions/`) | Kintsugi | ✅ Accepted |

**Next step**: Run `/project-plan jamtrack-radio` to produce `docs/project-plan/jamtrack-radio-plan.md` and create all GitHub milestones and sprint issues.
