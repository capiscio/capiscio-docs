---
title: Custom Timeout
description: Handle slow endpoints with custom timeout settings
---

# Custom Timeout

Adjust timeout settings for slow or distant endpoints.

---

## Problem

The default timeout (10 seconds) isn't enough when:

- Testing endpoints behind slow networks
- Validating agents with cold starts (serverless)
- Running against distant geographic regions
- Testing agents under load

---

## Solution

=== "npm"

    ```bash
    # Timeout in milliseconds
    npx capiscio validate ./agent-card.json --timeout 30000
    ```

=== "pip"

    ```bash
    # Timeout in milliseconds
    capiscio validate ./agent-card.json --timeout 30000
    ```

=== "Go"

    ```bash
    # Timeout in milliseconds
    capiscio-core validate ./agent-card.json --timeout 30000
    ```

---

## Timeout Values

| Value | Duration | Use Case |
|-------|----------|----------|
| `5000` | 5 seconds | Fast local networks |
| `10000` | 10 seconds | Default, most scenarios |
| `30000` | 30 seconds | Slow networks, cold starts |
| `60000` | 60 seconds | Very slow endpoints |
| `120000` | 2 minutes | Serverless with long cold starts |

---

## GitHub Action

```yaml title=".github/workflows/validate.yml"
- name: Validate Agent
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
    test-live: true
    timeout: 30000  # 30 seconds
```

---

## Per-Environment Timeouts

Different timeouts for different environments:

```yaml title=".github/workflows/validate.yml"
jobs:
  validate:
    strategy:
      matrix:
        include:
          - env: local
            card: ./agent-card.local.json
            timeout: 5000
          - env: staging
            card: https://staging.example.com/.well-known/agent-card.json
            timeout: 30000
          - env: production
            card: https://api.example.com/.well-known/agent-card.json
            timeout: 15000
    
    steps:
      - uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.card }}
          timeout: ${{ matrix.timeout }}
          test-live: true
```

---

## Retry with Increasing Timeout

For unreliable endpoints, retry with longer timeouts:

```bash
#!/bin/bash

timeouts=(10000 30000 60000)

for timeout in "${timeouts[@]}"; do
  echo "Trying with ${timeout}ms timeout..."
  if capiscio validate ./agent-card.json --test-live --timeout "$timeout"; then
    echo "Success!"
    exit 0
  fi
  echo "Failed, retrying with longer timeout..."
done

echo "All retries failed"
exit 1
```

---

## Timeout vs Skip Live Test

If timeouts are always a problem, consider skipping live testing:

```bash
# Use schema-only mode to skip all network requests
capiscio validate ./agent-card.json --schema-only
```

This gives you schema validation without network delays.

---

## Debugging Timeout Issues

If you're hitting timeouts, check:

1. **Endpoint accessibility:**
   ```bash
   curl -v https://your-agent.com/a2a/endpoint
   ```

2. **DNS resolution:**
   ```bash
   dig your-agent.com
   ```

3. **Cold start behavior:**
   ```bash
   # First request (cold)
   time curl https://your-agent.com/a2a/endpoint
   
   # Second request (warm)
   time curl https://your-agent.com/a2a/endpoint
   ```

---

## See Also

- [Validate from URL](validate-url.md) — Remote validation
- [Schema-Only Mode](schema-only.md) — Skip network tests
- [CI/CD Guide](../../getting-started/cicd/1-intro.md) — GitHub Action setup
