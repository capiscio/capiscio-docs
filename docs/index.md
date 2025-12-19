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
.md-typeset h1 {
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.hero-tagline {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--md-primary-fg-color);
  margin-bottom: 0.5rem;
}
.hero-subtitle {
  font-size: 1.1rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 2rem;
  max-width: 700px;
}
.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}
.value-prop {
  background: var(--md-code-bg-color);
  border-radius: 8px;
  padding: 2rem;
  margin: 2rem 0;
}
.value-prop h3 {
  margin-top: 0;
}
.install-box {
  background: var(--md-code-bg-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
}
.trust-levels {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1rem 0;
}
.trust-level {
  text-align: center;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background: var(--md-default-fg-color--lightest);
}
</style>

# CapiscIO

<p class="hero-tagline">The Authority Layer for AI Agents</p>

<p class="hero-subtitle">
Like Let's Encrypt revolutionized HTTPS, CapiscIO brings verifiable identity and trust to the agent economy. Give your agent a DID, earn trust badges, be discovered.
</p>

<div class="hero-buttons">
<a href="identity/" class="md-button md-button--primary">:material-identifier: Get Your Agent's Identity</a>
<a href="getting-started/" class="md-button">:material-rocket-launch: Quick Start</a>
</div>

---

## The Three Pillars

<div class="grid cards" markdown>

-   :material-identifier:{ .lg .middle } **Decentralized Identity**

    ---

    Every agent gets a **DID** (Decentralized Identifier) — a globally unique, cryptographically verifiable identity that travels with your agent.

    ```
    did:web:registry.capisc.io:agents:my-weather-bot
    ```
    
    - W3C standard — interoperable everywhere
    - Cryptographic proof — unforgeable
    - Portable — move providers, keep identity

    [:octicons-arrow-right-24: Learn about DIDs](identity/index.md)

-   :material-certificate:{ .lg .middle } **Trust Badges**

    ---

    Earn **trust levels 0-4** based on identity verification depth. Like SSL certificates for agents.

    | Level | Verification |
    |:-----:|--------------|
    | 0 | Self-signed |
    | 1 | Email verified |
    | 2 | Domain validated |
    | 3 | Organization validated |
    | 4 | Extended validation |

    [:octicons-arrow-right-24: Get a Trust Badge](trust/index.md)

-   :material-api:{ .lg .middle } **Registry API**

    ---

    REST API for managing agents, issuing badges, and resolving DIDs.

    - Agent CRUD operations
    - Badge issuance and verification
    - DID resolution
    - Public status endpoints

    [:octicons-arrow-right-24: Registry API](registry/index.md)

</div>

---

## Quick Start

<div class="install-box">

```bash
# 1. Install CLI
npm install -g capiscio       # or: pip install capiscio

# 2. Initialize your agent
capiscio init

# 3. Validate your agent card
capiscio validate
```

```
✅ Validation passed!

Compliance: 95/100 (A+)
Trust: 78/100 (Good)

Agent card is valid and ready to use.
```

</div>

[:material-rocket-launch: Full Getting Started Guide](getting-started/index.md){ .md-button .md-button--primary }
[:material-download: Download Samples](samples.md){ .md-button }

---

## Why CapiscIO?

<div class="value-prop" markdown>

### The Problem

AI agents are proliferating. But there's no standard way to:

- **Verify identity** — Is this really the agent it claims to be?
- **Establish trust** — Can I trust this agent with my data?
- **Validate compliance** — Does this agent card meet standards?

API keys prove you paid. OAuth tokens expire. Self-descriptions can be forged.

### The Solution

CapiscIO provides the **trust infrastructure** for the agent economy:

| Component | What It Solves |
|-----------|---------------|
| **DID Identity** | Permanent, verifiable, portable agent identity |
| **Trust Badges** | Tiered verification like SSL certificates |
| **Validation Engine** | Multi-dimensional agent card scoring |
| **SDK/CLI** | Frictionless integration for developers |

**Result:** Agents can prove who they are, establish trust, and find each other.

</div>

---

## Developer-First Design

We obsess over developer experience. Every feature works in **three commands or less**.

=== "Generate Identity"

    ```bash
    capiscio keygen
    # ✅ did:key:z6Mk... generated
    ```

=== "Validate Agent Card"

    ```bash
    capiscio validate agent-card.json
    # ✅ Validation passed: 95/100 (A+)
    ```

=== "Issue Badge"

    ```bash
    capiscio badge sign --trust-level 2
    # ✅ Badge signed with private key
    ```

=== "Add to Your App"

    ```python
    from capiscio_sdk import SimpleGuard

    guard = SimpleGuard(dev_mode=True)  # That's it!
    
    @app.post("/task")
    @guard.protect
    async def handle(request):
        # Requests are verified automatically
        pass
    ```

---

## Trust Hierarchy

<div class="trust-levels">
  <div class="trust-level">
    <strong>Level 0</strong><br/>
    <small>Self-Signed</small>
  </div>
  <div class="trust-level">
    <strong>Level 1</strong><br/>
    <small>Registered</small>
  </div>
  <div class="trust-level">
    <strong>Level 2</strong><br/>
    <small>Domain Validated</small>
  </div>
  <div class="trust-level">
    <strong>Level 3</strong><br/>
    <small>Org Validated</small>
  </div>
  <div class="trust-level">
    <strong>Level 4</strong><br/>
    <small>Extended</small>
  </div>
</div>

Higher levels = more verification = more trust. Choose what's right for your use case:

| Use Case | Recommended Level |
|----------|-------------------|
| Development & testing | 0 (self-signed) |
| Personal projects | 1 (registered) |
| Production APIs | 2 (domain validated) |
| Enterprise integrations | 3 (org validated) |
| Financial, healthcare | 4 (extended validation) |

[:octicons-arrow-right-24: Learn about Trust Levels](trust/index.md)

---

## What You Can Build

<div class="grid cards" markdown>

-   :material-robot:{ .lg .middle } **Secure Agent Networks**

    ---

    Build multi-agent systems where agents verify each other's identity before communicating.

-   :material-api:{ .lg .middle } **Trusted API Gateways**

    ---

    Enforce trust level requirements at your API boundary. Only Level 2+ agents can access production endpoints.

-   :material-magnify:{ .lg .middle } **Agent Marketplaces**

    ---

    Create directories of verified agents. Users trust your curation because trust is cryptographically proven.

-   :material-shield-lock:{ .lg .middle } **Enterprise Integrations**

    ---

    Meet compliance requirements with org-validated identities and audit trails.

</div>

---

## Built on Standards

CapiscIO implements and extends open standards:

| Standard | How We Use It |
|----------|---------------|
| **[A2A Protocol](https://github.com/a2aproject/A2A)** | Agent communication format |
| **[W3C DIDs](https://www.w3.org/TR/did-core/)** | Decentralized identifiers |
| **[JWS (RFC 7515)](https://tools.ietf.org/html/rfc7515)** | Request signing |
| **[Ed25519](https://ed25519.cr.yp.to/)** | Cryptographic keys |

We're not inventing new cryptography — we're applying proven standards to the agent economy.

### CapiscIO RFCs

Our core specifications are published as RFCs (Request for Comments):

| RFC | Title | What It Defines |
|-----|-------|----------------|
| **[RFC-001](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/001-agcp.md)** | Agent Governance Control Plane (AGCP) | Authority delegation and transitive trust model |
| **[RFC-002](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/002-trust-badge.md)** | Trust Badge Specification | Cryptographic identity credentials (JWS format) |
| **[RFC-003](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/003-key-ownership-proof.md)** | Key Ownership Proof Protocol | Challenge-response key binding for IAL-1 badges |

[:octicons-arrow-right-24: Browse All RFCs](https://github.com/capiscio/capiscio-rfcs)

---

## Documentation

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Step-by-step guides for common tasks.

    [:octicons-arrow-right-24: Getting Started](getting-started/index.md)

-   :material-book-open:{ .lg .middle } **Concepts**

    ---

    Understand how CapiscIO works under the hood.

    [:octicons-arrow-right-24: Concepts](concepts/index.md)

-   :material-clipboard-list:{ .lg .middle } **How-To Guides**

    ---

    Task-oriented recipes for specific problems.

    [:octicons-arrow-right-24: How-To Guides](how-to/index.md)

-   :material-api:{ .lg .middle } **Reference**

    ---

    Complete API documentation.

    [:octicons-arrow-right-24: Reference](reference/index.md)

</div>

---

## Open Source

CapiscIO is open source under the Apache 2.0 license.

<div class="grid cards" markdown>

-   :fontawesome-brands-github:{ .lg .middle } **capiscio-core**

    ---

    The Go CLI and core validation engine.

    [:octicons-arrow-right-24: GitHub](https://github.com/capiscio/capiscio-core)

-   :material-language-python:{ .lg .middle } **capiscio-sdk**

    ---

    Python SDK for runtime security.

    [:octicons-arrow-right-24: GitHub](https://github.com/capiscio/capiscio-sdk-python)

-   :material-server:{ .lg .middle } **capiscio-server**

    ---

    Registry and Badge CA server.

    [:octicons-arrow-right-24: GitHub](https://github.com/capiscio/capiscio-server)

-   :material-file-document:{ .lg .middle } **capiscio-docs**

    ---

    This documentation site.

    [:octicons-arrow-right-24: GitHub](https://github.com/capiscio/capiscio-docs)

</div>

---

## Get Started Now

<div class="hero-buttons">
<a href="identity/" class="md-button md-button--primary">:material-identifier: Get Your Agent's DID</a>
<a href="trust/" class="md-button">:material-certificate: Request a Badge</a>
<a href="registry/" class="md-button">:material-database-search: Browse Registry</a>
</div>

Questions? [Open an issue](https://github.com/capiscio/capiscio-core/issues) or [join the discussion](https://github.com/orgs/capiscio/discussions).
