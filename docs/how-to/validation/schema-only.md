---
title: Schema-Only Validation
description: Quick syntax check without live endpoint testing
---

# Schema-Only Validation

Run a fast syntax check when you just need to verify JSON structure.

---

## Problem

You want to quickly verify that your agent card:

- Is valid JSON
- Matches the A2A JSON schema
- Has all required fields

...without waiting for live endpoint tests.

---

## Solution

=== "npm"

    ```bash
    npx capiscio validate ./agent-card.json --schema-only
    ```

=== "pip"

    ```bash
    capiscio validate ./agent-card.json --schema-only
    ```

=== "Go"

    ```bash
    capiscio-core validate ./agent-card.json --schema-only
    ```

---

## What Gets Skipped

| Check | Schema-Only | Full Validation |
|-------|-------------|-----------------|
| JSON syntax | ✅ | ✅ |
| Schema compliance | ✅ | ✅ |
| Required fields | ✅ | ✅ |
| Recommended fields | ✅ | ✅ |
| Endpoint reachability | ❌ | ✅ |
| Response format | ❌ | ✅ |
| Trust score | ❌ | ✅ |
| Availability score | ❌ | ✅ |

---

## Speed Comparison

```bash
# Full validation (with network)
$ time capiscio validate ./agent-card.json --test-live
real    0m2.341s  # Depends on network

# Schema-only validation
$ time capiscio validate ./agent-card.json --schema-only
real    0m0.087s  # Nearly instant
```

---

## Use Cases

### 1. Pre-commit Hook

Fast validation before every commit:

```yaml title=".pre-commit-config.yaml"
repos:
  - repo: local
    hooks:
      - id: validate-agent-card
        name: Validate Agent Card
        entry: capiscio validate ./agent-card.json --schema-only
        language: system
        pass_filenames: false
        files: agent-card\.json$
```

### 2. Editor Integration

Run on save in VS Code:

```json title=".vscode/tasks.json"
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Validate Agent Card",
      "type": "shell",
      "command": "capiscio validate ${file} --schema-only",
      "presentation": { "reveal": "silent" },
      "problemMatcher": []
    }
  ]
}
```

### 3. Development Workflow

During rapid iteration:

```bash
# Watch mode with schema-only for speed
watch -n 1 'capiscio validate ./agent-card.json --schema-only --errors-only'
```

---

## Combine with Other Flags

Schema-only works with other flags:

```bash
# Schema-only with JSON output for parsing
capiscio validate ./agent-card.json --schema-only --json

# Schema-only with strict mode
capiscio validate ./agent-card.json --schema-only --strict
```

---

## When NOT to Use

Don't use schema-only when you need:

- ❌ Availability score (requires live testing)
- ❌ Trust score verification (requires signature checks)
- ❌ Production readiness assessment
- ❌ Full compliance score

---

## See Also

- [Strict Mode](strict-mode.md) — Full validation with strict rules
- [Pre-commit Hook](../cicd/pre-commit.md) — Validate before commits
- [Troubleshooting](../../troubleshooting.md) — Common issues and fixes
