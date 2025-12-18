---
title: Security Gateway Setup
description: Deploy the CapiscIO gateway to protect your agent endpoints
---

# Security Gateway Setup

Deploy the CapiscIO security gateway as a reverse proxy that validates trust badges before forwarding requests to your agent.

---

## Problem

You need to:

- Protect your agent's API endpoints from unauthorized access
- Validate trust badges on every incoming request
- Reject requests with invalid, expired, or missing badges
- Keep authentication logic separate from your agent code

---

## Solution

Run `capiscio gateway start` in front of your agent to handle all badge validation automatically.

### Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Client    │────▶│ CapiscIO Gateway │────▶│ Your Agent   │
│ (with badge)│     │   (port 8080)    │     │ (port 3000)  │
└─────────────┘     └─────────────────┘     └──────────────┘
                           │
                    ┌──────┴──────┐
                    │  Validates  │
                    │   badges    │
                    │  ✓ or 401   │
                    └─────────────┘
```

---

## Quick Start

### Local Mode (Single Key)

Verify badges against a single public key:

```bash
# Start your agent on port 3000
python my_agent.py  # Listens on localhost:3000

# Start gateway on port 8080
capiscio gateway start \
  --port 8080 \
  --target http://localhost:3000 \
  --local-key ./trusted-agent.pub.jwk
```

Now requests to `localhost:8080` require a valid badge signed by the trusted key.

### Cloud Mode (Registry)

Verify badges against the CapiscIO registry:

```bash
capiscio gateway start \
  --port 8080 \
  --target http://localhost:3000 \
  --registry-url https://registry.capisc.io
```

---

## Configuration Options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `8080` | Port the gateway listens on |
| `--target` | `http://localhost:3000` | Your agent's URL |
| `--local-key` | - | Path to trusted public key (JWK) |
| `--registry-url` | - | CapiscIO registry URL |

!!! warning "Choose One"
    You must provide either `--local-key` OR `--registry-url`, not both.

---

## Production Deployment

### With Docker

```dockerfile
FROM ghcr.io/capiscio/capiscio-core:latest

COPY trusted-keys/ /keys/

EXPOSE 8080

CMD ["gateway", "start", \
     "--port", "8080", \
     "--target", "http://agent:3000", \
     "--local-key", "/keys/trusted.pub.jwk"]
```

### With Docker Compose

```yaml
version: '3.8'

services:
  gateway:
    image: ghcr.io/capiscio/capiscio-core:latest
    command: >
      gateway start
      --port 8080
      --target http://agent:3000
      --local-key /keys/trusted.pub.jwk
    ports:
      - "8080:8080"
    volumes:
      - ./keys:/keys:ro
    depends_on:
      - agent

  agent:
    build: ./my-agent
    expose:
      - "3000"
    # No external ports - only accessible through gateway
```

### With Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: capiscio-gateway
spec:
  replicas: 2
  selector:
    matchLabels:
      app: capiscio-gateway
  template:
    metadata:
      labels:
        app: capiscio-gateway
    spec:
      containers:
      - name: gateway
        image: ghcr.io/capiscio/capiscio-core:latest
        args:
          - gateway
          - start
          - --port=8080
          - --target=http://my-agent-service:3000
          - --registry-url=https://registry.capisc.io
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: capiscio-gateway
spec:
  selector:
    app: capiscio-gateway
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

---

## Testing the Gateway

### Valid Request

```bash
# Get a badge (see badges recipe)
BADGE=$(capiscio badge issue \
  --sub "did:capiscio:agent:client" \
  --domain "client.example.com" \
  --key ./client-private.jwk)

# Make authenticated request
curl -X POST http://localhost:8080/api/task \
  -H "Authorization: Bearer $BADGE" \
  -H "Content-Type: application/json" \
  -d '{"task": "translate", "text": "Hello"}'
```

### Missing Badge (401)

```bash
curl -X POST http://localhost:8080/api/task \
  -H "Content-Type: application/json" \
  -d '{"task": "translate"}'

# Response: 401 Unauthorized
# {"error": "missing authorization header"}
```

### Invalid Badge (403)

```bash
curl -X POST http://localhost:8080/api/task \
  -H "Authorization: Bearer invalid.token.here" \
  -H "Content-Type: application/json" \
  -d '{"task": "translate"}'

# Response: 403 Forbidden
# {"error": "invalid badge signature"}
```

---

## Multiple Trusted Keys

To trust badges from multiple issuers, create a JWKS (JSON Web Key Set):

```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "key1-public-x-value",
      "kid": "partner-1",
      "alg": "EdDSA"
    },
    {
      "kty": "OKP",
      "crv": "Ed25519", 
      "x": "key2-public-x-value",
      "kid": "partner-2",
      "alg": "EdDSA"
    }
  ]
}
```

Then use the registry mode which supports JWKS endpoints.

---

## Gateway Behind Load Balancer

When running behind a load balancer (nginx, AWS ALB, etc.):

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/ssl/certs:ro
    depends_on:
      - gateway

  gateway:
    image: ghcr.io/capiscio/capiscio-core:latest
    command: gateway start --port 8080 --target http://agent:3000 --local-key /keys/trusted.pub.jwk
    expose:
      - "8080"
```

```nginx
# nginx.conf
upstream gateway {
    server gateway:8080;
}

server {
    listen 443 ssl;
    server_name agent.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/certs/key.pem;
    
    location / {
        proxy_pass http://gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring

### Logs

```bash
# View gateway logs
docker logs -f capiscio-gateway

# Example output:
# 2025/12/01 19:48:00 Starting Gateway in LOCAL MODE (Key: /keys/trusted.pub.jwk)
# 2025/12/01 19:48:00 Gateway listening on :8080 -> http://agent:3000
# 2025/12/01 19:48:15 [200] POST /api/task - valid badge from did:capiscio:agent:client
# 2025/12/01 19:48:20 [401] POST /api/task - missing authorization header
```

### Metrics (Prometheus)

The gateway exposes metrics at `/metrics`:

```bash
curl http://localhost:8080/metrics
```

---

## Troubleshooting

### "must provide either --local-key or --registry-url"

You need to specify how to verify badges:

```bash
# Use a local key
capiscio gateway start --local-key ./trusted.pub.jwk --target http://localhost:3000

# OR use the registry
capiscio gateway start --registry-url https://registry.capisc.io --target http://localhost:3000
```

### "invalid target URL"

The target must be a valid URL:

```bash
# Wrong
--target localhost:3000

# Correct
--target http://localhost:3000
```

### Gateway returns 502

Your agent isn't reachable:

1. Check agent is running: `curl http://localhost:3000/health`
2. Check network connectivity between gateway and agent
3. Verify the target URL is correct

---

## See Also

- [Issue and Verify Badges](./badges.md) - Create badges for testing
- [Badge Keeper](./badge-keeper.md) - Auto-renew client badges
- [CLI Reference: gateway](../../reference/cli/index.md#gateway-start) - Full command reference
