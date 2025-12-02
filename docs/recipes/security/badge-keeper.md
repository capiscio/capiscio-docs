---
title: Badge Keeper Daemon
description: Automatically renew trust badges before they expire
---

# Badge Keeper Daemon

Run a background daemon that automatically renews your agent's trust badge before expiration.

---

## Problem

Trust badges expire (typically every 1-24 hours for security). You need:

- Continuous authentication without manual renewal
- Zero-downtime badge rotation
- Automatic handling of badge lifecycle

---

## Solution

Use `capiscio badge keep` to run a daemon that monitors and renews badges automatically.

### Basic Usage

```bash
capiscio badge keep \
  --sub "did:capiscio:agent:my-agent" \
  --domain "my-agent.example.com" \
  --key ./private.jwk \
  --out ./current-badge.jwt \
  --exp 1h \
  --renew-before 10m
```

This will:

1. Issue an initial badge immediately
2. Write it to `./current-badge.jwt`
3. Renew it 10 minutes before expiration
4. Keep running until stopped

---

## Configuration Options

| Flag | Default | Description |
|------|---------|-------------|
| `--sub` | `did:capiscio:agent:test` | Your agent's DID |
| `--domain` | `example.com` | Your agent's domain |
| `--iss` | `https://registry.capisc.io` | Badge issuer |
| `--exp` | `1h` | Badge lifetime |
| `--key` | *(required)* | Path to private key |
| `--out` | `badge.jwt` | Output file for current badge |
| `--renew-before` | `10m` | Renew this long before expiry |
| `--check-interval` | `1m` | How often to check expiration |

---

## Production Deployment

### With systemd (Linux)

Create `/etc/systemd/system/capiscio-badge-keeper.service`:

```ini
[Unit]
Description=CapiscIO Badge Keeper
After=network.target

[Service]
Type=simple
User=myagent
WorkingDirectory=/opt/myagent
ExecStart=/usr/local/bin/capiscio badge keep \
  --sub "did:capiscio:agent:production-agent" \
  --domain "agent.mycompany.com" \
  --key /opt/myagent/keys/private.jwk \
  --out /opt/myagent/current-badge.jwt \
  --exp 1h \
  --renew-before 10m
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable capiscio-badge-keeper
sudo systemctl start capiscio-badge-keeper
sudo systemctl status capiscio-badge-keeper
```

### With Docker

```dockerfile
FROM alpine:latest

RUN apk add --no-cache curl
RUN curl -L https://github.com/capiscio/capiscio-core/releases/latest/download/capiscio-linux-amd64 \
    -o /usr/local/bin/capiscio && chmod +x /usr/local/bin/capiscio

COPY private.jwk /keys/private.jwk

CMD ["capiscio", "badge", "keep", \
     "--sub", "did:capiscio:agent:my-agent", \
     "--domain", "my-agent.example.com", \
     "--key", "/keys/private.jwk", \
     "--out", "/badges/current.jwt", \
     "--exp", "1h", \
     "--renew-before", "10m"]
```

### With Docker Compose

```yaml
version: '3.8'

services:
  badge-keeper:
    image: ghcr.io/capiscio/capiscio-core:latest
    command: >
      badge keep
      --sub "did:capiscio:agent:my-agent"
      --domain "my-agent.example.com"
      --key /keys/private.jwk
      --out /badges/current.jwt
      --exp 1h
      --renew-before 10m
    volumes:
      - ./keys:/keys:ro
      - badges:/badges
    restart: unless-stopped

  my-agent:
    build: .
    volumes:
      - badges:/badges:ro
    environment:
      - BADGE_FILE=/badges/current.jwt
    depends_on:
      - badge-keeper

volumes:
  badges:
```

---

## Reading the Badge in Your Agent

### Python

```python
import os
from pathlib import Path

def get_current_badge() -> str:
    """Read the current badge from the keeper's output file."""
    badge_path = Path(os.environ.get("BADGE_FILE", "./current-badge.jwt"))
    
    if not badge_path.exists():
        raise RuntimeError("Badge file not found. Is badge-keeper running?")
    
    return badge_path.read_text().strip()

# Use in requests
import httpx

badge = get_current_badge()
response = httpx.post(
    "https://other-agent.example.com/api/task",
    headers={"Authorization": f"Bearer {badge}"},
    json={"task": "process"}
)
```

### Node.js

```javascript
const fs = require('fs');
const path = require('path');

function getCurrentBadge() {
  const badgePath = process.env.BADGE_FILE || './current-badge.jwt';
  return fs.readFileSync(badgePath, 'utf-8').trim();
}

// Use in requests
const badge = getCurrentBadge();
const response = await fetch('https://other-agent.example.com/api/task', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${badge}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ task: 'process' })
});
```

---

## Monitoring

### Check if Keeper is Running

```bash
# Check process
pgrep -f "capiscio badge keep"

# Check badge file freshness
stat ./current-badge.jwt

# Decode and check expiration
cat ./current-badge.jwt | cut -d. -f2 | base64 -d 2>/dev/null | jq .exp
```

### Health Check Script

```bash
#!/bin/bash
# check-badge-health.sh

BADGE_FILE="${1:-./current-badge.jwt}"
MIN_REMAINING_SECONDS=300  # Alert if < 5 minutes remaining

if [ ! -f "$BADGE_FILE" ]; then
    echo "CRITICAL: Badge file not found"
    exit 2
fi

# Extract expiration
EXP=$(cat "$BADGE_FILE" | cut -d. -f2 | base64 -d 2>/dev/null | jq -r .exp)
NOW=$(date +%s)
REMAINING=$((EXP - NOW))

if [ $REMAINING -lt 0 ]; then
    echo "CRITICAL: Badge expired"
    exit 2
elif [ $REMAINING -lt $MIN_REMAINING_SECONDS ]; then
    echo "WARNING: Badge expires in ${REMAINING}s"
    exit 1
else
    echo "OK: Badge valid for ${REMAINING}s"
    exit 0
fi
```

---

## Troubleshooting

### Badge file not updating

1. Check keeper logs: `journalctl -u capiscio-badge-keeper -f`
2. Verify private key permissions: `ls -la ./private.jwk`
3. Check disk space: `df -h`

### "failed to write badge"

The output directory doesn't exist or isn't writable:

```bash
mkdir -p ./badges
chmod 755 ./badges
```

### High CPU usage

Reduce check frequency:

```bash
--check-interval 5m  # Check every 5 minutes instead of 1
```

---

## See Also

- [Issue and Verify Badges](./badges.md) - Manual badge workflow
- [Security Gateway](./gateway-setup.md) - Automatic badge validation
- [CLI Reference: badge keep](../../reference/cli/index.md#badge-keep) - Full command reference
