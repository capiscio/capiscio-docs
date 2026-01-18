# End-to-End Tutorial

<!-- 
  VERIFIED: 2025-12-11
  Based on: capiscio-core, capiscio-server, capiscio-sdk-python source code
-->

This tutorial walks through the complete CapiscIO workflow: from creating an A2A agent to deploying it with trust badge enforcement.

!!! abstract "What You'll Learn"
    1. Create an A2A-compliant agent with `agent-card.json`
    2. Validate locally with the CLI
    3. Register with capiscio-server
    4. Obtain a CA-signed badge (trust level 2)
    5. Deploy with gateway enforcement
    6. Monitor trust scores

---

## Prerequisites

- Python 3.10+ or Node.js 18+
- Docker (for local server)
- `capiscio` CLI installed

```bash
# Install CLI via pip
pip install capiscio

# Or via npm
npm install -g capiscio

# Verify installation
capiscio version
```

---

## Part 1: Create Your Agent

### 1.1 Create Agent Card

Every A2A agent needs an `agent-card.json` that describes its capabilities:

```json
{
  "name": "My Assistant Agent",
  "description": "A helpful assistant that can answer questions",
  "url": "https://my-agent.example.com",
  "version": "1.0.0",
  "provider": {
    "organization": "My Company",
    "url": "https://example.com"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
  "authentication": {
    "schemes": ["bearer"]
  },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [
    {
      "id": "general-qa",
      "name": "General Q&A",
      "description": "Answer general knowledge questions",
      "tags": ["qa", "knowledge"],
      "examples": [
        "What is the capital of France?",
        "Explain quantum computing"
      ]
    }
  ]
}
```

Save this as `agent-card.json` in your project root.

### 1.2 Validate Locally

Run basic schema validation:

```bash
capiscio validate ./agent-card.json
```

Expected output:

```
✅ Agent Card Valid!
   Name: My Assistant Agent
   URL: https://my-agent.example.com
   Skills: 1
```

### 1.3 Test with Strict Mode

For production readiness, use strict validation:

```bash
capiscio validate ./agent-card.json --strict --registry-ready
```

Fix any warnings before proceeding.

---

## Part 2: Generate Keys

### 2.1 Create Ed25519 Keypair

Generate a signing keypair for your agent:

```bash
capiscio key gen --out-priv private.jwk --out-pub public.jwk
```

!!! danger "Protect Your Private Key"
    Never commit `private.jwk` to version control. Add it to `.gitignore`:
    ```
    private.jwk
    *.pem
    ```

### 2.2 Add Public Key to Agent Card

Update your `agent-card.json` to include the public key:

```json
{
  "name": "My Assistant Agent",
  "...": "...",
  "publicKey": {
    "kty": "OKP",
    "crv": "Ed25519",
    "x": "YOUR_PUBLIC_KEY_X_VALUE",
    "kid": "key-1",
    "alg": "EdDSA",
    "use": "sig"
  }
}
```

---

## Part 3: Register with CapiscIO Server

### 3.1 Start Local Server (Development)

For local development, run capiscio-server with Docker:

!!! note "Enterprise License Required"
    Access to the capiscio-server repository requires an enterprise license. [Contact Sales](mailto:sales@capisc.io) for access.

```bash
# Clone the server repo (enterprise customers only)
git clone https://github.com/capiscio/capiscio-server
cd capiscio-server

# Start with Docker Compose
docker-compose up -d
```

Server runs at `http://localhost:8080`.

### 3.2 Create an Account

For production, sign up at [https://capiscio.io](https://capiscio.io).

For local development, the server auto-creates a test account.

### 3.3 Create an API Key

```bash
# Via API (local)
curl -X POST http://localhost:8080/v1/api-keys \
  -H "Content-Type: application/json" \
  -d '{"name": "Development Key"}'
```

Save the returned API key securely:

```bash
export CAPISCIO_API_KEY="cpsc_live_xxx"
```

### 3.4 Register Your Agent

```bash
curl -X POST http://localhost:8080/v1/agents \
  -H "X-Capiscio-Registry-Key: $CAPISCIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Assistant Agent",
    "domain": "my-agent.example.com",
    "description": "A helpful assistant agent"
  }'
```

Note the returned `id` (UUID):

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

```bash
export AGENT_ID="550e8400-e29b-41d4-a716-446655440000"
```

---

## Part 4: Get a CA-Signed Badge

### 4.1 Domain Verification (Trust Level 2)

For trust level 2+, add a DNS TXT record:

```
_capiscio.my-agent.example.com TXT "capiscio-verification=550e8400-e29b-41d4-a716-446655440000"
```

### 4.2 Request Badge

```bash
curl -X POST "http://localhost:8080/v1/agents/$AGENT_ID/badge" \
  -H "X-Capiscio-Registry-Key: $CAPISCIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "my-agent.example.com",
    "trustLevel": "2"
  }'
```

Response:

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
    "trustLevel": "2",
    "expiresAt": "2025-01-15T10:35:00Z"
  }
}
```

### 4.3 Use Badge Keeper for Auto-Renewal

Badges expire quickly (5 minutes by default). Use the badge keeper daemon:

=== "CLI"

    ```bash
    capiscio badge keep \
      --ca-url "http://localhost:8080" \
      --agent-id "$AGENT_ID" \
      --api-key "$CAPISCIO_API_KEY" \
      --domain "my-agent.example.com" \
      --out ./badge.jwt
    ```

=== "Python SDK"

    ```python
    from capiscio_sdk.badge import BadgeKeeper
    
    keeper = BadgeKeeper(
        ca_url="http://localhost:8080",
        agent_id=os.environ["AGENT_ID"],
        api_key=os.environ["CAPISCIO_API_KEY"],
        domain="my-agent.example.com",
        output_path="./badge.jwt",
    )
    keeper.start()
    ```

---

## Part 5: Deploy with Gateway

### 5.1 Start Your Agent

First, ensure your agent is running:

```python
# agent.py
from fastapi import FastAPI

