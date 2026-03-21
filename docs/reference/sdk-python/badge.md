---
title: Badge API
description: Trust Badge verification and management for agent identity
---

# Badge API

The Badge API provides portable, verifiable identity for agents through Trust Badges—signed JWS tokens that prove an agent's identity and trust level.

!!! info "RFC-002 Implementation"
    This API implements RFC-002: Trust Badge System for portable agent identity.

---

## Quick Start

```python
from capiscio_sdk import verify_badge, parse_badge, TrustLevel

# Verify a badge from another agent
result = verify_badge(
    token,
    trusted_issuers=["https://registry.capisc.io"],
    audience="https://my-service.example.com",
)

if result.valid:
    print(f"✅ Agent {result.claims.subject} verified")  # Agent DID
    print(f"   Trust Level: {result.claims.trust_level.value}")  # "0" to "4"
    print(f"   Domain: {result.claims.domain}")
    print(f"   IAL: {result.claims.ial}")  # Identity Assurance Level
else:
    print(f"❌ Verification failed: {result.error}")
```

---

## Functions

::: capiscio_sdk.badge.verify_badge
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.parse_badge
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.request_badge
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.request_badge_sync
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.request_pop_badge
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.request_pop_badge_sync
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.start_badge_keeper
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

---

## Classes

::: capiscio_sdk.badge.BadgeClaims
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.VerifyResult
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.VerifyOptions
    options:
      show_root_heading: true
      show_source: false
      members_order: source
      heading_level: 3
      show_signature_annotations: true
      separate_signature: true
      docstring_style: google
      docstring_section_style: spacy

::: capiscio_sdk.badge.VerifyMode
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      docstring_style: google

::: capiscio_sdk.badge.TrustLevel
    options:
      show_root_heading: true
      show_source: false
      heading_level: 3
      docstring_style: google

---

## Error Codes

RFC-002 defines these verification error codes:

| Code | Description |
|------|-------------|
| `BADGE_MALFORMED` | Token format invalid |
| `BADGE_SIGNATURE_INVALID` | Signature verification failed |
| `BADGE_EXPIRED` | Badge past expiration time |
| `BADGE_NOT_YET_VALID` | Badge not yet valid (iat in future) |
| `BADGE_ISSUER_UNTRUSTED` | Issuer not in trusted list |
| `BADGE_AUDIENCE_MISMATCH` | Your service not in audience |
| `BADGE_REVOKED` | Badge has been revoked |
| `BADGE_CLAIMS_INVALID` | Required claims missing/invalid |
| `BADGE_AGENT_DISABLED` | Agent has been disabled |

---

## Patterns

### Middleware Pattern

```python
from capiscio_sdk import verify_badge
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def verify_badge_middleware(request: Request, call_next):
    # Skip for health checks
    if request.url.path == "/health":
        return await call_next(request)
    
    # Get badge from Authorization header
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing badge")
    
    token = auth[7:]
    result = verify_badge(
        token,
        trusted_issuers=["https://registry.capisc.io"],
        audience=str(request.base_url),
    )
    
    if not result.valid:
        raise HTTPException(401, f"Invalid badge: {result.error}")
    
    # Attach claims to request state (matches SDK middleware pattern)
    request.state.agent = result.claims
    request.state.agent_id = result.claims.issuer
    return await call_next(request)
```

!!! tip "Use Built-in Middleware"
    For production, consider using the SDK's built-in `CapiscioMiddleware` which handles
    body integrity verification and proper error responses per RFC-002 §9.1.

### Trust Level Gate

```python
from capiscio_sdk import verify_badge, TrustLevel

def require_trust_level(token: str, min_level: TrustLevel) -> bool:
    """Require minimum trust level for sensitive operations.
    
    RFC-002 §5 Trust Levels:
    - LEVEL_0: Self-Signed (SS) - development only
    - LEVEL_1: Registered (REG) - account registration
    - LEVEL_2: Domain Validated (DV) - DNS/HTTP proof
    - LEVEL_3: Organization Validated (OV) - legal entity
    - LEVEL_4: Extended Validated (EV) - security audit
    """
    result = verify_badge(token)
    
    if not result.valid:
        return False
    
    # TrustLevel enum values are strings "0"-"4", compare as integers
    return int(result.claims.trust_level.value) >= int(min_level.value)

# Usage
if require_trust_level(token, TrustLevel.LEVEL_2):
    # Allow sensitive operation (DV or higher)
    pass
```

---

## See Also

- [Trust Badges Guide](../../how-to/security/badges.md) - CLI usage
- [Badge Keeper](../../how-to/security/badge-keeper.md) - Auto-renewal
- [Trust Model](../../concepts/trust-model.md) - Identity concepts
