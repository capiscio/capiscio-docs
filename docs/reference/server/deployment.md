# Deployment Guide

<!-- 
  VERIFIED: 2025-12-11
  Source: capiscio-server/README.md, capiscio-server/.env.example
-->

Deploy capiscio-server in production or development environments.

---

## Prerequisites

- **Go 1.23+** (for building from source)
- **PostgreSQL 15+** (database)
- **Docker** (recommended for deployment)

---

## Docker Deployment (Recommended)

### Quick Start with Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  server:
    image: ghcr.io/capiscio/capiscio-server:latest
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/capiscio?sslmode=disable
      - ENVIRONMENT=production
      - CA_ISSUER_URL=https://registry.example.com
    depends_on:
      - db
    volumes:
      - ./ca-keys:/app/keys  # Persist CA keys

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=capiscio
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Run:

```bash
docker-compose up -d
```

### Single Container

```bash
docker run -d \
  --name capiscio-server \
  -p 8080:8080 \
  -e DATABASE_URL="postgres://user:pass@host:5432/capiscio" \
  -e CA_ISSUER_URL="https://registry.example.com" \
  -v ./ca-keys:/app/keys \
  ghcr.io/capiscio/capiscio-server:latest
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `PORT` | No | `8080` | HTTP server port |
| `ENVIRONMENT` | No | `development` | `development` or `production` |
| `CA_KEY_PATH` | No | `./keys/ca.jwk` | Path to CA private key |
| `CA_ISSUER_URL` | Yes | — | Public URL for badge issuer claim |
| `CLERK_SECRET_KEY` | No | — | Clerk API key (for dashboard auth) |
| `CLERK_WEBHOOK_SECRET` | No | — | Clerk webhook secret |

### Example `.env` File

```bash
# Database
DATABASE_URL=postgres://postgres:postgres@localhost:5432/capiscio?sslmode=disable

# Server
PORT=8080
ENVIRONMENT=production

# CA Configuration
CA_KEY_PATH=/app/keys/ca.jwk
CA_ISSUER_URL=https://registry.capisc.io

# Authentication (optional - for dashboard)
CLERK_SECRET_KEY=sk_live_xxx
CLERK_WEBHOOK_SECRET=whsec_xxx
```

---

## Database Setup

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE capiscio;
```

### Migrations

Migrations run automatically on startup. The server uses embedded migrations.

---

## CA Key Management

### Key Generation

If `CA_KEY_PATH` doesn't exist, the server generates an ephemeral key on startup.

**For production**, persist the CA key:

```bash
# Create keys directory
mkdir -p /app/keys

# The server will generate and save the key on first run
# Alternatively, generate manually:
capiscio key gen --out-priv /app/keys/ca.jwk --out-pub /app/keys/ca-public.jwk
```

### Key Rotation

To rotate CA keys:

1. Generate new keypair
2. Update `CA_KEY_PATH` to point to new key
3. Restart server
4. Old badges remain valid until expiry (verify against old JWKS)

!!! warning "Key Persistence"
    Always back up your CA private key. Losing it means badges can't be verified.

---

## TLS Configuration

### Behind a Reverse Proxy (Recommended)

Use nginx, Caddy, or a cloud load balancer for TLS termination:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name registry.example.com;

    ssl_certificate /etc/letsencrypt/live/registry.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/registry.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Health Checks

The server exposes health endpoints:

```bash
# Liveness probe
curl http://localhost:8080/health

# Readiness probe (includes DB check)
curl http://localhost:8080/health/ready
```

### Kubernetes Example

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

## Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: capiscio-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: capiscio-server
  template:
    metadata:
      labels:
        app: capiscio-server
    spec:
      containers:
        - name: server
          image: ghcr.io/capiscio/capiscio-server:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: capiscio-secrets
                  key: database-url
            - name: CA_ISSUER_URL
              value: "https://registry.example.com"
          volumeMounts:
            - name: ca-keys
              mountPath: /app/keys
      volumes:
        - name: ca-keys
          secret:
            secretName: capiscio-ca-key
```

---

## Building from Source

!!! note "Enterprise License Required"
    Access to the capiscio-server repository requires an enterprise license. [Contact Sales](mailto:sales@capisc.io) for access.

```bash
# Clone repository (enterprise customers only)
git clone https://github.com/capiscio/capiscio-server
cd capiscio-server

# Build
make build

# Run
./bin/server
```

---

## Monitoring

### Metrics (Prometheus)

Coming soon: Prometheus metrics endpoint at `/metrics`.

### Logging

Logs are written to stdout in JSON format:

```json
{"level":"info","time":"2025-01-15T10:30:00Z","message":"Server started","port":8080}
{"level":"info","time":"2025-01-15T10:30:05Z","message":"Badge issued","agent_id":"550e8400...","trust_level":"2"}
```

---

## Troubleshooting

### Database Connection Failed

```
error: failed to connect to database
```

1. Verify `DATABASE_URL` is correct
2. Check PostgreSQL is running: `pg_isready -h localhost -p 5432`
3. Ensure database exists: `psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname = 'capiscio'"`

### CA Key Not Found

```
error: failed to load CA key
```

1. Check `CA_KEY_PATH` points to a valid file
2. Ensure the file is readable by the server process
3. For first run, the server generates a key automatically

### Badge Verification Fails

```
error: signature verification failed
```

1. Ensure client is using the correct JWKS URL
2. Check if CA key was rotated
3. Verify badge hasn't expired

---

## See Also

- [API Reference](api.md) — Full API documentation
- [Badge CA](badge-ca.md) — CA operations
- [Contact Sales](mailto:sales@capisc.io) — Enterprise deployment options (air-gapped, on-prem)
