---
title: Installation
description: Install CapiscIO MCP Guard for tool-level security on MCP servers.
---

# Installation

MCP Guard provides trust badges and identity verification for [Model Context Protocol](https://modelcontextprotocol.io) tool calls.

## Requirements

- Python 3.10+
- A CapiscIO account or self-hosted registry

## Install via pip

```bash
pip install capiscio-mcp
```

For MCP SDK integration (FastMCP wrapper):

```bash
pip install capiscio-mcp[mcp]
```

## Verify Installation

```bash
python -c "import capiscio_mcp; print(capiscio_mcp.__version__)"
```

## What's Included

| Package | Description |
|---------|-------------|
| `capiscio-mcp` | Core guard decorator and evidence logging |
| `capiscio-mcp[mcp]` | FastMCP integration for automatic tool wrapping |

## Next Steps

- [Quickstart](quickstart.md) — protect your first MCP tool in 5 minutes
