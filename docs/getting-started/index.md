---
title: Getting Started with CapiscIO
description: Get your agent identity, trust badge, and validation in minutes. Zero to production-ready.
---

# Getting Started

Get up and running with CapiscIO in minutes. **One command** gives your AI agent a cryptographic identity, just like Let's Encrypt did for HTTPS.

---

## Quick Install

```bash
npm install -g capiscio       # or: pip install capiscio
```

---

## The Fastest Path: One Command Setup

Get a complete agent identity in **under 60 seconds**:

=== "CLI"

    ```bash
    # Set your API key (get one free at app.capisc.io)
    export CAPISCIO_API_KEY=sk_live_...
    
    # That's it! One command does everything:
    capiscio init
    ```

=== "Python"

    ```python
    from capiscio_sdk import CapiscIO
    
    # One line - handles everything automatically
    agent = CapiscIO.connect(api_key="sk_live_...")
    
    print(agent.did)    # did:key:z6Mk...
    print(agent.badge)  # Your trust badge
    ```

=== "Environment Variables"

    ```python
    # Set CAPISCIO_API_KEY in your environment
    agent = CapiscIO.from_env()
    ```

**What happens automatically:**

1. ✅ Ed25519 key pair generated
2. ✅ `did:key` identity derived (RFC-002 compliant)
3. ✅ DID registered with CapiscIO registry
4. ✅ Agent card created with `x-capiscio` extension
5. ✅ Trust badge requested and stored

---

## Choose Your Setup Path

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Path 1: Quick Start (Recommended)**

    ---

    Just use your API key. We auto-discover your agent.

    ```bash
    export CAPISCIO_API_KEY=sk_live_...
    capiscio init
    ```

    **Best for:** Getting started fast, single-agent setups, demos.

-   :material-view-dashboard:{ .lg .middle } **Path 2: UI-First**

    ---

    Create your agent in the dashboard first, then initialize.

    ```bash
    # 1. Create agent at app.capisc.io → get agent ID
    # 2. Initialize with specific agent
    capiscio init --agent-id agt_abc123
    ```

    **Best for:** Teams, production, multiple agents per org.

</div>

---

## What You Get

After running `capiscio init`, your `.capiscio/` directory contains:

```
.capiscio/
├── private.jwk      # Ed25519 private key (keep secret!)
├── public.jwk       # Public key
├── did.txt          # Your agent's did:key identifier
└── agent-card.json  # A2A-compliant agent card
```

Your agent now has:

- **Cryptographic identity** - A globally unique `did:key` that proves who you are
- **Verifiable credentials** - Sign messages and prove authenticity
- **Trust badge** - Registered with CapiscIO for discovery and verification
- **A2A compliance** - Ready to interact with other A2A agents

---

## Choose Your Next Step

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validate Your Agent**

    ---

    Ensure your agent card is A2A-compliant.

    **5 minutes** · Beginner

    [:octicons-arrow-right-24: Start Validating](validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Secure Your Agent**

    ---

    Add request signing and verification.

    **15 minutes** · Intermediate

    [:octicons-arrow-right-24: Add Security](secure/1-intro.md)

-   :material-tools:{ .lg .middle } **Protect MCP Tools**

    ---

    Add tool-level authorization to Model Context Protocol servers.

    **10 minutes** · Intermediate

    [:octicons-arrow-right-24: MCP Guard Quickstart](../mcp-guard/getting-started/quickstart.md)

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

## Manual Setup (Advanced)

If you need more control, you can still do things step-by-step:

```bash
# Generate keys only (no server registration)
capiscio key gen --out-priv private.jwk --out-pub public.jwk

# Derive DID from existing key
capiscio key did --in public.jwk
```

See the [CLI Reference](../reference/cli.md) for all options.

---

## Prerequisites

| Path | Requirements |
|------|--------------|
| CLI (`capiscio init`) | Node.js 18+ or Python 3.10+ |
| Python SDK (`CapiscIO.connect()`) | Python 3.10+ |
| CI/CD | GitHub repository |

---

## SDK Quick Reference

=== "Python"

    ```python
    from capiscio_sdk import CapiscIO
    
    # Connect and get full identity
    agent = CapiscIO.connect(api_key="sk_live_...")
    
    # Or from environment
    agent = CapiscIO.from_env()  # Uses CAPISCIO_API_KEY
    
    # Use the agent
    print(agent.did)           # did:key:z6Mk...
    print(agent.badge)         # Current trust badge
    print(agent.status())      # Full status dict
    
    # Emit events for observability
    agent.emit("task_started", {"task_id": "123"})
    ```

=== "Node.js / TypeScript"

    ```typescript
    import { CapiscIO } from 'capiscio';
    
    // Connect and get full identity
    const agent = await CapiscIO.connect({ apiKey: 'sk_live_...' });
    
    console.log(agent.did);    // did:key:z6Mk...
    console.log(agent.badge);  // Current trust badge
    ```

=== "CLI"

    ```bash
    # Initialize agent identity
    capiscio init --api-key $CAPISCIO_API_KEY
    
    # Or with explicit agent ID
    capiscio init --agent-id agt_abc123
    
    # View your identity
    cat .capiscio/did.txt
    ```

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
