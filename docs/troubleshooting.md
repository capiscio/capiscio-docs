---
title: Troubleshooting
description: Solutions to common CapiscIO issues
---

# Troubleshooting

Quick solutions to common problems.

---

## Validation Issues

### "Invalid agent card schema"

**Problem:** Your agent card doesn't match the A2A schema.

**Solution:**

Run schema-only validation to see specific errors:

=== "Command"

    ```bash
    capiscio validate agent-card.json --schema-only --json | jq '.errors'
    ```

=== "Output"

    ```json
    [
      {
        "code": "MISSING_REQUIRED_FIELD",
        "path": "$.capabilities",
        "message": "Missing required field 'capabilities'"
      },
      {
        "code": "INVALID_TYPE",
        "path": "$.skills",
        "message": "Expected array, got object"
      }
    ]
    ```

Common fixes:

- Add missing required fields (`name`, `url`, `skills`, `capabilities`)
- Ensure `skills` is an array, not an object
- Use valid URL format (include `https://`)

---

### "Connection refused" or "Timeout"

**Problem:** Can't reach the agent endpoint.

**Solution:**

1. Verify the URL is correct:
   ```bash
   curl -v https://your-agent.example.com/.well-known/agent-card.json
   ```

2. Increase timeout for slow endpoints:
   ```bash
   capiscio validate $URL --timeout 30
   ```

3. Check if endpoint requires authentication

4. Verify firewall/network settings

---

### "--test-live fails but schema is valid"

**Problem:** Static validation passes but live testing fails.

**Solution:**

1. The agent URL in the card must be reachable:
   ```json
   {
     "url": "https://actually-reachable.example.com"
   }
   ```

2. Check if your agent is running:
   ```bash
   curl -I https://your-agent.example.com/health
   ```

3. For local development, use `--schema-only`:
   ```bash
   capiscio validate agent-card.json --schema-only
   ```

---

### "Score too low"

**Problem:** Validation passes but score is below threshold.

**Solution:**

Check what's lowering your score:

=== "Command"

    ```bash
    capiscio validate agent-card.json --json | jq '.scoringResult'
    ```

=== "Output"

    ```json
    {
      "complianceScore": 65,
      "trustScore": 0,
      "availabilityScore": null,
      "productionReady": false,
      "breakdown": {
        "missingDescription": -10,
        "httpNotHttps": -15,
        "missingAuth": -10
      }
    }
    ```

Common fixes:

| Issue | Impact | Fix |
|-------|--------|-----|
| Missing description | -10 | Add `description` field |
| Missing documentation URL | -5 | Add `documentationUrl` |
| No authentication info | -10 | Add `authentication` section |
| HTTP URL (not HTTPS) | -15 | Use HTTPS |
| Missing skill descriptions | -5 each | Add `description` to each skill |

---

## Security Issues

### "Key not found"

**Problem:** SimpleGuard can't find your private key.

**Solution:**

1. Check directory structure (SimpleGuard uses convention):
   ```
   your-project/
   ├── agent-card.json      # Required
   └── capiscio_keys/
       ├── private.pem      # Required for signing
       ├── public.pem       # Required
       └── trusted/         # Required for verification
   ```

2. Generate keys if missing:
   ```bash
   capiscio key gen --out capiscio_keys/
   ```

3. Or use dev mode to auto-generate:
   ```python
   guard = SimpleGuard(dev_mode=True)  # Auto-generates everything
   ```

4. Or specify a different base directory:
   ```python
   guard = SimpleGuard(base_dir="/path/to/config")
   ```

---

### "Signature verification failed"

**Problem:** Incoming request signature doesn't verify.

**Solution:**

Debug the verification process:

=== "Check Token"

    ```python
    # Extract and decode the JWS header
    import base64, json
    
    auth_header = request.headers.get("Authorization", "")
    jws_token = auth_header.replace("Bearer ", "")
    
    # Decode header (first part of JWS)
    header = jws_token.split('.')[0]
    decoded = json.loads(base64.urlsafe_b64decode(header + '=='))
    print(decoded)
    ```

    ```json
    {
      "alg": "EdDSA",
      "kid": "partner-key-2025",
      "typ": "JWT"
    }
    ```

=== "Verify Trust Store"

    ```bash
    # Check if the kid exists in your trust store
    ls capiscio_keys/trusted/
    ```

    ```
    partner-key-2025.pem  ← Must match the kid
    acme-agent.pem
    ```

