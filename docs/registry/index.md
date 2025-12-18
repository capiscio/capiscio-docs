---
title: Agent Registry - Discover and Be Discovered
description: The public directory of trusted AI agents. Register your agent, discover others, build the agent ecosystem.
---

# 📋 Agent Registry

> **The public directory of trusted AI agents. Register once, be discovered everywhere.**

## Why a Registry?

The agent economy needs a way to **find** agents:

| Without Registry | With Registry |
|-----------------|---------------|
| "What's the URL for that weather agent?" | Search: `weather forecast` |
| "Is this agent card real or spoofed?" | Verified agent cards |
| "Who runs this agent?" | Organization info + badges |
| "Which agents can do X?" | Skill-based discovery |

**CapiscIO Registry** is the index that makes the agent economy navigable.

---

## Register Your Agent in 2 Minutes

### Step 1: Install CLI

```bash
npm install -g capiscio   # or: pip install capiscio
```

### Step 2: Initialize Your Agent

```bash
capiscio init
```

This creates:
- `agent-card.json` — Your agent's public metadata
- `capiscio_keys/` — Your cryptographic identity

### Step 3: Register

```bash
capiscio register
```

```
🚀 Registering your agent...

✅ Agent registered!

Your Agent:
  DID:      did:web:registry.capisc.io:agents:weather-bot-12ab
  URL:      https://registry.capisc.io/agents/weather-bot-12ab
  Trust:    Level 1 (Registered)

Dashboard: https://registry.capisc.io/dashboard
Next step: Request a badge to increase trust → capiscio badge request
```

**That's it.** Your agent is now discoverable.

---

## What Gets Registered

When you register, your agent card is indexed:

```json
{
  "name": "Weather Forecast Agent",
  "description": "Provides accurate weather forecasts for any location",
  "url": "https://weather.example.com/agent",
  "version": "2.1.0",
  "provider": {
    "organization": "WeatherCorp Inc."
  },
  "skills": [
    {
      "id": "forecast",
      "name": "Weather Forecast",
      "description": "Get weather forecast for a location",
      "inputModes": ["text"],
      "outputModes": ["text", "json"]
    }
  ],
  "authentication": {
    "schemes": ["jws"],
    "credentials": [{ "..." }]
  }
}
```

The registry indexes:
- **Name & description** — For text search
- **Skills** — For capability-based discovery
- **Provider** — For organization lookup
- **Trust level** — From your badge
- **Availability** — Live health checks

---

## Discover Agents

### Web UI

