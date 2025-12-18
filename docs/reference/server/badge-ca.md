# Badge Certificate Authority

<!--
  VERIFIED: 2025-12-18
  Source: capiscio-server/internal/ca/ca.go
  Updated: Added RFC-003 PoP protocol documentation
-->

The capiscio-server includes a built-in Certificate Authority (CA) for issuing trust badges with two identity assurance levels.

---

## Overview

The Badge CA:

- Signs trust badges with the server's Ed25519 key
- Issues badges for registered agents only
- Supports IAL-0 (account-based) and IAL-1 (proof-of-possession) modes
- Implements RFC-003 Key Ownership Proof protocol
- Enforces trust level requirements
- Publishes public keys via JWKS endpoint

### Identity Assurance Levels

| Level | Name | Method | Description |
|-------|------|--------|-------------|
| **IAL-0** | Account-attested | API Key | Badge issued based on account ownership only |
| **IAL-1** | Proof of Possession | Challenge-Response | Badge cryptographically bound to agent's private key |

!!! note "RFC Compliance"
    - **RFC-002**: Trust Badge specification with 5 trust levels
    - **RFC-003**: Key Ownership Proof (PoP) protocol for IAL-1 assurance

```
┌─────────────────────────────────────────────────────────────┐
│                      Badge Issuance Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Agent ──▶ POST /v1/agents/{id}/badge ──▶ CA signs        │
│                                                             │
│                        │                                    │
│                        ▼                                    │
│              ┌─────────────────┐                            │
│              │   Badge (JWT)   │                            │
│              │ iss: CA URL     │                            │
│              │ sub: Agent DID  │                            │
│              │ level: 1-4      │                            │
│              └─────────────────┘                            │
│                        │                                    │
│                        ▼                                    │
│   Verifier ◀── /.well-known/jwks.json ◀── CA public key    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Trust Levels

The CA issues badges at different trust levels based on verification:

| Level | Name | Requirements |
|-------|------|--------------|
| 1 | Registered (REG) | Valid account |
| 2 | Domain Validated (DV) | DNS TXT record verified |
| 3 | Organization Validated (OV) | Legal entity verified |
| 4 | Extended Validated (EV) | Manual security audit passed |

!!! note "Level 0 (Self-Signed)"
    Level 0 badges are **not CA-issued**. They are self-signed by agents using `capiscio badge issue --self-sign` for development only.

---

## Issuing a Badge

The CA supports two badge issuance modes:

### IAL-0: Account-Based Issuance

Simple badge issuance based on API key authentication. Suitable for internal systems where the caller controls the agent.

```bash
curl -X POST https://registry.capisc.io/v1/agents/{did}/badge \
  -H "X-Capiscio-Registry-Key: cpsc_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "ial0",
    "domain": "my-agent.example.com",
    "badge_ttl": 300,
    "badge_aud": ["https://api.example.com"]
  }'
```

**Response:**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
    "jti": "badge-uuid",
    "subject": "did:web:registry.capisc.io:agents:550e8400",
    "trustLevel": "1",
    "expiresAt": "2025-12-18T10:05:00Z",
    "ial": "0"
  }
}
```

### IAL-1: Proof of Possession (RFC-003)

Two-phase challenge-response protocol that cryptographically proves the agent possesses the private key for their DID. This binds the badge to a specific key, preventing unauthorized use.

**Phase 1: Request Challenge**

```bash
curl -X POST https://registry.capisc.io/v1/agents/{did}/badge/challenge \
  -H "X-Capiscio-Registry-Key: cpsc_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "badge_ttl": 300,
    "challenge_ttl": 300,
    "badge_aud": ["https://api.example.com"]
  }'
```

**Response:**

```json
{
  "challenge_id": "ch-550e8400-e29b-41d4-a716-446655440000",
  "nonce": "dGhpcyBpcyBhIHJhbmRvbSBub25jZQ",
  "challenge_expires_at": "2025-12-18T10:05:00Z",
  "aud": "https://registry.capisc.io",
  "htu": "https://registry.capisc.io/v1/agents/did:key:z6Mk.../badge/pop",
  "htm": "POST"
}
```

**Phase 2: Submit Proof & Receive Badge**

The agent creates a proof JWS signed with their private key:

```json
{
  "cid": "ch-550e8400-e29b-41d4-a716-446655440000",
  "nonce": "dGhpcyBpcyBhIHJhbmRvbSBub25jZQ",
  "sub": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu",
  "aud": "https://registry.capisc.io",
  "htu": "https://registry.capisc.io/v1/agents/did:key:z6Mk.../badge/pop",
  "htm": "POST",
  "iat": 1734519900,
  "exp": 1734520200,
  "jti": "proof-uuid"
}
```

Then submit the proof:

```bash
curl -X POST https://registry.capisc.io/v1/agents/{did}/badge/pop \
  -H "Content-Type: application/json" \
  -d '{
    "challenge_id": "ch-550e8400-e29b-41d4-a716-446655440000",
    "proof_jws": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9..."
  }'
```

