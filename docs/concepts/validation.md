# Validation

Validation is the process of checking an agent card against the A2A protocol specification and CapiscIO's trust requirements. It answers the question: *"Is this agent correctly described and ready for production?"*

---

## What Gets Validated

The CapiscIO CLI validates agent cards across seven categories:

| Category | What It Checks |
|----------|---------------|
| **Schema** | Required fields, types, structure per A2A spec |
| **Discovery** | Whether the card can be fetched from `/.well-known/agent.json` |
| **Network** | HTTPS, response times, status codes |
| **Version Compatibility** | Feature usage matches declared A2A protocol version |
| **Security** | Authentication schemes, key presence |
| **Endpoint Availability** | Whether declared URLs respond (optional) |
| **Registry Readiness** | Additional fields needed for CapiscIO registration |

---

## Validation Modes

### Progressive (Default)

Reports all findings without stopping at the first error. Suitable for iterative development — you see everything that needs fixing in one pass.

### Strict

Treats warnings as errors. Required for production deployments and CI/CD pipelines where partial compliance is unacceptable.

---

## Trust Relationship

Validation is the first step in the CapiscIO trust pipeline:

```
Validate → Register → Badge → Enforce
```

An agent that fails validation cannot register with the CapiscIO server and therefore cannot obtain a trust badge. Higher trust levels (2+) require stricter validation results.

---

## When to Validate

- **During development** — catch schema errors before deployment
- **In CI/CD** — gate deployments on validation passing (`--strict`)
- **At registration** — the server re-validates before accepting an agent
- **Periodically** — detect drift as agent capabilities change

---

## See Also

- [Validation Process Reference](../reference/cli/validation.md) — Full details on error codes, modes, and output formats
- [How-To: Validate from URL](../how-to/validation/validate-url.md) — Validate a remote agent
- [How-To: Strict Mode](../how-to/validation/strict-mode.md) — Enforce strict validation
- [Scoring](scoring.md) — How validation results affect trust scores
