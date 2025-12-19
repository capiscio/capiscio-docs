---
title: Getting Started with CapiscIO
description: Get your agent identity, trust badge, and validation in minutes. Zero to production-ready.
---

# Getting Started

Get up and running with CapiscIO in minutes. Choose your path based on what you want to accomplish.

---

## Quick Install

```bash
npm install -g capiscio       # or: pip install capiscio
```

---

## Choose Your Path

<div class="grid cards" markdown>

-   :material-identifier:{ .lg .middle } **Get Agent Identity**

    ---

    Generate a DID for your agent in 60 seconds.

    ```bash
    capiscio keygen
    ```

    [:octicons-arrow-right-24: Identity Guide](../identity/index.md)

-   :material-check-decagram:{ .lg .middle } **Validate Your Agent**

    ---

    Ensure your agent card is A2A-compliant.

    **5 minutes** · Beginner

    [:octicons-arrow-right-24: Start Validating](validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Secure Your Agent**

    ---

    Add cryptographic identity and request verification.

    **15 minutes** · Intermediate

    [:octicons-arrow-right-24: Add Security](secure/1-intro.md)

-   :material-pipe:{ .lg .middle } **CI/CD Integration**

    ---

    Automate validation in GitHub Actions.

    **10 minutes** · Intermediate

    [:octicons-arrow-right-24: Setup CI/CD](cicd/1-intro.md)

-   :material-routes:{ .lg .middle } **Complete Workflow**

    ---

    End-to-end guide: identity → badge → validation → deployment.

    **30 minutes** · Comprehensive

    [:octicons-arrow-right-24: Full Walkthrough](complete-workflow.md)

</div>

---

## The Fast Path

If you just want to try CapiscIO quickly:

```bash
# 1. Install
npm install -g capiscio

# 2. Create a sample agent card
cat > agent-card.json << 'EOF'
{
  "name": "My Test Agent",
  "description": "Testing CapiscIO validation",
  "url": "https://example.com/agent",
  "version": "1.0.0",
  "protocolVersion": "0.2.0",
  "skills": [{ "id": "test", "name": "Test Skill", "description": "A test skill" }]
}
EOF

# 3. Validate
capiscio validate agent-card.json

# 4. Generate identity
capiscio keygen --output ./capiscio_keys
```

**Done!** You have a validated agent card and a cryptographic identity.

---

## Prerequisites

| Path | Requirements |
|------|--------------|
| CLI (validate, keygen) | Node.js 18+ or Python 3.10+ |
| Python SDK (SimpleGuard) | Python 3.10+, FastAPI or similar |
| CI/CD | GitHub repository |

---

## What's Next?

After getting started, explore:

<div class="grid cards" markdown>

-   :material-certificate:{ .lg .middle } **Get a Trust Badge**

    ---

    Upgrade from self-signed to verified trust.

    [:octicons-arrow-right-24: Trust Badges](../trust/index.md)

-   :material-book-open:{ .lg .middle } **Understand the Concepts**

    ---

    Learn how validation, scoring, and trust work.

    [:octicons-arrow-right-24: Concepts](../concepts/index.md)

-   :material-clipboard-list:{ .lg .middle } **How-To Guides**

    ---

    Solve specific problems with copy-paste recipes.

    [:octicons-arrow-right-24: How-To Guides](../how-to/index.md)

</div>
