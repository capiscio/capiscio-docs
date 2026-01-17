---
title: Concepts - Understanding CapiscIO
description: Deep dive into how CapiscIO works under the hood. Validation, scoring, trust models, and enforcement.
---

# Concepts

Understand how CapiscIO works under the hood. These docs explain the **why** and **how** behind the platform.

---

## Identity & Trust

<div class="grid cards" markdown>

-   :material-identifier:{ .lg .middle } **Identity & DIDs**

    ---

    Decentralized identifiers give your agent a permanent, cryptographically verifiable identity.

    [:octicons-arrow-right-24: Learn about DIDs](../identity/index.md)

-   :material-certificate:{ .lg .middle } **Trust Badges**

    ---

    Cryptographic credentials that attest to your agent's identity verification level (0-4).

    [:octicons-arrow-right-24: Understanding Badges](../trust/index.md)

-   :material-key:{ .lg .middle } **Trust Levels**

    ---

    The five-level verification hierarchy—from self-signed to extended validation.

    [:octicons-arrow-right-24: Trust Levels](trust-model.md)

</div>

---

## Validation & Scoring

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validation Process**

    ---

    How CapiscIO validates agent cards across 7+ categories: schema compliance, security, versioning, and more.

    [:octicons-arrow-right-24: Learn about Validation](validation.md)

-   :material-counter:{ .lg .middle } **Scoring System**

    ---

    The three-dimensional scoring model: Compliance, Trust, and Availability. What the numbers mean.

    [:octicons-arrow-right-24: Understanding Scores](scoring.md)

</div>

---

## Runtime Security

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } **Enforcement**

    ---

    How SimpleGuard enforces security policies on incoming requests. The runtime protection layer.

    [:octicons-arrow-right-24: Enforcement](enforcement.md)

-   :material-tools:{ .lg .middle } **MCP Security**

    ---

    RFC-006 (tool authorization) and RFC-007 (server verification) for Model Context Protocol.

    [:octicons-arrow-right-24: MCP Security](mcp-security.md)

</div>

---

## Infrastructure

<div class="grid cards" markdown>

-   :material-server:{ .lg .middle } **Agent Registry**

    ---

    The central registry for agent discovery, DID resolution, and badge verification.

    [:octicons-arrow-right-24: Registry](../registry/index.md)

</div>

---

## How It All Fits Together

```
┌─────────────────────────────────────────────────────────────────┐
│                     CapiscIO Architecture                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Identity   │    │    Trust     │    │   Registry   │       │
│  │              │    │              │    │              │       │
│  │  DID + Keys  │───▶│   Badges     │───▶│  Discovery   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         └───────────────────┼───────────────────┘                │
│                             │                                    │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Validation & Scoring                    │ │
│  │                                                             │ │
│  │  Compliance (0-100)  ×  Trust (0-100)  ×  Availability     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                             │                                    │
│                             ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Runtime Enforcement                     │ │
│  │                                                             │ │
│  │  SimpleGuard → Verify Signatures → Check Trust Level       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Concept Quick Reference

| Concept | What It Answers |
|---------|-----------------|
| **[Validation](validation.md)** | "Is this agent card correctly formatted?" |
| **[Scoring](scoring.md)** | "How good is this agent across compliance, trust, availability?" |
| **[Trust Model](trust-model.md)** | "How do I manage who my agent trusts?" |
| **[Enforcement](enforcement.md)** | "How do I protect my agent at runtime?" |
| **[MCP Guard](../mcp-guard/index.md)** | "How do I secure MCP tools?" |

---

## Specifications (RFCs)

For the formal technical specifications, see the CapiscIO RFCs:

| RFC | Title | Status |
|-----|-------|--------|
| **[RFC-001](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/001-agcp.md)** | Agent Governance Control Plane (AGCP) | ✅ Approved |
| **[RFC-002](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/002-trust-badge.md)** | Trust Badge Specification | ✅ Approved |
| **[RFC-003](https://github.com/capiscio/capiscio-rfcs/blob/main/docs/003-key-ownership-proof.md)** | Key Ownership Proof Protocol | ✅ Approved |
| **[RFC-006](../rfcs/006-mcp-tool-authority-evidence.md)** | MCP Tool Authority Evidence | ✅ Approved |
| **[RFC-007](../rfcs/007-mcp-server-identity-discovery.md)** | MCP Server Identity Discovery | ✅ Approved |

[:octicons-arrow-right-24: Browse All RFCs](https://github.com/capiscio/capiscio-rfcs){ .md-button }

---

## Next Steps

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Get Started**

    ---

    Ready to try it? Jump into the getting started guides.

    [:octicons-arrow-right-24: Getting Started](../getting-started/index.md)

-   :material-clipboard-list:{ .lg .middle } **How-To Guides**

    ---

    Task-oriented guides for specific problems.

    [:octicons-arrow-right-24: How-To Guides](../how-to/index.md)

</div>
