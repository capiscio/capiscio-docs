---
title: Deploying to Ephemeral Environments
description: Persist agent and MCP server identity in Docker, Lambda, Cloud Run, and Kubernetes
---

# Deploying to Ephemeral Environments

Both the **CapiscIO Python SDK** (agent identity) and **MCP Guard** (MCP server identity) use a "Let's Encrypt" style setup that generates cryptographic keys on first run and stores them locally. In ephemeral environments — Docker containers, serverless functions, CI runners — that local storage is lost on every restart.

This guide shows how to persist identity across restarts using environment variable key injection.

---

## The Problem

```mermaid
sequenceDiagram
    participant C as Container Start
    participant SDK as CapiscIO SDK
    participant R as Registry
    
    C->>SDK: connect()
    Note over SDK: No keys on disk
    SDK->>SDK: Generate new keypair
    SDK->>R: Register public key
    R-->>SDK: did:web assigned
    Note over SDK: Badge issued to DID-A
    
    C->>C: Container restarts
    C->>SDK: connect()
    Note over SDK: No keys on disk (wiped)
    SDK->>SDK: Generate DIFFERENT keypair
    SDK->>R: Register DIFFERENT key
    R-->>SDK: DIFFERENT did:web
    Note over SDK: Old badge invalid!
```

Without key persistence, each restart creates a **new identity** with a **different DID**. Any badges, trust relationships, or audit trails linked to the old DID are lost.

---

## The Solution: Environment Variable Key Injection

Both SDKs accept the private key as an environment variable. The key is loaded on startup, the same DID is recovered, and any existing badges remain valid.

=== "Agent SDK (capiscio-sdk-python)"

    | Variable | Format | Description |
    |----------|--------|-------------|
    | `CAPISCIO_AGENT_PRIVATE_KEY_JWK` | JSON string | Ed25519 private JWK with `kid` containing the DID |

    ```bash
    CAPISCIO_AGENT_PRIVATE_KEY_JWK='{"kty":"OKP","crv":"Ed25519","d":"...","x":"...","kid":"did:key:z6Mk..."}'
    ```

=== "MCP Guard (capiscio-mcp-python)"

    | Variable | Format | Description |
    |----------|--------|-------------|
    | `CAPISCIO_SERVER_PRIVATE_KEY_PEM` | PEM string | PKCS#8-encoded Ed25519 private key |

    ```bash
    CAPISCIO_SERVER_PRIVATE_KEY_PEM='-----BEGIN PRIVATE KEY-----\nMC4CAQ...xYz\n-----END PRIVATE KEY-----\n'
    ```

---

## Step 1: Capture the Key

On the very first run, the SDK generates a keypair and logs a **capture hint** to stderr:

=== "Agent SDK"

    ```
    ╔══════════════════════════════════════════════════════════════════╗
    ║  New agent identity generated — save key for persistence         ║
    ╚══════════════════════════════════════════════════════════════════╝

      Add to your secrets manager / .env:

        CAPISCIO_AGENT_PRIVATE_KEY_JWK='{"kty":"OKP","crv":"Ed25519","d":"nWGx...","x":"11qY...","kid":"did:key:z6MkEnv..."}'

      The DID will be recovered automatically from the JWK on startup.
    ```

=== "MCP Guard"

    ```
    ╔══════════════════════════════════════════════════════════════════╗
    ║  New server identity generated — save key for persistence        ║
    ╚══════════════════════════════════════════════════════════════════╝

      Add to your secrets manager / .env:

        CAPISCIO_SERVER_PRIVATE_KEY_PEM='-----BEGIN PRIVATE KEY-----\nMC4CAQ...xYz\n-----END PRIVATE KEY-----\n'

      The DID will be recovered automatically from the key on startup.
    ```

Run your agent or MCP server once locally, copy the key from stderr, and store it in your secrets manager.

---

## Step 2: Inject the Key

### Docker Compose

=== "Agent"

    ```yaml
    services:
      my-agent:
        build: .
        environment:
          CAPISCIO_API_KEY: "${CAPISCIO_API_KEY}"
          CAPISCIO_AGENT_PRIVATE_KEY_JWK: "${AGENT_KEY_JWK}"
    ```

=== "MCP Server"

    ```yaml
    services:
      mcp-server:
        build: .
        environment:
          CAPISCIO_SERVER_ID: "550e8400-..."
          CAPISCIO_API_KEY: "${CAPISCIO_API_KEY}"
          CAPISCIO_SERVER_PRIVATE_KEY_PEM: "${MCP_SERVER_KEY}"
    ```

