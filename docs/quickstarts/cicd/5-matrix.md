---
title: "Step 5: Matrix Testing"
description: Validate multiple agents across environments
---

# Step 5: Matrix Testing

Scale your CI/CD to validate multiple agents and configurations in parallel.

---

## Why Matrix Testing?

If you have multiple agents or environments:

- **Multi-agent repositories** - Validate all agents in one workflow
- **Environment-specific cards** - Test staging vs production configs
- **Different validation modes** - Strict for production, lenient for development

---

## Basic Matrix Strategy

Validate multiple agent cards in parallel:

```yaml title=".github/workflows/validate-agents.yml"
name: Validate All Agents

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false  # Continue validating other agents if one fails
      matrix:
        agent:
          - path: './agents/assistant/agent-card.json'
            name: 'Assistant Agent'
          - path: './agents/analyzer/agent-card.json'
            name: 'Analyzer Agent'
          - path: './agents/orchestrator/agent-card.json'
            name: 'Orchestrator Agent'
    
    name: Validate ${{ matrix.agent.name }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate ${{ matrix.agent.name }}
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.agent.path }}
      
      - name: Report Result
        run: |
          echo "## ${{ matrix.agent.name }}" >> $GITHUB_STEP_SUMMARY
          echo "- Result: ${{ steps.validate.outputs.result }}" >> $GITHUB_STEP_SUMMARY
          echo "- Compliance: ${{ steps.validate.outputs.compliance-score }}/100" >> $GITHUB_STEP_SUMMARY
```

---

## Environment-Specific Validation

Different thresholds for different environments:

```yaml title=".github/workflows/validate-agents.yml"
jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - environment: staging
            agent-card: './agent-card.staging.json'
            strict: false
            test-live: false
            min-compliance: 60
          
          - environment: production
            agent-card: './agent-card.json'
            strict: true
            test-live: true
            min-compliance: 85
    
    name: Validate (${{ matrix.environment }})
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate Agent
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.agent-card }}
          strict: ${{ matrix.strict }}
          test-live: ${{ matrix.test-live }}
      
      - name: Check Compliance Threshold
        if: steps.validate.outputs.compliance-score < matrix.min-compliance
        run: |
          echo "::error::${{ matrix.environment }} compliance score (${{ steps.validate.outputs.compliance-score }}) below minimum (${{ matrix.min-compliance }})"
          exit 1
```

---

## Auto-Discover Agent Cards

Dynamically find all agent cards in your repo:

```yaml title=".github/workflows/validate-all.yml"
name: Validate All Agents

on:
  pull_request:
    paths:
      - '**/agent-card.json'
      - '**/agent-card.*.json'

jobs:
  discover:
    runs-on: ubuntu-latest
    outputs:
      agents: ${{ steps.find.outputs.agents }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Find Agent Cards
        id: find
        run: |
          agents=$(find . -name 'agent-card*.json' -type f | jq -R -s -c 'split("\n")[:-1]')
          echo "agents=$agents" >> $GITHUB_OUTPUT
          echo "Found agents: $agents"
  
  validate:
    needs: discover
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        agent: ${{ fromJson(needs.discover.outputs.agents) }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate ${{ matrix.agent }}
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.agent }}
```

---

## Consolidated PR Comment

Post a single summary comment for all agents:

```yaml title=".github/workflows/validate-all.yml"
jobs:
  validate:
    # ... matrix job from above ...
    outputs:
      result-${{ strategy.job-index }}: ${{ steps.validate.outputs.result }}
      score-${{ strategy.job-index }}: ${{ steps.validate.outputs.compliance-score }}
  
  summary:
    needs: validate
    runs-on: ubuntu-latest
    if: always() && github.event_name == 'pull_request'
    steps:
      - name: Create Summary Comment
        uses: actions/github-script@v7
        with:
          script: |
            const jobs = ${{ toJson(needs.validate) }};
            
            let body = '## 🔍 A2A Agent Validation Summary\n\n';
            body += '| Agent | Result | Compliance |\n';
            body += '|-------|--------|------------|\n';
            
            // Parse results from matrix jobs
            for (const [key, value] of Object.entries(jobs.outputs || {})) {
              if (key.startsWith('result-')) {
                const index = key.replace('result-', '');
                const result = value;
                const score = jobs.outputs[`score-${index}`] || 'N/A';
                const icon = result === 'passed' ? '✅' : '❌';
                body += `| Agent ${index} | ${icon} ${result} | ${score}/100 |\n`;
              }
            }
            
            body += '\n---\n*Validated with [CapiscIO](https://docs.capisc.io)*';
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

---

## Monorepo Pattern

For monorepos with agents in different packages:

```yaml title=".github/workflows/validate-monorepo.yml"
name: Validate Monorepo Agents

