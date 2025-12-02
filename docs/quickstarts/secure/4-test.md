---
title: "Step 4: Test Enforcement"
description: Test that your security is working correctly
---

# Step 4: Test Enforcement

Let's test that SimpleGuard is actually protecting your agent. We'll send both valid and invalid requests to see the security in action.

---

## Start Your Agent

Make sure your agent is running:

```bash
python main.py
```

You should see:

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Create a Test Client

Create a new file `test_client.py`:

```python title="test_client.py"
import httpx
import json
from capiscio_sdk import SimpleGuard

# Initialize SimpleGuard (will use the same keys as our server)
guard = SimpleGuard(dev_mode=True)

def test_authenticated_request():
    """Send a properly signed request."""
    print("\n" + "="*50)
    print("TEST 1: Authenticated Request")
    print("="*50)
    
    # Prepare the request body
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": "test-1",
        "method": "greeting",
        "params": {"message": "Hello from authenticated client!"}
    }).encode()
    
    # Sign the request
    headers = guard.make_headers({}, body=body)
    headers["Content-Type"] = "application/json"
    
    print(f"📤 Sending signed request...")
    print(f"   JWS Token: {headers['X-Capiscio-JWS'][:50]}...")
    
    # Send it
    response = httpx.post(
        "http://localhost:8000/",
        content=body,
        headers=headers
    )
    
    print(f"📥 Response Status: {response.status_code}")
    print(f"   Response Body: {response.json()}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Authenticated request accepted!")
    else:
        print("❌ FAILED: Request rejected")

def test_unauthenticated_request():
    """Send a request without a signature."""
    print("\n" + "="*50)
    print("TEST 2: Unauthenticated Request (No JWS)")
    print("="*50)
    
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": "test-2",
        "method": "greeting",
        "params": {"message": "Hello without auth!"}
    }).encode()
    
    print(f"📤 Sending unsigned request...")
    
    response = httpx.post(
        "http://localhost:8000/",
        content=body,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"📥 Response Status: {response.status_code}")
    print(f"   Response Body: {response.json()}")
    
    if response.status_code == 401:
        print("✅ SUCCESS: Unauthenticated request correctly rejected!")
    else:
        print("❌ FAILED: Request should have been rejected")

def test_tampered_request():
    """Send a request with a valid signature but tampered body."""
    print("\n" + "="*50)
    print("TEST 3: Tampered Request (Modified Body)")
    print("="*50)
    
    # Original body
    original_body = json.dumps({
        "jsonrpc": "2.0",
        "id": "test-3",
        "method": "greeting",
        "params": {"message": "Original message"}
    }).encode()
    
    # Sign the original
    headers = guard.make_headers({}, body=original_body)
    headers["Content-Type"] = "application/json"
    
    # But send a DIFFERENT body (simulating tampering)
    tampered_body = json.dumps({
        "jsonrpc": "2.0",
        "id": "test-3",
        "method": "greeting",
        "params": {"message": "TAMPERED message!"}
    }).encode()
    
    print(f"📤 Sending tampered request...")
    print(f"   Original body hash was signed")
    print(f"   But sending different body")
    
    response = httpx.post(
        "http://localhost:8000/",
        content=tampered_body,
        headers=headers
    )
    
    print(f"📥 Response Status: {response.status_code}")
    print(f"   Response Body: {response.json()}")
    
    if response.status_code == 401:
        print("✅ SUCCESS: Tampered request correctly rejected!")
    else:
        print("❌ FAILED: Tampered request should have been rejected")

def test_untrusted_key():
    """Send a request signed with an unknown key."""
    print("\n" + "="*50)
    print("TEST 4: Untrusted Key")
    print("="*50)
    
    # Create a NEW guard with different keys
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a guard in a different directory (different keys)
        untrusted_guard = SimpleGuard(base_dir=tmpdir, dev_mode=True)
        
        body = json.dumps({
            "jsonrpc": "2.0",
            "id": "test-4",
            "method": "greeting",
            "params": {"message": "Hello from stranger!"}
        }).encode()
        
        headers = untrusted_guard.make_headers({}, body=body)
        headers["Content-Type"] = "application/json"
        
        print(f"📤 Sending request signed with unknown key...")
        
        response = httpx.post(
            "http://localhost:8000/",
            content=body,
            headers=headers
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"   Response Body: {response.json()}")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Untrusted key correctly rejected!")
        else:
            print("❌ FAILED: Untrusted key should have been rejected")

if __name__ == "__main__":
    print("🔐 CapiscIO Security Test Suite")
    print("================================")
    
    test_authenticated_request()
    test_unauthenticated_request()
    test_tampered_request()
    test_untrusted_key()
    
    print("\n" + "="*50)
    print("All tests completed!")
    print("="*50)
```

