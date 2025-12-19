---
title: "Step 4: PR Comments"
description: Add validation results as PR comments
---

# Step 4: PR Comments

Make validation results visible to PR reviewers by adding automated comments.

---

## Add PR Comments

Update your workflow to post validation results:

```yaml title=".github/workflows/validate-agent.yml"
name: Validate A2A Agent

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write  # Required for posting comments

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
      
      - name: Post PR Comment
        uses: actions/github-script@v7
        with:
          script: |
            const result = '${{ steps.validate.outputs.result }}';
            const compliance = '${{ steps.validate.outputs.compliance-score }}';
            const trust = '${{ steps.validate.outputs.trust-score }}';
            const availability = '${{ steps.validate.outputs.availability-score }}';
            const prodReady = '${{ steps.validate.outputs.production-ready }}';
            const errors = '${{ steps.validate.outputs.error-count }}';
            const warnings = '${{ steps.validate.outputs.warning-count }}';
            
            const icon = result === 'passed' ? '✅' : '❌';
            const prodIcon = prodReady === 'true' ? '✅' : '⚠️';
            
            const body = `## ${icon} A2A Agent Validation
            
            | Metric | Score |
            |--------|-------|
            | **Compliance** | ${compliance}/100 |
            | **Trust** | ${trust}/100 |
            | **Availability** | ${availability} |
            | **Production Ready** | ${prodIcon} ${prodReady} |
            
            **Issues:** ${errors} errors, ${warnings} warnings
            
            ---
            *Validated with [CapiscIO](https://docs.capisc.io)*`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

---

## Example PR Comment

When the workflow runs, it will post a comment like this:

> ## ✅ A2A Agent Validation
> 
> | Metric | Score |
> |--------|-------|
> | **Compliance** | 85/100 |
> | **Trust** | 0/100 |
> | **Availability** | not-tested |
> | **Production Ready** | ⚠️ false |
> 
> **Issues:** 0 errors, 2 warnings
> 
> ---
> *Validated with [CapiscIO](https://docs.capisc.io)*

---

## Update Comments Instead of Creating New Ones

To avoid comment spam on multiple commits, update the existing comment:

```yaml title=".github/workflows/validate-agent.yml"
- name: Find Existing Comment
  uses: peter-evans/find-comment@v2
  id: find-comment
  with:
    issue-number: ${{ github.event.pull_request.number }}
    comment-author: 'github-actions[bot]'
    body-includes: 'A2A Agent Validation'

- name: Create or Update PR Comment
  uses: peter-evans/create-or-update-comment@v3
  with:
    comment-id: ${{ steps.find-comment.outputs.comment-id }}
    issue-number: ${{ github.event.pull_request.number }}
    edit-mode: replace
    body: |
      ## ${{ steps.validate.outputs.result == 'passed' && '✅' || '❌' }} A2A Agent Validation
      
      | Metric | Score |
      |--------|-------|
      | **Compliance** | ${{ steps.validate.outputs.compliance-score }}/100 |
      | **Trust** | ${{ steps.validate.outputs.trust-score }}/100 |
      | **Availability** | ${{ steps.validate.outputs.availability-score }} |
      
      **Production Ready:** ${{ steps.validate.outputs.production-ready }}
      **Issues:** ${{ steps.validate.outputs.error-count }} errors, ${{ steps.validate.outputs.warning-count }} warnings
      
      ---
      *Validated with [CapiscIO](https://docs.capisc.io) • Updated: ${{ github.event.head_commit.timestamp || 'now' }}*
```

---

## Add Check Run Summary

For a cleaner look in the PR Checks tab:

```yaml title=".github/workflows/validate-agent.yml"
- name: Validate Agent Card
  id: validate
  uses: capiscio/validate-a2a@v1
  with:
    agent-card: './agent-card.json'

- name: Create Check Summary
  run: |
    echo "## 🔍 A2A Agent Validation Results" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "| Dimension | Score |" >> $GITHUB_STEP_SUMMARY
    echo "|-----------|-------|" >> $GITHUB_STEP_SUMMARY
    echo "| Compliance | ${{ steps.validate.outputs.compliance-score }}/100 |" >> $GITHUB_STEP_SUMMARY
    echo "| Trust | ${{ steps.validate.outputs.trust-score }}/100 |" >> $GITHUB_STEP_SUMMARY
    echo "| Availability | ${{ steps.validate.outputs.availability-score }} |" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    if [ "${{ steps.validate.outputs.production-ready }}" == "true" ]; then
      echo "✅ **Agent is production ready!**" >> $GITHUB_STEP_SUMMARY
    else
      echo "⚠️ **Agent is NOT production ready**" >> $GITHUB_STEP_SUMMARY
    fi
```

This creates a summary visible in the Actions tab.

---

## Complete Workflow with Comments

Here's a complete workflow with all features:

```yaml title=".github/workflows/validate-agent.yml"
name: Validate A2A Agent

on:
  pull_request:
    branches: [main]
    paths:
      - 'agent-card.json'

permissions:
  contents: read
  pull-requests: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Validate Agent Card
        id: validate
        uses: capiscio/validate-a2a@v1
        with:
          agent-card: './agent-card.json'
      
      - name: Create Summary
        run: |
          echo "## 🔍 Validation Results" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Result | ${{ steps.validate.outputs.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Compliance | ${{ steps.validate.outputs.compliance-score }}/100 |" >> $GITHUB_STEP_SUMMARY
          echo "| Trust | ${{ steps.validate.outputs.trust-score }}/100 |" >> $GITHUB_STEP_SUMMARY
          echo "| Availability | ${{ steps.validate.outputs.availability-score }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Errors | ${{ steps.validate.outputs.error-count }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Warnings | ${{ steps.validate.outputs.warning-count }} |" >> $GITHUB_STEP_SUMMARY
      
      - name: Find Comment
        uses: peter-evans/find-comment@v2
        id: fc
        with:
          issue-number: ${{ github.event.pull_request.number }}
          comment-author: 'github-actions[bot]'
          body-includes: 'A2A Agent Validation'
      
      - name: Post or Update Comment
        uses: peter-evans/create-or-update-comment@v3
        with:
          comment-id: ${{ steps.fc.outputs.comment-id }}
          issue-number: ${{ github.event.pull_request.number }}
          edit-mode: replace
          body: |
            ## ${{ steps.validate.outputs.result == 'passed' && '✅' || '❌' }} A2A Agent Validation
            
            | Dimension | Score | Status |
            |-----------|-------|--------|
            | Compliance | ${{ steps.validate.outputs.compliance-score }}/100 | ${{ steps.validate.outputs.compliance-score >= 80 && '✅' || '⚠️' }} |
            | Trust | ${{ steps.validate.outputs.trust-score }}/100 | ${{ steps.validate.outputs.trust-score >= 60 && '✅' || '⚠️' }} |
            | Availability | ${{ steps.validate.outputs.availability-score }} | - |
            
            **Production Ready:** ${{ steps.validate.outputs.production-ready == 'true' && '✅ Yes' || '❌ No' }}
            
            <details>
            <summary>Issue counts</summary>
            
            - Errors: ${{ steps.validate.outputs.error-count }}
            - Warnings: ${{ steps.validate.outputs.warning-count }}
            
            </details>
            
            ---
            <sub>Validated with [CapiscIO](https://docs.capisc.io) • [View logs](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})</sub>
```

---

## What's Next?

You now have:

- [x] Automated PR comments
- [x] Updateable comments (no spam)
- [x] GitHub Actions summaries
- [x] Clickable links to logs

Let's explore advanced patterns like matrix testing!

<div class="nav-buttons" markdown>
[:material-arrow-left: Back](3-thresholds.md){ .md-button }
[Continue :material-arrow-right:](5-matrix.md){ .md-button .md-button--primary }
</div>
