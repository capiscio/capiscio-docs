# CapiscIO Documentation Verification Report

**Generated:** 2026-01-18  
**Verified Against:** RFCs, capiscio-core, capiscio-sdk-python, capiscio-server, validate-a2a, capiscio-node, capiscio-python

---

## Executive Summary

A comprehensive audit of all documentation in `capiscio-docs/` was performed against the actual implementations and RFC specifications. **70+ issues** were identified across all documentation sections.

### Issue Severity Distribution

| Severity | Count | Impact |
|----------|-------|--------|
| **CRITICAL** | 15 | Will cause code failures |
| **MAJOR** | 28 | Significant documentation gaps, incorrect signatures |
| **MINOR** | 27+ | Polish, consistency issues |

---

## Critical Issues Summary (MUST FIX)

### 1. SDK Python Documentation (`reference/sdk-python/`)

| File | Issue | Fix Required |
|------|-------|--------------|
| `badge.md` | Missing `revoke_badge`, `get_badge_status` functions | Add documentation |
| `badge.md` | Missing `generate_badge_claims` generator | Add documentation |
| `badge.md` | TrustLevel enum values don't match RFC-002 | Levels 0-4 as strings |
| `errors.md` | Import path `from capiscio_sdk import` should be `from capiscio_sdk.errors import` | Fix import |
| `executor.md` | Constructor param is `executor=` not `wrapped_executor=` | Fix signature |
| `simple-guard.md` | Missing `validate_token`, `agent_id`, `badge_token` params | Add all params |
| `types.md` | Missing multi-dimensional scoring (`security_score`, `compliance_score`, `reliability_score`) | Add docs |

### 2. CLI Documentation (`reference/cli/`)

| Issue | Fix Required |
|-------|--------------|
| Missing `badge request-pop` command (PoP protocol) | Add full documentation |
| Missing `badge dv` subcommands (ACME-Lite) | Add `create`, `status`, `finalize` |
| Missing `rpc` command (gRPC server) | Add documentation |
| `verify` missing `--accept-self-signed` flag | Add to flags table |
| `key gen` missing `--out-did` and `--show-did` flags | Add to flags table |
| Trust levels say "1 (DV), 2 (OV), 3 (EV)" but should be "0=SS, 1=REG, 2=DV, 3=OV, 4=EV" | Fix descriptions |

### 3. Server API Documentation (`reference/server/`)

