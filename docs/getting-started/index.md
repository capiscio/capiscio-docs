---
title: Getting Started with CapiscIO
description: Get your agent identity, trust badge, and validation in minutes.
---

# Getting Started

Install CapiscIO and follow the guide that matches what you need to do.

```bash
npm install -g capiscio       # or: pip install capiscio
```

---

## Choose Your Path

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validate an Agent Card**

    ---

    Check your `agent-card.json` is A2A-compliant.

    **5 minutes** · Beginner

    [:octicons-arrow-right-24: Start Validating](validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Secure Your Agent**

    ---

    Add request signing, badges, and trust verification.

    **15 minutes** · Intermediate

    [:octicons-arrow-right-24: Add Security](secure/1-intro.md)

-   :material-tools:{ .lg .middle } **Protect MCP Tools**

    ---

    Add tool-level authorization to MCP servers.

    **10 minutes** · Intermediate

    [:octicons-arrow-right-24: MCP Guard Quickstart](../mcp-guard/getting-started/quickstart.md)

-   :material-pipe:{ .lg .middle } **CI/CD Integration**

    ---

    Automate validation in GitHub Actions.

    **10 minutes** · Intermediate

    [:octicons-arrow-right-24: Setup CI/CD](cicd/1-intro.md)

</div>

---

## End-to-End Walkthrough

If you want to see the full flow — identity, registration, badges, gateway — in one tutorial:

[:octicons-arrow-right-24: Complete Workflow](complete-workflow.md) (30 minutes)

---

## Prerequisites

| Path | Requirements |
|------|--------------|
| CLI (`capiscio init`) | Node.js 18+ or Python 3.10+ |
| Python SDK (`CapiscIO.connect()`) | Python 3.10+ |
| CI/CD | GitHub repository |

---

## What's Next?

- [Concepts](../concepts/index.md) — Understand how trust, scoring, and identity work
- [How-To Guides](../how-to/index.md) — Solve specific problems with copy-paste recipes
- [CLI Reference](../reference/cli/index.md) — All CLI commands and flags
