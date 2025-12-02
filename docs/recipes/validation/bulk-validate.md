---
title: Bulk Validation
description: Validate multiple agent cards at once
---

# Bulk Validation

Validate multiple agent cards in a single command.

---

## Problem

You have multiple agents to validate:

- Monorepo with several agents
- List of third-party agents to audit
- Migration from legacy configs

---

## Solution: Shell Loop

=== "Bash/Zsh"

    ```bash
    # Validate all agent cards in current directory
    for card in ./**/agent-card.json; do
      echo "Validating: $card"
      capiscio validate "$card"
    done
    ```

=== "PowerShell"

    ```powershell
    # Validate all agent cards in current directory
    Get-ChildItem -Recurse -Filter "agent-card.json" | ForEach-Object {
      Write-Host "Validating: $($_.FullName)"
      capiscio validate $_.FullName
    }
    ```

---

## Solution: xargs for Parallel Execution

```bash
# Find all agent cards and validate in parallel
find . -name 'agent-card.json' | xargs -P 4 -I {} capiscio validate {}
```

Options:
- `-P 4` — Run 4 validations in parallel
- `-I {}` — Replace `{}` with the filename

---

## Solution: With JSON Output

Collect all results into a single JSON file:

```bash
#!/bin/bash

echo "[" > results.json
first=true

for card in ./**/agent-card.json; do
  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> results.json
  fi
  
  capiscio validate "$card" --json >> results.json
done

echo "]" >> results.json
```

---

## Solution: From a List File

If you have a list of URLs to validate:

```bash title="agents.txt"
# Agent cards can be at any URL
https://weather-agent.example.com/agent-card.json
https://api.example.com/agents/calendar/agent-card.json
https://assistant.acme.io/agent-card.json
```

```bash
# Validate each URL
while read url; do
  echo "Validating: $url"
  capiscio validate "$url" --timeout 30000
done < agents.txt
```

---

## Summary Report

Generate a summary after bulk validation:

```bash
#!/bin/bash

passed=0
failed=0
total=0

for card in ./**/agent-card.json; do
  ((total++))
  if capiscio validate "$card" --errors-only > /dev/null 2>&1; then
    ((passed++))
    echo "✅ $card"
  else
    ((failed++))
    echo "❌ $card"
  fi
done

echo ""
echo "Summary: $passed/$total passed ($failed failed)"
```

---

## CI/CD with Matrix

For GitHub Actions, use matrix strategy:

```yaml title=".github/workflows/validate-all.yml"
name: Validate All Agents

on: [push, pull_request]

jobs:
  discover:
    runs-on: ubuntu-latest
    outputs:
      agents: ${{ steps.find.outputs.agents }}
    steps:
      - uses: actions/checkout@v4
      - id: find
        run: |
          agents=$(find . -name 'agent-card.json' | jq -R -s -c 'split("\n")[:-1]')
          echo "agents=$agents" >> $GITHUB_OUTPUT

  validate:
    needs: discover
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        agent: ${{ fromJson(needs.discover.outputs.agents) }}
    steps:
      - uses: actions/checkout@v4
      - uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.agent }}
```

---

## Performance Tips

| Technique | Use When |
|-----------|----------|
| Sequential | Small number of agents |
| `xargs -P` | Many agents, quick validation |
| Matrix strategy | CI/CD, need detailed per-agent results |
| `--schema-only` | Speed over completeness |

---

## See Also

- [CI/CD Matrix Testing](../../quickstarts/cicd/5-matrix.md) — Full matrix setup
- [Schema-Only Mode](schema-only.md) — Speed up bulk validation
- [Validate from URL](validate-url.md) — Validate remote agents
