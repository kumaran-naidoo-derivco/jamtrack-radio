# ADR-002: RS256 JWT for Authentication

**Status**: Accepted
**Date**: 2026-03-22

## Context

The platform needs stateless authentication that works across multiple microservices. The Identity Service issues tokens; all other services must validate them without calling back to Identity on every request. The signing algorithm choice determines the security model.

Options: HS256 (symmetric HMAC), RS256 (asymmetric RSA), ES256 (asymmetric ECDSA).

## Decision

Use **RS256 (RSA-SHA256)** for JWT signing.

- Identity Service holds the **private key** (in Key Vault at Phase 4+, in K8s Secret at Phase 3, in `.env.local` at Phase 2)
- All other services hold only the **public key** (distributed via a JWKS endpoint or mounted as a config file)
- Access token expiry: **15 minutes**
- Refresh token expiry: **90 days**, stored as SHA-256 hash in the database (never the raw token)
- Token claims: `sub` (userId), `email`, `roles[]`, `iat`, `exp`, `jti`

## Consequences

**What becomes easier:**
- No shared secret: downstream services cannot forge tokens even if compromised — they hold only the public key
- JWKS endpoint: public key rotation is transparent to consumers (they reload from the endpoint)
- Standard: widely understood, well-supported in `Microsoft.AspNetCore.Authentication.JwtBearer`
- Audit trail: `jti` (JWT ID) allows individual token revocation tracking

**What becomes harder:**
- Key management: the RSA private key is a critical secret. Loss = all tokens invalid. Compromise = all tokens forgeable. Azure Key Vault (Phase 4) is non-negotiable for production.
- Performance: RSA signing is ~10× slower than HMAC-SHA256. Acceptable at this scale; at 10,000+ logins/second, switch to ES256.
- Key rotation: requires a coordinated public key update across all services. JWKS endpoint mitigates this.

## Cost implication

£0 at Phase 2–3. Azure Key Vault at Phase 4: ~£1/month for key operations at this scale.