**Response (IAL-1 Badge):**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
    "jti": "badge-uuid",
    "subject": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu",
    "trustLevel": "1",
    "expiresAt": "2025-12-18T10:10:00Z",
    "ial": "1",
    "cnf": {
      "kid": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu#z6MkqsZ...",
      "jwk": {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": "qsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu"
      }
    }
  }
}
```

!!! warning "PoP Security Requirements"
    - Challenge is single-use (replay protection)
    - Challenge expires in 5 minutes (default)
    - Proof must be signed with the key from the agent's DID
    - Subject in badge matches the proven DID (e.g., `did:key`)
    - Badge includes `cnf` claim with full public key JWK

### Via Python SDK

```python
import asyncio
from capiscio_sdk import request_badge, TrustLevel

async def get_badge():
    return await request_badge(
        agent_id="550e8400-e29b-41d4-a716-446655440000",
        ca_url="https://registry.capisc.io",
        api_key="cpsc_live_xxx",
        domain="my-agent.example.com",
        trust_level=TrustLevel.LEVEL_2,
    )

badge_token = asyncio.run(get_badge())
```

### Via gRPC

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient

client = CapiscioRPCClient(address='localhost:50051')
response = client.request_badge(
    agent_id="550e8400-e29b-41d4-a716-446655440000",
    ca_url="https://registry.capisc.io",
    api_key="cpsc_live_xxx",
    domain="my-agent.example.com",
    trust_level="2",
)
print(response.token)
```

---

## Badge Claims

### IAL-0 Badge (Account-Based)

```json
{
  "jti": "badge-unique-id",
  "iss": "https://registry.capisc.io",
  "sub": "did:web:registry.capisc.io:agents:550e8400",
  "iat": 1734519600,
  "exp": 1734519900,
  "ial": "0",
  "vc": {
    "type": ["VerifiableCredential", "AgentIdentity"],
    "credentialSubject": {
      "domain": "my-agent.example.com",
      "level": "1"
    }
  }
}
```

### IAL-1 Badge (Proof of Possession)

IAL-1 badges include the `cnf` (confirmation) claim per RFC-7800, binding the badge to a specific cryptographic key:

```json
{
  "jti": "badge-unique-id",
  "iss": "https://registry.capisc.io",
  "sub": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu",
  "iat": 1734519600,
  "exp": 1734519900,
  "ial": "1",
  "cnf": {
    "kid": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu#z6MkqsZ...",
    "jwk": {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "qsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu",
      "kid": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu#z6MkqsZ..."
    }
  },
  "pop_challenge_id": "ch-550e8400-e29b-41d4-a716-446655440000",
  "vc": {
    "type": ["VerifiableCredential", "AgentIdentity"],
    "credentialSubject": {
      "domain": "my-agent.example.com",
      "level": "1"
    }
  }
}
```

### Claim Reference

| Claim | IAL | Description |
|-------|-----|-------------|
| `jti` | 0, 1 | Unique badge identifier |
| `iss` | 0, 1 | CA issuer URL |
| `sub` | 0, 1 | Agent's DID (`did:web` for IAL-0, `did:key` for IAL-1) |
| `iat` | 0, 1 | Issued at (Unix timestamp) |
| `exp` | 0, 1 | Expiration (Unix timestamp) |
| `ial` | 0, 1 | Identity Assurance Level |
| `cnf` | 1 | **Confirmation claim** - Contains key binding per RFC-7800 |
| `cnf.kid` | 1 | Key identifier (DID with fragment) |
| `cnf.jwk` | 1 | **Full public key JWK** (RFC-8037 format for Ed25519) |
| `pop_challenge_id` | 1 | Reference to PoP challenge (audit trail) |
| `vc.credentialSubject.domain` | 0, 1 | Verified domain |
| `vc.credentialSubject.level` | 0, 1 | Trust level (1-4) |

!!! info "DID Support"
    - **IAL-0 badges**: Use `did:web` format (generated from agent UUID)
    - **IAL-1 badges**: Use the proven DID from PoP (typically `did:key`)
    - Agents can register with any DID method in the `did` field

---

## JWKS Endpoint

The CA publishes its public key at `/.well-known/jwks.json`:

```bash
curl https://registry.capisc.io/.well-known/jwks.json
```

```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo",
      "kid": "capiscio-ca-1705315800",
      "alg": "EdDSA",
      "use": "sig"
    }
  ]
}
```

Verifiers fetch this endpoint to validate badge signatures.

---

## Badge Expiration

Badges have a short TTL by default (5 minutes per RFC-002). This:

- Limits exposure if a badge is compromised
- Forces agents to regularly check in with the CA
- Allows rapid revocation by disabling agents

Use the **Badge Keeper** daemon for automatic renewal:

```bash
capiscio badge keep \
  --agent-id "550e8400..." \
  --ca-url "https://registry.capisc.io" \
  --api-key "$API_KEY" \
  --out ./current-badge.jwt
```

---

## Key Management

### Key Generation

On first startup, if no key exists at `CA_KEY_PATH`, the server generates an Ed25519 keypair:

```go
// From ca.go
pub, priv, err := ed25519.GenerateKey(rand.Reader)
```

