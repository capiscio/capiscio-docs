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

## Programmatic Usage (Python)

```python
import subprocess
import json

def issue_badge(subject: str, domain: str, key_path: str, expiry: str = "1h") -> str:
    """Issue a trust badge using the CLI."""
    result = subprocess.run([
        "capiscio", "badge", "issue",
        "--sub", subject,
        "--domain", domain,
        "--exp", expiry,
        "--key", key_path
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Failed to issue badge: {result.stderr}")
    
    return result.stdout.strip()

def verify_badge(token: str, key_path: str) -> bool:
    """Verify a trust badge using the CLI."""
    result = subprocess.run([
        "capiscio", "badge", "verify", token,
        "--key", key_path
    ], capture_output=True, text=True)
    
    return result.returncode == 0

# Usage
badge = issue_badge(
    subject="did:capiscio:agent:my-agent",
    domain="my-agent.example.com",
    key_path="./private.jwk"
)

is_valid = verify_badge(badge, "./public.jwk")
print(f"Badge valid: {is_valid}")
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

- [Badge Keep Daemon](./badge-keeper.md) - Auto-renew badges
- [CLI Reference: badge](../../reference/cli/index.md#badge-issue) - Full command reference
- [Security Gateway](./gateway-setup.md) - Validate badges automatically
