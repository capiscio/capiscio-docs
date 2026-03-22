---
title: Embedded Policy Enforcement
description: How to use the local PDP for in-process policy evaluation in your agents.
---

# Embedded Policy Enforcement

The **Local Policy Decision Point (PDP)** evaluates policy decisions inside your agent process — no external service calls needed. It pulls policy bundles from the CapiscIO registry and evaluates them using an embedded [OPA](https://www.openpolicyagent.org/) engine.

## Why Embedded?

| Feature | Remote PDP | Local PDP |
|---------|-----------|-----------|
| Latency | Network round-trip per decision | Sub-millisecond |
| Availability | Depends on network | Always available |
| Offline support | ❌ | ✅ (last-known-good policy) |
| Setup | API calls | 3 environment variables |

## Quick Start (Go)

### Environment Variables

Set these in your agent's environment:

```bash
export CAPISCIO_BUNDLE_URL=https://api.capisc.io/v1/bundles/<your-org-id>
export CAPISCIO_API_KEY=<your-api-key>
export CAPISCIO_ENFORCEMENT_MODE=EM-OBSERVE   # Start in observe mode
```

### Initialize the PDP

```go
import "github.com/capiscio/capiscio-core/v2/pkg/pdp"

// One-line setup from environment variables
localPDP, err := pdp.NewLocalPDPFromEnv(ctx)
if err != nil {
    log.Fatal(err)
}
defer localPDP.Stop()

// localPDP.Client implements pip.PDPClient
// localPDP.Manager handles background refresh
```

### Evaluate a Policy Decision

```go
import "github.com/capiscio/capiscio-core/v2/pkg/pip"

resp, err := localPDP.Client.Evaluate(ctx, &pip.DecisionRequest{
    PIPVersion: pip.PIPVersion,
    Subject: pip.SubjectAttributes{
        DID:        incomingAgent.DID,
        TrustLevel: incomingAgent.Badge.TrustLevel,
    },
    Action: pip.ActionAttributes{
        Operation: "message/send",
    },
    Resource: pip.ResourceAttributes{
        Identifier: "my-agent",
    },
    Context: pip.ContextAttributes{
        EnforcementMode: "EM-OBSERVE",
    },
})

if resp.Decision == "deny" {
    // Block the request
}
```

## Enforcement Modes

Enforcement modes control how strictly policies are applied:

| Mode | Behavior | When to Use |
|------|----------|-------------|
| `EM-OBSERVE` | Log decisions, never block | Initial rollout, testing policies |
| `EM-GUARD` | Block violations, allow on PDP failure | Production with graceful degradation |
| `EM-DELEGATE` | Block violations, block on PDP failure | High-security environments |
| `EM-STRICT` | Block everything unless explicitly allowed | Zero-trust deployments |

Start with `EM-OBSERVE` to see how policies affect traffic without blocking anything. Promote to `EM-GUARD` or stricter once you've verified behavior.

### Staleness Behavior

When the PDP cannot refresh its policy bundle (e.g., network issues), behavior depends on the enforcement mode:

- **EM-OBSERVE / EM-GUARD**: Continue evaluating with the last-known-good bundle
- **EM-STRICT**: Deny all requests once the bundle exceeds the max age threshold

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CAPISCIO_BUNDLE_URL` | Yes | — | Bundle endpoint URL |
| `CAPISCIO_API_KEY` | Yes | — | API key with `bundle:read` permission |
| `CAPISCIO_ENFORCEMENT_MODE` | No | `EM-OBSERVE` | Enforcement strictness level |
| `CAPISCIO_POLL_INTERVAL` | No | `30s` | How often to check for policy updates |
| `CAPISCIO_MAX_AGE` | No | `10m` | Maximum bundle age before staleness |

### Programmatic Configuration

```go
cfg := pdp.PolicyEnforcementConfig{
    BundleURL:       "https://api.capisc.io/v1/bundles/your-org-id",
    APIKey:          "your-api-key",
    EnforcementMode: pip.EMGuard,
    PollInterval:    30 * time.Second,
    MaxAge:          10 * time.Minute,
}

localPDP, err := pdp.NewLocalPDP(ctx, cfg)
```

## Architecture

```
┌─────────────────────────────────────────────┐
│                Your Agent                    │
│                                              │
│  Request → PEP → LocalPDP.Evaluate() → PEP │
│                     │                        │
│              ┌──────┴──────┐                 │
│              │ OPA Engine  │  ← in-process   │
│              └──────┬──────┘                  │
│                     │                        │
│              ┌──────┴──────┐                 │
│              │BundleManager│  ← polls every  │
│              │  (refresh)  │    30 seconds    │
│              └──────┬──────┘                  │
│                     │                        │
└─────────────────────┼────────────────────────┘
                      │ HTTPS
               ┌──────┴──────┐
               │  CapiscIO   │
               │  Registry   │
               └─────────────┘
```

The **BundleManager** runs in the background:

1. Polls the registry for policy bundle updates at the configured interval
2. Compares the bundle revision — skips reload if unchanged
3. Hot-swaps the OPA engine's policy when updates are available
4. Uses exponential backoff with jitter on fetch failures

## Build Tags

The local PDP requires the `opa_no_wasm` build tag:

```bash
go build -tags opa_no_wasm ./...
go test -tags opa_no_wasm ./...
```

This excludes OPA's WebAssembly runtime (not needed for Rego evaluation) and reduces the binary size.

## Troubleshooting

### "pdp: bundle URL is required"

Set the `CAPISCIO_BUNDLE_URL` environment variable or pass it in `PolicyEnforcementConfig.BundleURL`.

### "pdp: bundle authentication failed (401)"

Your API key is invalid or missing the `bundle:read` permission. Check the key in the [Dashboard](https://app.capisc.io).

### "pdp: initial bundle fetch failed under EM-STRICT"

Under `EM-STRICT`, the PDP fails to start if it can't fetch an initial bundle. Either fix the network issue or start with `EM-OBSERVE` first.

### Bundle is stale but requests are still allowed

Under `EM-OBSERVE` and `EM-GUARD`, stale bundles continue to be evaluated. Switch to `EM-STRICT` if you need strict freshness guarantees.
