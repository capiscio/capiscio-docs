---
title: Jenkins Integration
description: Validate agent cards in Jenkins pipelines
---

# Jenkins Integration

Automate agent card validation in your Jenkins CI/CD pipelines.

---

## Problem

You need to:

- Validate agent cards in Jenkins pipelines
- Integrate with existing Jenkins jobs
- Support both freestyle and pipeline jobs
- Get validation results in Jenkins UI

---

## Solution: Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Validate Agent Card') {
            steps {
                sh '''
                    pip install capiscio
                    capiscio validate agent-card.json --strict
                '''
            }
        }
    }
}
```

---

## Declarative Pipeline

### Basic Validation

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Validate') {
            steps {
                sh 'capiscio validate agent-card.json --strict'
            }
        }
    }
}
```

### Full Pipeline

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    environment {
        AGENT_CARD_PATH = 'agent-card.json'
        PRODUCTION_URL = 'https://myagent.example.com'
        STAGING_URL = 'https://staging.myagent.example.com'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Lint') {
            steps {
                sh "capiscio validate ${AGENT_CARD_PATH} --schema-only"
            }
        }
        
        stage('Validate Strict') {
            steps {
                sh "capiscio validate ${AGENT_CARD_PATH} --strict --json > validation-report.json"
                archiveArtifacts artifacts: 'validation-report.json'
            }
        }
        
        stage('Deploy Staging') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo "Deploying to staging..."'
                // Your deployment steps
            }
        }
        
        stage('Verify Staging') {
            when {
                branch 'main'
            }
            steps {
                sh "capiscio validate ${STAGING_URL}/.well-known/agent-card.json --test-live"
            }
        }
        
        stage('Deploy Production') {
            when {
                buildingTag()
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh 'echo "Deploying to production..."'
                // Your deployment steps
            }
        }
        
        stage('Verify Production') {
            when {
                buildingTag()
            }
            steps {
                sh "capiscio validate ${PRODUCTION_URL}/.well-known/agent-card.json --test-live"
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Agent card validation failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        success {
            slackSend(
                color: 'good',
                message: "Agent card validation passed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

---

## Scripted Pipeline

```groovy
node {
    docker.image('python:3.11-slim').inside {
        stage('Checkout') {
            checkout scm
        }
        
        stage('Setup') {
            sh 'pip install capiscio'
        }
        
        stage('Validate') {
            try {
                sh 'capiscio validate agent-card.json --strict --json > validation.json'
                archiveArtifacts 'validation.json'
            } catch (err) {
                currentBuild.result = 'FAILURE'
                error "Validation failed: ${err}"
            }
        }
        
        if (env.BRANCH_NAME == 'main') {
            stage('Deploy Staging') {
                sh 'echo "Deploying..."'
            }
            
            stage('Verify Live') {
                sh 'capiscio validate https://staging.myagent.example.com/.well-known/agent-card.json --test-live'
            }
        }
    }
}
```

---

## Freestyle Job

For freestyle jobs, add a build step:

### Shell Build Step

```bash
#!/bin/bash
set -e

# Install capiscio
pip install capiscio

# Validate the agent card
capiscio validate agent-card.json --strict

# Save results
capiscio validate agent-card.json --json > validation-report.json
```

### With Virtual Environment

```bash
#!/bin/bash
set -e

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install and validate
pip install capiscio
capiscio validate agent-card.json --strict
```

---

## Multi-Agent Validation

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Validate All Agents') {
            steps {
                script {
                    def agentCards = findFiles(glob: 'agents/*/agent-card.json')
                    def failed = []
                    
                    for (card in agentCards) {
                        echo "Validating ${card.path}..."
                        def result = sh(
                            script: "capiscio validate ${card.path} --strict",
                            returnStatus: true
                        )
                        if (result != 0) {
                            failed.add(card.path)
                        }
                    }
                    
                    if (failed.size() > 0) {
                        error "Failed validations: ${failed.join(', ')}"
                    }
                }
            }
        }
    }
}
```

---

## Parallel Validation

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Validate') {
            parallel {
                stage('Schema Only') {
                    steps {
                        sh 'capiscio validate agent-card.json --schema-only'
                    }
                }
                stage('Strict') {
                    steps {
                        sh 'capiscio validate agent-card.json --strict'
                    }
                }
                stage('Live Test') {
                    when {
                        branch 'main'
                    }
                    steps {
                        sh 'capiscio validate https://myagent.example.com/.well-known/agent-card.json --test-live'
                    }
                }
            }
        }
    }
}
```

---

## Shared Library

Create a reusable shared library:

### vars/capiscioValidate.groovy

```groovy
def call(Map config = [:]) {
    def cardPath = config.cardPath ?: 'agent-card.json'
    def strict = config.strict ?: true
    def liveTest = config.liveTest ?: false
    def timeout = config.timeout ?: 10
    
    docker.image('python:3.11-slim').inside {
        sh 'pip install capiscio'
        
        def args = []
        if (strict) args.add('--strict')
        if (liveTest) args.add('--test-live')
        args.add("--timeout ${timeout}")
        
        sh "capiscio validate ${cardPath} ${args.join(' ')}"
    }
}
```

### Usage

```groovy
@Library('my-shared-library') _

pipeline {
    agent any
    
    stages {
        stage('Validate') {
            steps {
                capiscioValidate(
                    cardPath: 'agent-card.json',
                    strict: true
                )
            }
        }
    }
}
```

---

## Environment-Specific Validation

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Environment to validate'
        )
    }
    
    environment {
        URLS = [
            'development': 'https://dev.myagent.example.com',
            'staging': 'https://staging.myagent.example.com',
            'production': 'https://myagent.example.com'
        ]
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Validate') {
            steps {
                script {
                    def url = URLS[params.ENVIRONMENT]
                    sh "capiscio validate ${url}/.well-known/agent-card.json --test-live"
                }
            }
        }
    }
}
```

---

## JUnit Test Report

Generate JUnit-compatible output:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Validate') {
            steps {
                sh '''
                    # Run validation and convert to JUnit format
                    python3 << 'EOF'
import subprocess
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Run validation
result = subprocess.run(
    ['capiscio', 'validate', 'agent-card.json', '--json'],
    capture_output=True,
    text=True
)

# Parse result
try:
    data = json.loads(result.stdout)
    success = data.get('valid', False)
    errors = data.get('errors', [])
except:
    success = result.returncode == 0
    errors = [result.stderr] if result.stderr else []

# Build JUnit XML
testsuites = ET.Element('testsuites')
testsuite = ET.SubElement(testsuites, 'testsuite', {
    'name': 'AgentCardValidation',
    'tests': '1',
    'failures': '0' if success else '1'
})

testcase = ET.SubElement(testsuite, 'testcase', {
    'name': 'validate-agent-card',
    'classname': 'capiscio'
})

if not success:
    failure = ET.SubElement(testcase, 'failure', {
        'message': 'Validation failed'
    })
    failure.text = '\\n'.join(str(e) for e in errors)

# Write XML
xml_str = minidom.parseString(ET.tostring(testsuites)).toprettyxml(indent='  ')
with open('validation-results.xml', 'w') as f:
    f.write(xml_str)

exit(0 if success else 1)
EOF
                '''
            }
            post {
                always {
                    junit 'validation-results.xml'
                }
            }
        }
    }
}
```

