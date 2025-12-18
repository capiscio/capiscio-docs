---
title: Issue and Verify Trust Badges
description: Create and validate trust badges for agent authentication
---

# Issue and Verify Trust Badges

Create trust badges to authenticate your agent's identity and verify badges from other agents.

---

## Problem

You need to:

- Prove your agent's identity to other agents or registries
- Verify that incoming requests are from trusted agents
- Implement mutual authentication between agents

---

## Solution

=== "Python SDK"

    ### Verify a Badge

    ```python
    from capiscio_sdk import verify_badge, TrustLevel

    # Verify badge with trusted issuer check
    result = verify_badge(
        token,
        trusted_issuers=["https://registry.capisc.io"],
        audience="https://my-service.example.com",
    )

    if result.valid:
        print(f"✅ Agent: {result.claims.agent_id}")
        print(f"   Trust Level: {result.claims.trust_level}")
        print(f"   Domain: {result.claims.domain}")
    else:
        print(f"❌ Failed: {result.error}")
    ```

    ### Parse Without Verification

    ```python
    from capiscio_sdk import parse_badge

    # Inspect badge claims before verification
    claims = parse_badge(token)
    print(f"Issuer: {claims.issuer}")
    print(f"Expires: {claims.expires_at}")
    print(f"Is Expired: {claims.is_expired}")
    ```

    ### Request a New Badge

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

=== "CLI"

    ### Step 1: Generate a Key Pair

    First, create an Ed25519 key pair for signing badges:

    ```bash
    capiscio key gen --out-priv private.jwk --out-pub public.jwk
    ```

    !!! danger "Protect Your Private Key"
        Never share `private.jwk` or commit it to version control.

    ### Step 2: Issue a Badge

    Create a trust badge for your agent:

    ```bash
    capiscio badge issue \
      --sub "did:capiscio:agent:my-agent" \
      --domain "my-agent.example.com" \
      --exp 24h \
      --key ./private.jwk
    ```

    This outputs a JWT token:

    ```
    eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6Y2FwaXNjaW86YWdlbnQ6bXktYWdlbnQi...
    ```

    ### Step 3: Verify a Badge

    To verify a badge you've received:

    ```bash
    capiscio badge verify "eyJhbGciOiJFZERTQSI..." --key ./public.jwk
    ```

    Output on success:

    ```
    ✅ Badge Valid!
    Subject: did:capiscio:agent:my-agent
    Issuer: https://registry.capisc.io
    Expires: 2025-12-02T19:48:00Z
    ```

---

## Trust Levels

CapiscIO implements 5 trust levels (0-4) indicating the validation rigor applied during badge issuance:

| Level | Name | Validation | Issuer | Use Case |
|-------|------|------------|--------|----------|
| **0** | Self-Signed (SS) | None | Agent itself (`did:key`) | Development, testing, demos |
| **1** | Registered (REG) | Account verified | CapiscIO CA | Internal agents, early development |
| **2** | Domain Validated (DV) | DNS TXT or HTTP challenge | CapiscIO CA | Production B2B agents |
| **3** | Organization Validated (OV) | DV + legal entity verification | CapiscIO CA | High-trust production |
| **4** | Extended Validated (EV) | OV + manual security audit | CapiscIO CA | Regulated industries |

### Self-Signed Badges (Level 0)

For development and testing, issue self-signed badges:

=== "CLI"

    ```bash
    # Issue a self-signed badge (Level 0)
    capiscio badge issue --self-sign > badge.jwt
    
    # Verify with explicit self-signed acceptance
    capiscio badge verify --accept-self-signed < badge.jwt
    ```

=== "Python SDK"

    ```python
    from capiscio_sdk import verify_badge, TrustLevel

    # Development: Accept self-signed badges
    result = verify_badge(
        token,
        accept_self_signed=True,  # Required for Level 0
    )
    ```

!!! warning "Level 0 in Production"
    Self-signed badges are for **development only**. In production, verifiers should reject Level 0 badges by default.

