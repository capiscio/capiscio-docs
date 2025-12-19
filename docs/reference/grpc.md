# gRPC Services

<!-- 
  VERIFIED: 2025-12-11
  Source: capiscio-core/proto/capiscio/v1/*.proto
-->

`capiscio-core` exposes gRPC services for validation, scoring, and badge operations. Start the gRPC server with:

```bash
capiscio rpc --address :50051
```

## Overview

The gRPC API provides three core services:

| Service | Description |
|---------|-------------|
| `ScoringService` | Validate and score agent cards |
| `BadgeService` | Issue, verify, and manage trust badges |
| `ValidationService` | Schema validation for agent cards |

---

## Connecting to the Server

### Python SDK

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient

# Connect to local server
client = CapiscioRPCClient(address='localhost:50051', auto_start=False)

# Or auto-start embedded server
client = CapiscioRPCClient()  # Starts server automatically
```

### Go

```go
import (
    pb "github.com/capiscio/capiscio-core/pkg/rpc/gen/capiscio/v1"
    "google.golang.org/grpc"
)

conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
if err != nil {
    log.Fatal(err)
}
defer conn.Close()

scoringClient := pb.NewScoringServiceClient(conn)
badgeClient := pb.NewBadgeServiceClient(conn)
```

---

## ScoringService

Validates agent cards and generates trust scores.

### ScoreAgentCard

Score an agent card and get detailed category breakdowns.

```protobuf
rpc ScoreAgentCard(ScoreAgentCardRequest) returns (ScoreAgentCardResponse);
```

**Request:**

```python
response = client.score_agent_card(
    agent_card_json='{"name": "My Agent", ...}',
    rule_set_id='default',  # Optional
)
```

**Response:**

```json
{
  "result": {
    "overall_score": 0.85,
    "rating": "RATING_GOOD",
    "categories": [
      {
        "category": "SCORE_CATEGORY_COMPLIANCE",
        "score": 0.95,
        "rules_passed": 18,
        "rules_failed": 2
      },
      {
        "category": "SCORE_CATEGORY_SECURITY",
        "score": 0.75,
        "rules_passed": 8,
        "rules_failed": 4
      }
    ]
  }
}
```

### Score Categories

| Category | Description |
|----------|-------------|
| `SCORE_CATEGORY_IDENTITY` | Agent identity and DID validation |
| `SCORE_CATEGORY_CAPABILITIES` | Capability declarations |
| `SCORE_CATEGORY_SECURITY` | Security practices and authentication |
| `SCORE_CATEGORY_COMPLIANCE` | A2A protocol compliance |
| `SCORE_CATEGORY_TRANSPARENCY` | Documentation and provider info |

---

## BadgeService

Issue and verify trust badges per [RFC-002](https://docs.capisc.io/rfcs/blob/main/docs/002-trust-badge.md).

### SignBadge

Sign a new badge with a private key.

```protobuf
rpc SignBadge(SignBadgeRequest) returns (SignBadgeResponse);
```

**Request:**

```python
response = client.sign_badge(
    claims={
        "sub": "did:key:z6Mkf5rGMoatrSj1f4CyvuHBeXJELe9RPdzo2PKGNCKVtZxP",
        "domain": "my-agent.example.com",
        "trust_level": 1,  # TRUST_LEVEL_DV
    },
    private_key_jwk='{"kty": "OKP", "crv": "Ed25519", ...}',
    key_id="key-1",
)
print(response.token)  # Signed JWT
```

### VerifyBadge

Verify a badge signature.

```protobuf
rpc VerifyBadge(VerifyBadgeRequest) returns (VerifyBadgeResponse);
```

**Request:**

```python
response = client.verify_badge(
    token="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
    public_key_jwk='{"kty": "OKP", ...}',  # Optional if JWKS URL used
)

if response.valid:
    print(f"Subject: {response.claims.sub}")
    print(f"Trust Level: {response.claims.trust_level}")
else:
    print(f"Invalid: {response.error_message}")
```

### VerifyBadgeWithOptions

Full verification with online checks.

```protobuf
rpc VerifyBadgeWithOptions(VerifyBadgeWithOptionsRequest) returns (VerifyBadgeResponse);
```

**Options:**

```python
response = client.verify_badge_with_options(
    token="eyJhbGciOiJFZERTQSI...",
    options={
        "mode": "VERIFY_MODE_ONLINE",
        "trusted_issuers": ["https://registry.capisc.io"],
        "audience": "https://my-service.example.com",
        "accept_self_signed": False,  # Reject Level 0 in production
    },
)
```

### RequestBadge

Request a badge from a Certificate Authority (CA).

```protobuf
rpc RequestBadge(RequestBadgeRequest) returns (RequestBadgeResponse);
```

**Request:**

```python
response = client.request_badge(
    agent_id="550e8400-e29b-41d4-a716-446655440000",
    ca_url="https://registry.capisc.io",
    api_key="cpsc_live_xxx",
    domain="my-agent.example.com",
    trust_level=2,  # TRUST_LEVEL_OV
    ttl_seconds=300,
)

if response.success:
    print(f"Badge: {response.token}")
    print(f"Expires: {response.expires_at}")
```

### StartKeeper

Start a background daemon that auto-renews badges.

```protobuf
rpc StartKeeper(StartKeeperRequest) returns (stream KeeperEvent);
```

**Request:**

```python
# Stream keeper events
for event in client.start_keeper(
    mode="KEEPER_MODE_CA",
    agent_id="550e8400...",
    ca_url="https://registry.capisc.io",
    api_key="cpsc_live_xxx",
    output_file="./badge.jwt",
    ttl_seconds=300,
    renew_before_seconds=60,
):
    if event.type == "KEEPER_EVENT_RENEWED":
        print(f"Badge renewed: {event.badge_jti}")
    elif event.type == "KEEPER_EVENT_ERROR":
        print(f"Error: {event.error}")
```

---

## Trust Levels

The `TrustLevel` enum maps to badge trust levels:

| Enum Value | Level | Description |
|------------|-------|-------------|
| `TRUST_LEVEL_UNSPECIFIED` | - | Not specified |
| `TRUST_LEVEL_SELF_SIGNED` | 0 | Self-signed (`did:key`) |
| `TRUST_LEVEL_DV` | 1 | Domain Validated |
| `TRUST_LEVEL_OV` | 2 | Organization Validated |
| `TRUST_LEVEL_EV` | 3 | Extended Validated |
| `TRUST_LEVEL_CV` | 4 | Community Vouched |

---

## Proto Files

The protobuf definitions are located at:

```
capiscio-core/proto/capiscio/v1/
├── badge.proto      # BadgeService
├── scoring.proto    # ScoringService
├── common.proto     # Shared types
├── did.proto        # DID operations
├── registry.proto   # Registry operations
├── revocation.proto # Badge revocation
└── trust.proto      # Trust model types
```

### Generating Client Code

```bash
# Install protoc and plugins
brew install protobuf
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Generate Go code
cd capiscio-core/proto
buf generate
```

---

## CLI Usage

Start the gRPC server:

```bash
# Default port (50051)
capiscio rpc

# Custom address
capiscio rpc --address localhost:9090

# With TLS
capiscio rpc --tls --cert ./cert.pem --key ./key.pem
```

---

## Error Handling

gRPC errors use standard status codes:

| Code | Description |
|------|-------------|
| `OK` | Success |
| `INVALID_ARGUMENT` | Bad request parameters |
| `NOT_FOUND` | Resource not found |
| `UNAUTHENTICATED` | Missing or invalid credentials |
| `PERMISSION_DENIED` | Insufficient permissions |
| `INTERNAL` | Server error |

**Python example:**

```python
from grpc import RpcError, StatusCode

try:
    response = client.verify_badge(token=invalid_token)
except RpcError as e:
    if e.code() == StatusCode.INVALID_ARGUMENT:
        print(f"Invalid token: {e.details()}")
    elif e.code() == StatusCode.UNAUTHENTICATED:
        print("Authentication required")
```

---

## See Also

- [CLI Reference](cli/index.md) — Command-line interface
- [Python SDK](sdk-python/index.md) — `CapiscioRPCClient` wrapper
- [Badge CA](server/badge-ca.md) — CA operations
- [RFC-002: Trust Badge](https://docs.capisc.io/rfcs/blob/main/docs/002-trust-badge.md) — Badge specification
