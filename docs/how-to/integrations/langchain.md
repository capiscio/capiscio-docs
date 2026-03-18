---
title: LangChain Integration
description: Secure LangChain and LangGraph agents with langchain-capiscio
---

# LangChain Integration

Add trust enforcement to LangChain agents in 1–3 lines using the
[`langchain-capiscio`](https://pypi.org/project/langchain-capiscio/) package.

---

## Problem

You're building a LangChain or LangGraph agent and need to:

- Verify incoming caller trust badges before execution
- Enforce security policies (block / monitor / log)
- Emit structured audit events to the CapiscIO dashboard
- Compose trust checks with LangChain's LCEL pipe (`|`) operator

---

## Install

```bash
pip install langchain-capiscio
```

This installs `langchain-capiscio` along with `capiscio-sdk` and `langchain-core`.

---

## Quick Start: Zero-Config Guard

Set your API key in the environment and create a guard with **zero arguments**:

```bash
export CAPISCIO_API_KEY="cap_..."
```

```python
from langchain_capiscio import CapiscioGuard

secured = CapiscioGuard() | my_chain
result = secured.invoke({"input": "Summarize this ticket"})
```

`CapiscioGuard` reads `CAPISCIO_API_KEY` (and optionally `CAPISCIO_SERVER_URL`,
`CAPISCIO_AGENT_NAME`, `CAPISCIO_DEV_MODE`) from the environment. Connection
to the CapiscIO registry happens lazily on first `invoke()`.

---

## Enforcement Modes

```python
guard = CapiscioGuard(mode="block")    # Fail closed (production default)
guard = CapiscioGuard(mode="monitor")  # Warn but continue
guard = CapiscioGuard(mode="log")      # Log only — good for development
```

| Mode | On missing/invalid badge |
|------|--------------------------|
| `block` | Raises `CapiscioTrustError` |
| `monitor` | Logs warning, sets `verified=False` and `warnings` in `CapiscioRequestContext`, continues |
| `log` | Logs info, sets `verified=False` and `warnings` in `CapiscioRequestContext`, continues |

In all modes the guard is a **pure passthrough** — it returns the input unchanged.
Verification metadata is stored in the `CapiscioRequestContext` context variable,
not in the output.

---

## LCEL Pipe Composition

`CapiscioGuard` is a LangChain `Runnable`, so it composes with any chain or
agent via the `|` operator:

```python
from langchain_capiscio import CapiscioGuard
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools)

# Trust check runs before the agent on every invocation
secured = CapiscioGuard(mode="log") | agent
result = secured.invoke({"input": "What's 42 * 17?"})
```

---

## Configuration

### Environment variables (zero-config)

| Variable | Description | Default |
|----------|-------------|---------|
| `CAPISCIO_API_KEY` | Registry API key (**required** if not passed explicitly) | — |
| `CAPISCIO_SERVER_URL` | Registry URL override | `https://registry.capisc.io` |
| `CAPISCIO_AGENT_NAME` | Agent name for registration | — |
| `CAPISCIO_DEV_MODE` | Enable dev mode (`true` / `1` / `yes`) | `false` |

### Explicit parameters

```python
guard = CapiscioGuard(
    mode="block",
    api_key="cap_...",
    name="my-agent",
    server_url="https://dev.registry.capisc.io",
)
```

### `from_env()` class method

Mirrors `CapiscIO.from_env()` and `MCPServerIdentity.from_env()`:

```python
guard = CapiscioGuard.from_env(mode="log")
```

### Extra connection options via `connect_kwargs`

Pass additional keyword arguments through to `CapiscIO.connect()`:

```python
guard = CapiscioGuard(
    mode="log",
    connect_kwargs={
        "dev_mode": True,
        "keys_dir": "capiscio_keys/",
        "agent_card": agent_card_dict,
    },
)
```

Priority: explicit constructor args > `connect_kwargs` > env vars > SDK defaults.

---

## Callback Handler: Audit Events

`CapiscioCallbackHandler` wires LangChain lifecycle callbacks to the CapiscIO
EventEmitter for dashboard visibility and audit trails:

```python
from langchain_capiscio import CapiscioCallbackHandler

handler = CapiscioCallbackHandler(emitter=my_event_emitter)
result = chain.invoke(
    {"input": "..."},
    config={"callbacks": [handler]},
)
```

Events emitted:

| Event | Trigger |
|-------|---------|
| `task_started` | Chain starts |
| `task_completed` | Chain finishes successfully |
| `task_failed` | Chain or tool raises an exception |
| `tool_call` | Tool invocation begins |
| `tool_result` | Tool invocation completes |

---

## LangGraph Nodes

### Runnable as node

```python
from langchain_capiscio import CapiscioGuard

graph.add_node("verify", CapiscioGuard())
graph.add_edge("verify", "agent")
```

### Decorator

```python
from langchain_capiscio import capiscio_guard

@capiscio_guard(mode="block")
def call_external_agent(state: dict) -> dict:
    ...
```

Works with both sync and async functions.

---

## Badge Token Extraction

`CapiscioGuard` extracts the caller's badge JWT from (in priority order):

1. **Context variable** — set by A2A server perimeter middleware
2. **RunnableConfig** — `config={"configurable": {"capiscio_badge": token}}`
3. **Input dict** — `{"capiscio_badge": token, ...}`

For A2A endpoints, set context at the HTTP boundary:

```python
from langchain_capiscio import CapiscioRequestContext, set_capiscio_context

set_capiscio_context(CapiscioRequestContext(
    badge_token=badge_jwt,
    caller_did="did:web:caller.example.com",
))
```

After guard execution, read the verification result from the same context:

```python
from langchain_capiscio import get_capiscio_context

ctx = get_capiscio_context()
ctx.verified   # True if badge was valid
ctx.claims     # Decoded badge claims dict
ctx.warnings   # List of warning strings (monitor/log modes), or None
```

---

## Full Example: A2A Agent with Trust + Events

```python
from langchain_capiscio import CapiscioGuard, CapiscioCallbackHandler
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# 1. Guard — zero-config, reads CAPISCIO_API_KEY from env
guard = CapiscioGuard(mode="log")

# 2. Agent
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools=[...])

# 3. Compose — guard verifies trust before agent runs
secured = guard | agent

# 4. Callbacks — audit events to CapiscIO dashboard
handler = CapiscioCallbackHandler(identity=guard.identity)

result = secured.invoke(
    {"input": "Validate the agent at https://example.com"},
    config={"callbacks": [handler]},
)
```

---

## Tool-Level Enforcement

For fine-grained control, wrap individual tools:

```python
from langchain_capiscio import CapiscioTool

secured_tool = CapiscioTool(
    my_dangerous_tool,
    mode="block",
    identity=guard.identity,
)
```

---

## API Reference

### `CapiscioGuard`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | `str` | `"block"` | `"block"` \| `"monitor"` \| `"log"` |
| `api_key` | `str \| None` | `None` | Falls back to `CAPISCIO_API_KEY` env |
| `name` | `str \| None` | `None` | Falls back to `CAPISCIO_AGENT_NAME` env |
| `server_url` | `str \| None` | `None` | Falls back to `CAPISCIO_SERVER_URL` env |
| `connect_kwargs` | `dict \| None` | `None` | Extra kwargs for `CapiscIO.connect()` |
| `identity` | `AgentIdentity \| None` | `None` | Pre-existing identity (skips connect) |

**Methods:** `invoke()`, `ainvoke()`, `from_env()`

### `CapiscioCallbackHandler`

| Parameter | Type | Description |
|-----------|------|-------------|
| `emitter` | `EventEmitter \| None` | Event emitter instance |
| `identity` | `AgentIdentity \| None` | Used to obtain emitter if none provided |

### `@capiscio_guard`

```python
@capiscio_guard(mode="block", identity=None, config=None, api_key=None)
def my_node(state: dict) -> dict: ...
```

### `CapiscioTool`

| Parameter | Type | Description |
|-----------|------|-------------|
| `tool` | `Tool` | LangChain tool to wrap |
| `mode` | `str` | Enforcement mode |
| `identity` | `AgentIdentity \| None` | Pre-existing identity |

---

## See Also

- [Security Guide](../../getting-started/secure/1-intro.md) — Full CapiscIO security setup
- [Sign Outbound Requests](../security/sign-outbound.md) — Request signing details
- [Ephemeral Deployment](../security/ephemeral-deployment.md) — `from_env()` patterns for CI/CD
- [FastAPI Integration](fastapi.md) — FastAPI middleware setup
