---
title: Three-Dimensional Scoring System - CapiscIO Documentation
description: Complete guide to Compliance, Trust, and Availability scoring for A2A protocol agents with breakdowns, thresholds, and production criteria.
keywords: A2A scoring, agent compliance, trust scoring, availability testing, protocol validation, agent rating, production readiness, JWS signatures
og:image: https://docs.capisc.io/assets/social-card-scoring.png
canonical_url: https://docs.capisc.io/guides/scoring-system/
---

# 🎯 Three-Dimensional Scoring System

> **The authoritative guide to CapiscIO's scoring system** - Used by both CapiscIO CLI and Python SDK

## Why Three Dimensions?

**The Problem with Single Scores:**

Imagine you evaluate an agent and get a score of `67/100`. What does that tell you?

- Is it compliant with the protocol but untrusted?
- Is it trusted but often unavailable?
- Is it a security risk or just poorly configured?

**You can't tell. And you can't make informed decisions.**

### Real-World Scenario

You're building a payment processing agent. You discover two potential partner agents:

- **Agent A**: `Compliance: 95, Trust: 45, Availability: 90`
  - *Translation:* Perfectly follows the protocol, always up, but no signature verification, missing provider info. **Don't use for payments.**

- **Agent B**: `Compliance: 80, Trust: 95, Availability: 80`  
  - *Translation:* Minor protocol quirks, occasionally slow, but fully signed, verified provider, excellent security. **Good for payments.**

**A single score would show them both as ~75. Three dimensions tell you the REAL story.**

---

## Overview

Every agent card validation returns three independent score dimensions:

<div class="grid cards" markdown>

-   **📄 Spec Compliance (0-100)**

    ---

    How well does the agent card conform to the A2A v0.3.0 specification?
    
    Measures protocol adherence, required fields, format validation, and data quality.

-   **🔐 Trust (0-100)**

    ---

    How trustworthy and secure is this agent?
    
    Measures security practices, cryptographic signatures, provider info, and documentation.

-   **🚀 Availability (0-100)**

    ---

    Is the agent operationally available and responding correctly?
    
    Measures endpoint health, transport support, and response quality. *(Optional - requires live testing)*

</div>

Each dimension has its own detailed breakdown, rating enum, and independent scoring logic.

---

## 📄 Dimension 1: Spec Compliance (100 points)

**What it measures:** How well the agent card adheres to the A2A v0.3.0 specification.

**Why it matters:** Protocol compliance ensures interoperability. An agent with poor compliance won't work correctly with other agents, registries, or tooling.

### Scoring Breakdown

The compliance score uses a **60/20/15/5 weighting** across four categories:

#### Core Fields (60 points)

Checks for presence of all 9 required A2A v0.3.0 fields:

| Field | Points | Purpose |
|-------|--------|---------|
| `protocolVersion` | 6.67 | Declares A2A version (e.g., "0.3.0") |
| `name` | 6.67 | Agent display name |
| `description` | 6.67 | Agent description |
| `url` | 6.67 | Agent base URL |
| `version` | 6.67 | Agent semantic version |
| `capabilities` | 6.67 | Supported capabilities |
| `defaultInputModes` | 6.67 | Accepted MIME types |
| `defaultOutputModes` | 6.67 | Response MIME types |
| `skills` | 6.67 | Available skills array |

**Penalty:** Each missing field costs 6.67 points.

#### Skills Quality (20 points)

Evaluates the quality of the skills array:

- **Skills present** (10 points) - At least one skill defined
- **Required fields** (5 points) - All skills have `id`, `name`, `description`
- **Tags present** (5 points) - All skills have at least one tag

**Penalties:**
- -2 points per skill missing required fields
- -1 point per skill without tags

#### Format Compliance (15 points)

Validates proper formatting across the agent card:

- **Valid semver** (3 points) - `version` follows semantic versioning (e.g., `1.0.0`)
- **Valid protocol version** (3 points) - `protocolVersion` is `0.3.0`
- **Valid URL** (3 points) - `url` is a proper HTTPS URL
- **Valid transports** (3 points) - Transport protocols are `JSONRPC`, `GRPC`, or `HTTP+JSON`
- **Valid MIME types** (3 points) - Input/output modes are valid MIME types