### CA-Issued Badges (Levels 1-4)

For production use, obtain badges from the CapiscIO Registry:

```python
from capiscio_sdk import TrustLevel

# Check trust level thresholds
if result.claims.trust_level >= TrustLevel.LEVEL_2:
    print("Domain verified - standard access")
elif result.claims.trust_level >= TrustLevel.LEVEL_3:
    print("Organization verified - elevated access")
elif result.claims.trust_level == TrustLevel.LEVEL_4:
    print("Extended validation - full access granted")
else:
    print("Basic verification - limited access")
```

---

## Complete Example

Here's a full workflow for two agents authenticating with each other:

### Agent A: Issue and Share Badge

```bash
# Generate keys
capiscio key gen --out-priv alice-private.jwk --out-pub alice-public.jwk

# Issue badge
ALICE_BADGE=$(capiscio badge issue \
  --sub "did:capiscio:agent:alice" \
  --domain "alice.example.com" \
  --exp 1h \
  --key ./alice-private.jwk)

echo "Alice's badge: $ALICE_BADGE"

# Share alice-public.jwk with Bob (via secure channel)
```

### Agent B: Verify Alice's Badge

```bash
# Bob receives Alice's badge and public key
capiscio badge verify "$ALICE_BADGE" --key ./alice-public.jwk
```

---

## Badge Claims

The issued badge contains these JWT claims:

| Claim | Description | Example |
|-------|-------------|---------|
| `sub` | Subject DID | `did:capiscio:agent:my-agent` |
| `iss` | Issuer URL | `https://registry.capisc.io` |
| `iat` | Issued at (Unix timestamp) | `1733080880` |
| `exp` | Expiration (Unix timestamp) | `1733167280` |
| `domain` | Agent's domain | `my-agent.example.com` |

---

## Using Badges in Requests

Include the badge in HTTP requests to authenticated endpoints:

```bash
curl -X POST https://other-agent.example.com/api/task \
  -H "Authorization: Bearer $BADGE" \
  -H "Content-Type: application/json" \
  -d '{"task": "translate", "text": "Hello"}'
```

---

## Programmatic Usage (Python SDK)

The Python SDK provides a native API for badge verification (recommended over CLI subprocess):

```python
from capiscio_sdk import verify_badge, parse_badge, TrustLevel

# Verify a badge with full validation
result = verify_badge(
    token,
    trusted_issuers=["https://registry.capisc.io"],
    audience="https://my-agent.example.com",
)

if result.valid:
    claims = result.claims
    print(f"Agent: {claims.agent_id}")
    print(f"Trust Level: {claims.trust_level}")
    print(f"Domain: {claims.domain}")
    print(f"Expires: {claims.expires_at}")
else:
    print(f"Verification failed: {result.error}")
    print(f"Error code: {result.error_code}")
```

### FastAPI Middleware Example

```python
from capiscio_sdk import verify_badge
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.middleware("http")
async def badge_auth(request: Request, call_next):
    if request.url.path in ["/health", "/docs"]:
        return await call_next(request)
    
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "Missing badge token")
    
    result = verify_badge(
        auth[7:],
        trusted_issuers=["https://registry.capisc.io"],
    )
    
    if not result.valid:
        raise HTTPException(401, f"Invalid badge: {result.error}")
    
    request.state.agent = result.claims
    return await call_next(request)
```

---

## Troubleshooting

### "verification failed: token expired"

The badge has expired. Issue a new one or use `badge keep` for auto-renewal.

### "verification failed: invalid signature"

The public key doesn't match the private key used to sign. Ensure you're using the correct key pair.

### "failed to read key file"

Check the key path exists and has correct permissions.

---

## See Also

- [Badge API Reference](../../reference/sdk-python/badge.md) - Full Python SDK reference
- [Badge Keep Daemon](./badge-keeper.md) - Auto-renew badges
- [CLI Reference: badge](../../reference/cli/index.md#badge-issue) - Full command reference
- [Security Gateway](./gateway-setup.md) - Validate badges automatically
