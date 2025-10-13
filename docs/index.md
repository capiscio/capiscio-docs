---
title: CapiscIO Documentation - Security & Tooling for A2A Protocol
description: Unified docs for A2A Security middleware and CLI tool. Protect AI agents with runtime security, signature verification, and protocol compliance.
keywords: A2A protocol, AI agent security, agent validation, protocol compliance, CapiscIO CLI, A2A Security middleware
og:image: https://docs.capisc.io/assets/social-card-home.png
canonical_url: https://docs.capisc.io/
---

# CapiscIO Documentation

Technical documentation for CapiscIO security and tooling infrastructure for the [A2A protocol](https://github.com/a2aproject/A2A){:target="_blank"}.

---

## Documentation by Product

<div class="product-grid" markdown>

<div class="product-card" markdown>
### 📦 A2A Security Middleware

Runtime security for A2A agents. Message validation, signature verification, and protocol compliance.

**Use when:** Building production A2A agents that need protection from malformed messages, protocol violations, and SSRF attacks.

**Quick Links:**
- [Quick Start →](a2a-security/getting-started/quickstart/)
- [Installation Guide](a2a-security/getting-started/installation/)
- [Configuration Reference](a2a-security/guides/configuration/)
- [Scoring System](a2a-security/guides/scoring/)

[![PyPI](https://img.shields.io/pypi/v/capiscio-a2a-security.svg)](https://pypi.org/project/capiscio-a2a-security/){:target="_blank"}
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/){:target="_blank"}

[Browse A2A Security Docs →](a2a-security/){ .md-button .md-button--primary }
</div>

<div class="product-card" markdown>
### 🔧 CapiscIO CLI

Command-line validation for A2A agent cards. Three-dimensional scoring, JWS signature verification, live endpoint testing, and compliance checking.

**Use when:** Validating agent cards during development, CI/CD pipelines, or registry submissions.

**Quick Links:**
- [Getting Started](capiscio-cli/)
- [Validation Process](capiscio-cli/validation-process/)
- [Scoring System](capiscio-cli/scoring-system/)
- [API Reference](capiscio-cli/api-reference/)

[![npm version](https://img.shields.io/npm/v/capiscio-cli.svg)](https://www.npmjs.com/package/capiscio-cli){:target="_blank"}
[![Downloads](https://img.shields.io/npm/dm/capiscio-cli)](https://www.npmjs.com/package/capiscio-cli){:target="_blank"}

[Browse CLI Docs →](capiscio-cli/){ .md-button .md-button--primary }
[Try Online Validator →](https://capisc.io/validator){ .md-button target="_blank" }
</div>

</div>

---

## When to Use Which Product?

<div class="grid cards" markdown>

-   :material-shield-lock:{ .lg .middle } **A2A Security Middleware**

    ---

    Choose when you're **building an A2A agent** and need runtime protection:

    - ✅ Validating incoming requests before processing
    - ✅ Protecting against malformed messages
    - ✅ Rate limiting and SSRF prevention
    - ✅ Integrating security into your Python agent

    **Installation:** `pip install capiscio-a2a-security`

-   :material-check-decagram:{ .lg .middle } **CapiscIO CLI**

    ---

    Choose when you need to **validate agent cards**:

    - ✅ Testing agent cards during development
    - ✅ CI/CD validation in your pipeline
    - ✅ Registry submission compliance checking
    - ✅ Understanding scoring and trust metrics

    **Installation:** `npm install -g capiscio-cli`

</div>

!!! tip "Use Both Together"
    Most production A2A agents benefit from **both** tools:
    
    - **capiscio-cli** validates your agent card during development
    - **A2A Security** protects your agent at runtime

---

## Resources

<div class="link-grid" markdown>

- [:material-github: **GitHub**<br/>Source code & issues](https://github.com/capiscio){:target="_blank"}
- [:material-package: **PyPI**<br/>Python packages](https://pypi.org/user/capiscio/){:target="_blank"}
- [:material-npm: **npm**<br/>Node.js packages](https://www.npmjs.com/~capiscio){:target="_blank"}
- [:material-file-document: **A2A Spec**<br/>Protocol reference](https://github.com/a2aproject/A2A){:target="_blank"}

</div>

---

## Need Help?

- **Found a bug?** Open an issue on the relevant repository (see product documentation)
- **General questions?** Check the [CapiscIO website](https://capisc.io){:target="_blank"}

<div style="text-align: center; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid var(--md-default-fg-color--lightest); color: var(--md-default-fg-color--light); font-size: 0.9em;">
Latest: A2A Security v0.1.0 • CLI v2.0.0 • License: MIT & Apache-2.0
</div>