**Special penalty:** -10 points for invalid MIME types (security risk)

#### Data Quality (5 points)

Checks for data integrity and security:

- **No duplicate skill IDs** (2 points) - Each skill has a unique identifier
- **Field lengths valid** (2 points) - Names, descriptions within reasonable limits
- **No SSRF risks** (1 point) - URLs don't point to internal/private networks

### Rating Levels

| Score | Rating | Description |
|-------|--------|-------------|
| 100 | **Perfect** | Flawless protocol compliance |
| 90-99 | **Excellent** | Minor omissions only |
| 75-89 | **Good** | Usable with some issues |
| 60-74 | **Fair** | Significant improvements needed |
| <60 | **Poor** | Major protocol violations |

### Common Issues

- ❌ Missing required fields like `protocolVersion` or `capabilities`
- ❌ Skills without tags (reduces discoverability)
- ❌ Invalid MIME types in input/output modes
- ❌ Using HTTP instead of HTTPS for URLs
- ❌ Invalid semantic version strings

---

## 🔐 Dimension 2: Trust (100 points + multiplier)

**What it measures:** How trustworthy and secure is this agent? Can users verify its authenticity?

**Why it matters:** Trust is critical for adoption. Without signatures, users can't verify your agent's identity. Security claims without proof get penalized.

### The Trust Confidence Multiplier 🔑

**Revolutionary concept:** The presence and validity of cryptographic signatures affects ALL trust claims via a confidence multiplier:

- **✅ Valid JWS signature**: `1.0x` multiplier (full trust)
- **⚪ No signature**: `0.6x` multiplier (unverified claims)
- **❌ Invalid signature**: `0.4x` multiplier (active distrust)

**Why this matters:** An agent claiming strong security without signatures gets reduced trust. This prevents "trust washing" where agents make security claims they can't prove.

### Scoring Breakdown

The trust score uses a **40/25/20/15 weighting** across four categories:

#### Signatures (40 points + confidence key)

The foundation of trust:

- **Valid signature present** (30 points) - JWS signature verified
- **Multiple signatures** (+3 points) - Redundant verification
- **Comprehensive coverage** (+4 points) - Signature covers all critical fields
- **Recent signature** (+3 points) - Signed within last 90 days

**Penalties:**
- **Invalid signature** (-15 points + 0.4x multiplier) - Worse than no signature!
- **Expired signature** (-10 points + 0.6x multiplier)

#### Provider Information (25 points)

Who is behind this agent?

- **Organization specified** (10 points) - `provider.organization` present
- **Provider URL** (10 points) - `provider.url` present and uses HTTPS
- **URL reachable** (+5 bonus) - Provider website responds *(requires live testing)*

#### Security Practices (20 points)

How secure is the implementation?

- **HTTPS-only endpoints** (10 points) - All URLs use HTTPS
- **Security schemes declared** (5 points) - `securitySchemes` defined in agent card
- **Strong authentication** (5 points) - OAuth2, OpenID Connect, or similar

**Penalty:** -10 points for any HTTP URLs (major security risk)

#### Documentation (15 points)

Transparency and user support:

- **Documentation URL** (5 points) - `documentationUrl` provided
- **Terms of Service** (5 points) - `termsOfServiceUrl` provided
- **Privacy Policy** (5 points) - `privacyPolicyUrl` provided

### Rating Levels

| Score | Rating | Description |
|-------|--------|-------------|
| 80-100 | **Highly Trusted** | Cryptographically verified, excellent security |
| 60-79 | **Trusted** | Good security practices, some verification |
| 40-59 | **Moderate Trust** | Basic security, unverified claims |
| 20-39 | **Low Trust** | Minimal security indicators |
| <20 | **Untrusted** | Security red flags present |

### Example: Confidence Multiplier in Action

**Scenario:** Agent card claims strong security (OAuth2, HTTPS-only, security schemes) = 40 raw points

- **With valid signature**: `40 × 1.0 = 40 points` ✅ (Claims verified)
- **Without signature**: `40 × 0.6 = 24 points` ⚠️ (Unverified claims)
- **Invalid signature**: `40 × 0.4 = 16 points` ❌ (Active red flag)

