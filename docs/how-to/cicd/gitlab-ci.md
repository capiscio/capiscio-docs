---
title: GitLab CI Integration
description: Validate agent cards in GitLab CI/CD pipelines
---

# GitLab CI Integration

Automate agent card validation in your GitLab CI/CD pipelines.

---

## Problem

You need to:

- Validate agent cards on every commit
- Block merges if validation fails
- Support multiple environments (staging, production)
- Integrate with GitLab's merge request workflow

---

## Solution: GitLab CI Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy

variables:
  # Timeout for live validation (seconds)
  VALIDATION_TIMEOUT: "10"

validate-agent-card:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate agent-card.json --strict
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

---

## Basic Configuration

### Validate Local File

```yaml
# .gitlab-ci.yml
validate-agent-card:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate agent-card.json --strict
  only:
    changes:
      - agent-card.json
```

### Validate Live URL

```yaml
validate-live-agent:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate https://myagent.example.com/.well-known/agent-card.json --test-live
  environment:
    name: production
  only:
    - main
```

---

## Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - validate
  - deploy
  - verify

variables:
  AGENT_CARD_PATH: "agent-card.json"
  PRODUCTION_URL: "https://myagent.example.com"
  STAGING_URL: "https://staging.myagent.example.com"

# Cache pip packages
.pip-cache: &pip-cache
  cache:
    key: pip-cache
    paths:
      - .pip-cache/
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

# Reusable validation template
.validate-template: &validate-template
  image: python:3.11-slim
  <<: *pip-cache
  before_script:
    - pip install capiscio

# ===== LINT STAGE =====
lint-agent-card:
  <<: *validate-template
  stage: lint
  script:
    - capiscio validate $AGENT_CARD_PATH --schema-only
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - $AGENT_CARD_PATH
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      changes:
        - $AGENT_CARD_PATH

# ===== VALIDATE STAGE =====
validate-strict:
  <<: *validate-template
  stage: validate
  script:
    - capiscio validate $AGENT_CARD_PATH --strict --json > validation-report.json
    - cat validation-report.json
  artifacts:
    paths:
      - validation-report.json
    reports:
      dotenv: validation.env
    expire_in: 1 week
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ===== DEPLOY STAGE =====
deploy-staging:
  stage: deploy
  script:
    - echo "Deploying to staging..."
    # Your deployment commands here
  environment:
    name: staging
    url: $STAGING_URL
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  script:
    - echo "Deploying to production..."
    # Your deployment commands here
  environment:
    name: production
    url: $PRODUCTION_URL
  rules:
    - if: $CI_COMMIT_TAG
  when: manual

# ===== VERIFY STAGE =====
verify-staging:
  <<: *validate-template
  stage: verify
  script:
    - capiscio validate $STAGING_URL/.well-known/agent-card.json --test-live --timeout 15
  environment:
    name: staging
  needs:
    - deploy-staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

verify-production:
  <<: *validate-template
  stage: verify
  script:
    - capiscio validate $PRODUCTION_URL/.well-known/agent-card.json --test-live --timeout 15
  environment:
    name: production
  needs:
    - deploy-production
  rules:
    - if: $CI_COMMIT_TAG
```

---

## Merge Request Integration

### Block MRs on Validation Failure

```yaml
validate-on-mr:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate agent-card.json --strict
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  allow_failure: false  # Block MR if validation fails
```

### Report Validation Results

```yaml
validate-with-report:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - |
      capiscio validate agent-card.json --json > validation.json
      if [ $? -eq 0 ]; then
        echo "✅ Validation passed"
      else
        echo "❌ Validation failed"
        cat validation.json
        exit 1
      fi
  artifacts:
    paths:
      - validation.json
    when: always
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## Multi-Agent Validation

```yaml
validate-all-agents:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - |
      FAILED=0
      for card in agents/*/agent-card.json; do
        echo "Validating $card..."
        if ! capiscio validate "$card" --strict; then
          FAILED=$((FAILED + 1))
        fi
      done
      
      if [ $FAILED -gt 0 ]; then
        echo "❌ $FAILED agent cards failed validation"
        exit 1
      fi
      
      echo "✅ All agent cards valid"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - agents/**/*
```

---

## Using Docker Image

Create a reusable Docker image:

```yaml
# Include in .gitlab-ci.yml
validate-agent-card:
  stage: validate
  image: 
    name: ghcr.io/capiscio/capiscio:latest
    entrypoint: [""]
  script:
    - capiscio validate agent-card.json --strict
```

Or build your own:

```dockerfile
# Dockerfile.ci
FROM python:3.11-slim
RUN pip install --no-cache-dir capiscio
ENTRYPOINT ["capiscio"]
```

```yaml
# .gitlab-ci.yml
build-validator:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -f Dockerfile.ci -t $CI_REGISTRY_IMAGE/validator:latest .
    - docker push $CI_REGISTRY_IMAGE/validator:latest
  only:
    - main

validate-agent-card:
  stage: validate
  image: $CI_REGISTRY_IMAGE/validator:latest
  script:
    - capiscio validate agent-card.json --strict
```

---

## Environment Variables

```yaml
validate-with-env:
  stage: validate
  image: python:3.11-slim
  variables:
    CAPISCIO_TIMEOUT: "30"
  before_script:
    - pip install capiscio
  script:
    - capiscio validate $AGENT_URL --test-live --timeout $CAPISCIO_TIMEOUT
```

---

## Scheduled Validation

Monitor production endpoints continuously:

```yaml
scheduled-validation:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate $PRODUCTION_URL/.well-known/agent-card.json --test-live
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

Create a schedule in GitLab:
1. Go to **CI/CD → Schedules**
2. Create new schedule
3. Set cron expression (e.g., `0 */6 * * *` for every 6 hours)
4. Set target branch

---

## Notifications

### Slack Notification on Failure

```yaml
validate-agent-card:
  stage: validate
  image: python:3.11-slim
  before_script:
    - pip install capiscio
  script:
    - capiscio validate agent-card.json --strict
  after_script:
    - |
      if [ "$CI_JOB_STATUS" == "failed" ]; then
        curl -X POST -H 'Content-type: application/json' \
          --data '{"text":"❌ Agent card validation failed in '$CI_PROJECT_NAME'"}' \
          $SLACK_WEBHOOK_URL
      fi
```

---

## Troubleshooting

### Job Fails but Card is Valid

Check timeout settings:

```yaml
validate-agent-card:
  timeout: 5m  # Increase if needed
  script:
    - capiscio validate $URL --test-live --timeout 30
```

### Network Issues

Add retry logic:

```yaml
validate-agent-card:
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

### Debug Output

```yaml
validate-debug:
  script:
    - capiscio validate agent-card.json --json 2>&1 | tee validation-output.json
    - cat validation-output.json
```

---

## See Also

- [GitHub Actions](../cicd/pre-commit.md) — GitHub alternative
- [Jenkins Integration](jenkins.md) — Jenkins alternative
- [Strict Mode Validation](../validation/strict-mode.md) — Strict mode details
