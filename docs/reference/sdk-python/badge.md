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
    print(f"✅ Agent {result.claims.agent_id} verified")
    print(f"   Trust Level: {result.claims.trust_level}")
    print(f"   Domain: {result.claims.domain}")
else:
    print(f"❌ Verification failed: {result.error}")
```

---

## Functions

### verify_badge

Verify a Trust Badge token with full RFC-002 validation.

```python
def verify_badge(
    token: str,
    *,
    trusted_issuers: Optional[List[str]] = None,
    audience: Optional[str] = None,
    mode: VerifyMode = VerifyMode.ONLINE,
    skip_revocation_check: bool = False,
    skip_agent_status_check: bool = False,
    public_key_jwk: Optional[str] = None,
    options: Optional[VerifyOptions] = None,
) -> VerifyResult
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | The badge JWT/JWS token to verify |
| `trusted_issuers` | `List[str]` | Trusted issuer URLs. If empty, all issuers accepted |
| `audience` | `str` | Your service URL for audience validation |
| `mode` | `VerifyMode` | Verification mode (online, offline, hybrid) |
| `skip_revocation_check` | `bool` | Skip revocation check (testing only) |
| `skip_agent_status_check` | `bool` | Skip agent status check (testing only) |
| `public_key_jwk` | `str` | Override public key for offline verification |
| `options` | `VerifyOptions` | Alternative to individual parameters |

**Returns:** `VerifyResult` with validation status and claims.

**Example:**

```python
from capiscio_sdk import verify_badge

# Basic verification
result = verify_badge(token)

# With trusted issuers (recommended for production)
result = verify_badge(
    token,
    trusted_issuers=["https://registry.capisc.io", "https://my-ca.example.com"],
)

# With audience check
result = verify_badge(
    token,
    audience="https://my-agent.example.com",
)
```

---

### parse_badge

Parse badge claims without verification. Use for inspection before full verification.

```python
def parse_badge(token: str) -> BadgeClaims
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `token` | `str` | The badge JWT/JWS token to parse |

**Returns:** `BadgeClaims` object with parsed claims.

**Raises:** `ValueError` if the token cannot be parsed.

**Example:**

```python
from capiscio_sdk import parse_badge

# Inspect badge before verification
claims = parse_badge(token)
print(f"Agent: {claims.agent_id}")
print(f"Issuer: {claims.issuer}")
print(f"Expires: {claims.expires_at}")
print(f"Expired: {claims.is_expired}")
```

---

### request_badge

Request a new Trust Badge from a Certificate Authority (async).

```python
async def request_badge(
    agent_id: str,
    *,
    ca_url: str = "https://registry.capisc.io",
    api_key: Optional[str] = None,
    domain: Optional[str] = None,
    trust_level: TrustLevel = TrustLevel.LEVEL_1,
    audience: Optional[List[str]] = None,
    timeout: float = 30.0,
) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent_id` | `str` | Agent identifier to request badge for |
| `ca_url` | `str` | Certificate Authority URL |
| `api_key` | `str` | API key for CA authentication |
| `domain` | `str` | Agent's domain (required for verification) |
| `trust_level` | `TrustLevel` | Requested trust level |
| `audience` | `List[str]` | Optional audience restrictions |
| `timeout` | `float` | Request timeout in seconds |

**Returns:** The signed badge JWT token.

**Example:**

```python
import asyncio
from capiscio_sdk import request_badge, TrustLevel

async def get_badge():
    token = await request_badge(
        agent_id="my-agent",
        ca_url="https://registry.capisc.io",
        api_key=os.environ["CAPISCIO_API_KEY"],
        domain="example.com",
        trust_level=TrustLevel.LEVEL_2,
    )
    return token

badge = asyncio.run(get_badge())
```

---

### request_badge_sync

Synchronous version of `request_badge`.

```python
def request_badge_sync(
    agent_id: str,
    *,
    ca_url: str = "https://registry.capisc.io",
    api_key: Optional[str] = None,
    domain: Optional[str] = None,
    trust_level: TrustLevel = TrustLevel.LEVEL_1,
    audience: Optional[List[str]] = None,
    timeout: float = 30.0,
) -> str
```

**Example:**

```python
from capiscio_sdk import request_badge_sync

