---
title: CapiscIO Documentation - The Authority Layer for A2A
description: Unified documentation for CapiscIO. The Authority Layer for the Agent-to-Agent (A2A) Protocol.
keywords: A2A protocol, AI agent validation, agent trust, protocol compliance, agent security, CapiscIO
og:image: https://docs.capisc.io/assets/social-card-home.png
canonical_url: https://docs.capisc.io/
---

# CapiscIO Documentation

Welcome to the official documentation for **CapiscIO**, the Authority Layer for the [Agent-to-Agent (A2A) Protocol](https://github.com/a2aproject/A2A){:target="_blank"}.

---

## Explore the Platform

<div class="grid cards" markdown>

-   :material-server-network:{ .lg .middle } **The Authority Layer**

    ---

    The core binary that powers the CapiscIO ecosystem. It handles validation, scoring, and trust verification.

    [Explore Core Docs →](capiscio-core/index.md){ .md-button }

-   :material-tools:{ .lg .middle } **Developer Tools**

    ---

    CLI wrappers and CI/CD actions to integrate CapiscIO into your workflow.

    - [Python CLI](capiscio-python-cli/index.md)
    - [Node.js CLI](capiscio-node-js-cli/index.md)
    - [GitHub Action](capiscio-github-action/index.md)

-   :material-code-braces:{ .lg .middle } **SDKs & Libraries**

    ---

    Integrate CapiscIO directly into your agent code.

    - [Python SDK](capiscio-python-sdk/index.md)

</div>

---

## Getting Started

If you are new to CapiscIO, we recommend starting with the **CLI** for your preferred language to validate your first Agent Card.

1.  **Install the CLI:**
    ```bash
    # Python
    pip install capiscio

    # Node.js
    npm install -g capiscio
    ```

2.  **Validate an Agent:**
    ```bash
    capiscio validate ./agent-card.json
    ```

3.  **Integrate in CI/CD:**
    Use the [GitHub Action](capiscio-github-action/index.md) to automatically validate your agent on every commit.

---

## Resources

<div class="link-grid" markdown>

- [:material-github: **GitHub**<br/>Source code & issues](https://github.com/capiscio){:target="_blank"}
- [:material-file-document: **A2A Spec**<br/>Protocol reference](https://github.com/a2aproject/A2A){:target="_blank"}

</div>
