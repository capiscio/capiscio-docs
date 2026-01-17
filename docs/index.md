---
title: CapiscIO - The Authority Layer for AI Agents
description: Verifiable identity and trust for the Agent-to-Agent (A2A) Protocol. Like Let's Encrypt, but for AI agents.
keywords: A2A protocol, AI agent identity, DID, decentralized identifier, agent trust, trust badges, agent registry
og:image: https://docs.capisc.io/assets/social-card-home.png
canonical_url: https://docs.capisc.io/
hide:
  - navigation
  - toc
---

<style>
.md-typeset h1 { font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; }
.hero-tagline { font-size: 1.6rem; font-weight: 500; color: var(--md-primary-fg-color); margin-bottom: 1rem; }
.hero-subtitle { font-size: 1.15rem; color: var(--md-default-fg-color--light); margin-bottom: 2rem; max-width: 680px; }
.hero-buttons { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 3rem; }
</style>

# CapiscIO

<p class="hero-tagline">The Authority Layer for AI Agents</p>

<p class="hero-subtitle">
Like Let's Encrypt revolutionized HTTPS, CapiscIO brings verifiable identity and trust to the agent economy. Cryptographic proof of who your agent is—and who it can trust.
</p>

<div class="hero-buttons">
<a href="getting-started/" class="md-button md-button--primary">Get Started</a>
<a href="overview/index.md" class="md-button">How It Works</a>
</div>

---

## What Do You Want to Do?

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validate My Agent Card**

    ---

    Check if your A2A agent card is compliant and production-ready.

    [:octicons-arrow-right-24: Start Validating](getting-started/validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Secure Agent Communication**

    ---

    Add authentication, signing, and trust enforcement to your agent.

    [:octicons-arrow-right-24: Add Security](getting-started/secure/1-intro.md)

-   :material-tools:{ .lg .middle } **Protect MCP Tools**

    ---

    Add trust-level authorization to your Model Context Protocol servers.

    [:octicons-arrow-right-24: MCP Guard](mcp-guard/getting-started/quickstart.md)

-   :fontawesome-solid-gears:{ .lg .middle } **Add to CI/CD Pipeline**

    ---

    Automate validation with GitHub Actions, GitLab CI, or Jenkins.

    [:octicons-arrow-right-24: CI/CD Setup](getting-started/cicd/1-intro.md)

</div>

---

## The CapiscIO Stack

Three products that work together to secure the agent economy:

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **CapiscIO Core**

    ---

    **CLI & validation engine** — Validate agent cards, generate keys, issue badges.

    ```bash
    pip install capiscio  # or npm install -g capiscio
    capiscio validate agent-card.json
    ```

    [:octicons-arrow-right-24: CLI Reference](reference/cli/index.md)

-   :material-language-python:{ .lg .middle } **CapiscIO SDK**

    ---

    **Runtime security** — Sign requests, verify badges, enforce trust in your code.

    ```python
    from capiscio_sdk import SimpleGuard
    guard = SimpleGuard(dev_mode=True)
    ```

    [:octicons-arrow-right-24: Python SDK](reference/sdk-python/index.md)

-   :material-shield-check:{ .lg .middle } **MCP Guard**

    ---

    **Tool authorization** — Protect MCP tools with trust-level requirements.

    ```python
    @guard(min_trust_level=2)
    async def read_database(query: str):
        pass
    ```

    [:octicons-arrow-right-24: MCP Guard](mcp-guard/index.md)

</div>

[:octicons-arrow-right-24: See how these fit together](overview/index.md)

---

## Developers Love CapiscIO

Every feature works in **three commands or less**.

=== "Validate"

    ```bash
    capiscio validate agent-card.json
    # ✅ Validation passed: 95/100 (A+)
    ```

=== "Sign Requests"

    ```python
    from capiscio_sdk import sign_request
    signed = sign_request(request, badge)
    ```

=== "Protect APIs"

    ```python
    @guard.protect(min_trust_level=2)
    async def handle_task(request):
        pass  # Only trusted agents reach here
    ```

=== "Guard MCP Tools"

    ```python
    @guard(min_trust_level=3)
    async def write_file(path: str, content: str):
        pass  # Enterprise agents only
    ```

---

## Quick Links

<div class="grid cards" markdown>

-   [:material-rocket-launch: **Getting Started**](getting-started/index.md)

    Step-by-step tutorials to get up and running

-   [:material-book-open: **Concepts**](concepts/index.md)

    Understand DIDs, trust badges, and the trust model

-   [:material-clipboard-list: **How-To Guides**](how-to/index.md)

    Task-focused recipes for common scenarios

-   [:material-api: **API Reference**](reference/index.md)

    Complete CLI, SDK, and server API documentation

-   [:material-file-document: **RFCs**](rfcs/index.md)

    Protocol specifications and standards

-   [:material-help-circle: **Troubleshooting**](troubleshooting.md)

    Common issues and solutions

</div>

---

<div style="text-align: center; margin-top: 2rem;">
Questions? <a href="https://github.com/capiscio/capiscio-core/issues">Open an issue</a> · <a href="https://github.com/orgs/capiscio/discussions">Join discussions</a> · <a href="community/support/">Get support</a>
</div>
