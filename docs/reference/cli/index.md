# CLI Reference

<!-- 
  VERIFIED: 2025-12-01
  Source: capiscio-core/cmd/capiscio/*.go
  All flags verified against Go source code.
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
| [`badge keep`](#badge-keep) | Daemon to auto-renew badges |
| [`gateway start`](#gateway-start) | Start the security gateway |

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

### Example

```bash
# Generate keys with default names
capiscio key gen

# Generate keys to specific paths
capiscio key gen --out-priv ./keys/private.jwk --out-pub ./keys/public.jwk
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

Issue a new trust badge for an agent. Trust badges are JWTs that attest to an agent's identity.

### Usage

```bash
capiscio badge issue [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sub` | `string` | `did:capiscio:agent:test` | Subject DID (agent identifier) |
| `--iss` | `string` | `https://registry.capisc.io` | Issuer URL |
| `--domain` | `string` | `example.com` | Agent domain |
| `--exp` | `duration` | `1h` | Expiration duration |
| `--key` | `string` | *(none)* | Path to private key file (JWK). If omitted, generates ephemeral key. |

### Examples

```bash
# Issue badge with ephemeral key (prints public key to stderr)
capiscio badge issue --sub "did:capiscio:agent:my-agent" --domain "my-agent.example.com"

# Issue badge with your private key
capiscio badge issue \
  --sub "did:capiscio:agent:my-agent" \
  --domain "my-agent.example.com" \
  --exp 24h \
  --key ./private.jwk

# Custom issuer
capiscio badge issue \
  --sub "did:capiscio:agent:my-agent" \
  --iss "https://my-registry.example.com" \
  --key ./private.jwk
```

### Output

The command outputs the signed JWT token to stdout:

```
eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6Y2FwaXNjaW86YWdlbnQ6bXktYWdlbnQiLC...
```

---

## badge verify

Verify a trust badge's signature and expiration.

### Usage

```bash
capiscio badge verify [token] [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--key` | `string` | *(required)* | Path to public key file (JWK) |

### Example

```bash
capiscio badge verify "eyJhbGciOiJFZERTQSI..." --key ./public.jwk
```

### Output

```
✅ Badge Valid!
Subject: did:capiscio:agent:my-agent
Issuer: https://registry.capisc.io
Expires: 2025-12-02T19:48:00Z
```

---

## badge keep

Run a daemon that automatically renews badges before expiration. Useful for long-running agents that need continuous authorization.

### Usage

```bash
capiscio badge keep [flags]
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--sub` | `string` | `did:capiscio:agent:test` | Subject DID |
| `--iss` | `string` | `https://registry.capisc.io` | Issuer URL |
| `--domain` | `string` | `example.com` | Agent domain |
| `--exp` | `duration` | `1h` | Expiration duration for each badge |
| `--key` | `string` | *(required)* | Path to private key file |
| `--out` | `string` | `badge.jwt` | Output file path for the badge |
| `--renew-before` | `duration` | `10m` | Time before expiry to renew |
| `--check-interval` | `duration` | `1m` | Interval to check for renewal |

### Example

```bash
capiscio badge keep \
  --sub "did:capiscio:agent:my-agent" \
  --domain "my-agent.example.com" \
  --key ./private.jwk \
  --out ./current-badge.jwt \
  --exp 1h \
  --renew-before 10m
```

### Behavior

The daemon will:

1. Issue an initial badge immediately
2. Write it to the output file
3. Check periodically if renewal is needed
4. Renew the badge when it's within `--renew-before` of expiry

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

## Global Flags

These flags are available for all commands:

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help for any command |
| `--version` | Show version information |

---

## Wrapper-Specific Commands

### npm (capiscio-node)

The npm distribution is a pass-through wrapper. All commands work identically.

### pip (capiscio-python)

The pip distribution includes wrapper management commands:

| Command | Description |
|---------|-------------|
| `capiscio --wrapper-version` | Show the Python wrapper version |
| `capiscio --wrapper-clean` | Remove cached binary (forces re-download) |

---

## See Also

- [Go API Reference](../go-api.md) - Programmatic usage of capiscio-core
- [Quickstart: Validate Your First Agent](../../quickstarts/validate/1-intro.md)
- [Configuration Reference](../configuration.md)
- [Agent Card Schema](../agent-card-schema.md)
