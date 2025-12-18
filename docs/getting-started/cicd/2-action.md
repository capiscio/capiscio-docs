---
title: "Step 2: Add the Action"
description: Add the validate-a2a GitHub Action to your workflow
---

# Step 2: Add the Action

Let's add the CapiscIO validation action to your GitHub repository.

---

## Create the Workflow File

Create `.github/workflows/validate-agent.yml`:

```yaml title=".github/workflows/validate-agent.yml"
name: Validate A2A Agent

on:
  push:
    branches: [main]
    paths:
      - 'agent-card.json'
  pull_request:
    branches: [main]
    paths:
      - 'agent-card.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Validate Agent Card
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
```

That's it! This workflow will:

1. Run on pushes to `main` that modify `agent-card.json`
2. Run on PRs to `main` that modify `agent-card.json`
3. Validate the agent card and report results

---

## Test It

Commit and push the workflow:

```bash
git add .github/workflows/validate-agent.yml
git commit -m "Add A2A agent validation"
git push
```

Now make a change to your `agent-card.json` (or create one if you don't have it):

```bash
# Create a sample agent card
cat > agent-card.json << 'EOF'
{
  "name": "My Agent",
  "description": "A sample A2A agent",
  "url": "https://example.com/agent",
  "version": "1.0.0",
  "protocolVersion": "0.2.0",
  "provider": {
    "organization": "My Company"
  },
  "capabilities": {
    "streaming": false
  },
  "skills": [
    {
      "id": "greeting",
      "name": "Greeting",
      "description": "Returns a greeting"
    }
  ]
}
EOF

git add agent-card.json
git commit -m "Add agent card"
git push
```

Check the Actions tab in your GitHub repository to see the validation run!

---

## Understanding the Output

When the action runs, you'll see output like:

```
✅ A2A AGENT VALIDATION PASSED
Score: 75/100
Version: 0.2.0
Agent passed with warnings

ISSUES FOUND:
⚠️ [MISSING_OPTIONAL_FIELD] warning: Missing recommended field 'authentication'
```

The action sets these outputs for use in subsequent steps:

| Output | Description | Example |
|--------|-------------|---------|
| `result` | "passed" or "failed" | "passed" |
| `compliance-score` | 0-100 | "75" |
| `trust-score` | 0-100 | "0" |
| `availability-score` | 0-100 or "not-tested" | "not-tested" |
| `production-ready` | "true" or "false" | "false" |
| `error-count` | Number of errors | "0" |
| `warning-count` | Number of warnings | "2" |

---

## Action Inputs

The action accepts these inputs:

| Input | Default | Description |
|-------|---------|-------------|
| `agent-card` | `./agent-card.json` | Path or URL to validate |
| `strict` | `false` | Enable strict validation mode |
| `test-live` | `false` | Test live agent endpoint |
| `skip-signature` | `false` | Skip JWS signature verification |
| `timeout` | `10000` | Request timeout in milliseconds |
| `fail-on-warnings` | `false` | Fail if there are warnings |

---

## Running on All Pushes

To run on every push (not just when agent-card.json changes):

```yaml title=".github/workflows/validate-agent.yml" hl_lines="4-6"
name: Validate A2A Agent

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
```

---

## Validating from URL

If your agent card is hosted:

```yaml
- uses: capiscio/validate-a2a@v1
  with:
    agent-card: 'https://myagent.example.com/.well-known/agent-card.json'
```

---

## What's Next?

You now have:

- [x] GitHub Action added to your workflow
- [x] Basic validation running on pushes and PRs

Let's configure validation thresholds!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](1-intro.md){ .md-button }
[Continue :material-arrow-right:](3-thresholds.md){ .md-button .md-button--primary }
</div>