### Kubernetes

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: capiscio-identity
type: Opaque
stringData:
  api-key: "sk_live_..."
  # Choose the appropriate key for your use case:
  agent-private-key-jwk: '{"kty":"OKP","crv":"Ed25519","d":"...","x":"...","kid":"did:key:z6Mk..."}'
  server-private-key-pem: |
    -----BEGIN PRIVATE KEY-----
    MC4CAQ...xYz
    -----END PRIVATE KEY-----
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent
spec:
  template:
    spec:
      containers:
        - name: agent
          env:
            - name: CAPISCIO_API_KEY
              valueFrom:
                secretKeyRef:
                  name: capiscio-identity
                  key: api-key
            - name: CAPISCIO_AGENT_PRIVATE_KEY_JWK
              valueFrom:
                secretKeyRef:
                  name: capiscio-identity
                  key: agent-private-key-jwk
```

### AWS Lambda

```bash
aws lambda update-function-configuration \
  --function-name my-agent \
  --environment "Variables={
    CAPISCIO_API_KEY=sk_live_...,
    CAPISCIO_AGENT_PRIVATE_KEY_JWK=$(cat agent-key.json)
  }"
```

!!! tip "Use AWS Secrets Manager"
    For production, store the key in AWS Secrets Manager and reference it
    via a Lambda layer or the Secrets Manager SDK rather than inline env vars.

### Google Cloud Run

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-agent
spec:
  template:
    spec:
      containers:
        - image: gcr.io/my-project/my-agent
          env:
            - name: CAPISCIO_API_KEY
              valueFrom:
                secretKeyRef:
                  name: capiscio-api-key
                  key: latest
            - name: CAPISCIO_AGENT_PRIVATE_KEY_JWK
              valueFrom:
                secretKeyRef:
                  name: agent-private-key
                  key: latest
```

---

## Key Resolution Priority

Both SDKs follow the same priority order:

| Priority | Source | When Used |
|----------|--------|-----------|
| **1** | Environment variable | Containers, serverless, CI |
| **2** | Local key file on disk | Persistent VMs, bare metal |
| **3** | Generate new keypair | First run only |

If the env var is set, it always wins — even if a different key exists on disk. This lets you override identity for testing or migration.

!!! warning "DID Changes on New Key Generation"
    If neither the env var nor local files are available, the SDK generates a **new** keypair with a **different** DID. Any badges issued to the old DID will no longer be valid. Always persist the key in ephemeral environments.

---

## Key Rotation

To rotate either an agent or MCP server identity:

1. **Unset** the environment variable (`CAPISCIO_AGENT_PRIVATE_KEY_JWK` or `CAPISCIO_SERVER_PRIVATE_KEY_PEM`)
2. **Remove** local key files if present
3. **Restart** the service — a new keypair and DID will be generated
4. **Capture** the new key from the log hint
5. **Store** the new key in your secrets manager

!!! danger "Badge Invalidation"
    Rotating keys changes the DID, which invalidates all existing badges.
    The SDK will automatically request a new badge on the next `connect()` call.
    Plan rotation during maintenance windows.

See [Key Rotation](key-rotation.md) for more advanced patterns.

---

## Complete Environment Variable Reference

### Agent SDK (`CapiscIO.from_env()`)

| Variable | Required | Description |
|----------|----------|-------------|
| `CAPISCIO_API_KEY` | Yes | Registry API key |
| `CAPISCIO_AGENT_NAME` | No | Agent name for lookup/creation |
| `CAPISCIO_AGENT_ID` | No | Specific agent UUID |
| `CAPISCIO_SERVER_URL` | No | Registry URL |
| `CAPISCIO_DEV_MODE` | No | Enable dev mode |
| `CAPISCIO_AGENT_PRIVATE_KEY_JWK` | No | Ed25519 private JWK (JSON string) |

### MCP Guard (`MCPServerIdentity.from_env()`)

| Variable | Required | Description |
|----------|----------|-------------|
| `CAPISCIO_SERVER_ID` | Yes | Server UUID from dashboard |
| `CAPISCIO_API_KEY` | Yes | Registry API key |
| `CAPISCIO_SERVER_URL` | No | Registry URL |
| `CAPISCIO_SERVER_DOMAIN` | No | Domain for badge issuance |
| `CAPISCIO_SERVER_PRIVATE_KEY_PEM` | No | Ed25519 private key (PEM string) |

### Security Middleware (`SecurityConfig.from_env()`)

See [Configuration Reference](../../reference/configuration.md) for the full list of `SecurityConfig` environment variables.

---

## Next Steps

- [Key Rotation](key-rotation.md) — Advanced rotation patterns
- [Badge Keeper](badge-keeper.md) — Automatic badge renewal
- [Dev Mode](dev-mode.md) — Local development without a registry
