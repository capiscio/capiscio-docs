# Sample Files

Download ready-to-use sample files to get started quickly.

---

## Agent Cards

### Basic Agent Card

A minimal, valid agent card with all required fields.

```json title="agent-card.json"
{
  "name": "My First Agent",
  "description": "A helpful AI assistant built with CapiscIO",
  "url": "https://my-agent.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "general-assistant",
      "name": "General Assistant",
      "description": "Answers questions and helps with various tasks",
      "tags": ["general", "assistant"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

[:material-download: Download agent-card.json](assets/samples/agent-card.json){ .md-button .md-button--primary }

---

### Full-Featured Agent Card

A complete agent card with all optional fields, multiple skills, and authentication.

```json title="agent-card-full.json"
{
  "name": "CodeReview Pro",
  "description": "AI-powered code review assistant",
  "url": "https://codereview.example.com",
  "version": "2.1.0",
  "documentationUrl": "https://docs.codereview.example.com",
  "provider": {
    "organization": "DevTools Inc",
    "url": "https://devtools.example.com",
    "contactEmail": "support@devtools.example.com"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "code-review",
      "name": "Code Review",
      "description": "Reviews code for bugs and security issues",
      "tags": ["code", "security"],
      "inputModes": ["text", "file"],
      "outputModes": ["text"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "authentication": {
    "schemes": ["bearer", "oauth2"],
    "credentials": "header"
  }
}
```

[:material-download: Download agent-card-full.json](assets/samples/agent-card-full.json){ .md-button }

---

### Invalid Agent Card (for Testing)

An intentionally invalid card to test validation error messages.

```json title="agent-card-invalid.json"
{
  "name": "",
  "description": "Missing required field: name is empty",
  "url": "not-a-valid-url",
  "version": "1.0.0",
  "capabilities": {
    "streaming": "yes"
  },
  "skills": [],
  "defaultInputModes": ["telepathy"],
  "defaultOutputModes": ["text"]
}
```

[:material-download: Download agent-card-invalid.json](assets/samples/agent-card-invalid.json){ .md-button }

**Expected errors when validating:**

- `name` cannot be empty
- `url` must be a valid HTTPS URL
- `capabilities.streaming` must be boolean (got string)
- `skills` array cannot be empty
- `telepathy` is not a valid input mode

---

## Quick Test

After downloading, validate immediately:

=== "Basic Card"

    ```bash
    capiscio validate agent-card.json
    ```
    
    Expected: **✅ PASSED** with score ~85

=== "Full Card"

    ```bash
    capiscio validate agent-card-full.json
    ```
    
    Expected: **✅ PASSED** with score ~95

=== "Invalid Card"

    ```bash
    capiscio validate agent-card-invalid.json
    ```
    
    Expected: **❌ FAILED** with 5 errors

---

## GitHub Actions Workflow

A ready-to-use CI workflow for validating agent cards:

```yaml title=".github/workflows/validate-agent.yml"
name: Validate Agent Card

on:
  push:
    paths:
      - 'agent-card.json'
      - '.well-known/agent-card.json'
  pull_request:
    paths:
      - 'agent-card.json'
      - '.well-known/agent-card.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Agent Card
        uses: capiscio/validate-a2a@v1
        with:
          path: agent-card.json
          strict: true
          fail-on-warning: false
```

[:material-download: Download validate-agent.yml](assets/samples/validate-agent.yml){ .md-button }

---

## Python Integration

A complete FastAPI example with security:

```python title="secure_agent.py"
"""
Secure A2A Agent with CapiscIO
Run: uvicorn secure_agent:app --reload
"""

from fastapi import FastAPI, Request, HTTPException
from capiscio_sdk import SimpleGuard
from capiscio_sdk.errors import VerificationError

app = FastAPI(title="Secure A2A Agent")

# Initialize security (use dev_mode=False in production)
guard = SimpleGuard(dev_mode=True)

@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Serve the agent card."""
    return {
        "name": "My Secure Agent",
        "description": "A CapiscIO-secured A2A agent",
        "url": "https://my-agent.example.com",
        "version": "1.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [{
            "id": "echo",
            "name": "Echo",
            "description": "Echoes back your message"
        }],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"]
    }

@app.post("/a2a")
async def handle_a2a(request: Request):
    """Handle A2A requests with signature verification."""
    signature = request.headers.get("X-Capiscio-Signature")
    body = await request.body()
    
    # Verify signature if present
    if signature:
        try:
            claims = guard.verify_inbound(signature, body)
            print(f"Verified request from: {claims.get('iss')}")
        except VerificationError:
            raise HTTPException(401, "Invalid signature")
    
    # Process request
    data = await request.json()
    
    # Sign response
    response = {
        "jsonrpc": "2.0",
        "result": {"echo": data.get("params", {}).get("message", "Hello!")},
        "id": data.get("id")
    }
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

[:material-download: Download secure_agent.py](assets/samples/secure_agent.py){ .md-button }

---

## See Also

- [Quickstart: Validate Your First Agent](quickstarts/validate/1-intro.md)
- [Quickstart: Secure Your Agent](quickstarts/secure/1-intro.md)
- [Agent Card Schema Reference](reference/agent-card-schema.md)
