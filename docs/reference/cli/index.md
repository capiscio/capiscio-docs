# CLI Reference

<!-- 
  VERIFIED: 2025-12-26
  Source: capiscio-core/cmd/capiscio/*.go
  All flags verified against actual CLI --help output.
-->

The `capiscio` CLI provides commands for validating Agent Cards, managing cryptographic keys, issuing trust badges, and running the security gateway.

!!! info "Distribution Packages"
    The CLI is available through multiple distribution methods, all wrapping the same Go binary:
    
    - **npm**: `npm install -g capiscio` (via [capiscio-node](https://github.com/capiscio/capiscio-node))
    - **pip**: `pip install capiscio` (via [capiscio-python](https://github.com/capiscio/capiscio-python))
    - **Docker**: `docker pull ghcr.io/capiscio/capiscio-core:latest`
    - **Binary**: Download from [GitHub Releases](https://github.com/capiscio/capiscio-core/releases)

## Installation

=== "npm"

    ```bash
    npm install -g capiscio
    ```

=== "pip"

    ```bash
    pip install capiscio
    ```

=== "Docker"

    ```bash
    docker pull ghcr.io/capiscio/capiscio-core:latest
    alias capiscio="docker run --rm -v $(pwd):/data ghcr.io/capiscio/capiscio-core"
    ```

=== "Binary"

    ```bash
    # macOS (Apple Silicon)
    curl -L https://github.com/capiscio/capiscio-core/releases/latest/download/capiscio-darwin-arm64 -o capiscio
    chmod +x capiscio
    sudo mv capiscio /usr/local/bin/
    
    # macOS (Intel)
    curl -L https://github.com/capiscio/capiscio-core/releases/latest/download/capiscio-darwin-amd64 -o capiscio
    
    # Linux (x64)
    curl -L https://github.com/capiscio/capiscio-core/releases/latest/download/capiscio-linux-amd64 -o capiscio
    ```

---

## Commands Overview

| Command | Description |
|---------|-------------|
| [`validate`](#validate) | Validate an Agent Card from file or URL |
| [`key gen`](#key-gen) | Generate Ed25519 key pair |
| [`badge issue`](#badge-issue) | Issue a trust badge |
| [`badge verify`](#badge-verify) | Verify a trust badge |
| [`badge request`](#badge-request) | Request a badge from CA via PoP protocol (RFC-003) |
| [`badge dv`](#badge-dv) | Domain Validation commands (create, status, finalize) |
| [`badge keep`](#badge-keep) | Daemon to auto-renew badges |
| [`trust`](#trust) | Manage the local trust store |
| [`gateway start`](#gateway-start) | Start the security gateway |
| [`rpc`](#rpc) | Start the gRPC server for SDK integration |

---

## validate

Validate an Agent Card from a local file or URL. Performs schema validation, signature verification, and optional live endpoint testing.

### Usage

```bash
capiscio validate [file-or-url] [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--json` | `bool` | `false` | Output results as JSON |
| `--strict` | `bool` | `false` | Enable strict validation mode |
| `--schema-only` | `bool` | `false` | Validate schema only, skip endpoint testing |
| `--test-live` | `bool` | `false` | Test live agent endpoint |
| `--skip-signature` | `bool` | `false` | Skip JWS signature verification |
| `--registry-ready` | `bool` | `false` | Check registry deployment readiness |
| `--errors-only` | `bool` | `false` | Show only errors and warnings |
| `--timeout` | `duration` | `10s` | Request timeout |

!!! warning "Deprecated Flag"
    `--live` is deprecated. Use `--test-live` instead.

### Examples

```bash
# Basic validation
capiscio validate ./agent-card.json

# Validate from URL with live endpoint test
capiscio validate https://my-agent.example.com/.well-known/agent.json --test-live

# JSON output for CI/CD
capiscio validate ./agent-card.json --json

# Strict mode (fails on warnings)
capiscio validate ./agent-card.json --strict

# Schema validation only
capiscio validate ./agent-card.json --schema-only

# Registry submission readiness check
capiscio validate ./agent-card.json --registry-ready
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Validation passed |
| `1` | Validation failed or error |

---

## key gen

Generate a new Ed25519 key pair for signing Agent Cards and badges.

### Usage

```bash
capiscio key gen [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--out-priv` | `string` | `private.jwk` | Output path for private key |
| `--out-pub` | `string` | `public.jwk` | Output path for public key |
| `--out-did` | `string` | *(none)* | Output path for DID document |
| `--show-did` | `bool` | `false` | Print the generated DID to stdout |

### Example

```bash
# Generate keys with default names
capiscio key gen

# Generate keys to specific paths
capiscio key gen --out-priv ./keys/private.jwk --out-pub ./keys/public.jwk

# Generate keys and show the DID
capiscio key gen --show-did

# Generate keys and save DID document
capiscio key gen --out-priv ./keys/private.jwk --out-pub ./keys/public.jwk --out-did ./keys/did.json
```

### Output Format

Keys are saved in JWK (JSON Web Key) format:

=== "private.jwk"

    ```json
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo",
      "d": "nWGxne_9WmC6hEr0kuwsxERJxWl7MmkZcDusAxyuf2A",
      "kid": "key-1",
      "alg": "EdDSA",
      "use": "sig"
    }
    ```

=== "public.jwk"

    ```json
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "11qYAYKxCrfVS_7TyWQHOg7hcvPapiMlrwIaaPcHURo",
      "kid": "key-1",
      "alg": "EdDSA",
      "use": "sig"
    }
    ```

!!! danger "Security"
    Keep your private key secure. Never commit it to version control or share it publicly.
    The private key file is created with `0600` permissions (owner read/write only).

---

## badge issue

Issue a new trust badge for an agent. Trust badges are JWTs that attest to an agent's identity per RFC-002.

### Usage

```bash
capiscio badge issue [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--self-sign` | `bool` | `false` | Self-sign for development (implies level 0) |
| `--sub` | `string` | `did:web:registry.capisc.io:agents:test` | Subject DID (did:web format, auto-set for level 0) |
| `--iss` | `string` | `did:web:registry.capisc.io` | Issuer DID (auto-set to did:key for level 0) |
| `--domain` | `string` | `example.com` | Agent domain |
| `--level` | `string` | `1` | Trust level: 0=SS, 1=REG, 2=DV, 3=OV, 4=EV (RFC-002 §5) |
| `--exp` | `duration` | `5m` | Expiration duration (default 5m per RFC-002) |
| `--aud` | `string` | *(none)* | Audience (comma-separated URLs) |
| `--key` | `string` | *(none)* | Path to private key file (JWK, auto-generates if not provided) |

!!! note "Trust Levels (RFC-002 §5)"
    - **0**: Self-Signed (SS) — Development only, `did:key` issuer, implied by `--self-sign`
    - **1**: Registered (REG) — Account registration with CapiscIO CA
    - **2**: Domain Validated (DV) — DNS/HTTP domain ownership proof
    - **3**: Organization Validated (OV) — Legal entity verification
    - **4**: Extended Validated (EV) — Manual review + security audit

### Examples

```bash
# Self-signed badge for development (auto-generates did:key)
capiscio badge issue --self-sign

# Self-signed badge with explicit subject
capiscio badge issue --self-sign --sub did:web:example.com:agents:my-agent

# With audience restriction
capiscio badge issue --self-sign --aud "https://api.example.com,https://backup.example.com"

# Production: Issue badge with your private key
capiscio badge issue \
  --key ./private.jwk \
  --sub "did:web:mycompany.com:agents:my-agent" \
  --domain "mycompany.com" \
  --level 2
```

### Output

The command outputs the signed JWT token to stdout:

```
eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6d2ViOmV4YW1wbGUuY29tOmFnZW50czpteS1hZ2VudCIs...
```

---

## badge verify

Verify a trust badge's signature, expiration, and claims per RFC-002 §8.1.

### Usage

```bash
capiscio badge verify [token] [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--accept-self-signed` | `bool` | `false` | Accept Level 0 (self-signed) badges (dev only) |
| `--key` | `string` | *(none)* | Path to public key file (JWK) |
| `--offline` | `bool` | `false` | Offline mode (uses local trust store) |
| `--audience` | `string` | *(none)* | Verifier's identity for audience validation |
| `--skip-revocation` | `bool` | `false` | Skip revocation check (testing only) |
| `--skip-agent-status` | `bool` | `false` | Skip agent status check (testing only) |
| `--trusted-issuers` | `string` | *(none)* | Comma-separated list of trusted issuer URLs |

!!! warning "Self-Signed Badges"
    The `--accept-self-signed` flag is for **development only**. In production, verifiers MUST reject Level 0 badges by default.

### Examples

```bash
# Online verification with local key
capiscio badge verify "$TOKEN" --key ca-public.jwk

# Accept self-signed badges (development)
capiscio badge verify "$TOKEN" --accept-self-signed

# Offline verification (uses trust store)
capiscio badge verify "$TOKEN" --offline

# With audience check
capiscio badge verify "$TOKEN" --key ca.jwk --audience https://api.example.com

# With trusted issuers list
capiscio badge verify "$TOKEN" --key ca.jwk --trusted-issuers "https://registry.capisc.io"
```

### Verification Steps (per RFC-002 §8.1)

1. Parse and validate JWS structure
2. Verify signature against CA key
3. Validate claims (exp, iat, iss, aud)
4. Check revocation status (online mode)
5. Check agent status (online mode)

### Output

```
✅ Badge Valid!
Subject: did:web:example.com:agents:my-agent
Issuer: https://registry.capisc.io
Trust Level: 2 (OV)
Expires: 2025-12-02T19:48:00Z
```

---

## badge request

Request a Trust Badge from a Certificate Authority using the Proof of Possession (PoP) protocol defined in RFC-003. This is the standard production flow for obtaining badges from the CapiscIO Registry.

### Usage

```bash
capiscio badge request [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--did` | `string` | *(required)* | Agent DID (did:web or did:key format) |
| `--key` | `string` | *(required)* | Path to private key file (JWK) for PoP signing |
| `--ca` | `string` | `https://registry.capisc.io` | Certificate Authority URL |
| `--api-key` | `string` | *(none)* | API key for CA authentication |
| `--out` | `string` | *(stdout)* | Output file path for the badge |
| `--ttl` | `duration` | `5m` | Requested badge TTL |
| `--audience` | `string` | *(none)* | Audience restriction (comma-separated URLs) |

### Examples

```bash
# Request badge from CapiscIO Registry
capiscio badge request \
  --did "did:web:example.com:agents:my-agent" \
  --key ./private.jwk \
  --api-key "$CAPISCIO_API_KEY"

# Request badge with specific TTL and audience
capiscio badge request \
  --did "did:web:example.com:agents:my-agent" \
  --key ./private.jwk \
  --api-key "$CAPISCIO_API_KEY" \
  --ttl 10m \
  --audience "https://api.example.com"

# Save badge to file
capiscio badge request \
  --did "did:web:mycompany.com:agents:service-agent" \
  --key ./keys/private.jwk \
  --api-key "$CAPISCIO_API_KEY" \
  --out ./current-badge.jwt
```

### PoP Protocol Flow (RFC-003)

1. Client generates a nonce and creates a PoP token signed with their private key
2. Client sends PoP token to CA along with their DID
3. CA verifies the PoP token against the DID's public key
4. CA issues a signed badge with the requested claims
5. Client receives the badge JWT

!!! note "Difference from `badge issue`"
    - `badge issue` creates self-signed badges locally (development)
    - `badge request` obtains CA-signed badges via the PoP protocol (production)

---

## badge dv

Domain Validation commands for obtaining Level 2 (DV) trust badges. DV requires proving ownership of a domain via DNS TXT record or HTTP well-known file.

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `badge dv create` | Start a new DV challenge |
| `badge dv status` | Check status of a DV challenge |
| `badge dv finalize` | Complete DV and obtain badge |

### badge dv create

Start a new Domain Validation challenge.

```bash
capiscio badge dv create [flags]
```

**Flags:**

| Flag | Type | Description |
|------|------|-------------|
| `--domain` | `string` | Domain to validate |
| `--method` | `string` | Validation method: `dns` or `http` |
| `--ca` | `string` | CA URL (default: https://registry.capisc.io) |
| `--api-key` | `string` | API key for authentication |

**Example:**

```bash
# Start DNS-based DV challenge
capiscio badge dv create \
  --domain example.com \
  --method dns \
  --api-key "$CAPISCIO_API_KEY"

# Output: Challenge created
# DNS TXT Record: _capiscio-challenge.example.com
# Value: abc123-xyz789-challenge-token
```

### badge dv status

Check the status of a pending DV challenge.

```bash
capiscio badge dv status [challenge-id] [flags]
```

**Flags:**

| Flag | Type | Description |
|------|------|-------------|
| `--ca` | `string` | CA URL |
| `--api-key` | `string` | API key for authentication |

**Example:**

```bash
capiscio badge dv status ch_abc123 --api-key "$CAPISCIO_API_KEY"

# Output: 
# Status: pending
# Domain: example.com
# Method: dns
# Created: 2025-01-15T10:00:00Z
# Expires: 2025-01-22T10:00:00Z
```

### badge dv finalize

Complete the DV process after placing the challenge record. The CA will verify the challenge and issue a Level 2 badge.

```bash
capiscio badge dv finalize [challenge-id] [flags]
```

**Flags:**

| Flag | Type | Description |
|------|------|-------------|
| `--ca` | `string` | CA URL |
| `--api-key` | `string` | API key for authentication |
| `--key` | `string` | Private key for badge signing |
| `--out` | `string` | Output file for badge |

**Example:**

```bash
# After placing DNS TXT record, finalize the challenge
capiscio badge dv finalize ch_abc123 \
  --api-key "$CAPISCIO_API_KEY" \
  --key ./private.jwk \
  --out ./dv-badge.jwt

# Output:
# ✅ Domain validated: example.com
# Badge saved to: ./dv-badge.jwt
# Trust Level: 2 (DV)
```

### DV Workflow

```
1. Create challenge:    capiscio badge dv create --domain example.com --method dns
2. Add DNS TXT record:  _capiscio-challenge.example.com → <challenge-token>
3. Wait for DNS propagation (usually 1-5 minutes)
4. Check status:        capiscio badge dv status <challenge-id>
5. Finalize:           capiscio badge dv finalize <challenge-id> --key ./private.jwk
```

---

## badge keep

Run a daemon that automatically renews badges before expiration. Useful for long-running agents that need continuous authorization per RFC-002 §7.3.

### Usage

```bash
capiscio badge keep [flags]
```

### Modes

The badge keeper supports two modes:

| Mode | Description |
|------|-------------|
| **Self-sign** | Generate badges locally with `--self-sign` (development only) |
| **CA mode** | Request badges from CA with `--ca` and `--agent-id` (production) |

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--self-sign` | `bool` | `false` | Self-sign instead of requesting from CA |
| `--key` | `string` | *(required for self-sign)* | Path to private key file (JWK) |
| `--agent-id` | `string` | *(none)* | Agent ID (UUID) to request badges for (CA mode) |
| `--domain` | `string` | *(none)* | Agent domain (optional, uses agent's registered domain) |
| `--level` | `string` | `1` | Trust level: 1=REG, 2=DV, 3=OV, 4=EV (per RFC-002 §5) |
| `--exp` | `duration` | `5m` | Expiration duration for each badge |
| `--out` | `string` | `badge.jwt` | Output file path for the badge |
| `--renew-before` | `duration` | `1m` | Time before expiry to renew |
| `--check-interval` | `duration` | `30s` | Interval to check for renewal |
| `--ca` | `string` | `https://registry.capisc.io` | CA URL for badge requests |
| `--api-key` | `string` | *(none)* | API key for CA authentication (or use `CAPISCIO_API_KEY` env) |

### Examples

```bash
# Self-signed mode for development
capiscio badge keep --self-sign --key private.jwk --out badge.jwt

# With custom expiration and renewal timing
capiscio badge keep \
  --self-sign \
  --key ./private.jwk \
  --out ./current-badge.jwt \
  --exp 5m \
  --renew-before 1m

# CA mode (production) - request badges from registry
capiscio badge keep \
  --agent-id "550e8400-e29b-41d4-a716-446655440000" \
  --api-key "$CAPISCIO_API_KEY" \
  --out ./current-badge.jwt

# CA mode with custom settings
capiscio badge keep \
  --agent-id "550e8400-e29b-41d4-a716-446655440000" \
  --ca https://registry.capisc.io \
  --api-key "$CAPISCIO_API_KEY" \
  --level 2 \
  --exp 10m \
  --renew-before 2m
```

### Behavior

The daemon will:

1. Issue an initial badge immediately
2. Write it to the output file
3. Check periodically (every `--check-interval`) if renewal is needed
4. Renew the badge when it's within `--renew-before` of expiry
5. Write the new badge to the output file

!!! tip "Environment Variable"
    Set `CAPISCIO_API_KEY` environment variable to avoid passing `--api-key` on every command.

---

## trust

Manage the local trust store for offline badge verification. The trust store contains CA public keys that are trusted for badge verification, enabling offline and air-gapped deployments.

**Location:** `~/.capiscio/trust/` (or `$CAPISCIO_TRUST_PATH`)

See RFC-002 §13.1 for details.

### trust add

Add a CA public key to the trust store.

```bash
capiscio trust add [jwk-file] [flags]
```

**Flags:**

| Flag | Type | Description |
|------|------|-------------|
| `--from-jwks` | `string` | Fetch from JWKS URL or '-' for stdin |

**Examples:**

```bash
# Add from a JWK file
capiscio trust add ca-public.jwk

# Add from JWKS URL (production CA)
capiscio trust add --from-jwks https://registry.capisc.io/.well-known/jwks.json

# Add from stdin (pipe from curl)
curl -s https://registry.capisc.io/.well-known/jwks.json | capiscio trust add --from-jwks -
```

### trust list

List trusted CA keys.

```bash
capiscio trust list
```

### trust remove

Remove a CA key from the trust store.

```bash
capiscio trust remove [key-id]
```

---

## gateway start

Start the CapiscIO security gateway. The gateway acts as a reverse proxy that validates incoming request badges before forwarding to your agent.

### Usage

```bash
capiscio gateway start [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--port` | `int` | `8080` | Port to listen on |
| `--target` | `string` | `http://localhost:3000` | Upstream target URL |
| `--local-key` | `string` | *(none)* | Path to local public key file (JWK) |
| `--registry-url` | `string` | *(none)* | URL of the CapiscIO Registry |

!!! warning "Required"
    You must provide either `--local-key` OR `--registry-url` (but not both).

### Examples

```bash
# Local mode (verify against a single public key)
capiscio gateway start \
  --port 8080 \
  --target http://localhost:3000 \
  --local-key ./public.jwk

# Cloud mode (verify against registry)
capiscio gateway start \
  --port 8080 \
  --target http://localhost:3000 \
  --registry-url https://registry.capisc.io
```

### Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Client    │────▶│ CapiscIO Gateway │────▶│ Your Agent   │
│             │     │   (port 8080)    │     │ (port 3000)  │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Validates  │
                    │   Badges    │
                    └─────────────┘
```

---

## rpc

Start the gRPC server for SDK integration. This server provides programmatic access to all CapiscIO functionality and is used by the Python and Node.js SDKs.

!!! info "Auto-Start by SDKs"
    Normally, you don't need to run this command manually. The SDKs automatically start and manage the gRPC server process. Use this command only for debugging or custom integrations.

### Usage

```bash
capiscio rpc [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--address` | `string` | `unix://~/.capiscio/rpc.sock` | gRPC server address (unix socket or tcp) |
| `--socket` | `string` | *(none)* | Unix socket path (alternative to --address) |

### Examples

```bash
# Start with default Unix socket
capiscio rpc

# Start on a specific socket path
capiscio rpc --socket /tmp/capiscio.sock

# Start on TCP (for remote access, use with caution)
capiscio rpc --address tcp://localhost:50051
```

### gRPC Services

The server exposes 7 services:

| Service | Methods |
|---------|---------|
| `BadgeService` | SignBadge, VerifyBadge, ParseBadge, RequestBadge, StartBadgeKeeper |
| `DIDService` | ParseDID |
| `TrustStoreService` | AddTrustedKey, ListTrustedKeys, RemoveTrustedKey |
| `RevocationService` | CheckRevocation |
| `ScoringService` | ScoreAgentCard, ValidateRules |
| `SimpleGuardService` | SignPayload, VerifyPayload |
| `RegistryService` | FetchAgentCard |

---

## gRPC Server (SDK Integration)

The gRPC server provides programmatic access to all CapiscIO functionality for SDKs in Python, Node.js, and other languages. 

!!! info "Auto-Start Behavior"
    The SDKs automatically manage the gRPC server process. You don't need to manually start it. The server runs on a Unix socket by default (`~/.capiscio/rpc.sock`).

### Exposed Services (7 total)

| Service | Description |
|---------|-------------|
| `BadgeService` | Sign, verify, parse, request badges; start badge keeper |
| `DIDService` | Parse did:web identifiers |
| `TrustStoreService` | Add trusted CA keys |
| `RevocationService` | Check revocation status |
| `ScoringService` | Score agent cards, validate rules |
| `SimpleGuardService` | Sign/verify payloads with JWS |
| `RegistryService` | Fetch agent cards |

### Python SDK Usage

```python
from capiscio_sdk._rpc.client import CapiscioRPCClient

# Auto-starts gRPC server via process manager
with CapiscioRPCClient() as client:
    # Verify a badge
    valid, claims, warnings, err = client.badge.verify_badge_with_options(
        token="eyJhbGciOiJFZERTQSI...",
        accept_self_signed=True,  # SDK flag for development only
    )
    if valid:
        print(f"Subject: {claims['sub']}")
        print(f"Trust Level: {claims['trust_level']}")
```

For full gRPC documentation, see [gRPC Services Reference](../grpc.md).

---

## Global Flags

These flags are available for all commands:

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help for any command |
| `-v, --version` | Show version information |

---

## Wrapper-Specific Commands

### npm (capiscio-node)

The npm distribution is a pass-through wrapper. All commands work identically, plus:

| Command | Description |
|---------|-------------|
| `capiscio --wrapper-version` | Show the Node.js wrapper version |
| `capiscio --wrapper-clean` | Remove cached binary (forces re-download) |

### pip (capiscio-python)

The pip distribution includes wrapper management commands:

| Command | Description |
|---------|-------------|
| `capiscio --wrapper-version` | Show the Python wrapper version |
| `capiscio --wrapper-clean` | Remove cached binary (forces re-download) |

---

## See Also

- [Go API Reference](../go-api.md) - Programmatic usage of capiscio-core
- [Getting Started: Validate Your First Agent](../../getting-started/validate/1-intro.md)
- [Configuration Reference](../configuration.md)
- [Agent Card Schema](../agent-card-schema.md)
