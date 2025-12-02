"""
Secure A2A Agent with CapiscIO
Run: uvicorn secure_agent:app --reload
"""

from fastapi import FastAPI, Request, HTTPException
from capiscio_sdk import SimpleGuard, CapiscioSignatureError

app = FastAPI(title="Secure A2A Agent")

# Initialize security (use dev_mode=False in production)
guard = SimpleGuard(dev_mode=True)


@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """Serve the agent card."""
    return {
        "name": "My Secure Agent",
        "description": "A CapiscIO-secured A2A agent",
        "url": "https://my-agent.example.com",
        "version": "1.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [
            {
                "id": "echo",
                "name": "Echo",
                "description": "Echoes back your message",
            }
        ],
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
    }


@app.post("/a2a")
async def handle_a2a(request: Request):
    """Handle A2A requests with signature verification."""
    signature = request.headers.get("X-Capiscio-Signature")
    body = await request.body()

    # Verify signature if present
    if signature:
        try:
            claims = guard.verify_inbound(signature, body)
            print(f"Verified request from: {claims.get('iss')}")
        except CapiscioSignatureError:
            raise HTTPException(401, "Invalid signature")

    # Process request
    data = await request.json()

    # Sign response
    response = {
        "jsonrpc": "2.0",
        "result": {"echo": data.get("params", {}).get("message", "Hello!")},
        "id": data.get("id"),
    }

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