app = FastAPI()

@app.post("/task")
async def handle_task(request: dict):
    return {"result": "Task completed!"}

@app.get("/.well-known/agent.json")
async def agent_card():
    return {
        "name": "My Assistant Agent",
        # ... rest of agent card
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
```

```bash
python agent.py
# Agent running at http://localhost:3000
```

### 5.2 Start the Gateway

The gateway validates badges before forwarding requests to your agent:

```bash
capiscio gateway start \
  --port 8080 \
  --target http://localhost:3000 \
  --registry-url http://localhost:8080
```

Architecture:

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Client    │────▶│ CapiscIO Gateway │────▶│ Your Agent   │
│             │     │   (port 8080)    │     │ (port 3000)  │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │
                           │ Validates badge
                           ▼
                    ┌─────────────────┐
                    │ capiscio-server │
                    │  /.well-known/  │
                    │    jwks.json    │
                    └─────────────────┘
```

### 5.3 Test with Badge

```bash
# Get your badge
BADGE=$(cat badge.jwt)

# Make request through gateway
curl -X POST http://localhost:8080/task \
  -H "Authorization: Bearer $BADGE" \
  -H "Content-Type: application/json" \
  -d '{"task": "hello"}'
```

### 5.4 Alternative: Python SDK Middleware

For simpler deployments, use the SDK middleware instead of the gateway:

```python
from fastapi import FastAPI
from capiscio_sdk import CapiscioMiddleware, SecurityConfig

app = FastAPI()

# Add badge verification middleware
app.add_middleware(
    CapiscioMiddleware,
    config=SecurityConfig.production(
        trusted_issuers=["https://registry.capisc.io"],
        min_trust_level=2,
    ),
)

@app.post("/task")
async def handle_task(request: dict):
    return {"result": "Task completed!"}
```

---

## Part 6: Monitor Trust Scores

### 6.1 Check Validation Score

```bash
capiscio validate ./agent-card.json --json | jq '.scores'
```

Output:

```json
{
  "compliance": 95,
  "trust": 80,
  "availability": 100
}
```

### 6.2 Score Categories

| Category | What It Measures |
|----------|------------------|
| **Compliance** | Schema correctness, required fields |
| **Trust** | Signature validity, identity verification |
| **Availability** | Endpoint reachability, response times |

### 6.3 Improve Your Score

- **Compliance**: Fix all schema warnings
- **Trust**: Use CA-signed badges (level 2+)
- **Availability**: Ensure `/.well-known/agent.json` is accessible

---

## Part 7: Production Checklist

Before going to production:

- [ ] Agent card passes `--strict --registry-ready` validation
- [ ] Private key secured (not in version control)
- [ ] Domain verification completed (DNS TXT record)
- [ ] Badge keeper daemon running
- [ ] Gateway or SDK middleware configured
- [ ] HTTPS enabled (TLS)
- [ ] Health endpoints implemented
- [ ] Monitoring configured

---

## Summary

You've learned the complete CapiscIO workflow:

1. **Create** an A2A agent card
2. **Validate** with the CLI
3. **Generate** Ed25519 keys
4. **Register** with capiscio-server
5. **Obtain** CA-signed badges
6. **Deploy** with gateway enforcement
7. **Monitor** trust scores

---

## Next Steps

- [Trust Model](../concepts/trust-model.md) — Understand trust levels
- [Badge Guides](../how-to/security/badges.md) — Advanced badge operations
- [Gateway Setup](../how-to/security/gateway-setup.md) — Gateway configuration
- [Python SDK](../reference/sdk-python/index.md) — SDK reference
