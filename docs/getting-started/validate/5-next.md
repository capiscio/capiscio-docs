---
title: "Step 5: Next Steps"
description: Where to go from here
---

# Step 5: Next Steps

Congratulations! :tada: You've completed the Validation Quickstart. You can now validate any A2A agent card using the CapiscIO CLI.

---

## What You Learned

In this quickstart, you learned how to:

- [x] Install the CapiscIO CLI (npm, pip, or Go)
- [x] Validate a local agent-card.json file
- [x] Use different validation modes (progressive, strict)
- [x] Interpret the three-dimensional scoring system
- [x] Read and understand validation reports
- [x] Get JSON output for automation

---

## Quick Reference

Here's a cheat sheet for common validation tasks:

```bash
# Basic validation
capiscio validate agent-card.json

# Strict mode for production
capiscio validate agent-card.json --strict

# Validate from URL (any URL works)
capiscio validate https://my-agent.example.com/agent-card.json

# Test live endpoint
capiscio validate agent-card.json --test-live

# JSON output for scripts
capiscio validate agent-card.json --json

# Schema only (skip network)
capiscio validate agent-card.json --schema-only

# Skip signature verification (dev only)
capiscio validate agent-card.json --skip-signature
```

---

## Continue Your Journey

<div class="grid cards" markdown>

-   :material-shield-lock:{ .lg .middle } **Add Security**

    ---

    Learn how to sign agent cards and verify requests with SimpleGuard.

    [:octicons-arrow-right-24: Security Quickstart](../secure/1-intro.md)

-   :material-github:{ .lg .middle } **Automate with CI/CD**

    ---

    Add validation to your GitHub workflows to catch issues early.

    [:octicons-arrow-right-24: CI/CD Quickstart](../cicd/1-intro.md)

-   :material-book-open:{ .lg .middle } **Deep Dive: Scoring**

    ---

    Understand the complete scoring system in detail.

    [:octicons-arrow-right-24: Scoring System](../../concepts/scoring.md)

-   :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Complete Python SDK reference documentation.

    [:octicons-arrow-right-24: Python SDK Reference](../../reference/sdk-python/index.md)

</div>

---

## Common Use Cases

Now that you know the basics, here are practical scenarios:

### Validate Before Deploying

Add validation to your deployment script:

```bash
#!/bin/bash
# deploy.sh

echo "Validating agent card..."
if ! capiscio validate agent-card.json --strict; then
    echo "Validation failed! Aborting deployment."
    exit 1
fi

echo "Validation passed! Deploying..."
# your deployment commands here
```

### Validate Multiple Agents

Create a script to validate all agents in a directory:

```bash
#!/bin/bash
# validate-all.sh

for card in agents/*/agent-card.json; do
    echo "Validating $card..."
    capiscio validate "$card" --strict
done
```

### Monitor External Agents

Validate agents you depend on:

```bash
#!/bin/bash
# monitor.sh

agents=(
    "https://weather-agent.example.com/agent-card.json"
    "https://api.acme.io/agents/calendar/agent-card.json"
)

for url in "${agents[@]}"; do
    echo "Checking $url..."
    capiscio validate "$url" --test-live --json | jq '.success'
done
```

---

## Get Help

If you run into issues:

- **CLI Help**: `capiscio validate --help`
- **GitHub Issues**: [github.com/capiscio/capiscio-core/issues](https://github.com/capiscio/capiscio-core/issues)
- **Community**: [Join our Discord](#) (coming soon)

---

## Feedback

Was this quickstart helpful? We'd love to hear from you!

- Found an error? [Open an issue](https://github.com/capiscio/capiscio-docs/issues)
- Have suggestions? [Start a discussion](https://github.com/orgs/capiscio/discussions)

---

**Thank you for completing the Validation Quickstart!** :rocket:

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](4-reports.md){ .md-button }
[:material-home: Quickstarts](../index.md){ .md-button .md-button--primary }
</div>
