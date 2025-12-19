---
title: "Step 3: Configure Thresholds"
description: Set up validation thresholds for your pipeline
---

# Step 3: Configure Thresholds

Now let's configure when validation should pass or fail based on your requirements.

---

## Strict Mode

For production deployments, enable strict mode:

```yaml title=".github/workflows/validate-agent.yml" hl_lines="15"
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
          strict: true
```

Strict mode:

- Requires compliance score ≥ 95
- Requires trust score ≥ 60 (if signatures present)
- Requires availability score ≥ 80 (if tested)
- Treats warnings as errors

---

## Fail on Warnings

Even without strict mode, you can fail on any warnings:

```yaml hl_lines="5"
- uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
    fail-on-warnings: true
```

---

## Custom Score Thresholds

For custom thresholds, use the action outputs with a conditional step:

```yaml title=".github/workflows/validate-agent.yml"
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
      
      - name: Validate Agent Card
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
      
      - name: Check Compliance Score
        if: ${{ steps.validate.outputs.compliance-score < 80 }}
        run: |
          echo "::error::Compliance score (${{ steps.validate.outputs.compliance-score }}) is below threshold (80)"
          exit 1
      
      - name: Check Production Readiness
        if: ${{ steps.validate.outputs.production-ready == 'false' }}
        run: |
          echo "::warning::Agent is not production ready"
          # Don't fail, just warn
```

---

## Different Thresholds for Different Branches

```yaml title=".github/workflows/validate-agent.yml"
name: Validate A2A Agent

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Strict validation for main branch
      - name: Validate (Production)
        if: github.ref == 'refs/heads/main' || github.base_ref == 'main'
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
          strict: true
      
      # Lenient validation for develop branch
      - name: Validate (Development)
        if: github.ref == 'refs/heads/develop' || github.base_ref == 'develop'
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
          strict: false
```

---

## Testing Live Endpoints

For staging/production validation, test the live endpoint:

```yaml hl_lines="5"
- uses: capiscio/validate-a2a@v1
  with:
    agent-card: 'https://staging.myagent.com/.well-known/agent-card.json'
    test-live: true
    timeout: 30000  # 30 seconds for slower endpoints
```

!!! warning "Live Testing"
    Live testing sends actual A2A messages to your agent. Only enable this for deployed endpoints, not local files.

---

## Skip Signature Verification

During development, you might not have signatures set up:

```yaml hl_lines="5"
- uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'
    skip-signature: true
```

!!! danger "Not for Production"
    Always verify signatures in production workflows. Unsigned agent cards have a trust score of 0.

---

## Complete Example: Environment-Based Validation

```yaml title=".github/workflows/validate-agent.yml"
name: Validate A2A Agent

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main, staging]

env:
  # Production thresholds
  PROD_COMPLIANCE_MIN: 95
  PROD_TRUST_MIN: 60
  # Staging thresholds
  STAGING_COMPLIANCE_MIN: 80
  STAGING_TRUST_MIN: 0

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Agent Card
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
      
      - name: Enforce Production Thresholds
        if: github.ref == 'refs/heads/main'
        run: |
          compliance=${{ steps.validate.outputs.compliance-score }}
          trust=${{ steps.validate.outputs.trust-score }}
          
          if [ "$compliance" -lt "$PROD_COMPLIANCE_MIN" ]; then
            echo "::error::Compliance score ($compliance) below production minimum ($PROD_COMPLIANCE_MIN)"
            exit 1
          fi
          
          if [ "$trust" -lt "$PROD_TRUST_MIN" ]; then
            echo "::error::Trust score ($trust) below production minimum ($PROD_TRUST_MIN)"
            exit 1
          fi
          
          echo "✅ Production thresholds met!"
      
      - name: Enforce Staging Thresholds
        if: github.ref == 'refs/heads/staging'
        run: |
          compliance=${{ steps.validate.outputs.compliance-score }}
          
          if [ "$compliance" -lt "$STAGING_COMPLIANCE_MIN" ]; then
            echo "::error::Compliance score ($compliance) below staging minimum ($STAGING_COMPLIANCE_MIN)"
            exit 1
          fi
          
          echo "✅ Staging thresholds met!"
```

---

## What's Next?

You now have:

- [x] Basic validation
- [x] Strict mode for production
- [x] Custom score thresholds
- [x] Environment-based validation

Let's add PR comments so reviewers can see results!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](2-action.md){ .md-button }
[Continue :material-arrow-right:](4-comments.md){ .md-button .md-button--primary }
</div>
