# Security Architecture: Jamtrack Radio

**Date**: 2026-03-22
**Author**: Kintsugi (Security Architect)
**Status**: Accepted
**Skill**: `/arch-security jamtrack-radio` — DISCOVERY Step 5d
**Inputs**: `software-arch.md` (6 services), `data-arch.md` (data classification, schema), `jamtrack-radio-requirements.md` (RS256 JWT, TOTP AES-256, HTTPS mandatory)

---

## 1. Trust Boundary Diagram

Shows every trust boundary, data classification zone, and authentication mechanism between zones. Colour coding: Internet/Untrusted (red), DMZ/TLS-terminated (orange), Internal Service Network (blue), Data Zone (purple).

```drawio
<mxGraphModel dx="1422" dy="762" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="900" math="0" shadow="0">
  <root>
    <mxCell id="0" />
    <mxCell id="1" parent="0" />
    <mxCell id="2" value="&lt;b&gt;Internet / Untrusted&lt;/b&gt;" style="swimlane;startSize=25;fillColor=#ffcccc;strokeColor=#b71c1c;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="20" y="20" width="1100" height="120" as="geometry" />
    </mxCell>
    <mxCell id="3" value="&lt;b&gt;Browser Client&lt;/b&gt;&lt;br&gt;JavaScript SPA" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="2">
      <mxGeometry x="420" y="40" width="160" height="60" as="geometry" />
    </mxCell>
    <mxCell id="4" value="&lt;b&gt;DMZ / TLS-Terminated&lt;/b&gt;&lt;br&gt;&lt;i&gt;TLS 1.3 terminates here — no plain HTTP beyond this boundary&lt;/i&gt;" style="swimlane;startSize=25;fillColor=#ffe6cc;strokeColor=#e65100;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="20" y="180" width="1100" height="130" as="geometry" />
    </mxCell>
    <mxCell id="5" value="&lt;b&gt;Azure Application Gateway&lt;/b&gt;&lt;br&gt;+ WAF v2 (OWASP ruleset)&lt;br&gt;TLS termination&lt;br&gt;&lt;i&gt;Phase 4+; localhost Phase 2&lt;/i&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#E65100;" vertex="1" parent="4">
      <mxGeometry x="350" y="35" width="250" height="70" as="geometry" />
    </mxCell>
    <mxCell id="6" value="&lt;b&gt;Internal Service Network / Trusted&lt;/b&gt;&lt;br&gt;&lt;i&gt;JWT Bearer validated on every request — mTLS deferred to Phase 5&lt;/i&gt;" style="swimlane;startSize=25;fillColor=#dae8fc;strokeColor=#0078D4;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="20" y="350" width="1100" height="200" as="geometry" />
    </mxCell>
    <mxCell id="7" value="&lt;b&gt;Identity Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;&lt;br&gt;JWT issuance" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="6">
      <mxGeometry x="30" y="40" width="140" height="70" as="geometry" />
    </mxCell>
    <mxCell id="8" value="&lt;b&gt;Track Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="6">
      <mxGeometry x="210" y="40" width="140" height="70" as="geometry" />
    </mxCell>
    <mxCell id="9" value="&lt;b&gt;Playlist Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="6">
      <mxGeometry x="390" y="40" width="140" height="70" as="geometry" />
    </mxCell>
    <mxCell id="10" value="&lt;b&gt;Streaming Service&lt;/b&gt;&lt;br&gt;&lt;&lt;api&gt;&gt; REST&lt;br&gt;JWT + ownership check" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="6">
      <mxGeometry x="570" y="40" width="140" height="70" as="geometry" />
    </mxCell>
    <mxCell id="11" value="&lt;b&gt;Storage Service&lt;/b&gt;&lt;br&gt;&lt;&lt;gRPC&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="6">
      <mxGeometry x="750" y="40" width="140" height="70" as="geometry" />
    </mxCell>
    <mxCell id="12" value="&lt;b&gt;Dapr Pub/Sub&lt;/b&gt;&lt;br&gt;&lt;&lt;async&gt;&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="6">
      <mxGeometry x="930" y="40" width="130" height="70" as="geometry" />
    </mxCell>
    <mxCell id="13" value="&lt;b&gt;Data Zone / Most Trusted&lt;/b&gt;&lt;br&gt;&lt;i&gt;SSL connections only — credentials from Key Vault (Phase 4+)&lt;/i&gt;" style="swimlane;startSize=25;fillColor=#f3e5f5;strokeColor=#7b1fa2;dashed=1;rounded=1;fontStyle=1;" vertex="1" parent="1">
      <mxGeometry x="20" y="590" width="1100" height="180" as="geometry" />
    </mxCell>
    <mxCell id="14" value="&lt;b&gt;PostgreSQL&lt;/b&gt;&lt;br&gt;(per service, isolated)&lt;br&gt;Encrypted at rest" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="13">
      <mxGeometry x="80" y="35" width="180" height="100" as="geometry" />
    </mxCell>
    <mxCell id="15" value="&lt;b&gt;Azure Key Vault&lt;/b&gt;&lt;br&gt;RS256 private key&lt;br&gt;DB connection strings&lt;br&gt;TOTP encryption key" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="13">
      <mxGeometry x="380" y="35" width="160" height="100" as="geometry" />
    </mxCell>
    <mxCell id="16" value="&lt;b&gt;Azure Blob Storage&lt;/b&gt;&lt;br&gt;Audio files + artwork&lt;br&gt;No public URLs&lt;br&gt;Authenticated access only" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="13">
      <mxGeometry x="640" y="35" width="160" height="100" as="geometry" />
    </mxCell>
    <mxCell id="17" value="&lt;b&gt;Entra ID&lt;/b&gt;&lt;br&gt;Managed Identity&lt;br&gt;Workload Identity" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f3e5f5;strokeColor=#9e3799;" vertex="1" parent="13">
      <mxGeometry x="880" y="35" width="160" height="100" as="geometry" />
    </mxCell>
    <mxCell id="18" value="HTTPS TLS 1.3&lt;br&gt;&lt;i&gt;[STRIDE: Spoofing, Info Disclosure]&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="2" target="4" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="19" value="gRPC + JWT Bearer validation&lt;br&gt;&lt;i&gt;[STRIDE: Spoofing, EoP]&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="4" target="6" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="20" value="SSL + DB credentials from Key Vault&lt;br&gt;&lt;i&gt;[STRIDE: Info Disclosure]&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" source="6" target="13" parent="1">
      <mxGeometry relative="1" as="geometry" />
    </mxCell>
    <mxCell id="21" value="Managed Identity token&lt;br&gt;&lt;i&gt;[STRIDE: Info Disclosure]&lt;/i&gt;" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;" edge="1" source="6" target="13" parent="1">
      <mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="800" y="555" /><mxPoint x="800" y="590" /></Array></mxGeometry>
    </mxCell>
  </root>
</mxGraphModel>
```

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
