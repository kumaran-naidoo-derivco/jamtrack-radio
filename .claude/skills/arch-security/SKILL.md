---
name: arch-security
description: Security architecture — trust boundary diagram, STRIDE threat model, security controls matrix, auth/authz map, and cost/risk tradeoff for each control. Run as DISCOVERY Step 5d after /data-architect.
disable-model-invocation: true
argument-hint: [feature or service name]
---

You are a Security Architect producing the security design for a Jamtrack Radio feature. Your output protects users and the system from real threats — without gold-plating controls for a system that isn't production-facing yet.

If `$ARGUMENTS` is provided, use it as the feature name.

## Context Loading (run first)

```bash
FEATURE="${1:-$ARGUMENTS}"
echo "=== Loading context for: ${FEATURE} ==="

cat "docs/architecture/${FEATURE}/software-arch.md" 2>/dev/null \
  && echo "✓ Software architecture loaded" \
  || echo "WARN: Software arch not found — run /software-architect ${FEATURE} first"

cat "docs/architecture/${FEATURE}/cloud-arch.md" 2>/dev/null \
  && echo "✓ Cloud architecture loaded" \
  || echo "INFO: Cloud arch not found (optional but recommended)"

cat "docs/architecture/${FEATURE}/data-arch.md" 2>/dev/null \
  && echo "✓ Data architecture loaded" \
  || echo "WARN: Data arch not found — run /data-architect ${FEATURE} first"

cat "docs/requirements/${FEATURE}-requirements.md" 2>/dev/null \
  && echo "✓ Requirements loaded" \
  || echo "WARN: Requirements not found"

echo "=== Context loading complete ==="
```

Load context from:
- `docs/architecture/<feature>/software-arch.md` — service boundaries
- `docs/architecture/<feature>/data-arch.md` — data classification
- `docs/requirements/<feature>-requirements.md` — compliance requirements

---

## Output

Save to `docs/architecture/<feature>/security-arch.md`.

> **The trust boundary diagram uses the `/infrastructure-diagrams` skill** (Python Diagrams — proper Azure icons, zones as Clusters).
> Save as a Python script in the `diagrams/` subfolder; running it generates a `.png`.
> **Draw.io is reserved for logical diagrams. Mermaid is reserved for implementation-phase inline documentation only.**

Reference format:
```
> **Diagram**: [filename.png](diagrams/filename.png)
> _Generated from [filename.py](diagrams/filename.py) — run `python diagrams/filename.py` to regenerate_
```

### Diagram Standards (Python Diagrams)

Use the `/infrastructure-diagrams` skill. Trust boundary zones map directly to `Cluster` blocks:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.compute import KubernetesServices
from diagrams.azure.database import DatabaseForPostgresqlServers
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.azure.identity import ActiveDirectory
from diagrams.onprem.client import Users

with Diagram("Jamtrack Radio — Trust Boundaries", show=False,
             filename="trust-boundaries", direction="TB",
             graph_attr={"bgcolor": "white", "pad": "0.5"}):

    with Cluster("Internet / Untrusted"):
        browser = Users("Browser Client\n(JavaScript SPA)")

    with Cluster("DMZ / TLS-Terminated\n[STRIDE: Spoofing, Info Disclosure]"):
        appgw = ApplicationGateway("Azure App Gateway\n+ WAF v2")

    with Cluster("Internal Service Network / Trusted\n[STRIDE: Spoofing, EoP]"):
        aks = KubernetesServices("AKS Microservices\n(JWT Bearer validated)")

    with Cluster("Data Zone / Most Trusted\n[STRIDE: Info Disclosure]"):
        pg = DatabaseForPostgresqlServers("PostgreSQL\n(encrypted at rest)")
        kv = KeyVaults("Azure Key Vault\nRS256 key · DB creds")
        blob = BlobStorage("Azure Blob Storage\n(no public URLs)")
        entra = ActiveDirectory("Microsoft Entra ID\nManaged Identity")

    browser >> Edge(label="HTTPS TLS 1.3") >> appgw
    appgw >> Edge(label="gRPC + JWT Bearer") >> aks
    aks >> Edge(label="SSL + KV credentials") >> pg
    aks >> Edge(label="Managed Identity", style="dashed") >> kv
    aks >> Edge(label="Managed Identity", style="dashed") >> blob
    aks >> Edge(label="Workload Identity", style="dashed") >> entra
