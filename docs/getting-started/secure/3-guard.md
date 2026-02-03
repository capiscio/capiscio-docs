---
title: "Step 3: Configure SimpleGuard"
description: Understand and customize SimpleGuard settings
---

# Step 3: Configure SimpleGuard

Now let's understand how SimpleGuard works and see it in action.

---

## Project Structure

SimpleGuard uses convention-over-configuration:

```
your-project/
├── agent-card.json           # Your agent's identity
├── capiscio_keys/
│   ├── private.pem           # Your signing key (SECRET!)
│   ├── public.pem            # Your public key
│   └── trusted/              # Keys you trust
│       └── partner.pem       # Trusted agent's public key
```

---

## Sign an Outbound Request

=== "Code"

    ```python title="sign_request.py"
    from capiscio_sdk import SimpleGuard
    import json
    
    guard = SimpleGuard(dev_mode=True)
    
    # Your request body
    body = {"jsonrpc": "2.0", "method": "hello", "params": {}}
    body_bytes = json.dumps(body).encode('utf-8')
    
    # Sign it - pass claims dict and body bytes
    signature = guard.sign_outbound({}, body=body_bytes)
    
    print(f"Signature: {signature[:50]}...")
    ```

=== "Output"

    ```json
    Signature: eyJhbGciOiJFZERTQSIsImtpZCI6ImxvY2FsLWRl...
    
    Decoded claims:
    {
      "iss": "local-dev-agent",
      "iat": 1701432000,
      "exp": 1701432060,
      "bh": "sha256:a1b2c3d4e5f6..."
    }
    ```

### Use the Signature in HTTP

=== "Code"

    ```python title="send_request.py"
    import httpx
    from capiscio_sdk import SimpleGuard
    
    guard = SimpleGuard(dev_mode=True)
    
    body = {"jsonrpc": "2.0", "method": "hello"}
    body_bytes = json.dumps(body).encode('utf-8')
    
    # Use make_headers helper for convenience
    headers = guard.make_headers({}, body=body_bytes)
    headers["Content-Type"] = "application/json"
    
    response = httpx.post(
        "https://partner-agent.example.com/a2a",
        data=body_bytes,  # Send exact bytes that were signed
        headers=headers
    )
    ```

=== "Request Sent"

    ```http
    POST /a2a HTTP/1.1
    Host: partner-agent.example.com
    Content-Type: application/json
    X-Capiscio-Badge: eyJhbGciOiJFZERTQSIsImtpZCI6ImxvY2FsLWRl...
    
    {"jsonrpc": "2.0", "method": "hello"}
    ```

---

## Verify an Inbound Request

=== "Code"

    ```python title="verify_request.py"
    from capiscio_sdk import SimpleGuard
    from capiscio_sdk.errors import VerificationError
    
    guard = SimpleGuard(dev_mode=True)
    
    # Incoming request data
    badge = request.headers.get("X-Capiscio-Badge")
    body = request.body
    
    try:
        claims = guard.verify_inbound(jws=badge, body=body)
        print(f"✓ Valid request from: {claims['iss']}")
        print(f"  Issued at: {claims['iat']}")
        print(f"  Expires: {claims['exp']}")
    except VerificationError as e:
        print(f"✗ Invalid: {e}")
    ```

=== "Valid Request"

    ```
    ✓ Valid request from: partner-agent
      Issued at: 1701432000
      Expires: 1701432060
    ```

=== "Invalid Request"

    ```
    ✗ Invalid: Untrusted key ID: unknown-agent-key
    ```

---

## Complete Example: Both Sides

### Agent A (Sender)

```python title="agent_a.py"
from capiscio_sdk import SimpleGuard
import httpx

# SimpleGuard auto-finds keys in capiscio_keys/ directory
guard = SimpleGuard()

def call_partner(message: str):
    import json
    
    body = {
        "jsonrpc": "2.0",
        "method": "process",
        "params": {"message": message}
    }
    body_bytes = json.dumps(body).encode('utf-8')
    
    # Sign the exact bytes we'll send
    headers = guard.make_headers({}, body=body_bytes)
    headers["Content-Type"] = "application/json"
    
    response = httpx.post(
        "https://agent-b.example.com/a2a",
        data=body_bytes,
        headers=headers
    )
    
    return response.json()
```

### Agent B (Receiver)

```python title="agent_b.py"
from fastapi import FastAPI, Request, HTTPException
from capiscio_sdk import SimpleGuard
from capiscio_sdk.errors import VerificationError

app = FastAPI()

# SimpleGuard auto-finds trust store in capiscio_keys/trusted/
guard = SimpleGuard()

@app.post("/a2a")
async def handle_a2a(request: Request):
    badge = request.headers.get("X-Capiscio-Badge")
    body = await request.body()
    
    # Verify the request
    try:
        claims = guard.verify_inbound(jws=badge, body=body)
    except VerificationError:
        raise HTTPException(401, "Invalid badge")
    
    # Process the request
    data = await request.json()
    return {
        "jsonrpc": "2.0",
        "result": f"Hello from Agent B! Received: {data['params']['message']}",
        "id": data.get("id")
    }
```

---

## Verification Checks

When you call `verify_inbound()`, SimpleGuard checks:

| Check | What it validates | Error if failed |
|-------|-------------------|-----------------|
| **Key ID** | `kid` header exists | `Missing 'kid' in header` |
| **Trust** | Key in trust store | `Untrusted key ID: {kid}` |
| **Signature** | Ed25519 valid | `Invalid signature` |
| **Body Hash** | `bh` matches body | `Integrity check failed` |
| **Not Expired** | `exp` > now | `Token expired` |
| **Not Future** | `iat` <= now | `Token not yet valid` |

---

## Managing the Trust Store

### Add a Trusted Agent

```bash
# Get their public key and save it
curl https://partner.example.com/.well-known/jwks.json \
  | jq '.keys[0]' > capiscio_keys/trusted/partner.jwk
```

### Remove Trust

```bash
rm capiscio_keys/trusted/partner.jwk
```

### List Trusted Keys

```bash
ls capiscio_keys/trusted/
# partner.jwk  another-agent.jwk
```

---

## Development vs Production

| Setting | Dev Mode | Production |
|---------|----------|------------|
| `dev_mode=True` | Auto-generates keys | Requires existing keys |
| Key location | Auto-created | Must exist at paths |
| Self-trust | Enabled | Disabled |
| Use case | Local testing | Real deployments |

```python
# Development - auto-generates keys if missing
guard = SimpleGuard(dev_mode=True)

# Production - uses existing keys in capiscio_keys/
# Run from directory containing capiscio_keys/ and agent-card.json
guard = SimpleGuard()

# Or specify a different base directory
guard = SimpleGuard(base_dir="/etc/capiscio")
```

!!! danger "Never use dev_mode in production"
    Dev mode keys are deterministic and publicly known. Always use real keys in production.

---

## What's Next?

You now understand:

- [x] How to sign outbound requests
- [x] How to verify inbound requests  
- [x] The complete request/response flow
- [x] Managing trusted keys

Let's test everything works!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](2-sdk.md){ .md-button }
[Continue :material-arrow-right:](4-test.md){ .md-button .md-button--primary }
</div>
