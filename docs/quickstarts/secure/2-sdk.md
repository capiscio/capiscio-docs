---
title: "Step 2: Add the SDK"
description: Install and configure the CapiscIO Python SDK
---

# Step 2: Add the SDK

Let's install the CapiscIO Python SDK and set up a basic FastAPI application.

---

## Install the SDK

```bash
pip install capiscio-sdk
```

Verify the installation:

```bash
python -c "import capiscio_sdk; print(capiscio_sdk.__version__)"
```

Expected output:
```
0.2.0
```

---

## Install FastAPI (Optional)

If you don't have a FastAPI app yet, let's create one:

```bash
pip install fastapi uvicorn
```

---

## Create a Basic Agent

Create a new file `main.py`:

```python title="main.py"
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="My A2A Agent")

@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Return the agent card (A2A discovery endpoint)."""
    return {
        "name": "My Secure Agent",
        "description": "An A2A agent with CapiscIO security",
        "url": "http://localhost:8000",
        "version": "1.0.0",
        "protocolVersion": "0.2.0",
        "provider": {
            "organization": "My Company"
        },
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },
        "skills": [
            {
                "id": "greeting",
                "name": "Greeting",
                "description": "Returns a friendly greeting"
            }
        ]
    }

@app.post("/")
async def handle_message(request: Request):
    """Handle incoming A2A messages."""
    body = await request.json()
    
    # Simple echo response
    return JSONResponse({
        "jsonrpc": "2.0",
        "id": body.get("id"),
        "result": {
            "message": f"Hello! You said: {body.get('params', {}).get('message', 'nothing')}"
        }
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Test it:

```bash
python main.py
```

Visit http://localhost:8000/.well-known/agent-card.json to see your agent card.

---

## Add SimpleGuard

Now let's add security! Update `main.py`:

```python title="main.py" hl_lines="2-3 7-8 21-23 28-30"
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from capiscio_sdk import SimpleGuard

app = FastAPI(title="My A2A Agent")

# Initialize SimpleGuard in dev mode (auto-generates keys)
guard = SimpleGuard(dev_mode=True)

@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Return the agent card (A2A discovery endpoint)."""
    return {
        "name": "My Secure Agent",
        "description": "An A2A agent with CapiscIO security",
        "url": "http://localhost:8000",
        "version": "1.0.0",
        "protocolVersion": "0.2.0",
        "provider": {"organization": "My Company"},
        "capabilities": {"streaming": False, "pushNotifications": False},
        "public_keys": [
            # SimpleGuard exposes the public key for the agent card
        ],
        "skills": [
            {
                "id": "greeting",
                "name": "Greeting",
                "description": "Returns a friendly greeting"
            }
        ]
    }

@app.post("/")
async def handle_message(request: Request):
    """Handle incoming A2A messages with signature verification."""
    
    # 1. Get the JWS token from header
    jws_token = request.headers.get("X-Capiscio-JWS")
    if not jws_token:
        raise HTTPException(status_code=401, detail="Missing X-Capiscio-JWS header")
    
    # 2. Get the request body
    body = await request.body()
    
    # 3. Verify the signature
    try:
        claims = guard.verify_inbound(jws_token, body=body)
        print(f"✅ Verified request from: {claims.get('iss')}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Signature verification failed: {e}")
    
    # 4. Process the message
    data = await request.json()
    response_data = {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "message": f"Hello! You said: {data.get('params', {}).get('message', 'nothing')}"
        }
    }
    
    # 5. Sign the response
    response_body = JSONResponse(response_data).body
    response_headers = guard.make_headers({}, body=response_body)
    
    return JSONResponse(response_data, headers=response_headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## What Just Happened?

When you run this code with `dev_mode=True`, SimpleGuard automatically:

1. **Created** `capiscio_keys/` directory
2. **Generated** Ed25519 keypair (`private.pem`, `public.pem`)
3. **Created** `agent-card.json` with your public key
4. **Set up** self-trust in `capiscio_keys/trusted/`

Check your project directory:

```bash
ls -la
```

You should see:

```
.
├── main.py
├── agent-card.json           # Auto-generated
└── capiscio_keys/
    ├── private.pem           # Your private key (keep secret!)
    ├── public.pem            # Your public key
    └── trusted/
        └── local-dev-key.pem # Self-trust for testing
```

---

## Verify the Setup

Check the generated agent card:

```bash
cat agent-card.json
```

You'll see your public key embedded:

```json
{
  "agent_id": "local-dev-agent",
  "public_keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "base64-encoded-public-key",
      "kid": "local-dev-key",
      "use": "sig"
    }
  ],
  "protocolVersion": "0.3.0",
  ...
}
```

---

## What's Next?

You now have:

- [x] CapiscIO SDK installed
- [x] SimpleGuard configured
- [x] Auto-generated keys and agent card

Let's test the security flow!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](1-intro.md){ .md-button }
[Continue :material-arrow-right:](3-guard.md){ .md-button .md-button--primary }
</div>
