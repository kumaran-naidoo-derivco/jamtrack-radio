# Security Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Security Architect)
**Status**: Accepted
**Skill**: `/arch-security jamtrack-radio` — DISCOVERY Step 5d
**Inputs**: `software-arch.md` (6 services), `data-arch.md` (data classification, schema), `jamtrack-radio-requirements.md` (RS256 JWT, TOTP AES-256, HTTPS mandatory)

---

## 1. Trust Boundary Diagram

Shows every trust boundary, data classification zone, and authentication mechanism between zones. Colour coding: Internet/Untrusted (red), DMZ/TLS-terminated (orange), Internal Service Network (blue), Data Zone (purple).

> **Diagram**: [trust-boundaries.drawio](diagrams/trust-boundaries.drawio)
> _Open in VS Code with the [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) extension (`hediet.vscode-drawio`)_

---

## 2. Data Classification

| Data type | Classification | Examples | Protection required |
|-----------|---------------|----------|-------------------|
| Public | Public | Track titles, genres, artist names, playlist names | Integrity only (no tampering) |
| User-private | Confidential | Listening history, stream events, display name | Access control, user data isolation |
| PII | Restricted | Email addresses, IP addresses, OAuth subjects | GDPR controls, hashed in logs, pseudonymised in analytics |
| Credentials | Secret | Password hashes, refresh token hashes, TOTP seeds | BCrypt / SHA-256 / AES-256; never logged; Key Vault at Phase 4 |
| Signing keys | Secret | RS256 private key | Key Vault (Phase 4+); K8s Secret (Phase 3); `.env.local` (Phase 2) |

---

## 3. STRIDE Threat Model

| Threat | Example | Affected component | Likelihood | Impact | Risk | Control |
|--------|---------|-------------------|------------|--------|------|---------|
| **Spoofing** | Forged JWT `sub` claim | All services | Medium | High | High | RS256 signature validation on every request; `jti` claim for token uniqueness |
| **Spoofing** | OAuth token replay | Identity Service | Low | High | Medium | OAuth state parameter; PKCE flow; tokens discarded after user profile extraction |
| **Tampering** | SQL injection in track search | Track Service | Medium | High | High | Dapper parameterised queries by default; never string-interpolate SQL |
| **Tampering** | Playlist reorder with forged `userId` | Playlist Service | Medium | High | High | `userId` extracted from JWT claims — never from request body |
| **Repudiation** | Denied track deletion | Track Service | Low | Medium | Low | Immutable audit log: `track.deleted` event with `userId` and `timestamp` |
| **Information Disclosure** | Stack trace in error response | All services | High | Medium | High | `ProblemDetails` middleware; suppress details in production |
| **Information Disclosure** | Email address in logs | All services | High | Medium | High | Serilog destructuring exclusion for `email`, `password`, `token` fields |
| **Information Disclosure** | Audio file accessible without auth | Streaming Service | Medium | High | High | All streaming endpoints require Bearer JWT; no public blob URLs |
| **Denial of Service** | Brute-force login | Identity Service | High | High | High | Rate limiting: 5 attempts/min per IP; exponential backoff; account lockout at 10 |
| **Denial of Service** | Large file upload flood | Track Service / Storage | Medium | Medium | Medium | File size limit: 500 MB per upload; upload rate limit per user |
| **Escalation of Privilege** | User accessing another user's tracks | Track Service | Medium | High | High | `userId` claim validation on every Track/Playlist/Stream endpoint; 403 if mismatch |
| **Escalation of Privilege** | Non-admin accessing admin endpoints | All services | Medium | High | High | `role:admin` claim required; deny-by-default; `[AllowAnonymous]` only on register/login |

---

## 4. Security Controls Matrix

| Control | Implementation | Phase | Cost | Covers |
|---------|---------------|-------|------|--------|
| Password hashing | BCrypt (cost factor 12) via `BCrypt.Net-Next` | Phase 2 | £0 | Spoofing — credential theft |
| JWT RS256 validation | `Microsoft.AspNetCore.Authentication.JwtBearer` | Phase 2 | £0 | Spoofing, escalation |
| TOTP 2FA | `Otp.NET`; seed encrypted with AES-256-GCM | Phase 2 | £0 | Spoofing — account takeover |
| Input validation | `FluentValidation` on all gRPC request DTOs | Phase 2 | £0 | Tampering, DoS |
| Rate limiting | `AspNetCoreRateLimit` (5 req/min on auth endpoints) | Phase 2 | £0 | DoS — brute force |
| HTTPS only | `UseHttpsRedirection()` + HSTS | Phase 2 | £0 | Information disclosure |
| Parameterised queries | Dapper default — no string SQL concatenation | Phase 2 | £0 | Tampering — SQL injection |
| User data isolation | `userId` from JWT on every endpoint; 403 on mismatch | Phase 2 | £0 | Escalation of privilege |
| Secrets in environment | `.env.local` gitignored; never in `appsettings.json` | Phase 2 | £0 | Information disclosure |
| Generic error responses | `ProblemDetails` middleware suppresses stack traces | Phase 2 | £0 | Information disclosure |
| Scrub sensitive fields in logs | `Serilog.Destructuring` — exclude `email`, `password`, `token` | Phase 2 | £0 | Information disclosure |
| K8s Secrets for credentials | Replace `.env.local` with K8s Secrets | Phase 3 | £0 | Information disclosure |
| Network policies (default-deny) | K8s NetworkPolicy per namespace | Phase 3 | £0 | Spoofing, escalation |
| Azure Key Vault | RS256 private key, DB connection strings | Phase 4 | ~£1/month | Information disclosure |
| WAF (OWASP ruleset) | Azure Application Gateway WAF v2 | Phase 4 | ~£183/month | Tampering, DoS |
| Managed Identity | All AKS → Azure service auth via Entra ID workload identity | Phase 4 | £0 | Information disclosure — no credential secrets in pods |
| Audit logging to ELK | Serilog structured events → Log Analytics | Phase 4 | Log storage cost | Repudiation |
| Signed container images | Cosign + Azure Container Registry trust policy | Phase 5 | £0 | Tampering — supply chain |
| mTLS between services | Dapr mTLS (built-in) | Phase 5 | Operational cost | Spoofing — internal network |