---

## Scheduled Validation

Create a separate job for scheduled monitoring:

```groovy
// Jenkinsfile.monitor
pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
        }
    }
    
    triggers {
        cron('H */6 * * *')  // Every 6 hours
    }
    
    environment {
        PRODUCTION_URL = 'https://myagent.example.com'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install capiscio'
            }
        }
        
        stage('Monitor') {
            steps {
                sh "capiscio validate ${PRODUCTION_URL}/.well-known/agent-card.json --test-live --timeout 30"
            }
        }
    }
    
    post {
        failure {
            emailext(
                subject: "⚠️ Agent Card Monitoring Failed",
                body: "Production agent card validation failed. Check ${BUILD_URL}",
                to: 'ops@example.com'
            )
        }
    }
}
```

---

## Troubleshooting

### Python Not Found

Use Docker or specify Python path:

```groovy
stage('Validate') {
    steps {
        sh '/usr/bin/python3 -m pip install capiscio'
        sh '/usr/bin/python3 -m capiscio validate agent-card.json'
    }
}
```

### Timeout Issues

```groovy
stage('Validate Live') {
    options {
        timeout(time: 5, unit: 'MINUTES')
    }
    steps {
        sh 'capiscio validate $URL --test-live --timeout 60'
    }
}
```

### Permission Issues

```groovy
stage('Setup') {
    steps {
        sh 'pip install --user capiscio'
        sh 'export PATH=$PATH:$HOME/.local/bin && capiscio validate agent-card.json'
    }
}
```

---

## See Also

- [GitLab CI](gitlab-ci.md) — GitLab alternative
- [GitHub Actions](../cicd/pre-commit.md) — GitHub alternative
- [Strict Mode](../validation/strict-mode.md) — Validation details
