---
title: CapiscIO - The Authority Layer for AI Agents
description: Verifiable identity and trust for the Agent-to-Agent (A2A) Protocol. Like Let's Encrypt, but for AI agents.
keywords: A2A protocol, AI agent identity, DID, decentralized identifier, agent trust, trust badges, agent registry
og:image: https://docs.capisc.io/assets/social-card-home.png
canonical_url: https://docs.capisc.io/
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

## Developers Love CapiscIO

Every feature works in **three commands or less**.

=== "Validate"

    ```bash
    capiscio validate agent-card.json
    # ✅ Validation passed: 95/100 (A+)
    ```

=== "Sign Requests"

    ```python
    from capiscio_sdk import SimpleGuard

    guard = SimpleGuard()
    headers = guard.make_headers({"sub": agent_did})
    ```

=== "Verify Badges"

    ```python
    from capiscio_sdk import verify_badge

    result = verify_badge(token, trusted_issuers=["https://registry.capisc.io"])
    if result.valid:
        print(f"Trusted: {result.claims.subject}")
    ```

=== "Guard MCP Tools"

    ```python
    @guard(min_trust_level=3)
    async def write_file(path: str, content: str):
        pass  # Enterprise agents only
    ```

---

<div style="text-align: center; margin-top: 2rem;">
Questions? <a href="https://github.com/capiscio/capiscio-core/issues">Open an issue</a> · <a href="https://github.com/orgs/capiscio/discussions">Join discussions</a> · <a href="community/support/">Get support</a>
</div>
