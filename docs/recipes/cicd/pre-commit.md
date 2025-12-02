---
title: Pre-commit Hook
description: Validate agent cards before every commit
---

# Pre-commit Hook

Catch agent card issues before they reach your repository.

---

## Problem

You want to:

- Prevent invalid agent cards from being committed
- Get instant feedback during development
- Enforce standards without manual checks
- Share validation rules with the team

---

## Solution: pre-commit Framework

### 1. Install pre-commit

```bash
pip install pre-commit
```

### 2. Create Configuration

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card
        name: Validate Agent Card
        entry: capiscio validate
        language: system
        files: agent-card\.json$
        pass_filenames: true
```

### 3. Install the Hook

```bash
pre-commit install
```

### 4. Test It

```bash
# Make a change to agent-card.json
echo '{}' > agent-card.json
git add agent-card.json
git commit -m "test"

# Hook will fail with validation errors!
```

---

## Configuration Options

### Basic Validation

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card
        name: Validate Agent Card
        entry: capiscio validate
        language: system
        files: agent-card\.json$
        pass_filenames: true
```

### Strict Validation

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card-strict
        name: Validate Agent Card (Strict)
        entry: capiscio validate --strict
        language: system
        files: agent-card\.json$
        pass_filenames: true
```

### Schema-Only (Fast)

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card
        name: Validate Agent Card Schema
        entry: capiscio validate --schema-only
        language: system
        files: agent-card\.json$
        pass_filenames: true
```

---

## Multiple Agent Cards

For monorepos with multiple agents:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-cards
        name: Validate All Agent Cards
        entry: capiscio validate
        language: system
        files: (agent-card\.json|agent-card\..+\.json)$
        pass_filenames: true
```

This matches:
- `agent-card.json`
- `agent-card.staging.json`
- `agent-card.production.json`
- `apps/foo/agent-card.json`

---

## Using Node CLI

If you prefer the Node.js CLI:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card
        name: Validate Agent Card
        entry: npx capiscio validate
        language: system
        files: agent-card\.json$
        pass_filenames: true
```

---

## Husky Alternative (Node.js Projects)

For npm/yarn projects, use Husky:

### 1. Install Husky

```bash
npm install --save-dev husky
npx husky init
```

### 2. Add Hook

```bash title=".husky/pre-commit"
#!/bin/sh

# Find and validate all agent cards
for card in $(git diff --cached --name-only | grep 'agent-card.*\.json$'); do
  echo "Validating: $card"
  npx capiscio validate "$card" || exit 1
done
```

### 3. Make Executable

```bash
chmod +x .husky/pre-commit
```

---

## lint-staged Alternative

For more granular control with lint-staged:

```json title="package.json"
{
  "lint-staged": {
    "agent-card*.json": [
      "npx capiscio validate"
    ]
  }
}
```

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: lint-staged
        name: lint-staged
        entry: npx lint-staged
        language: system
        pass_filenames: false
```

---

## Skip Hook When Needed

Sometimes you need to commit despite validation errors:

```bash
# Skip all hooks
git commit --no-verify -m "WIP: fixing agent card"

# Skip specific hook (pre-commit framework)
SKIP=validate-agent-card git commit -m "WIP"
```

---

## Team Setup

Add instructions to your README:

```markdown title="README.md"
## Development Setup

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install hooks:
   ```bash
   pre-commit install
   ```

Agent card validation runs automatically on every commit.
```

---

## CI Backup

Pre-commit hooks can be skipped. Add CI validation as a safety net:

```yaml title=".github/workflows/validate.yml"
name: Validate

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

---

## Common Issues

??? question "Hook not running?"
    
    Make sure hooks are installed:
    ```bash
    pre-commit install
    ```
    
    Verify the config:
    ```bash
    pre-commit run --all-files
    ```

??? question "CLI not found?"
    
    Ensure the CLI is installed globally or in your PATH:
    ```bash
    which capiscio
    # or
    which npx
    ```

??? question "Wrong file matched?"
    
    Test your regex pattern:
    ```bash
    pre-commit run validate-agent-card --files path/to/agent-card.json
    ```

---

## See Also

- [CI/CD Quickstart](../../quickstarts/cicd/1-intro.md) — Full CI setup
- [Schema-Only Mode](../validation/schema-only.md) — Fast validation
- [Strict Mode](../validation/strict-mode.md) — Production standards