on:
  pull_request:
    branches: [main]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      agents: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v4
      
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            agent-a:
              - 'packages/agent-a/**'
            agent-b:
              - 'packages/agent-b/**'
            agent-c:
              - 'packages/agent-c/**'
  
  validate:
    needs: changes
    if: needs.changes.outputs.agents != '[]'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        agent: ${{ fromJson(needs.changes.outputs.agents) }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate ${{ matrix.agent }}
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './packages/${{ matrix.agent }}/agent-card.json'
```

---

## Complete Multi-Agent Workflow

Here's a production-ready workflow with all features:

```yaml title=".github/workflows/validate-all-agents.yml"
name: Validate All A2A Agents

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'  # Weekly Monday 9am

permissions:
  contents: read
  pull-requests: write

jobs:
  # 1. Discover all agent cards
  discover:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.discover.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      
      - name: Discover Agents
        id: discover
        run: |
          # Find all agent cards
          agents=$(find . -name 'agent-card.json' -o -name 'agent-card.*.json' | while read f; do
            dir=$(dirname "$f")
            name=$(basename "$dir")
            echo "{\"path\":\"$f\",\"name\":\"$name\"}"
          done | jq -s -c '.')
          
          echo "matrix={\"include\":$agents}" >> $GITHUB_OUTPUT

  # 2. Validate each agent in parallel
  validate:
    needs: discover
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: ${{ fromJson(needs.discover.outputs.matrix) }}
    
    name: 🔍 ${{ matrix.name }}
    
    outputs:
      results: ${{ steps.collect.outputs.results }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: ${{ matrix.path }}
          strict: ${{ github.ref == 'refs/heads/main' }}
      
      - name: Step Summary
        run: |
          echo "### ${{ matrix.name }}" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Result | ${{ steps.validate.outputs.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Compliance | ${{ steps.validate.outputs.compliance-score }}/100 |" >> $GITHUB_STEP_SUMMARY
          echo "| Trust | ${{ steps.validate.outputs.trust-score }}/100 |" >> $GITHUB_STEP_SUMMARY
          echo "| Production Ready | ${{ steps.validate.outputs.production-ready }} |" >> $GITHUB_STEP_SUMMARY

  # 3. Post consolidated summary
  report:
    needs: [discover, validate]
    if: always() && github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Post PR Summary
        uses: actions/github-script@v7
        with:
          script: |
            const body = `## 🔍 A2A Validation Complete
            
            All agent cards have been validated. Check the individual job summaries for detailed results.
            
            | Job | Status |
            |-----|--------|
            ${Object.entries(JSON.parse('${{ toJson(needs.validate) }}')).map(([k,v]) => 
              `| ${k} | ${v.result === 'success' ? '✅' : '❌'} |`
            ).join('\n')}
            
            ---
            *Powered by [CapiscIO](https://docs.capisc.io)*`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body
            });
```

---

## 🎉 Quickstart Complete!

Congratulations! You've learned how to:

- [x] Add validation to your CI/CD pipeline
- [x] Configure thresholds and enforce quality gates
- [x] Post PR comments with validation results
- [x] Scale with matrix testing for multiple agents

---

## What's Next?

<div class="grid cards" markdown>

-   :material-security:{ .lg .middle } **Add Security**

    ---

    Cryptographically sign your agent cards

    [:octicons-arrow-right-24: Secure Quickstart](../secure/1-intro.md)

-   :material-book-open-variant:{ .lg .middle } **API Reference**

    ---

    Explore all validation options

    [:octicons-arrow-right-24: Python SDK Reference](../../reference/sdk-python/index.md)

-   :material-chef-hat:{ .lg .middle } **Recipes**

    ---

    Real-world CI/CD patterns

    [:octicons-arrow-right-24: CI/CD Recipes](../../recipes/index.md)

-   :material-help-circle:{ .lg .middle } **Troubleshooting**

    ---

    Common CI/CD issues and fixes

    [:octicons-arrow-right-24: Troubleshooting Guide](../../troubleshooting.md)

</div>

---

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](4-comments.md){ .md-button }
[:material-home: Quickstarts](../index.md){ .md-button .md-button--primary }
</div>
