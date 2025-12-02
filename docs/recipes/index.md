---
title: Recipes
description: Copy-paste solutions for common CapiscIO tasks
---

# Recipes

Real-world, copy-paste solutions for common tasks. Each recipe is self-contained and tested.

---

## :material-check-all: Validation Recipes

| Recipe | Description | Time |
|--------|-------------|------|
| [Validate from URL](validation/validate-url.md) | Validate a remote agent card | 2 min |
| [Bulk Validation](validation/bulk-validate.md) | Validate multiple agents at once | 5 min |
| [Schema-Only Mode](validation/schema-only.md) | Quick syntax check without live testing | 2 min |
| [Strict Mode for Production](validation/strict-mode.md) | Enforce all best practices | 3 min |
| [Custom Timeout](validation/custom-timeout.md) | Handle slow endpoints | 2 min |

---

## :material-shield-lock: Security Recipes

| Recipe | Description | Time |
|--------|-------------|------|
| [Sign Outbound Requests](security/sign-outbound.md) | Add JWS signatures to A2A calls | 5 min |
| [Verify Inbound Requests](security/verify-inbound.md) | Validate incoming JWS signatures | 5 min |
| [Key Rotation](security/key-rotation.md) | Rotate keys without downtime | 10 min |
| [Trust Store Setup](security/trust-store.md) | Configure which agents to trust | 5 min |
| [Dev Mode Security](security/dev-mode.md) | Use security features in development | 3 min |

---

## :material-puzzle: Integration Recipes

| Recipe | Description | Time |
|--------|-------------|------|
| [FastAPI Middleware](integrations/fastapi.md) | Add CapiscIO to FastAPI | 5 min |
| [Flask Integration](integrations/flask.md) | Add CapiscIO to Flask | 5 min |
| [Express.js Middleware](integrations/express.md) | Add CapiscIO to Express | 5 min |
| [Langchain Agent](integrations/langchain.md) | Secure a Langchain agent | 10 min |

---

## :material-pipe: CI/CD Recipes

| Recipe | Description | Time |
|--------|-------------|------|
| [GitLab CI](cicd/gitlab-ci.md) | Validate agents in GitLab CI/CD | 5 min |
| [Jenkins Pipeline](cicd/jenkins.md) | Validate agents in Jenkins | 5 min |
| [Pre-commit Hook](cicd/pre-commit.md) | Validate before every commit | 3 min |

---

## Recipe Format

Every recipe follows the same structure:

1. **Problem** — What you're trying to do
2. **Solution** — Copy-paste code
3. **How It Works** — Brief explanation
4. **See Also** — Related recipes and references

---

## Can't Find What You Need?

<div class="grid cards" markdown>

-   :material-lightbulb:{ .lg .middle } **Request a Recipe**

    ---

    Open an issue to suggest a new recipe.

    [:octicons-arrow-right-24: Request Recipe](https://github.com/capiscio/capiscio-docs/issues/new?template=recipe-request.md)

-   :material-account-plus:{ .lg .middle } **Contribute a Recipe**

    ---

    Share your solutions with the community.

    [:octicons-arrow-right-24: Contributing Guide](../community/contributing.md)

</div>