---

## 5. Authentication & Authorisation Map

| Endpoint | AuthN | AuthZ rule | Claims required |
|----------|-------|------------|----------------|
| `POST /auth/register` | None | Public | — |
| `POST /auth/login` | None | Public | — |
| `POST /auth/refresh` | Refresh token (body) | Valid, unexpired, not revoked | — |
| `POST /auth/totp/enable` | Bearer JWT | Authenticated user | `sub` |
| `GET /tracks` | Bearer JWT | Authenticated user; own tracks only | `sub` |
| `POST /tracks` | Bearer JWT | Authenticated user | `sub` |
| `PUT /tracks/{id}` | Bearer JWT | Track owner only (`userId == sub`) | `sub` |
| `DELETE /tracks/{id}` | Bearer JWT | Track owner only | `sub` |
| `GET /playlists` | Bearer JWT | Authenticated user; own playlists only | `sub` |
| `POST /playlists` | Bearer JWT | Authenticated user | `sub` |
| `PUT /playlists/{id}` | Bearer JWT | Playlist owner only | `sub` |
| `GET /stream/{trackId}` | Bearer JWT | Track owner only | `sub` |
| Admin endpoints (`/admin/*`) | Bearer JWT | Admin role only | `sub`, `role:admin` |

**JWT design:**
- Access token expiry: **15 minutes**
- Refresh token expiry: **90 days** — stored as SHA-256 hash in `refresh_tokens` table
- Signing: **RS256** — private key in Key Vault (Phase 4+), K8s Secret (Phase 3), `.env.local` (Phase 2)
- Claims: `sub` (userId), `email`, `roles[]`, `iat`, `exp`, `jti`
- TOTP: optional; enabled per user; seed encrypted with AES-256-GCM before storage; encryption key in Key Vault

---

## 6. OWASP Top 10 Checklist

| # | Category | Status | Implementation |
|---|----------|--------|---------------|
| A01 | Broken Access Control | ✅ Controlled | Deny-by-default; `userId` from JWT on every endpoint; 403 on mismatch |
| A02 | Cryptographic Failures | ✅ Controlled | BCrypt passwords; HTTPS; RS256 JWT; AES-256-GCM for TOTP seeds |
| A03 | Injection | ✅ Controlled | Dapper parameterised queries; `FluentValidation` on all inputs |
| A04 | Insecure Design | ✅ In progress | This document — STRIDE threat model + controls matrix |
| A05 | Security Misconfiguration | ⚠️ Monitor | No default credentials; no stack traces in prod; `X-Powered-By` removed |
| A06 | Vulnerable Components | ⚠️ Monitor | Dependabot enabled; `dotnet-outdated` in CI (Phase 3) |
| A07 | Identity & Auth Failures | ✅ Controlled | Rate limiting; RS256 JWT; short expiry; refresh token rotation; TOTP |
| A08 | Software & Data Integrity | ⚠️ Phase 5 | Signed container images (Cosign + ACR); SBOM generation in CI |
| A09 | Security Logging & Monitoring | ⚠️ Phase 4 | Structured Serilog events; ELK alerts on `login_failed` spikes |
| A10 | SSRF | ✅ N/A (Phase 2) | No user-controllable URLs at Phase 2; evaluate at Phase 4 for webhook features |

---

## 7. Security Cost / Risk Tradeoff

| Control | Cost | Threat probability | Threat impact | Risk | Verdict |
|---------|------|-------------------|---------------|------|---------|
| BCrypt hashing | £0 dev time | High (credential stuffing common) | Critical | Critical | Must do — Phase 2 |
| Rate limiting | ~2h dev time | High (brute force on login) | High | High | Must do — Phase 2 |
| User data isolation | ~1h per endpoint | Medium (curious users) | High | High | Must do — Phase 2 |
| TOTP 2FA | ~1 day dev time | Medium (account takeover) | High | High | Must do — Phase 2 |
| Azure Key Vault | ~£1/month | Medium (secret exposure) | Critical | High | Phase 4 — do on first Azure deploy |
| WAF | ~£183/month | Medium (OWASP attacks) | High | High | Phase 4 |
| mTLS between services | Operational overhead | Low (internal VNet attack) | High | Medium | Phase 5 — defer |
| HSM for JWT signing | £750+/month | Very low | Critical | Medium | Defer indefinitely — oversized for Jamtrack Radio scale |
| Penetration test | £5,000–10,000 | — | — | — | Phase 4 go-live if real users |