token = request_badge_sync(
    agent_id="my-agent",
    api_key=os.environ["CAPISCIO_API_KEY"],
    domain="example.com",
)
```

---

## Classes

### BadgeClaims

Parsed badge claims from a Trust Badge token.

```python
@dataclass
class BadgeClaims:
    jti: str                    # Unique badge identifier (UUID)
    issuer: str                 # Badge issuer URL (CA)
    subject: str                # Agent DID (did:web format)
    issued_at: datetime         # When issued
    expires_at: datetime        # When expires
    trust_level: TrustLevel     # Trust level (1=DV, 2=OV, 3=EV)
    domain: str                 # Agent's verified domain
    agent_name: str             # Human-readable name
    audience: List[str]         # Intended audience URLs
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `agent_id` | `str` | Extracted agent ID from subject DID |
| `is_expired` | `bool` | Whether badge has expired |
| `is_not_yet_valid` | `bool` | Whether badge is not yet valid |

**Methods:**

| Method | Description |
|--------|-------------|
| `from_dict(data)` | Create from dictionary |
| `to_dict()` | Convert to dictionary |

---

### VerifyResult

Result of badge verification.

```python
@dataclass
class VerifyResult:
    valid: bool                           # Whether valid
    claims: Optional[BadgeClaims]         # Parsed claims
    error: Optional[str]                  # Error message
    error_code: Optional[str]             # RFC-002 error code
    warnings: List[str]                   # Non-fatal issues
    mode: VerifyMode                      # Mode used
```

---

### VerifyOptions

Options for badge verification.

```python
@dataclass
class VerifyOptions:
    mode: VerifyMode = VerifyMode.ONLINE
    trusted_issuers: List[str] = []
    audience: Optional[str] = None
    skip_revocation_check: bool = False
    skip_agent_status_check: bool = False
    public_key_jwk: Optional[str] = None
```

**Example:**

```python
from capiscio_sdk import verify_badge, VerifyOptions, VerifyMode

options = VerifyOptions(
    mode=VerifyMode.HYBRID,
    trusted_issuers=["https://registry.capisc.io"],
    audience="https://my-service.example.com",
)

result = verify_badge(token, options=options)
```

---

### VerifyMode

Badge verification mode.

```python
class VerifyMode(Enum):
    ONLINE = "online"    # Real-time checks against registry
    OFFLINE = "offline"  # Local trust store and cache only
    HYBRID = "hybrid"    # Try online, fall back to cache
```

---

### TrustLevel

Trust level as defined in RFC-002.

```python
class TrustLevel(Enum):
    LEVEL_1 = "1"  # Domain Validated (DV)
    LEVEL_2 = "2"  # Organization Validated (OV)
    LEVEL_3 = "3"  # Extended Validation (EV)
```

| Level | Name | Description |
|-------|------|-------------|
| 1 | Domain Validated (DV) | Basic domain ownership verification |
| 2 | Organization Validated (OV) | Business identity verification |
| 3 | Extended Validation (EV) | Rigorous vetting process |

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
    
    # Attach claims to request state
    request.state.agent_claims = result.claims
    return await call_next(request)
```

### Trust Level Gate

```python
from capiscio_sdk import verify_badge, TrustLevel

def require_trust_level(token: str, min_level: TrustLevel) -> bool:
    """Require minimum trust level for sensitive operations."""
    result = verify_badge(token)
    
    if not result.valid:
        return False
    
    # Compare trust levels
    level_order = {TrustLevel.LEVEL_1: 1, TrustLevel.LEVEL_2: 2, TrustLevel.LEVEL_3: 3}
    return level_order[result.claims.trust_level] >= level_order[min_level]

# Usage
if require_trust_level(token, TrustLevel.LEVEL_2):
    # Allow sensitive operation
    pass
```

---

## See Also

- [Trust Badges Guide](../../how-to/security/badges.md) - CLI usage
- [Badge Keeper](../../how-to/security/badge-keeper.md) - Auto-renewal
- [Trust Model](../../concepts/trust-model.md) - Identity concepts
