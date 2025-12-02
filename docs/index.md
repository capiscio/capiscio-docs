---
title: CapiscIO Documentation - The Authority Layer for A2A
description: Unified documentation for CapiscIO. The Authority Layer for the Agent-to-Agent (A2A) Protocol.
keywords: A2A protocol, AI agent validation, agent trust, protocol compliance, agent security, CapiscIO
og:image: https://docs.capisc.io/assets/social-card-home.png
canonical_url: https://docs.capisc.io/
hide:
  - navigation
  - toc
---

<style>
.md-typeset h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.hero-subtitle {
  font-size: 1.25rem;
  color: var(--md-default-fg-color--light);
  margin-bottom: 2rem;
}
.quickstart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}
.quickstart-card {
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}
.quickstart-card:hover {
  border-color: var(--md-accent-fg-color);
  transform: translateY(-2px);
}
.quickstart-card h3 {
  margin-top: 0;
}
.time-badge {
  display: inline-block;
  padding: 2px 8px;
  background: var(--md-accent-fg-color--transparent);
  border-radius: 4px;
  font-size: 0.75rem;
  color: var(--md-accent-fg-color);
}
.install-tabs {
  margin: 2rem 0;
}
</style>

# CapiscIO Documentation

<p class="hero-subtitle">
The Authority Layer for the Agent-to-Agent (A2A) Protocol.<br/>
Validate compliance. Verify identity. Secure your agents.
</p>

---

## :material-rocket-launch: Quickstarts

Get started in minutes. Each quickstart is self-contained and builds on practical examples.

<div class="grid cards" markdown>

-   :material-check-decagram:{ .lg .middle } **Validate Your Agent**

    ---

    Ensure your agent card is A2A-compliant with the CapiscIO CLI.

    **5 minutes** · Beginner

    [:octicons-arrow-right-24: Start Validating](quickstarts/validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Secure Your Agent**

    ---

    Add cryptographic identity and request verification to your agent.

    **15 minutes** · Intermediate

    [:octicons-arrow-right-24: Add Security](quickstarts/secure/1-intro.md)

-   :material-pipe:{ .lg .middle } **CI/CD Integration**

    ---

    Automate validation in GitHub Actions with PR comments and quality gates.

    **10 minutes** · Intermediate

    [:octicons-arrow-right-24: Setup CI/CD](quickstarts/cicd/1-intro.md)

</div>

---

## :material-play-circle: Try It Now

Install the CLI and validate a sample agent card in under 60 seconds:

=== "1. Install"

    ```bash
    npm install -g capiscio   # or: pip install capiscio
    ```

=== "2. Download Sample"

    ```bash
    curl -O https://docs.capisc.io/assets/samples/agent-card.json
    ```

=== "3. Validate"

    ```bash
    capiscio validate agent-card.json
    ```

=== "4. See Results"

    ```ansi
    [32m✅ A2A AGENT VALIDATION PASSED[0m

    Score: [1m85/100[0m
    
    [32m✓[0m Schema validation passed
    [32m✓[0m Required fields present  
    [32m✓[0m Skills properly defined
    [33m○[0m Endpoint not tested (use --test-live)
    ```

[:material-download: Download Sample Files](samples.md){ .md-button .md-button--primary }
[:material-book-open-variant: Full Quickstart](quickstarts/validate/1-intro.md){ .md-button }

---

## :material-compass: Learn the Concepts

<div class="grid cards" markdown>

-   :material-ruler-square:{ .lg .middle } **How Validation Works**

    ---

    Understand the three-dimensional scoring system: Compliance, Trust, and Availability.

    [:octicons-arrow-right-24: Validation Process](concepts/validation.md)

-   :material-counter:{ .lg .middle } **Understanding Scores**

    ---

    What the numbers mean and how to improve them.

    [:octicons-arrow-right-24: Scoring System](concepts/scoring.md)

-   :material-shield-check:{ .lg .middle } **Enforcement First**

    ---

    How Guard verifies requests.

    [:octicons-arrow-right-24: Enforcement Guide](guides/enforcement-first.md)

-   :material-key:{ .lg .middle } **Trust Model**

    ---

    How keys and trust stores work.

    [:octicons-arrow-right-24: Trust Model](concepts/trust-model.md)

</div>

---

## :material-book-open-variant: Reference Documentation

Complete API documentation for every package in the ecosystem.

<div class="grid cards" markdown>

-   :material-console:{ .lg .middle } **CLI Reference**

    ---

    All commands, flags, and examples.

    [:octicons-arrow-right-24: CLI Docs](reference/cli/index.md)

-   :material-language-python:{ .lg .middle } **Python SDK**

    ---

    SimpleGuard, Executor, and all classes.

    [:octicons-arrow-right-24: SDK Docs](reference/sdk-python/index.md)

-   :material-code-json:{ .lg .middle } **Agent Card Schema**

    ---

    Complete JSON Schema reference.

    [:octicons-arrow-right-24: Schema Docs](reference/agent-card-schema.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    All config options and environment variables.

    [:octicons-arrow-right-24: Config Docs](reference/configuration.md)

</div>

---

## :material-frequently-asked-questions: Common Questions

??? question "What's the difference between the CLI and SDK?"

    **CLI tools** (`capiscio` on npm/pip) are for **validation** - checking that agent cards are A2A-compliant.
    
    **The SDK** (`capiscio-sdk` on pip) is for **security** - adding cryptographic identity and request verification to your running agent.

??? question "Do I need to run the Go binary directly?"

    No! The Node.js and Python CLIs automatically download and run the correct binary for your platform. Use the wrapper that matches your development environment.

??? question "What's a compliance score of 85 mean?"

    Your agent card passes all required A2A fields and 85% of recommended best practices. See [Understanding Scores](concepts/scoring.md) for the full breakdown.

---

## :material-link: Resources

<div class="grid cards" markdown>

-   :fontawesome-brands-github:{ .lg .middle } **GitHub**

    ---

    Source code, issues, and discussions.

    [:octicons-arrow-right-24: github.com/capiscio](https://github.com/capiscio)

-   :material-file-document:{ .lg .middle } **A2A Specification**

    ---

    The official Agent-to-Agent protocol spec.

    [:octicons-arrow-right-24: A2A Project](https://github.com/a2aproject/A2A)

-   :material-help-circle:{ .lg .middle } **Get Help**

    ---

    Found a bug? Need help?

    [:octicons-arrow-right-24: Open an Issue](https://github.com/capiscio/capiscio-core/issues/new)

</div>