Browse the registry at **[registry.capisc.io](https://registry.capisc.io)**

### CLI Search

```bash
# Search by keyword
capiscio search "weather forecast"

# Filter by trust level
capiscio search "payment" --min-trust-level 3

# Filter by skill
capiscio search --skill "image-generation"
```

```
Found 3 agents:

┌─────────────────────────────────────────────────────────────────┐
│ 🏅 ACME Weather Bot                            Trust: ⭐⭐⭐ (OV) │
├─────────────────────────────────────────────────────────────────┤
│ Accurate weather forecasts for any location worldwide          │
│ Skills: forecast, alerts, historical                           │
│ DID: did:web:registry.capisc.io:agents:acme-weather           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🏅 MeteoAgent                                   Trust: ⭐⭐ (DV) │
├─────────────────────────────────────────────────────────────────┤
│ European weather specialist with radar imagery                 │
│ Skills: forecast, radar, marine                                │
│ DID: did:web:registry.capisc.io:agents:meteo-agent            │
└─────────────────────────────────────────────────────────────────┘
```

### API Access

```bash
curl "https://registry.capisc.io/api/v1/agents?q=weather&min_trust=2"
```

```json
{
  "agents": [
    {
      "did": "did:web:registry.capisc.io:agents:acme-weather",
      "name": "ACME Weather Bot",
      "trust_level": 3,
      "url": "https://weather.acme.io/agent",
      "skills": ["forecast", "alerts"],
      "verified": true
    }
  ],
  "total": 1,
  "page": 1
}
```

---

## Registry Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CapiscIO Registry                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Agent Index  │  │  Badge CA    │  │ DID Resolver │          │
│  │              │  │              │  │              │          │
│  │ • Search     │  │ • Issue      │  │ • did:web    │          │
│  │ • Filter     │  │ • Verify     │  │ • Resolution │          │
│  │ • Sort       │  │ • Revoke     │  │ • Caching    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                      │
│                    ┌──────────────┐                              │
│                    │   REST API   │                              │
│                    └──────────────┘                              │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
        CLI Tools      Web Dashboard    Your Agent
```

---

## API Reference

### List Agents

```http
GET /api/v1/agents
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query |
| `skill` | string | Filter by skill |
| `min_trust` | int | Minimum trust level (0-4) |
| `provider` | string | Filter by organization |
| `page` | int | Page number |
| `limit` | int | Results per page (max 100) |

### Get Agent

```http
GET /api/v1/agents/{did}
```

Returns full agent card with trust info.

### Register Agent

```http
POST /api/v1/agents
Authorization: Bearer {token}
Content-Type: application/json

{
  "agent_card": { ... },
  "public_key": { ... }
}
```

### Update Agent

```http
PUT /api/v1/agents/{did}
Authorization: Bearer {token}
```

### DID Resolution

```http
GET /agents/{id}/did.json
```

Returns W3C DID Document for `did:web:registry.capisc.io:agents:{id}`.

---

## Self-Hosting

For enterprise deployments, run your own registry:

```bash
docker run -d \
  -p 8080:8080 \
  -e DATABASE_URL=postgres://... \
  -e CA_PRIVATE_KEY_PATH=/keys/ca.pem \
  ghcr.io/capiscio/capiscio-server:latest
```

Your agents get DIDs like:
```
did:web:your-company.com:agents:internal-bot
```

See [Server Deployment Guide](../reference/server/deployment.md) for full setup.

---

## Privacy & Control

| Data | Visibility | Your Control |
|------|------------|--------------|
| Agent name/description | Public | You choose what to publish |
| Skills | Public | Define your capabilities |
| Organization | Public (optional) | Opt-in to org verification |
| Endpoint URL | Public | Required for discovery |
| Private keys | Never uploaded | Stay on your infrastructure |
| Request logs | Not collected | We don't track agent traffic |

**You own your identity.** The registry indexes public metadata only.

---

## Developer Integration

### Fetch Agent by DID

```python
from capiscio_sdk import Registry

registry = Registry()

# Get agent info
agent = await registry.get_agent("did:web:registry.capisc.io:agents:weather")
print(agent.name, agent.trust_level)

# Search agents
results = await registry.search("weather", min_trust_level=2)
for agent in results:
    print(f"{agent.name}: {agent.url}")
```

### Verify Before Calling

```python
async def call_agent(did: str, task: dict):
    # Resolve and verify agent
    agent = await registry.get_agent(did)
    
    if agent.trust_level < 2:
        raise InsufficientTrustError(f"Agent {did} is trust level {agent.trust_level}")
    
    # Agent is verified, make the call
    async with guard.client() as client:
        return await client.post(agent.url, json=task)
```

---

## Next Steps

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Register Now**

    ---

    Get your agent into the registry in 2 minutes.

    ```bash
    capiscio register
    ```

-   :material-certificate:{ .lg .middle } **Upgrade Trust Level**

    ---

    Request a badge to increase visibility.

    [:octicons-arrow-right-24: Trust Badges](../trust/index.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Full REST API documentation.

    [:octicons-arrow-right-24: Server API](../reference/server/api.md)

-   :material-server:{ .lg .middle } **Self-Host**

    ---

    Run your own enterprise registry.

    [:octicons-arrow-right-24: Deployment Guide](../reference/server/deployment.md)

</div>

---

## FAQ

??? question "Is the registry required?"
    
    No! You can use CapiscIO with self-signed `did:key` identities and direct peer-to-peer trust. The registry adds **discoverability** and **verified trust levels**.

??? question "What does registration cost?"
    
    Registration is **free**. Trust badges:
    - Level 0-2: Free
    - Level 3-4: TBD (requires manual verification)

??? question "Can I remove my agent?"
    
    Yes. `capiscio unregister` removes your agent from the index. Your DID continues to work for direct communication.

??? question "How is uptime monitored?"
    
    The registry periodically pings registered agent endpoints. Availability metrics are shown on agent profiles but don't affect trust level.
