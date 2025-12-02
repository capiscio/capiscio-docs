---
title: Quickstarts
description: Get started with CapiscIO in 5 minutes
---

# Quickstarts

Choose your path to get started with CapiscIO. Each quickstart takes about 5 minutes and gets you to a working result.

## Choose Your Goal

| Quickstart | Description | Time | Difficulty |
|------------|-------------|------|------------|
| [**Validate Your First Agent**](validate/1-intro.md) | Check if an AI agent is A2A compliant | ~5 min | :material-star: Easy |
| [**Secure a FastAPI Agent**](secure/1-intro.md) | Add authentication to your A2A agent | ~10 min | :material-star::material-star: Medium |
| [**CI/CD with GitHub Actions**](cicd/1-intro.md) | Automate validation in your workflows | ~5 min | :material-star: Easy |

---

## What You'll Learn

<div class="grid cards" markdown>

-   :material-check-circle:{ .lg .middle } **Validation Quickstart**

    ---

    - Install the CapiscIO CLI
    - Validate a local agent-card.json
    - Understand validation reports
    - Check compliance scores

    [:octicons-arrow-right-24: Start Validating](validate/1-intro.md)

-   :material-shield-lock:{ .lg .middle } **Security Quickstart**

    ---

    - Add SimpleGuard to your agent
    - Generate cryptographic keys
    - Sign outbound requests
    - Verify inbound requests

    [:octicons-arrow-right-24: Start Securing](secure/1-intro.md)

-   :material-github:{ .lg .middle } **CI/CD Quickstart**

    ---

    - Add the GitHub Action
    - Configure validation thresholds
    - Add PR comments
    - Block non-compliant deployments

    [:octicons-arrow-right-24: Start Automating](cicd/1-intro.md)

</div>

---

## Prerequisites

Before starting any quickstart, make sure you have:

=== "For CLI Quickstarts"

    - **Node.js 18+** or **Python 3.10+** installed
    - A terminal/command line
    - An agent-card.json file (we'll provide a sample)

=== "For SDK Quickstart"

    - **Python 3.10+** installed
    - A FastAPI or similar web application
    - Basic understanding of async Python

=== "For CI/CD Quickstart"

    - A GitHub repository
    - Basic understanding of GitHub Actions

---

## Sample Agent Card

Don't have an agent-card.json yet? Use this sample to follow along:

```json title="agent-card.json"
{
  "name": "My First Agent",
  "description": "A sample A2A agent for testing",
  "url": "https://example.com/agent",
  "version": "1.0.0",
  "protocolVersion": "0.2.0",
  "provider": {
    "organization": "My Company"
  },
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "greeting",
      "name": "Greeting",
      "description": "Returns a friendly greeting"
    }
  ]
}
```

Save this as `agent-card.json` in your working directory to use in the quickstarts.

---

## Next Steps After Quickstarts

Once you've completed a quickstart, explore:

- [**Concepts**](../concepts/validation.md) — Deep dive into how CapiscIO works
- [**Recipes**](../recipes/index.md) — Practical solutions for specific problems
- [**Troubleshooting**](../troubleshooting.md) — Solutions to common problems
