---
title: LangChain Integration
description: Secure LangChain agents with CapiscIO
---

# LangChain Integration

Build secure AI agents using LangChain with CapiscIO request signing.

---

## Problem

You're building a LangChain-based agent and need to:

- Expose it as an A2A-compliant endpoint
- Sign all outgoing tool calls to other agents
- Verify incoming requests from calling agents
- Integrate with LangChain's callback system

---

## Solution: LangChain + CapiscIO

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from capiscio_sdk.simple_guard import SimpleGuard
import httpx
import json

# Initialize CapiscIO guard (uses convention-based key discovery)
guard = SimpleGuard(dev_mode=True)  # Use dev_mode=False in production

def make_secure_request(url: str, body: dict) -> dict:
    """Make a signed request to another A2A agent."""
    body_bytes = json.dumps(body).encode()
    headers = guard.make_headers({}, body=body_bytes)
    
    response = httpx.post(url, json=body, headers=headers)
    return response.json()

# Create a secure tool
external_agent_tool = Tool(
    name="external_agent",
    description="Call an external A2A agent securely",
    func=lambda query: make_secure_request(
        "https://other-agent.example.com/a2a/tasks",
        {"method": "tasks/send", "params": {"message": query}}
    )
)

# Initialize the agent
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    tools=[external_agent_tool],
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS
)
```

---

## Full Implementation

### Step 1: Project Setup

```bash
pip install langchain langchain-openai capiscio-sdk httpx fastapi uvicorn
capiscio key gen --out capiscio_keys/
mkdir -p capiscio_keys/trusted/
```

### Step 2: Create the Agent

```python
# agent.py
import json
from typing import Any
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool, StructuredTool
from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from capiscio_sdk.simple_guard import SimpleGuard
import httpx

# Security setup - SimpleGuard uses convention (capiscio_keys/ directory)
guard = SimpleGuard(dev_mode=True)  # Use dev_mode=False in production

class SecureA2AClient:
    """Client for making secure A2A requests."""
    
    def __init__(self, guard: SimpleGuard):
        self.guard = guard
        self.client = httpx.Client(timeout=30.0)
    
    def call_agent(self, url: str, message: str, task_id: str = None) -> dict:
        """Send a signed request to another A2A agent."""
        body = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": message}]
                }
            },
            "id": task_id or "1"
        }
        
        body_bytes = json.dumps(body).encode()
        headers = self.guard.make_headers({}, body=body_bytes)
        headers["Content-Type"] = "application/json"
        
        response = self.client.post(url, content=body_bytes, headers=headers)
        response.raise_for_status()
        return response.json()

# Create secure client
secure_client = SecureA2AClient(guard)

# Define tools that call other agents
def call_validator_agent(agent_card_url: str) -> str:
    """Validate an agent card using the validator service."""
    result = secure_client.call_agent(
        "https://validator.capiscio.dev/a2a/tasks",
        f"Validate the agent card at: {agent_card_url}"
    )
    return json.dumps(result, indent=2)

def call_analytics_agent(query: str) -> str:
    """Get analytics data from the analytics agent."""
    result = secure_client.call_agent(
        "https://analytics.example.com/a2a/tasks",
        query
    )
    return json.dumps(result, indent=2)

# Create LangChain tools
tools = [
    Tool(
        name="validate_agent",
        description="Validate an A2A agent card URL. Use when asked to check if an agent is compliant.",
        func=call_validator_agent
    ),
    Tool(
        name="get_analytics",
        description="Query the analytics agent for usage data and metrics.",
        func=call_analytics_agent
    )
]

# Initialize the LangChain agent
llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

def run_agent(user_message: str) -> str:
    """Run the agent with a user message."""
    return agent_executor.invoke({"input": user_message})["output"]
```

### Step 3: Expose as A2A Endpoint

```python
# server.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

from agent import guard, run_agent

app = FastAPI()

class TextPart(BaseModel):
    type: str = "text"
    text: str

class Message(BaseModel):
    role: str
    parts: List[TextPart]

class TaskParams(BaseModel):
    message: Message

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