The key is saved in JWK format with restrictive permissions (0600).

### Key Storage

```json
// ca.jwk (private key - NEVER share)
{
  "kty": "OKP",
  "crv": "Ed25519",
  "x": "base64url-public-key",
  "d": "base64url-private-key",
  "kid": "capiscio-ca-1705315800",
  "alg": "EdDSA",
  "use": "sig"
}
```

### Key Rotation

To rotate the CA key:

1. **Generate new key** on a secure machine
2. **Add new key** to JWKS (keep old key for overlap period)
3. **Update server** to sign with new key
4. **Remove old key** after all badges signed with it have expired

!!! warning "Key Security"
    The CA private key is the root of trust. Compromise allows forging badges for any agent.

---

## Agent Lifecycle

### Registration

```bash
# Register agent
curl -X POST https://registry.capisc.io/v1/agents \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"name": "My Agent", "domain": "my-agent.example.com"}'
```

### Badge Issuance

Only enabled agents can receive badges:

```go
// From router.go
if agent.Status != "enabled" {
    return 403, "Agent is disabled"
}
```

### Disabling Agents

Disabling an agent immediately prevents new badge issuance:

```bash
curl -X POST https://registry.capisc.io/v1/agents/{id}/disable \
  -H "Authorization: Bearer $API_KEY"
```

Existing badges remain valid until expiry, but no new badges can be issued.

---

## Verification Flow

```
Verifier                                      CA
   │                                           │
   │ 1. Receive badge token                    │
   │                                           │
   │ 2. GET /.well-known/jwks.json ──────────▶│
   │◀────────────────────────────── JWKS ─────│
   │                                           │
   │ 3. Verify signature with CA public key   │
   │                                           │
   │ 4. Check exp, iss, sub claims            │
   │                                           │
   │ 5. Accept/reject request                  │
```

---

## RFC-003 Security Features

The PoP implementation includes multiple security layers:

### Rate Limiting

Challenge requests are rate-limited per DID:

- **Default**: 10 challenges per DID per 5 minutes
- **Purpose**: Prevents brute-force attacks
- **Error**: HTTP 429 with `rate_limit_exceeded` error code

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded: too many challenge requests for this DID"
}
```

### Replay Protection

Each challenge can only be used once:

- Challenges are marked as "used" after successful badge issuance
- Attempting to reuse a challenge returns HTTP 403
- Database constraint enforces single-use

```json
{
  "error": "challenge_used",
  "message": "Challenge already used (replay protection)"
}
```

### Challenge Expiration

Challenges have configurable TTL (default 5 minutes):

- Set via `challenge_ttl` parameter in seconds
- Expired challenges cannot be used for proof
- Automatic cleanup of expired challenges

```json
{
  "error": "challenge_expired",
  "message": "Challenge has expired"
}
```

### Proof Validation

The proof JWS must satisfy all requirements:

- **Signature**: Valid Ed25519 signature from DID's key
- **Claims**: Must include `cid`, `nonce`, `sub`, `aud`, `htu`, `htm`
- **Nonce**: Must match challenge nonce exactly
- **Audience**: Must match CA issuer URL
- **HTTP binding**: `htu` and `htm` must match badge endpoint
- **Expiration**: Proof must not be expired
- **Key relationship**: Key must have "authentication" relationship in DID document

### DID Resolution

The CA resolves DIDs to verify keys:

- **did:key**: Extracts public key from DID directly
- **did:web**: Fetches DID document via HTTPS
- **Verification**: Ensures key has authentication capability

---

## Agent DID Field

Agents in the registry have a `did` field supporting any DID method:

```go
type Agent struct {
    ID           uuid.UUID
    DID          *string  // e.g., "did:key:z6Mk...", "did:web:..."
    Domain       *string
    // ... other fields
}
```

**Registration with DID:**

```bash
curl -X POST https://registry.capisc.io/v1/agents \
  -H "X-Capiscio-Registry-Key: cpsc_live_xxx" \
  -d '{
    "name": "My Agent",
    "did": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu",
    "domain": "my-agent.example.com"
  }'
```

**Update Agent DID:**

```bash
curl -X PUT https://registry.capisc.io/v1/agents/{agent-id} \
  -H "X-Capiscio-Registry-Key: cpsc_live_xxx" \
  -d '{
    "did": "did:key:z6MkqsZXWXcZbFwUrNXBMZg9uHEAj9Ryz6e1Yx97FtBAqxzu"
  }'
```

!!! note "DID Resolution"
    The PoP protocol uses the DID field to:
    - Identify which agent is requesting the badge
    - Resolve the agent's public key for proof verification
    - Set the badge subject to the proven DID

---

## See Also

- [API Reference](api.md) — Badge endpoints
- [Trust Model](../../concepts/trust-model.md) — Trust level explanation
- [Badges Guide](../../how-to/security/badges.md) — Practical examples
- [RFC-002](https://docs.capisc.io/rfcs/blob/main/docs/002-trust-badge.md) — Badge specification
- [RFC-003](https://docs.capisc.io/rfcs/blob/main/docs/003-key-ownership-proof.md) — Proof of Possession protocol
