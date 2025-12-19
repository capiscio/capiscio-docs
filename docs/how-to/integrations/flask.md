---
title: Flask Integration
description: Add CapiscIO security to Flask applications
---

# Flask Integration

Protect your Flask-based A2A agent with request signing and verification.

---

## Problem

You have a Flask application serving as an A2A agent and need to:

- Verify incoming request signatures
- Sign outgoing responses
- Handle unauthorized requests gracefully
- Integrate with Flask's request lifecycle

---

## Solution: Flask Middleware

```python
from flask import Flask, request, jsonify, g
from functools import wraps
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError

app = Flask(__name__)

# SimpleGuard uses convention - finds keys in capiscio_keys/
guard = SimpleGuard(dev_mode=True)  # Use dev_mode=False in production

def require_signature(f):
    """Decorator to verify incoming request signatures."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the JWS from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        jws_token = auth_header[7:]  # Remove "Bearer " prefix
        
        try:
            # Verify the signature
            claims = guard.verify_inbound(jws_token, body=request.get_data())
            # Store claims for route handler
            g.verified_claims = claims
        except VerificationError as e:
            return jsonify({"error": f"Signature verification failed: {e}"}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route("/a2a/tasks", methods=["POST"])
@require_signature
def handle_task():
    """Process an A2A task request."""
    # Access verified claims
    issuer = g.verified_claims.get("iss", "unknown")
    
    # Process the task
    task = request.get_json()
    result = {"status": "completed", "verified_from": issuer}
    
    # Sign the response
    response_body = jsonify(result).get_data()
    signature = guard.sign_outbound({}, body=response_body)
    
    response = app.make_response(jsonify(result))
    response.headers["X-A2A-Signature"] = signature
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

---

## Step-by-Step Setup

### Step 1: Install Dependencies

```bash
pip install flask capiscio-sdk
```

### Step 2: Generate Keys

```bash
pip install capiscio
capiscio key gen --out capiscio_keys/
mkdir -p capiscio_keys/trusted/
```

### Step 3: Create the Application

Create `app.py`:

```python
from flask import Flask, request, jsonify, g
from functools import wraps
from capiscio_sdk.simple_guard import SimpleGuard
import os

app = Flask(__name__)

# Configure based on environment
DEV_MODE = os.environ.get("CAPISCIO_DEV_MODE", "false").lower() == "true"

# SimpleGuard uses convention - keys in capiscio_keys/ relative to cwd
guard = SimpleGuard(dev_mode=DEV_MODE)

def require_signature(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        jws_token = auth_header[7:]
        
        try:
            claims = guard.verify_inbound(jws_token, body=request.get_data())
            g.verified_claims = claims
        except Exception as e:
            return jsonify({"error": f"Signature verification failed: {e}"}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route("/a2a/tasks", methods=["POST"])
@require_signature
def handle_task():
    issuer = g.verified_claims.get("iss", "unknown")
    task = request.get_json()
    
    result = {
        "status": "completed",
        "task_id": task.get("id"),
        "verified_from": issuer
    }
    
    response_body = jsonify(result).get_data()
    signature = guard.sign_outbound({}, body=response_body)
    
    response = app.make_response(jsonify(result))
    response.headers["X-A2A-Signature"] = signature
    return response

@app.route("/.well-known/agent-card.json")
def agent_card():
    """Serve your agent card (no signature required)."""
    # Load from agent-card.json file (created by SimpleGuard in dev_mode)
    import json
    with open("agent-card.json") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

### Step 4: Run the Application

```bash
# Development (skip signature verification)
CAPISCIO_DEV_MODE=true python app.py

# Production
python app.py
```

---

## Blueprint Pattern

For larger applications, use a Blueprint:

```python
# security.py
from flask import Blueprint, request, g, current_app
from functools import wraps
from capiscio_sdk.simple_guard import SimpleGuard
from capiscio_sdk.errors import VerificationError

security_bp = Blueprint("security", __name__)
guard = None

def init_guard(app):
    """Initialize SimpleGuard from app config."""
    global guard
    dev_mode = app.config.get("CAPISCIO_DEV_MODE", False)
    base_dir = app.config.get("CAPISCIO_BASE_DIR", None)
    guard = SimpleGuard(base_dir=base_dir, dev_mode=dev_mode)

def require_signature(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if guard is None:
            raise RuntimeError("SimpleGuard not initialized")
        
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return {"error": "Missing Authorization"}, 401
        
        try:
            claims = guard.verify_inbound(auth_header[7:], body=request.get_data())
            g.verified_claims = claims
        except VerificationError as e:
            return {"error": str(e)}, 401
        
        return f(*args, **kwargs)
    return decorated
```

```python
# app.py
from flask import Flask
from security import security_bp, init_guard

app = Flask(__name__)
app.config.update(
    CAPISCIO_BASE_DIR=".",  # Or path to directory with capiscio_keys/
    CAPISCIO_DEV_MODE=False
)

init_guard(app)
app.register_blueprint(security_bp)
```

---

## Error Handling

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": -32001,
            "message": "Unauthorized: Invalid or missing signature"
        },
        "id": None
    }), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": -32002,
            "message": "Forbidden: Key not in trust store"
        },
        "id": None
    }), 403
```

---

## Testing

```python
# test_app.py
import pytest
from app import app, guard

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_missing_auth(client):
    """Test request without Authorization header."""
    response = client.post("/a2a/tasks", json={"id": "test"})
    assert response.status_code == 401

def test_invalid_signature(client):
    """Test request with invalid signature."""
    response = client.post(
        "/a2a/tasks",
        json={"id": "test"},
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401

def test_valid_signature(client):
    """Test request with valid signature."""
    body = b'{"id": "test"}'
    signature = guard.sign_outbound({}, body=body)
    
    response = client.post(
        "/a2a/tasks",
        data=body,
        content_type="application/json",
        headers={"Authorization": f"Bearer {signature}"}
    )
    # Will pass if your own key is in trust store (testing scenario)
```

---

## Production Deployment

### With Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### With Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Don't include private keys in image!
# Mount them at runtime

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

```bash
docker run -v $(pwd)/capiscio_keys:/app/capiscio_keys myagent:latest
```

---

## See Also

- [FastAPI Integration](fastapi.md) — Similar pattern for FastAPI
- [Sign Outbound Requests](../security/sign-outbound.md) — Signing details
- [Verify Inbound Requests](../security/verify-inbound.md) — Verification details