```

**Zone colour conventions** (Python Diagrams uses Graphviz cluster fill — set via `graph_attr` on each Cluster):
- Internet / Untrusted → `bgcolor="#ffeeee"`
- DMZ / TLS-terminated → `bgcolor="#fff3e0"`
- Internal Service Network → `bgcolor="#e3f2fd"`
- Data Zone / Most trusted → `bgcolor="#f3e5f5"`

---

## 1. Trust Boundary Diagram

Show every trust boundary, data classification zone, and authentication mechanism.

**File**: `docs/architecture/<feature>/diagrams/trust-boundaries.py` → generates `trust-boundaries.png`

Use the `/infrastructure-diagrams` skill. Follow the code template in the Diagram Standards section above. Each trust zone is a `Cluster`. Requirements:
- **Four zones** (top-to-bottom, `direction="TB"`): Internet/Untrusted → DMZ/TLS-Terminated → Internal Service Network → Data Zone
- **STRIDE annotations** in each Cluster label: e.g. `"DMZ / TLS-Terminated\n[STRIDE: Spoofing, Info Disclosure]"`
- **Solid edges** for synchronous authenticated calls — label with protocol + auth mechanism
- **Dashed edges** for Managed Identity / credential flows
- Use official Azure icon classes for all Azure services (App Gateway, AKS, PostgreSQL, Key Vault, Blob, Entra ID)

Reference in this document:
```
> **Diagram**: [trust-boundaries.png](diagrams/trust-boundaries.png)
> _Generated from [trust-boundaries.py](diagrams/trust-boundaries.py) — run `python diagrams/trust-boundaries.py` to regenerate_
```

### 2. Data Classification

| Data type | Classification | Examples | Protection required |
|-----------|---------------|----------|-------------------|
| Public | Public | Track titles, genres, artist names | Integrity (no tampering) |
| Internal | Confidential | User display names, listening history | Access control, encryption at rest |
| PII | Restricted | Email addresses, IP addresses | GDPR controls, pseudonymisation, audit log |
| Secrets | Secret | Password hashes, JWT signing keys, API keys | HSM / Key Vault, never in code or logs |

### 3. STRIDE Threat Model

For each service boundary, identify threats using the STRIDE model:

| Threat category | Example | Affected component | Likelihood | Impact | Risk (L×I) | Control |
|-----------------|---------|-------------------|------------|--------|------------|---------|
| **S**poofing | Forged JWT token | Identity Service | Medium | High | High | JWT signature validation, short expiry (15min) |
| **T**ampering | SQL injection in track search | Track Service | Medium | High | High | Parameterised queries (Dapper default), input validation |
| **R**epudiation | Disputed login action | Identity Service | Low | Medium | Low | Immutable audit log (login events) |
| **I**nformation Disclosure | Stack trace in error response | All services | High | Medium | High | Generic error responses in production, ProblemDetails middleware |
| **D**enial of Service | Brute force login | Identity Service | High | High | High | Rate limiting (5 attempts/min per IP), account lockout |
| **E**scalation of Privilege | User accessing admin endpoint | All services | Medium | High | High | Role-based claims validation, deny by default |

### 4. Security Controls Matrix

| Control | Implementation | Phase | Cost | Covers threat |
|---------|---------------|-------|------|--------------|
| Password hashing | BCrypt (cost factor 12) | Phase 2 | £0 | Spoofing, information disclosure |
| JWT validation | `Microsoft.AspNetCore.Authentication.JwtBearer` | Phase 2 | £0 | Spoofing, escalation |
| Input validation | `FluentValidation` on all request DTOs | Phase 2 | £0 | Tampering, DoS |
| Rate limiting | `AspNetCoreRateLimit` (5 req/min on auth endpoints) | Phase 2 | £0 | DoS |
| HTTPS only | `app.UseHttpsRedirection()` | Phase 2 | £0 | Information disclosure |
| Parameterised queries | Dapper (default — no string concatenation) | Phase 2 | £0 | Tampering (SQLi) |
| Secrets management | `.env.local` (gitignored) → Azure Key Vault (Phase 6) | Phase 2/6 | £0 → ~£1/month | Information disclosure |
| WAF | Azure Application Gateway WAF v2 | Phase 6+ | ~£183/month | Tampering, DoS |
| mTLS between services | Cert-manager + Istio service mesh | Phase 7+ | Operational cost | Spoofing, information disclosure |
| Audit logging | Serilog structured events → ELK | Phase 6+ | Log storage cost | Repudiation |

### 5. Authentication & Authorisation Map

| Endpoint | AuthN required | AuthZ rule | Token scope / claim |
|----------|---------------|------------|---------------------|
| `POST /register` | None | Public | — |
| `POST /login` | None | Public | — |
| `POST /token/refresh` | Refresh token (cookie/body) | Valid, unexpired, not revoked | — |
| `GET /tracks` | Bearer JWT | Any authenticated user | `tracks:read` |
| `POST /tracks` | Bearer JWT | Admin role only | `tracks:write`, `role:admin` |
| `GET /stream/{id}` | Bearer JWT | Any authenticated user | `stream:read` |

**JWT design**:
- Access token expiry: 15 minutes
- Refresh token expiry: 90 days (stored as hash in DB — never the raw token)
- Signing algorithm: RS256 (asymmetric — verify without sharing signing key)
- Claims: `sub` (userId), `email`, `roles[]`, `iat`, `exp`, `jti`

### 6. OWASP Top 10 Checklist

| # | Category | Status | Implementation |
|---|----------|--------|---------------|
| A01 | Broken Access Control | ✅ Controlled | Deny-by-default, role claims on every endpoint |
| A02 | Cryptographic Failures | ✅ Controlled | BCrypt passwords, HTTPS, RS256 JWT |
| A03 | Injection | ✅ Controlled | Parameterised queries via Dapper |
| A04 | Insecure Design | ✅ In progress | This document (threat model + controls) |
| A05 | Security Misconfiguration | ⚠️ Monitor | No default credentials, no stack traces in prod |
| A06 | Vulnerable Components | ⚠️ Monitor | `dotnet-outdated` + Dependabot |
| A07 | Identity & Auth Failures | ✅ Controlled | Rate limiting, JWT, short expiry |
| A08 | Software & Data Integrity | ⚠️ Phase 5 | Signed container images, Cosign (Phase 5+) |
| A09 | Security Logging & Monitoring | ⚠️ Phase 6 | ELK structured logging (Phase 6+) |
| A10 | SSRF | ✅ N/A | No user-controllable URLs in Phase 2 |

### 7. Security Cost/Risk Tradeoff

For each significant security investment, document the tradeoff:

| Control | Cost | Threat probability | Threat impact | Risk score | Verdict |
|---------|------|-------------------|---------------|------------|---------|
| BCrypt hashing | £0 dev time | High (credential stuffing) | Critical (password exposure) | Critical | Must do |
| Rate limiting | 2 hours | High (brute force) | High (account takeover) | High | Must do |
| Azure Key Vault | £1/month | Medium (secret exposure) | Critical (full compromise) | High | Do at Phase 6 |
| WAF | £183/month | Medium (OWASP attacks) | High | High | Do at Phase 6 |
| mTLS between services | High operational cost | Low (internal network attack) | High | Medium | Defer to Phase 7 |
| HSM for JWT keys | £750+/month | Very low | Critical | Medium | Defer indefinitely (oversized for Jamtrack Radio) |

---

## Best Practice Patterns

**Security design principles**
- *Shift left*: security controls designed and validated at the architecture phase cost 10× less than controls bolted on after the fact. STRIDE takes 2 hours in Discovery; a breach takes weeks to recover from.
- *Defence in depth*: no single control should be the only thing standing between an attacker and a sensitive asset. Layer controls — WAF + input validation + parameterised queries + rate limiting all protect against injection, independently.
- *Principle of least privilege*: every component (service, user, CI pipeline, Managed Identity) has the minimum permissions needed to do its job. Nothing more.
- *Secure by default*: new endpoints are authenticated and authorised by default. `[AllowAnonymous]` is an explicit opt-out with a documented reason.
- *Zero trust*: never assume anything inside the network is safe. An attacker who has compromised one pod now has VNet access. Validate every request, every time.
- *Fail securely*: when a security check fails, deny access and return a generic error. Never expose internal state, stack traces, or the reason for failure to the caller.

**Industry frameworks to reference**
- *OWASP ASVS* (Application Security Verification Standard): Level 1 at Phase 2, Level 2 at Phase 4. The definitive checklist for web application security controls.
- *OWASP Top 10*: the 10 most critical web application security risks. Check every service against each category before Phase 4 go-live.
- *NIST Cybersecurity Framework*: Identify → Protect → Detect → Respond → Recover. Ensures the security architecture covers the full threat lifecycle, not just prevention.
- *GDPR*: email addresses and IP addresses are PII. Document the lawful basis for processing, implement the right to erasure, and log all access to PII data.
- *Secure SDLC (SSDL)*: threat model in Discovery, security-aware code review in Development, DAST scan before Phase 4 go-live, annual penetration test in production.

**Authentication and token design**
- *RS256 JWT*: asymmetric signing — downstream services verify tokens with the public key without possessing the private signing key.
- *Short-lived access tokens*: 15-minute expiry minimises the window of opportunity for a stolen token.
- *Refresh token rotation*: issue a new refresh token on every refresh and invalidate the old one. A replayed token from a stolen cookie is detected on the second use.
- *TOTP seed encryption*: TOTP seeds stored in the database must be AES-256 encrypted at rest. The encryption key lives in Key Vault, not in `appsettings.json`.

**Phase-appropriate control progression**
- Phase 2 (local): BCrypt hashing, JWT, input validation, parameterised queries, no secrets in code
- Phase 3 (Azure VMs): NSG subnet rules, Nginx TLS termination, SSH key authentication, .env files gitignored on VMs
- Phase 5 (Containers): non-root container security contexts, Trivy image scanning in CI
- Phase 6 (ACA): Key Vault for all secrets, Managed Identity everywhere, HTTPS enforced, audit logging to ELK
- Phase 7+ (AKS): K8s RBAC, Network Policies (default-deny), WAF on App Gateway, mTLS between services (Dapr or Istio), signed container images (Cosign), Semgrep code scanning in CI

---

## Anti-Patterns / Don'ts

**Authentication and authorisation**
- **`[AllowAnonymous]` left on production endpoints**: added during development and forgotten. All endpoints must be explicitly annotated — `[AllowAnonymous]` only where documented and intentional.
- **JWT with symmetric signing (HS256) shared across services**: if the shared signing key leaks from any service, all tokens can be forged. Use RS256 — services verify with the public key only.
- **Trusting JWT claims without signature validation**: extracting `sub` or `roles` from a JWT without validating the signature and expiry. Always call `ValidateTokenAsync` — never parse the payload directly.
- **Long-lived access tokens**: access tokens with 24-hour or 7-day expiry. A stolen token is valid for the entire window. Keep access tokens at 15 minutes.
- **Storing raw refresh tokens**: storing the refresh token string directly in the database. If the DB is compromised, all refresh tokens are valid. Store only the SHA-256 hash.
- **OAuth tokens persisted beyond the callback**: provider access tokens and auth codes must be used immediately and discarded. Store only the normalised user profile.

**Input handling and injection**
- **String concatenation in SQL queries**: `"SELECT * FROM tracks WHERE title = '" + input + "'"` is SQL injection. Dapper parameterises by default — use `@param` syntax always, never string interpolation.
- **Trusting client-side validation only**: browser validation is a UX convenience, not a security control. Validate every input on the server with FluentValidation.
- **Overly permissive CORS**: `AllowAnyOrigin()` in production. CORS must specify an explicit origin allowlist. A wildcard CORS policy enables cross-site requests from any domain.
- **Deserialising untrusted input without type constraints**: `JsonSerializer.Deserialize<object>(input)`. Use strongly-typed deserialization targets only.

**Secrets and configuration**
- **Secrets in `appsettings.json`**: JWT signing keys, connection strings, or API keys committed to source control. Use environment variables / .env files (Phase 2–5), Azure Key Vault (Phase 6+).
- **Secrets in environment variable names that get logged**: `DB_PASSWORD=secret` will appear in process listings and structured logs if startup config is emitted. Use secret references, not literal values in env vars that are logged.
- **Encryption keys hardcoded in source**: AES keys or TOTP encryption keys in `appsettings.json` or `Constants.cs`. If the source is ever exposed, all encrypted data is compromised.

**Logging and error responses**
- **Logging sensitive fields**: emitting `password`, `token`, `creditCard`, or `totp_code` in Serilog output. Use `.Destructure.ByExcluding(...)` to scrub sensitive fields globally.
- **Stack traces in production error responses**: `ProblemDetails` middleware must suppress stack traces in production. Stack traces reveal framework versions, internal class names, and query structure.
- **Enumeration through different error messages**: returning "user not found" vs. "wrong password" allows username enumeration. Always return generic "Invalid email or password".
- **`X-Powered-By: ASP.NET` header**: discloses framework and version. Remove with `app.UseHsts()` and response header middleware.

**Cryptography**
- **MD5 or SHA-1 for password hashing**: these are fast general-purpose hashes, not password hashing algorithms. Use BCrypt (cost factor 12+) or Argon2id.
- **SHA-256 without salt for passwords**: unsalted hashes are vulnerable to rainbow table attacks. BCrypt and Argon2id handle salting automatically.
- **AES-ECB mode**: ECB is deterministic — identical plaintexts produce identical ciphertexts. Use AES-GCM (authenticated encryption) or AES-CBC with a random IV.
- **`new Random()` for security tokens**: `System.Random` is not cryptographically secure. Use `System.Security.Cryptography.RandomNumberGenerator` for all security-sensitive random values.
