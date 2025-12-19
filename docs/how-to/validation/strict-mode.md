---
title: Strict Mode for Production
description: Enforce all A2A best practices before deploying to production
---

# Strict Mode for Production

Use strict validation to ensure your agent card follows all A2A best practices before going live.

---

## Problem

You want to enforce the highest quality standards before deploying:

- All recommended fields should be present
- No warnings allowed
- Full compliance with A2A specification

---

## Solution

=== "npm"

    ```bash
    npx capiscio validate ./agent-card.json --strict
    ```

=== "pip"

    ```bash
    capiscio validate ./agent-card.json --strict
    ```

=== "Go"

    ```bash
    capiscio-core validate ./agent-card.json --strict
    ```

---

## What Strict Mode Does

| Normal Mode | Strict Mode |
|-------------|-------------|
| Validates required fields | Validates required AND recommended fields |
| Warnings don't fail | Warnings ARE errors |
| Flexible on optional fields | Expects completeness |
| Score threshold: pass at 60+ | Score threshold: pass at 85+ |

---

## Example Output

```bash
$ capiscio validate ./agent-card.json --strict

❌ Validation Failed (Strict Mode)

Score: 72/100 (Minimum required: 85)

Errors:
  • Missing recommended field: skills[0].inputModes
  • Missing recommended field: skills[1].outputModes
  • Provider.url should use HTTPS
  • Missing optional but recommended: version

Run without --strict to see the difference.
```

---

## CI/CD Integration

Add strict validation to your GitHub Actions:

```yaml title=".github/workflows/validate.yml"
- name: Validate (Strict)
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
    strict: true
```

---

## Progressive Strategy

Use different modes for different environments:

```yaml title=".github/workflows/validate.yml"
jobs:
  validate:
    strategy:
      matrix:
        include:
          - branch: develop
            strict: false
          - branch: main
            strict: true
    steps:
      - uses: capiscio/validate-a2a@v1
        if: github.ref == format('refs/heads/{0}', matrix.branch)
        with:
          strict: ${{ matrix.strict }}
```

---

## How It Works

Strict mode elevates the validation rules:

1. **Recommended → Required**: Fields marked "recommended" in the A2A spec are treated as required
2. **Warnings → Errors**: Any warning becomes a blocking error
3. **Higher Threshold**: The compliance score must be 85+ instead of 60+
4. **Complete Skills**: All skill fields must be fully populated

---

## See Also

- [Schema-Only Mode](schema-only.md) — Quick syntax check
- [CI/CD Guide](../../getting-started/cicd/1-intro.md) — Set up automated validation
- [Scoring System](../../concepts/scoring.md) — Understand the scores
