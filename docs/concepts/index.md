---
title: Concepts - Understanding CapiscIO
description: Deep dive into how CapiscIO works under the hood. Validation, scoring, trust models, and enforcement.
---

# Concepts

Understand how CapiscIO works under the hood. These docs explain the **why** and **how** behind the platform.

---

## Core Concepts

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validation Process**

    ---

    How CapiscIO validates agent cards across 7+ categories: schema compliance, security, versioning, and more.

    [:octicons-arrow-right-24: Learn about Validation](validation.md)

-   :material-counter:{ .lg .middle } **Scoring System**

    ---

    The three-dimensional scoring model: Compliance, Trust, and Availability. What the numbers mean.

    [:octicons-arrow-right-24: Understanding Scores](scoring.md)

-   :material-key:{ .lg .middle } **Trust Model**

    ---

    How Ed25519 keys, trust stores, and cryptographic verification work. The SSH-like model explained.

    [:octicons-arrow-right-24: Trust Model](trust-model.md)

-   :material-shield-check:{ .lg .middle } **Enforcement**

    ---

    How SimpleGuard enforces security policies on incoming requests. The runtime protection layer.

    [:octicons-arrow-right-24: Enforcement](enforcement.md)

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
