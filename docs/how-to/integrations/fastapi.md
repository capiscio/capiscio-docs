---
title: FastAPI Integration
description: Add CapiscIO security to FastAPI applications
---

# FastAPI Integration

Add cryptographic security to your FastAPI A2A agent in under 5 minutes.

---

## Problem

You have a FastAPI application that serves as an A2A agent and you want to:

- Verify incoming requests have valid signatures
- Sign outgoing requests to other agents
- Meet production security requirements
- Do it with minimal code changes

---

## Solution: Middleware

```python
from fastapi import FastAPI
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.integrations.fastapi import CapiscioMiddleware

app = FastAPI()

# Initialize guard
guard = SimpleGuard(dev_mode=True)

# Add middleware - automatic verification for all requests
app.add_middleware(CapiscioMiddleware, guard=guard)

@app.post("/a2a")
async def handle_a2a(request):
    # Requests are automatically verified
    return {"status": "ok"}
```

That's it! All requests are now cryptographically verified.

---

## Access Verified Claims

Get information about the verified caller:

```python
from fastapi import FastAPI, Request

app = FastAPI()
app.add_middleware(CapiscioMiddleware, guard=SimpleGuard(dev_mode=True))

@app.post("/a2a")
async def handle_a2a(request: Request):
    # Access verified claims
    agent = request.state.agent       # Full payload dict with claims
    agent_id = request.state.agent_id # Shortcut to issuer (iss claim)
    
    return {"message": f"Hello {agent_id}!"}
```

---

## Exclude Routes

Some routes shouldn't require signatures (health checks, public endpoints):

```python
from capiscio_sdk.integrations.fastapi import CapiscioMiddleware

app.add_middleware(
    CapiscioMiddleware,
    guard=guard,
    exclude_paths=[
        "/health",
        "/ready",
        "/.well-known/agent-card.json",  # Agent card is public
    ]
)
```

---

## Full Example

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.integrations.fastapi import CapiscioMiddleware
from capiscio_sdk.errors import VerificationError
import json

app = FastAPI(title="My A2A Agent")

# Setup guard
guard = SimpleGuard(dev_mode=True)

# Add middleware with exclusions
app.add_middleware(
    CapiscioMiddleware,
    guard=guard,
    exclude_paths=["/health", "/.well-known/agent-card.json"]
)

# Agent card endpoint (public, no signature required)
@app.get("/.well-known/agent-card.json")
async def agent_card():
    return {
        "name": "My Agent",
        "version": "1.0.0",
        "url": "https://my-agent.example.com/a2a",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },
        "skills": [{
            "id": "qa",
            "name": "Q&A",
            "description": "Answer questions"
        }]
    }

# Health check (public)
@app.get("/health")
async def health():
    return {"status": "healthy"}

# A2A endpoint (protected)
@app.post("/a2a")
async def handle_a2a(request: Request):
    agent_id = request.state.agent_id  # Issuer from verified claims
    body = await request.json()
    
    # Log the caller
    print(f"Request from: {agent_id}")
    
    # Process the A2A request
    return {
        "jsonrpc": "2.0",
        "result": {
            "message": {
                "role": "assistant",
                "parts": [{"text": "Hello! How can I help?"}]
            }
        },
        "id": body.get("id")
    }

# Error handler
@app.exception_handler(VerificationError)
async def signature_error_handler(request, exc):
    return JSONResponse(
        status_code=401,
        content={"error": "Invalid signature", "detail": str(exc)}
    )
```

---

## Making Outbound Calls

Use the guard to sign requests to other agents:

```python
import httpx
from fastapi import Request

@app.post("/query-weather")
async def query_weather(request: Request):
    # Create outbound request
    weather_agent_url = "https://weather-agent.example.com/a2a"
    request_body = json.dumps({
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "params": {"message": {"role": "user", "parts": [{"text": "Weather in Paris?"}]}},
        "id": "req-001"
    })
    
    # Sign the request
    headers = guard.make_headers(
        payload={"iss": "my-agent", "sub": "weather-agent"},
        body=request_body
    )
    
    # Send signed request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            weather_agent_url,
            headers=headers,
            content=request_body
        )
    
    return response.json()
```

---

## Production Configuration

For production, disable dev_mode. SimpleGuard finds keys via convention:

```python
import os
from capiscio_sdk.simple_guard import SimpleGuard

# SimpleGuard looks for capiscio_keys/ in project root (walks up directory tree)
guard = SimpleGuard()  # dev_mode=False is default

# Or specify a different base directory
guard = SimpleGuard(base_dir=os.environ.get("CAPISCIO_BASE_DIR", "."))
```

**Expected structure:**
```
your-project/
├── agent-card.json
└── capiscio_keys/
    ├── private.pem
    ├── public.pem
    └── trusted/
        └── {kid}.pem
```

---

## Testing

Test your integration with these examples:

=== "curl (No Signature)"

    ```bash
    curl -X POST http://localhost:8000/a2a \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","method":"tasks/send","id":"test-1"}'
    ```

    ```json
    {
      "error": "Invalid badge",
      "detail": "Missing X-Capiscio-Badge header"
    }
    ```

=== "curl (With Badge)"

    ```bash
    # Generate badge headers using SimpleGuard
    BADGE=$(capiscio badge issue --self-sign)
    
    curl -X POST http://localhost:8000/a2a \
      -H "Content-Type: application/json" \
      -H "X-Capiscio-Badge: $BADGE" \
      -d '{"jsonrpc":"2.0","method":"tasks/send","id":"test-1"}'
    ```

    ```json
    {
      "jsonrpc": "2.0",
      "result": {
        "message": {
          "role": "assistant",
          "parts": [{"text": "Hello! How can I help?"}]
        }
      },
      "id": "test-1"
    }
    ```

=== "Python (pytest)"

    ```python
    import pytest
    from fastapi.testclient import TestClient
    
    def test_protected_endpoint_without_signature():
        client = TestClient(app)
        response = client.post("/a2a", json={"test": "data"})
        assert response.status_code == 401

    def test_protected_endpoint_with_signature():
        client = TestClient(app)
        
        # Sign the request
        body = '{"test": "data"}'
        headers = guard.make_headers({"iss": "test-agent"}, body)
        
        response = client.post("/a2a", content=body, headers=headers)
        assert response.status_code == 200

    def test_excluded_path_no_signature_needed():
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
    ```

---

## See Also

- [Flask Integration](flask.md) — Flask equivalent
- [Security Guide](../../getting-started/secure/1-intro.md) — Full walkthrough
- [Sign Outbound Requests](../security/sign-outbound.md) — Signing details