| Issue | Fix Required |
|-------|--------------|
| API keys path is `/api-keys` not `/v1/keys` | Fix all endpoint paths |
| Badge verification endpoint is `/v1/validate` not `/v1/badges/verify` | Fix endpoint path |
| Auth header is `X-Capiscio-Registry-Key` not `Authorization: Bearer` for API keys | Fix all auth examples |
| Missing `/health/ready` endpoint (documented but doesn't exist) | Remove or implement |
| Missing entire SDK API section (`/v1/sdk/*` endpoints) | Add section |
| Missing entire MCP Server section (`/v1/servers/*` endpoints) | Add section |
| Missing entire DV section (ACME-Lite: `/v1/badges/dv/*`) | Add section |

### 4. Concepts Documentation (`concepts/`)

| Issue | Fix Required |
|-------|--------------|
| IAL (Identity Assurance Level) not documented | Add IAL-0 vs IAL-1 section |
| PoP protocol not referenced | Add RFC-003 reference |
| `ial`, `key`, `vc`, `cnf` claims not documented | Add complete badge claims |
| Clock skew is 5s but RFC says 60s | Fix to 60 seconds |
| Verification algorithm incomplete | Add all 10 RFC-002 §8.1 steps |
| Error codes not referenced | Add RFC-002 §8.5 codes |

### 5. Getting Started Documentation (`getting-started/`)

| Issue | Fix Required |
|-------|--------------|
| CapiscioMiddleware import wrong | `from capiscio_sdk.integrations.fastapi import CapiscioMiddleware` |
| CapiscioMiddleware takes `guard=` not `config=` | Fix constructor |
| Header is `X-Capiscio-Badge` not `X-Capiscio-Signature` | Fix everywhere |
| SDK version shown as 0.2.0, actual is 2.3.1 | Update version |
| BadgeKeeper params: `api_url` not `ca_url`, `output_file` not `output_path` | Fix params |
| CLI `badge keep` flag is `--ca` not `--ca-url` | Fix flag name |

### 6. How-To Guides (`how-to/`)

| Issue | Fix Required |
|-------|--------------|
| Express.md references non-existent Node.js SDK | Add warning or remove |
| FastAPI.md: `request.state.capiscio_claims` should be `request.state.agent` | Fix attribute name |
| FastAPI.md: `exclude_paths` parameter doesn't exist | Remove or implement |
| dev-mode.md: `dev_identity` should be `agent_id` | Fix param name |
| verify-inbound.md: Uses `Authorization: Bearer` but should use `X-Capiscio-Badge` | Fix header |
| CLI key gen outputs `.jwk` not `.pem` | Fix all file extensions |

### 7. Wrapper Documentation (`reference/wrappers/`)

| Issue | Fix Required |
|-------|--------------|
| python.md: `capiscio.BINARY_PATH` doesn't exist | Remove or fix |
| node.md & python.md: Version 0.3.0 shown, actual is 2.3.1 | Update versions |
| Cache locations documented incorrectly | Fix cache paths |

---

## Issues By Documentation File

### reference/sdk-python/

<details>
<summary>Click to expand full list (16 issues)</summary>

1. **index.md** - Missing imports in Quick Import Reference
2. **index.md** - Missing DV API imports
3. **badge.md** - Missing `revoke_badge`, `get_badge_status` docs
4. **badge.md** - Missing `generate_badge_claims` generator
5. **badge.md** - TrustLevel enum inconsistent with RFC-002
6. **badge.md** - BadgeResult missing `level` and `valid` fields
7. **config.md** - SecurityConfig example completely wrong
8. **config.md** - Missing DownstreamConfig and UpstreamConfig
9. **errors.md** - Exception hierarchy incomplete
10. **errors.md** - Import path wrong
11. **executor.md** - Constructor signature wrong
12. **executor.md** - `run()` example wrong
13. **mcp.md** - Internal API exposed without warning
14. **simple-guard.md** - Missing constructor params
15. **simple-guard.md** - Missing `validate_token` method
16. **types.md** - Missing multi-dimensional scoring

</details>

### reference/cli/

<details>
<summary>Click to expand full list (10 issues)</summary>

1. Missing `badge request-pop` command
2. Missing `badge dv` subcommands
3. Missing `rpc` command
4. `verify` missing `--accept-self-signed` flag
5. `key gen` missing `--out-did`, `--show-did` flags
6. `badge issue` defaults wrong
7. `badge keep` completely different architecture
8. Trust level values incomplete (missing 0, 4)
9. JWK output example outdated
10. `validate --live` deprecation not mentioned

</details>

### reference/server/

<details>
<summary>Click to expand full list (14 issues)</summary>

1. `/v1/keys` should be `/api-keys`
2. `/v1/badges/verify` should be `/v1/validate`
3. `/health/ready` doesn't exist
4. Auth header wrong (should be X-Capiscio-Registry-Key)
5. Missing SDK endpoints (`/v1/sdk/*`)
6. Missing MCP Server endpoints (`/v1/servers/*`)
7. Missing DV endpoints (`/v1/badges/dv/*`)
8. Missing PoP challenge endpoint in main docs
9. API key prefix `cpsc_live_` should be `sk_live_`
10. Missing `/version` endpoint
11. Environment variables incomplete
12. Agent status values not documented
13. Error response format incomplete
14. Missing public endpoints documentation

</details>

### concepts/

<details>
<summary>Click to expand full list (12 issues)</summary>

1. IAL levels not documented at all
2. PoP protocol not referenced
3. `ial` claim missing from badge docs
4. `vc` claim structure not documented
5. `cnf` claim for IAL-1 not explained
6. Level 0 IAL constraint not documented
7. Verification algorithm incomplete (only 3 of 10 steps)
8. Clock skew 5s should be 60s
9. RFC-002 §8.5 error codes missing
10. RFC-006 MCP error codes missing
11. Evidence logging not explained
12. Progressive assurance model incomplete

</details>

### getting-started/

<details>
<summary>Click to expand full list (10 issues)</summary>

1. CapiscioMiddleware import wrong
2. CapiscioMiddleware constructor params wrong
3. X-Capiscio-Signature should be X-Capiscio-Badge
4. Key file format inconsistency (.jwk vs .pem)
5. SDK version 0.2.0 should be 2.3.1
6. BadgeKeeper API params wrong
7. Gateway port conflict in example
8. `--ca-url` should be `--ca`
9. Protocol version inconsistency
10. `--live` deprecation not mentioned

</details>

### how-to/

<details>
<summary>Click to expand full list (21 issues)</summary>

1. express.md references non-existent Node.js SDK
2. fastapi.md: `capiscio_claims` should be `agent`
3. fastapi.md: `exclude_paths` doesn't exist
4. badges.md: `verify_badge` signature wrong
5. badges.md: TrustLevel only has 1-3, missing 0,4
6. dev-mode.md: `dev_identity` should be `agent_id`
7. sign-outbound.md: Header inconsistency
8. verify-inbound.md: Uses Authorization: Bearer
9. CLI key gen outputs .jwk not .pem
10. gateway-setup.md: Missing health endpoint
11. flask.md: Body binding pattern wrong
12. badge-keeper.md: CLI flag inconsistency
13. validate-url.md: `--live` deprecation not mentioned
14. strict-mode.md: Score threshold unverified
15. langchain.md: Missing Response import
16. langchain.md: Duplicate route decorator
17. pre-commit.md: Wrong language setting
18. gitlab-ci.md: Package name unclear
19. jenkins.md: Package name unclear
20. trust-store.md: File format inconsistency
21. key-rotation.md: Path conventions wrong

</details>

### reference/wrappers/

<details>
<summary>Click to expand full list (7 issues)</summary>

1. python.md: `BINARY_PATH` doesn't exist
2. python.md: Version 0.3.0 should be 2.3.1
3. python.md: Cache location wrong
4. node.md: Version 0.3.0 should be 2.3.1
5. node.md: Cache location incomplete
6. node.md: Missing environment variables
7. github-action.md: All correct ✓

</details>

---

## Recommended Fix Priority

### Phase 1: Critical Issues (Week 1)
Focus on issues that will cause user code to fail:
- Fix all endpoint paths in server docs
- Fix all import statements in SDK docs
- Fix all header names (X-Capiscio-Badge)
- Add missing commands to CLI docs
- Fix constructor signatures

### Phase 2: Major Issues (Week 2)
Focus on significant gaps:
- Add IAL documentation to concepts
- Add complete badge claims documentation
- Add missing API sections (SDK, MCP, DV)
- Fix verification algorithm in concepts
- Update all version numbers

### Phase 3: Minor Issues (Week 3)
Polish and consistency:
- Standardize file extensions
- Add deprecation notices
- Fix small signature mismatches
- Update examples for consistency

---

## Recommendations for Future Accuracy

See `DOCS_ACCURACY_GUIDE.md` for detailed best practices.

Key recommendations:
1. **Automated testing** - Extract code examples and run them in CI
2. **Schema validation** - Auto-generate API docs from OpenAPI spec
3. **Version pinning** - Document which versions examples apply to
4. **Single source of truth** - Generate from code comments where possible
5. **Review checklist** - Require verification against implementation for all doc PRs