=== "Enable Debug Mode"

    ```python
    from capiscio_sdk.simple_guard import SimpleGuard
    from capiscio_sdk.errors import VerificationError
    import logging
    
    # Enable logging to see detailed errors
    logging.basicConfig(level=logging.DEBUG)
    
    guard = SimpleGuard(dev_mode=True)
    
    try:
        claims = guard.verify_inbound(jws_token, body=body)
    except VerificationError as e:
        print(f"Verification failed: {e}")
    ```
    ```

Common causes:

- Request body was modified after signing
- Key ID (kid) not in trust store
- Clock skew (signature expired)
- Wrong key type (expecting Ed25519, got RSA)

---

### "Invalid JWS format"

**Problem:** The signature header isn't a valid JWS.

**Solution:**

1. Check the Authorization header format:
   ```
   Authorization: Bearer eyJ...  ← Must be "Bearer " + JWS token
   ```

2. Ensure you're extracting the token correctly:
   ```python
   auth_header = request.headers.get("Authorization", "")
   if auth_header.startswith("Bearer "):
       jws_token = auth_header[7:]  # Skip "Bearer "
   ```

3. Verify the sender is signing correctly:
   ```python
   # Sender should use:
   signature = guard.sign_outbound({}, body=body_bytes)
   headers = {"Authorization": f"Bearer {signature}"}
   ```

---

### "Key ID not found in trust store"

**Problem:** The `kid` in the JWS doesn't match any trusted key.

**Solution:**

1. Get the sender's `kid`:
   ```python
   import base64, json
   header = jws_token.split('.')[0]
   decoded = json.loads(base64.urlsafe_b64decode(header + '=='))
   print(decoded['kid'])
   ```

2. Add their key with matching filename:
   ```bash
   # If kid is "partner-key-2025"
   cp partner-public.pem capiscio_keys/trusted/partner-key-2025.pem
   ```

---

## Installation Issues

### "Command not found: capiscio"

**Problem:** CLI not in PATH after installation.

**Solution:**

=== "npm"
    ```bash
    # Option 1: Use npx
    npx capiscio validate agent-card.json
    
    # Option 2: Global install
    npm install -g capiscio
    
    # Option 3: Add to PATH
    export PATH="./node_modules/.bin:$PATH"
    ```

=== "pip"
    ```bash
    # Option 1: Use python -m
    python -m capiscio validate agent-card.json
    
    # Option 2: Add local bin to PATH
    export PATH="$HOME/.local/bin:$PATH"
    
    # Option 3: Reinstall with --user
    pip install --user capiscio
    ```

---

### "Module not found: capiscio_sdk"

**Problem:** SDK not installed correctly.

**Solution:**

```bash
# Install the SDK (not the CLI)
pip install capiscio-sdk

# Verify installation
python -c "from capiscio_sdk.simple_guard import SimpleGuard; print('OK')"
```

Note: `capiscio` is the CLI, `capiscio-sdk` is the Python SDK.

---

### "Binary not found" (Go core)

**Problem:** The Go binary isn't accessible.

!!! info "Automatic Download (Python SDK)"
    As of SDK v2.4.1+, the Python SDK **automatically downloads** the capiscio-core binary if not found. No manual installation needed!

**Solution for manual installation:**

```bash
# Verify Go binary exists
which capiscio-core

# Or download directly
curl -L https://github.com/capiscio/capiscio-core/releases/latest/download/capiscio-$(uname -s)-$(uname -m) -o /usr/local/bin/capiscio
chmod +x /usr/local/bin/capiscio
```

**Custom binary location:**
```bash
# Override automatic detection
export CAPISCIO_BINARY=/path/to/capiscio-core
```

---

## CI/CD Issues

### "Action fails with permission denied"

**Problem:** GitHub Action can't execute.

**Solution:**

```yaml
- uses: capiscio/validate-a2a@v1
  with:
    path: agent-card.json
# No special permissions needed for basic validation
```

If accessing private repos:
```yaml
permissions:
  contents: read
```

---

### "Validation passes locally but fails in CI"

**Problem:** Environment differences between local and CI.

**Solution:**

1. Check network access:
   ```yaml
   - name: Debug
     run: curl -v ${{ inputs.url }}
   ```

2. Use same CLI version:
   ```yaml
   - name: Install specific version
     run: npm install capiscio@1.0.2
   ```

3. Set timeout for CI networks:
   ```yaml
   - uses: capiscio/validate-a2a@v1
     with:
       timeout: 30
   ```

---

### "PR comment not appearing"

**Problem:** Bot can't comment on PR.

**Solution:**

Add permissions:
```yaml
permissions:
  pull-requests: write
```

---

## Still Stuck?

<div class="grid cards" markdown>

-   :material-github:{ .lg .middle } **GitHub Issues**

    ---

    Search existing issues or open a new one.

    [:octicons-arrow-right-24: Open Issue](https://github.com/capiscio/capiscio-docs/issues)

-   :material-chat:{ .lg .middle } **Community**

    ---

    Ask the community for help.

    [:octicons-arrow-right-24: Discussions](https://github.com/orgs/capiscio/discussions)

</div>
