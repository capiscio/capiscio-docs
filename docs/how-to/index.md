---
title: How-To Guides
description: Task-oriented guides for common CapiscIO tasks. Copy-paste solutions that work.
---

# How-To Guides

Task-oriented guides for specific problems. Each guide is self-contained with copy-paste code.

---

## :material-check-all: Validation

| Guide | What You'll Do | Time |
|-------|----------------|------|
| [Validate from URL](validation/validate-url.md) | Validate a remote agent card | 2 min |
| [Bulk Validation](validation/bulk-validate.md) | Validate multiple agents at once | 5 min |
| [Schema-Only Mode](validation/schema-only.md) | Quick syntax check without live testing | 2 min |
| [Strict Mode](validation/strict-mode.md) | Enforce all best practices for production | 3 min |
| [Custom Timeout](validation/custom-timeout.md) | Handle slow endpoints | 2 min |

---

## :material-shield-lock: Security

| Guide | What You'll Do | Time |
|-------|----------------|------|
| [Sign Outbound Requests](security/sign-outbound.md) | Add JWS signatures to A2A calls | 5 min |
| [Verify Inbound Requests](security/verify-inbound.md) | Validate incoming JWS signatures | 5 min |
| [Trust Badges](security/badges.md) | Request and use trust badges | 10 min |
| [Badge Keeper](security/badge-keeper.md) | Auto-renew badges before expiry | 5 min |
| [Security Gateway](security/gateway-setup.md) | Deploy a trust-enforcing gateway | 15 min |
| [Dev Mode](security/dev-mode.md) | Security features in development | 3 min |
| [Key Rotation](security/key-rotation.md) | Rotate keys without downtime | 10 min |
| [Trust Store](security/trust-store.md) | Configure which agents to trust | 5 min |

---

## :material-puzzle: Integrations

| Guide | What You'll Do | Time |
|-------|----------------|------|
| [FastAPI](integrations/fastapi.md) | Add CapiscIO middleware to FastAPI | 5 min |
| [Flask](integrations/flask.md) | Add CapiscIO to Flask apps | 5 min |
| [Express.js](integrations/express.md) | Add CapiscIO to Express | 5 min |
| [LangChain](integrations/langchain.md) | Secure a LangChain agent | 10 min |

---

## :material-tools: MCP Guard

| Guide | What You'll Do | Time |
|-------|----------------|------|
| [Protect MCP Tools](../mcp-guard/guides/server-side.md) | Add `@guard` decorator to MCP tools | 5 min |
| [Verify MCP Servers](../mcp-guard/guides/client-side.md) | Verify server identity before connecting | 5 min |
| [Evidence Logging](../mcp-guard/guides/evidence.md) | Log tool calls for compliance | 5 min |
| [MCP SDK Integration](../mcp-guard/guides/mcp-integration.md) | Integrate with official MCP SDK | 10 min |

---

## :material-pipe: CI/CD

| Guide | What You'll Do | Time |
|-------|----------------|------|
| [Pre-commit Hook](cicd/pre-commit.md) | Validate before every commit | 3 min |
| [GitLab CI](cicd/gitlab-ci.md) | Validate agents in GitLab pipelines | 5 min |
| [Jenkins](cicd/jenkins.md) | Validate agents in Jenkins | 5 min |

---

## Guide Format

Every guide follows the same structure:

1. **Problem** — What you're trying to do
2. **Solution** — Copy-paste code that works
3. **How It Works** — Brief explanation
4. **See Also** — Related guides and references

---

## Can't Find What You Need?

<div class="grid cards" markdown>

-   :material-lightbulb:{ .lg .middle } **Request a Guide**

    ---

    Open an issue to suggest a new how-to guide.

    [:octicons-arrow-right-24: Request Guide](https://github.com/capiscio/capiscio-docs/issues/new?template=howto-request.md)

-   :material-account-plus:{ .lg .middle } **Contribute**

    ---

    Share your solutions with the community.

    [:octicons-arrow-right-24: Contributing Guide](../community/contributing.md)

</div>
