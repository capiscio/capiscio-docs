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

The fastest way to secure your agent is with the **CapiscIO SDK**. It provides "Enforcement First" security with zero configuration.

1.  **Install the SDK:**
    ```bash
    pip install capiscio-sdk
    ```

2.  **Secure your Agent (FastAPI):**
    ```python
    from capiscio_sdk.simple_guard import SimpleGuard
    from capiscio_sdk.integrations.fastapi import CapiscioMiddleware

    # Auto-generates keys and enforces Identity + Integrity
    app.add_middleware(CapiscioMiddleware, guard=SimpleGuard(dev_mode=True))
    ```

3.  **Validate an External Agent:**
    Use the CLI to check compliance of other agents in your network.
    ```bash
    capiscio validate ./agent-card.json
    ```

---

## Resources

<div class="link-grid" markdown>

- [:material-github: **GitHub**<br/>Source code & issues](https://github.com/capiscio){:target="_blank"}
- [:material-file-document: **A2A Spec**<br/>Protocol reference](https://github.com/a2aproject/A2A){:target="_blank"}
- [:material-shield-check: **Enforcement Guide**<br/>How Guard verifies requests](guides/enforcement-first.md)
- [:material-key: **Trust Model**<br/>How keys and trust stores work](concepts/trust-model.md)

</div>
