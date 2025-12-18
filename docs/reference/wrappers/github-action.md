# GitHub Action

> **Validate A2A agents in your CI/CD pipeline with `validate-a2a`**

The **CapiscIO GitHub Action** (`validate-a2a`) automatically validates your Agent-to-Agent (A2A) Protocol implementation in GitHub Actions workflows.

---

## Quick Start

```yaml
- name: Validate Agent Card
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
```

---

## Features

- ✅ **Schema validation** against A2A specification
- 📊 **Three-dimensional scoring** (compliance, trust, availability)
- 🔐 **Cryptographic verification** of JWS signatures
- 🌐 **Live endpoint testing** (optional)
- 📝 **PR comments** with validation results

---

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `agent-card` | Path to agent-card.json or URL | No | `./agent-card.json` |
| `strict` | Enable strict validation mode | No | `false` |
| `test-live` | Test live agent endpoint | No | `false` |
| `skip-signature` | Skip JWS signature verification | No | `false` |
| `timeout` | Request timeout in milliseconds | No | `10000` |
| `fail-on-warnings` | Fail if there are warnings | No | `false` |

---

## Outputs

| Output | Description |
|--------|-------------|
| `result` | `"passed"` or `"failed"` |
| `compliance-score` | Compliance score (0-100) |
| `trust-score` | Trust score (0-100) |
| `availability-score` | Availability score (0-100) or `"not-tested"` |
| `production-ready` | `"true"` or `"false"` |
| `error-count` | Number of validation errors |
| `warning-count` | Number of validation warnings |

---

## Examples

### Basic Validation

```yaml
name: Validate Agent

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Agent Card
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
```

### Strict Mode with Score Thresholds

```yaml
- name: Validate Agent Card
  id: validate
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
    strict: 'true'
    
- name: Check Production Readiness
  run: |
    if [ "${{ steps.validate.outputs.production-ready }}" != "true" ]; then
      echo "❌ Agent not production ready"
      echo "Compliance: ${{ steps.validate.outputs.compliance-score }}"
      echo "Trust: ${{ steps.validate.outputs.trust-score }}"
      exit 1
    fi
```

### Live Endpoint Testing

```yaml
- name: Validate Live Agent
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: 'https://my-agent.example.com/.well-known/agent.json'
    test-live: 'true'
    timeout: '30000'
```

### Matrix Testing Multiple Agents

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent: [agent-a.json, agent-b.json, agent-c.json]
    steps:
      - uses: actions/checkout@v4
      - name: Validate ${{ matrix.agent }}
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './${{ matrix.agent }}'
          strict: 'true'
```

---

## Production Readiness

The `production-ready` output is `"true"` when:

- **Compliance score** ≥ 95
- **Trust score** ≥ 60
- **No validation errors**

Use this for deployment gates:

```yaml
- name: Deploy
  if: steps.validate.outputs.production-ready == 'true'
  run: ./deploy.sh
```

---

## See Also

- [:octicons-arrow-right-24: CI/CD Guide](../../getting-started/cicd/1-intro.md) — Step-by-step CI/CD guide
- [:octicons-arrow-right-24: CLI Reference](../cli/index.md) — Use CLI directly in workflows
- [:octicons-arrow-right-24: Python Wrapper](python.md) — Alternative: pip install
- [:octicons-arrow-right-24: Node.js Wrapper](node.md) — Alternative: npm install
