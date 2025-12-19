---
title: Validate from URL
description: Validate a remote agent card directly from its URL
---

# Validate from URL

Validate an agent card hosted at a URL without downloading it first.

---

## Problem

You want to validate an agent card that's hosted remotely, such as:

- An agent in production at any URL (e.g., `https://agent.example.com/agent-card.json`, `https://api.example.com/agents/my-agent`)
- A colleague's staging environment
- A third-party agent you're considering integrating with

---

## Solution

=== "npm"

    ```bash
    npx capiscio validate https://agent.example.com/agent-card.json
    ```

=== "pip"

    ```bash
    capiscio validate https://agent.example.com/agent-card.json
    ```

=== "Go"

    ```bash
    capiscio-core validate https://agent.example.com/agent-card.json
    ```

---

## With Live Endpoint Testing

Add `--test-live` to also check if the agent's endpoint responds correctly:

=== "npm"

    ```bash
    npx capiscio validate https://agent.example.com/agent-card.json --test-live
    ```

=== "pip"

    ```bash
    capiscio validate https://agent.example.com/agent-card.json --test-live
    ```

---

## How It Works

1. The CLI fetches the agent card from the URL
2. Validates the JSON structure against the A2A schema
3. Checks all required and recommended fields
4. (With `--test-live`) Makes a test request to the agent's declared endpoint

---

## Common Issues

??? warning "Certificate errors"

    If you get SSL certificate errors:
    
    ```bash
    # Not recommended for production, but useful for testing
    NODE_TLS_REJECT_UNAUTHORIZED=0 npx capiscio validate https://...
    ```

??? warning "Timeout errors"

    For slow endpoints, increase the timeout:
    
    ```bash
    capiscio validate https://... --timeout 30000
    ```

---

## See Also

- [Bulk Validation](bulk-validate.md) — Validate multiple URLs at once
- [Custom Timeout](custom-timeout.md) — Handle slow endpoints
- [Troubleshooting](../../troubleshooting.md) — Common issues and fixes