@app.post("/a2a/tasks")
async def handle_task(request: Request):
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify signature
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    try:
        claims = guard.verify_inbound(auth_header[7:], body)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Verification failed: {e}")
    
    # Parse request
    data = json.loads(body)
    method = data.get("method")
    params = data.get("params", {})
    request_id = data.get("id")
    
    if method != "tasks/send":
        raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
    
    # Extract message
    message = params.get("message", {})
    parts = message.get("parts", [])
    text = parts[0].get("text", "") if parts else ""
    
    # Run the agent
    result = run_agent(text)
    
    # Build response
    response_data = {
        "jsonrpc": "2.0",
        "result": {
            "status": "completed",
            "response": {
                "role": "assistant",
                "parts": [{"type": "text", "text": result}]
            }
        },
        "id": request_id
    }
    
    # Sign response
    response_body = json.dumps(response_data).encode()
    signature = guard.sign_outbound({}, body=response_body)
    
    return Response(
        content=response_body,
        media_type="application/json",
        headers={"X-A2A-Signature": signature}
    )

@app.get("/.well-known/agent-card.json")
@app.get("/.well-known/agent-card.json")
async def agent_card():
    # Load from agent-card.json (created by SimpleGuard in dev_mode)
    import json
    with open("agent-card.json") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Custom Callback Handler

Log all secure agent-to-agent calls:

```python
from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("a2a")

class A2ACallbackHandler(BaseCallbackHandler):
    """Log A2A interactions."""
    
    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs
    ):
        tool_name = serialized.get("name", "unknown")
        logger.info(f"🔧 Tool call: {tool_name}")
        logger.info(f"   Input: {input_str[:100]}...")
    
    def on_tool_end(self, output: str, **kwargs):
        logger.info(f"✅ Tool response: {output[:100]}...")
    
    def on_tool_error(self, error: Exception, **kwargs):
        logger.error(f"❌ Tool error: {error}")

# Use the callback
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    callbacks=[A2ACallbackHandler()],
    verbose=True
)
```

---

## Async Support

```python
import asyncio
import httpx
from langchain.tools import Tool

class AsyncSecureA2AClient:
    """Async client for A2A requests."""
    
    def __init__(self, guard: SimpleGuard):
        self.guard = guard
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def call_agent(self, url: str, message: str) -> dict:
        body = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": message}]
                }
            },
            "id": "1"
        }
        
        body_bytes = json.dumps(body).encode()
        headers = self.guard.make_headers({}, body=body_bytes)
        headers["Content-Type"] = "application/json"
        
        response = await self.client.post(url, content=body_bytes, headers=headers)
        return response.json()

# For async tools, use asyncio.run() wrapper or async agent
async_client = AsyncSecureA2AClient(guard)

def call_agent_sync(url: str, message: str) -> str:
    """Sync wrapper for async client."""
    result = asyncio.run(async_client.call_agent(url, message))
    return json.dumps(result)
```

---

## Multi-Agent Orchestration

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

# Define multiple agent endpoints
AGENTS = {
    "validator": "https://validator.capiscio.dev/a2a/tasks",
    "summarizer": "https://summarizer.example.com/a2a/tasks",
    "translator": "https://translator.example.com/a2a/tasks",
}

def create_agent_tool(name: str, url: str, description: str) -> Tool:
    """Factory for creating secure agent tools."""
    
    def call_fn(message: str) -> str:
        result = secure_client.call_agent(url, message)
        return json.dumps(result, indent=2)
    
    return Tool(
        name=f"call_{name}",
        description=description,
        func=call_fn
    )

# Create tools for each agent
tools = [
    create_agent_tool(
        "validator",
        AGENTS["validator"],
        "Validate A2A agent cards for compliance"
    ),
    create_agent_tool(
        "summarizer",
        AGENTS["summarizer"],
        "Summarize long documents or conversations"
    ),
    create_agent_tool(
        "translator",
        AGENTS["translator"],
        "Translate text between languages"
    ),
]

# The LLM decides which agents to call
orchestrator = initialize_agent(
    tools=tools,
    llm=ChatOpenAI(model="gpt-4o"),
    agent=AgentType.OPENAI_FUNCTIONS
)
```

---

## See Also

- [FastAPI Integration](fastapi.md) — FastAPI setup details
- [Sign Outbound Requests](../security/sign-outbound.md) — Signing details
- [Security Quickstart](../../quickstarts/secure/1-intro.md) — Full security setup