---

## Run the Tests

With your agent running in one terminal, open another and run:

```bash
python test_client.py
```

You should see:

```
🔐 CapiscIO Security Test Suite
================================

==================================================
TEST 1: Authenticated Request
==================================================
📤 Sending signed request...
   JWS Token: eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCIsImtpZCI6...
📥 Response Status: 200
   Response Body: {'jsonrpc': '2.0', 'id': 'test-1', 'result': {'message': 'Hello! You said: Hello from authenticated client!'}}
✅ SUCCESS: Authenticated request accepted!

==================================================
TEST 2: Unauthenticated Request (No JWS)
==================================================
📤 Sending unsigned request...
📥 Response Status: 401
   Response Body: {'detail': 'Missing X-Capiscio-JWS header'}
✅ SUCCESS: Unauthenticated request correctly rejected!

==================================================
TEST 3: Tampered Request (Modified Body)
==================================================
📤 Sending tampered request...
   Original body hash was signed
   But sending different body
📥 Response Status: 401
   Response Body: {'detail': 'Signature verification failed: Integrity Check Failed: Body modified'}
✅ SUCCESS: Tampered request correctly rejected!

==================================================
TEST 4: Untrusted Key
==================================================
📤 Sending request signed with unknown key...
📥 Response Status: 401
   Response Body: {'detail': 'Signature verification failed: Untrusted key ID: local-dev-key'}
✅ SUCCESS: Untrusted key correctly rejected!

==================================================
All tests completed!
==================================================
```

---

## Understanding the Results

| Test | What It Proves |
|------|----------------|
| **Test 1** | Valid signatures are accepted |
| **Test 2** | Missing signatures are rejected (Identity) |
| **Test 3** | Tampered bodies are detected (Integrity) |
| **Test 4** | Unknown keys are rejected (Trust) |

---

## Check Server Logs

Look at your server terminal. You should see:

```
✅ Verified request from: local-dev-agent
INFO:     127.0.0.1:xxxxx - "POST / HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST / HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:xxxxx - "POST / HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:xxxxx - "POST / HTTP/1.1" 401 Unauthorized
```

And JSON logs from SimpleGuard:

```json
{"event": "agent_call_allowed", "iss": "local-dev-agent", "kid": "local-dev-key"}
{"event": "agent_call_denied", "kid": "unknown-key", "reason": "untrusted_key"}
```

---

## Testing with cURL

You can also test manually with cURL, but you'll need to generate the JWS token:

```python
# Generate a token to use with cURL
from capiscio_sdk import SimpleGuard
guard = SimpleGuard(dev_mode=True)

body = b'{"jsonrpc":"2.0","id":"curl-test","method":"greeting","params":{}}'
headers = guard.make_headers({}, body=body)
print(f"Token: {headers['X-Capiscio-JWS']}")
```

Then use it:

```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "X-Capiscio-JWS: <paste-token-here>" \
  -d '{"jsonrpc":"2.0","id":"curl-test","method":"greeting","params":{}}'
```

---

## What's Next?

You've verified that SimpleGuard:

- [x] Accepts valid signed requests
- [x] Rejects unsigned requests
- [x] Detects body tampering
- [x] Rejects untrusted keys

Let's learn how to deploy this to production!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](3-guard.md){ .md-button }
[Continue :material-arrow-right:](5-production.md){ .md-button .md-button--primary }
</div>