The same security features are worth **167% more** with a valid signature!

### Common Issues

- ❌ No cryptographic signatures (reduces trust by 40%)
- ❌ Missing provider information
- ❌ No documentation or privacy policy URLs
- ❌ Using HTTP instead of HTTPS
- ❌ No security schemes declared

---

## 🚀 Dimension 3: Availability (100 points)

**What it measures:** Is the agent operationally available and responding correctly?

**Why it matters:** An agent with perfect compliance and trust scores is useless if it's unreachable. Availability testing catches deployment issues before users encounter them.

!!! warning "Live Testing Required"
    This score is **only calculated when live endpoint testing is enabled**. Without it, availability shows as "Not Tested".

### Scoring Breakdown

The availability score uses a **50/30/20 weighting** across three categories:

#### Primary Endpoint (50 points)

Can we reach your agent?

- **Endpoint responds** (30 points) - Returns a valid HTTP response
- **Fast response** (10 points) - Responds in under 3 seconds
- **CORS configured** (5 points) - Proper CORS headers for web access
- **Valid TLS certificate** (5 points) - HTTPS certificate is valid and trusted

#### Transport Support (30 points)

Are the declared transports working?

- **Preferred transport works** (20 points) - Primary protocol responds correctly
- **Additional interfaces** (10 points) - Alternative transports also functional

#### Response Quality (20 points)

How well-formed are the responses?

- **Valid A2A structure** (10 points) - Responses follow A2A message format
- **Proper content-type** (5 points) - Correct HTTP headers
- **Error handling** (5 points) - Graceful error responses

### Rating Levels

| Score | Rating | Description |
|-------|--------|-------------|
| 95-100 | **Fully Available** | Fast, reliable, production-ready |
| 80-94 | **Available** | Functional with minor latency |
| 60-79 | **Degraded** | Intermittent issues, slow responses |
| 40-59 | **Unstable** | Frequent failures or timeouts |
| <40 | **Unavailable** | Endpoint unreachable or broken |

### Common Issues

- ❌ Endpoint timeouts (> 3 seconds)
- ❌ Connection refused or DNS errors
- ❌ Invalid TLS certificates (expired, self-signed)
- ❌ Missing or incorrect CORS headers
- ❌ Responses not following A2A message structure
- ❌ Declared transports returning errors

---

## Production Readiness

The scoring system automatically determines if an agent is **production ready** based on these thresholds:

| Dimension | Minimum | Rationale |
|-----------|---------|-----------|
| **Compliance** | ≥ 95 | Nearly perfect spec adherence required |
| **Trust** | ≥ 60 | At least "Trusted" level security |
| **Availability** | ≥ 80 | Available or better *(if tested)* |

Agents meeting all thresholds receive a **"✅ Production ready"** recommendation.

---

## When to Use Each Dimension

### Compliance Matters Most

**Use cases:**
- Protocol testing and validation tools
- Compliance auditing and certification
- Interoperability testing between vendors
- Agent registry quality gates

**Decision logic:** Reject agents with compliance < 90

### Trust Matters Most

**Use cases:**
- Financial transactions (payments, invoicing)
- Identity verification (KYC, authentication)
- Sensitive data handling (PII, health records, legal)
- High-value API calls

**Decision logic:** Require trust ≥ 80 for sensitive operations

### Availability Matters Most

**Use cases:**
- Real-time systems (chat, live updates, streaming)
- Critical path operations (task dependencies, workflows)
- High-volume APIs (data sync, batch processing)
- Time-sensitive integrations

**Decision logic:** Only call agents with availability ≥ 90

---

## Using Scores in Your Application

### CLI Validation

```bash
# Get detailed scores
capiscio validate agent-card.json --detailed-scores

# Include availability testing
capiscio validate https://agent.example.com --detailed-scores --test-live

# JSON output for CI/CD
capiscio validate agent.json --detailed-scores --json > scores.json
```

[**See full CLI usage guide →**](../capiscio-node-js-cli/reference/api.md)

### Python API

