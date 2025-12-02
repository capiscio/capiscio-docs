---
title: Verify Inbound Requests
description: Validate JWS signatures on incoming A2A requests
---

# Verify Inbound Requests

Validate that incoming requests are from trusted agents with valid signatures.

---

## Problem

When receiving A2A requests, you need to:

- Verify the JWS signature is valid
- Confirm the sender is who they claim to be
- Reject tampered or forged requests
- Ensure message integrity

---

## Solution: SimpleGuard

```python
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError

guard = SimpleGuard(dev_mode=True)

def handle_request(request):
    # Get the JWS from header
    jws = request.headers.get("X-Capiscio-JWS")
    body = request.body
    
    try:
        # Verify the signature
        payload = guard.verify_inbound(jws, body=body)
        
        # Signature valid! payload contains claims
        print(f"Request from: {payload['iss']}")
        
        # Process the request...
        
    except VerificationError as e:
        # Invalid signature - reject request
        return {"error": "Invalid signature", "detail": str(e)}, 401
```

---

## What verify_inbound Returns

On success, `verify_inbound` returns the decoded JWT payload:

```python
payload = guard.verify_inbound(jws, body=body)

# Returns dict like:
{
    "iss": "calling-agent-id",      # Who sent the request (auto-injected)
    "iat": 1704067200,              # Issued at timestamp (auto-injected)
    "exp": 1704070800,              # Expiration timestamp (auto-injected)
    "bh": "abc123..."               # Body hash for integrity (if body provided)
}
```

---

## FastAPI Integration

Use the middleware for automatic verification:

```python
from fastapi import FastAPI, Request
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.integrations.fastapi import CapiscioMiddleware

app = FastAPI()
guard = SimpleGuard(dev_mode=True)

# Add middleware - all routes automatically verified
app.add_middleware(CapiscioMiddleware, guard=guard)

@app.post("/a2a")
async def handle_a2a(request: Request):
    # Request is already verified when it reaches here
    # The verified claims are available in request.state
    caller = request.state.capiscio_claims["iss"]
    return {"message": f"Hello {caller}!"}
```

---

## Manual Verification Pattern

For custom frameworks:

```python
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError

guard = SimpleGuard(dev_mode=True)

class A2AHandler:
    def handle(self, headers: dict, body: bytes):
        # 1. Extract JWS header
        jws = headers.get("X-Capiscio-JWS")
        if not jws:
            raise ValueError("Missing X-Capiscio-JWS header")
        
        # 2. Verify signature
        try:
            claims = guard.verify_inbound(jws, body=body)
        except VerificationError:
            raise PermissionError("Invalid signature")
        
        # 3. Check expiration (SimpleGuard does this automatically)
        # But you can add extra checks if needed
        
        # 4. Optional: Check issuer is in allowlist
        allowed_issuers = {"trusted-agent-1", "trusted-agent-2"}
        if claims["iss"] not in allowed_issuers:
            raise PermissionError(f"Issuer {claims['iss']} not trusted")
        
        # 5. Verified! Process request
        return self.process(body, claims)
```

---

## Trust Store Setup

For production, configure which agents to trust via the file system:

```python
from capiscio_sdk.simple_guard import SimpleGuard

# SimpleGuard auto-finds capiscio_keys/trusted/ in project root
guard = SimpleGuard()  # dev_mode=False is default
```

**Expected structure:**
```
your-project/
├── agent-card.json
└── capiscio_keys/
    ├── private.pem
    ├── public.pem
    └── trusted/          # Trust store directory
        ├── agent-1.pem   # Filename must match key's 'kid'
        └── agent-2.pem
```

To trust an agent, add their public key to `capiscio_keys/trusted/` with the filename matching their key ID (kid).

---

## Error Handling

Handle different verification failures:

```python
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError, ConfigurationError

guard = SimpleGuard(dev_mode=True)

def verify_request(jws: str, body: bytes):
    try:
        return guard.verify_inbound(jws, body=body)
        
    except VerificationError as e:
        # Signature invalid, key untrusted, token expired, etc.
        log.warning(f"Verification failed: {e}")
        return None, 401, "Verification failed"
        
    except ConfigurationError as e:
        # Guard misconfigured (missing keys, etc.)
        log.error(f"Configuration error: {e}")
        return None, 500, "Internal error"
        
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return None, 500, "Internal error"
```

---

## Testing Verification

```python
import pytest
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError

def test_verify_valid_signature():
    guard = SimpleGuard(dev_mode=True)
    
    # Create a valid signed request
    body = b'{"message": "test"}'
    payload = {"sub": "test-request"}  # iss auto-injected
    jws = guard.sign_outbound(payload, body=body)
    
    # Verify it
    claims = guard.verify_inbound(jws, body=body)
    
    assert "iss" in claims
    assert "iat" in claims
    assert "exp" in claims

def test_verify_tampered_body():
    guard = SimpleGuard(dev_mode=True)
    
    body = b'{"message": "original"}'
    payload = {}
    jws = guard.sign_outbound(payload, body=body)
    
    # Tamper with body
    tampered = b'{"message": "tampered"}'
    
    with pytest.raises(VerificationError):
        guard.verify_inbound(jws, body=tampered)
```

---

## See Also

- [Sign Outbound Requests](sign-outbound.md) — The sending side
- [Trust Store Setup](trust-store.md) — Configure trusted agents
- [FastAPI Middleware](../integrations/fastapi.md) — Full integration
