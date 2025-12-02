---
title: Sign Outbound Requests
description: Add JWS signatures to your A2A calls
---

# Sign Outbound Requests

Add cryptographic signatures to requests when calling other A2A agents.

---

## Problem

When your agent calls another A2A agent, you need to:

- Prove your identity
- Ensure message integrity
- Meet security requirements for production A2A networks

---

## Solution: SimpleGuard

The easiest way is using `SimpleGuard`:

```python
from capiscio_sdk.simple_guard import SimpleGuard
import json

# Initialize guard (auto-generates keys in dev_mode)
guard = SimpleGuard(dev_mode=True)

# Sign an outbound request
payload = {"sub": "weather-request"}  # JWT claims (optional)
body_dict = {"message": "Hello from my agent"}
body_bytes = json.dumps(body_dict).encode('utf-8')

# Generate signed headers
headers = guard.make_headers(payload, body=body_bytes)
headers["Content-Type"] = "application/json"

# Use with httpx/requests
import httpx
response = httpx.post(
    "https://other-agent.com/a2a",
    headers=headers,
    content=body_bytes
)
```

---

## What make_headers Returns

```python
headers = guard.make_headers(payload, body)

# Returns dict like:
{
    "X-Capiscio-JWS": "eyJhbGciOiJFZERTQSIsInR5cCI6Ikp..."  # JWS signature
}
```
```

---

## Using sign_outbound Directly

For more control:

```python
from capiscio_sdk.simple_guard import SimpleGuard
import json

guard = SimpleGuard(dev_mode=True)

# Payload contains optional JWT claims
# iss, iat, exp are auto-injected if missing
payload = {
    "sub": "weather-agent"  # Optional: subject claim
}

body_dict = {"query": "What is the weather?"}
body_bytes = json.dumps(body_dict).encode('utf-8')

# Get just the JWS signature
jws = guard.sign_outbound(payload, body=body_bytes)
print(jws)  # eyJhbGciOiJFZERTQSIs...
```

---

## Production Setup

For production, don't use `dev_mode`. SimpleGuard finds keys via convention:

```python
from capiscio_sdk.simple_guard import SimpleGuard

# SimpleGuard looks for keys in capiscio_keys/ relative to base_dir
# Walks up directory tree to find agent-card.json
guard = SimpleGuard()  # dev_mode=False is default
```

Or specify a different base directory:

```python
from capiscio_sdk.simple_guard import SimpleGuard

guard = SimpleGuard(base_dir="/etc/capiscio")
```

**Expected structure:**
```
/etc/capiscio/
├── agent-card.json
└── capiscio_keys/
    ├── private.pem
    ├── public.pem
    └── trusted/
```

---

## Generate Keys

If you need to generate Ed25519 keys:

```bash
# Using the CLI
capiscio key gen --out-priv private.key --out-pub public.key
```

Or in Python:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# Generate
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Save private key
with open("private.key", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Save public key
with open("public.key", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
```

---

## Complete Example

```python
import httpx
from capiscio_sdk.simple_guard import SimpleGuard
import json

# Setup
guard = SimpleGuard(dev_mode=True)

# Prepare request
target_url = "https://weather-agent.example.com/a2a"
request_body = json.dumps({
    "jsonrpc": "2.0",
    "method": "tasks/send",
    "params": {
        "message": {
            "role": "user",
            "parts": [{"text": "What's the weather in Paris?"}]
        }
    },
    "id": "req-001"
}).encode('utf-8')

# Create signed payload (iss, iat, exp auto-injected)
payload = {
    "sub": "weather-request"  # Optional additional claims
}

# Sign and send
headers = guard.make_headers(payload, body=request_body)
headers["Content-Type"] = "application/json"
response = httpx.post(target_url, headers=headers, content=request_body)

print(response.json())
```

---

## See Also

- [Verify Inbound Requests](verify-inbound.md) — The receiving side
- [Key Rotation](key-rotation.md) — Rotate keys safely
- [Security Quickstart](../../quickstarts/secure/1-intro.md) — Full security setup