```python
from capiscio_sdk import secure, SecurityConfig

# Wrap your agent with security
agent = secure(MyAgentExecutor(), SecurityConfig.production())

# Validate an agent card
result = await agent.validate_agent_card("https://partner.example.com")

# Access scores
print(f"Compliance: {result.compliance.total}")  # 0-100
print(f"Trust: {result.trust.total}")            # 0-100  
print(f"Availability: {result.availability.total}")  # 0-100 or None

# Use ratings for decisions
if result.trust.rating == TrustRating.HIGHLY_TRUSTED:
    await process_payment(partner_url)
```

[**See full Python usage guide →**](../capiscio-python-sdk/guides/scoring.md)

---

## Decision-Making Examples

### Example 1: Production Deployment

```python
result = await validate_agent_card(candidate_url)

# Financial transactions: Require high trust AND compliance
if result.trust.rating == TrustRating.HIGHLY_TRUSTED and \
   result.compliance.total >= 90:
    await process_payment(candidate_url)
else:
    log_rejection(candidate_url, "Insufficient trust/compliance")

# Data sync: Prioritize availability
if result.availability.rating == AvailabilityRating.FULLY_AVAILABLE:
    await sync_data(candidate_url)
else:
    schedule_retry(candidate_url)
```

### Example 2: Monitoring and Alerting

```python
result = await validate_agent_card(partner_url)

# Alert on trust degradation
if result.trust.total < 70:
    alert("Partner trust score dropped", severity="HIGH")
    # Possible causes: expired signatures, provider changes
    
# Alert on availability issues  
if result.availability.rating == AvailabilityRating.UNAVAILABLE:
    alert("Partner unreachable", severity="MEDIUM")
    failover_to_backup()

# Log compliance warnings
if result.compliance.total < 80:
    log_warning("Partner has compliance issues", result.issues)
```

### Example 3: Agent Selection

```python
# Rank multiple candidates by weighted score
candidates = [await validate_agent_card(url) for url in urls]

def score_for_payments(result):
    return (
        result.trust.total * 0.5 +           # Trust matters most
        result.compliance.total * 0.3 +      # Compliance important
        (result.availability.total or 0) * 0.2  # Availability nice-to-have
    )

best_agent = max(candidates, key=score_for_payments)
```

---

## Migration from Single Score

If you're migrating from the legacy single-score system:

### Old API (Deprecated)

```python
result = validator.validate(agent_card)
if result.score >= 80:
    deploy_agent()
```

### New API (Current)

```python
result = validator.validate(agent_card)

# Be specific about what matters
if result.compliance.total >= 90 and result.trust.total >= 80:
    deploy_agent()
```

The old `result.score` property still exists but returns `compliance.total` and is deprecated. Use the three dimensions for all new code.

---

## FAQ

??? question "Is the legacy `score` property still available?"
    Yes, but it returns `compliance.total` and is deprecated. Migrate to the three-dimensional system for all new code.

??? question "How do I access detailed breakdowns?"
    Each dimension has a `.breakdown` property with scoring details:
    
    ```python
    print(result.compliance.breakdown.core_fields.score)
    print(result.trust.breakdown.signatures.score)
    ```

??? question "Can availability be null?"
    Yes. If live testing is not performed, `availability.total` is `None` and `availability.rating` is `AvailabilityRating.NOT_TESTED`.

??? question "Why does my trust score seem low?"
    If you have security features but no signature, the 0.6x confidence multiplier reduces your score by 40%. Add JWS signatures to achieve full trust potential.

??? question "What if I only care about one dimension?"
    You can ignore the others, but we recommend considering all three. An agent with perfect compliance but zero trust is still a security risk.

---

## See Also

- **[CapiscIO CLI Scoring](../capiscio-node-js-cli/reference/api.md)** - Command-line usage and flags
- **[Python SDK Scoring](../capiscio-python-sdk/guides/scoring.md)** - Python API and patterns
- **[Core Concepts](../capiscio-python-sdk/getting-started/concepts.md)** - Understanding validation architecture

---

**Version:** 1.0  
**Last Updated:** October 2025  
**Maintained by:** CapiscIO Documentation Team
