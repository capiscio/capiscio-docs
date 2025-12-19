# Agent Card Schema Reference

The Agent Card is a JSON document that describes an A2A-compliant agent. This reference covers the complete JSON Schema specification.

---

## Overview

An Agent Card is a JSON document that can be hosted at any URL. Common patterns include:

- **Direct URL**: `https://my-agent.example.com/agent-card.json`
- **Well-known (for discovery)**: `https://domain.com/.well-known/agent-card.json`
- **API path**: `https://api.example.com/agents/weather/agent-card.json`

The `/.well-known/` path is recommended for public agent discovery but is not required.

An Agent Card contains:

- **Identity**: Agent name, description, and provider
- **Capabilities**: Skills and supported protocols  
- **Endpoints**: URLs for agent communication
- **Authentication**: Supported auth methods
- **Security**: Cryptographic signatures and trust badges

---

## Minimal Example

```json
{
  "name": "My Agent",
  "description": "A helpful AI assistant",
  "url": "https://my-agent.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "general-chat",
      "name": "General Chat",
      "description": "General conversation and Q&A"
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

---

## Complete Schema

### Root Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | ✓ | Human-readable agent name |
| `description` | `string` | ✓ | Brief description of the agent |
| `url` | `string` | ✓ | Base URL of the agent |
| `version` | `string` | ✓ | Agent version (semver recommended) |
| `capabilities` | `object` | ✓ | Agent capabilities |
| `skills` | `array` | ✓ | List of agent skills |
| `defaultInputModes` | `array` | ✓ | Default input modes |
| `defaultOutputModes` | `array` | ✓ | Default output modes |
| `provider` | `object` | | Provider information |
| `documentationUrl` | `string` | | URL to documentation |
| `authentication` | `object` | | Authentication configuration |
| `supportsAuthenticatedExtendedCard` | `boolean` | | Extended card support |

### capabilities

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `streaming` | `boolean` | ✓ | | Supports streaming responses |
| `pushNotifications` | `boolean` | ✓ | | Supports push notifications |
| `stateTransitionHistory` | `boolean` | | `false` | Tracks state history |

```json
{
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  }
}
```

### skills

Array of skill objects. At least one skill is required.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✓ | Unique skill identifier |
| `name` | `string` | ✓ | Human-readable skill name |
| `description` | `string` | ✓ | Skill description |
| `tags` | `array` | | Categorization tags |
| `examples` | `array` | | Example inputs |
| `inputModes` | `array` | | Override default input modes |
| `outputModes` | `array` | | Override default output modes |

```json
{
  "skills": [
    {
      "id": "code-review",
      "name": "Code Review",
      "description": "Reviews code for bugs, style issues, and improvements",
      "tags": ["development", "code-quality"],
      "examples": [
        "Review this Python function for bugs",
        "Check this code for security issues"
      ],
      "inputModes": ["text", "file"],
      "outputModes": ["text"]
    }
  ]
}
```

### provider

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `organization` | `string` | ✓ | Organization name |
| `url` | `string` | | Organization website |
| `contactEmail` | `string` | | Support email |

```json
{
  "provider": {
    "organization": "Acme AI",
    "url": "https://acme.ai",
    "contactEmail": "support@acme.ai"
  }
}
```

### authentication

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schemes` | `array` | ✓ | Supported auth schemes |
| `credentials` | `string` | | Where credentials are sent |

**Supported schemes:**

| Scheme | Description |
|--------|-------------|
| `none` | No authentication required |
| `bearer` | Bearer token authentication |
| `oauth2` | OAuth 2.0 flow |
| `apiKey` | API key authentication |

```json
{
  "authentication": {
    "schemes": ["bearer", "oauth2"],
    "credentials": "header"
  }
}
```

### Input/Output Modes

| Mode | Description |
|------|-------------|
| `text` | Plain text |
| `file` | File upload/download |
| `image` | Image data |
| `audio` | Audio data |
| `video` | Video data |
| `data` | Structured JSON data |

---

## Signed Agent Card

For production deployments, Agent Cards should be signed using JWS (JSON Web Signature).

### Structure

A signed Agent Card wraps the card in a JWS envelope:

```json
{
  "payload": "<base64url-encoded-agent-card>",
  "protected": "<base64url-encoded-header>",
  "signature": "<base64url-encoded-signature>"
}
```

### Header

```json
{
  "alg": "EdDSA",
  "kid": "did:capiscio:agent:my-agent#key-1"
}
```

### Signing Example

```bash
# Generate keys
capiscio key gen --out-priv private.jwk --out-pub public.jwk

# Sign the agent card (coming soon)
capiscio sign ./agent-card.json --key private.jwk --out signed-agent-card.json
```

---

## Extended Card

An extended card provides additional information available only to authenticated clients.

```json
{
  "name": "My Agent",
  "description": "A helpful AI assistant",
  "supportsAuthenticatedExtendedCard": true,
  "extendedCard": {
    "url": "https://my-agent.example.com/.well-known/agent-extended.json",
    "authentication": {
      "schemes": ["bearer"]
    }
  }
}
```

---

## Validation Rules

### Required Fields

The following fields must be present:

- `name` - Non-empty string
- `description` - Non-empty string  
- `url` - Valid HTTPS URL
- `version` - Non-empty string
- `capabilities.streaming` - Boolean
- `capabilities.pushNotifications` - Boolean
- `skills` - Non-empty array
- `skills[].id` - Unique non-empty string
- `skills[].name` - Non-empty string
- `skills[].description` - Non-empty string
- `defaultInputModes` - Non-empty array
- `defaultOutputModes` - Non-empty array

### URL Requirements

- Must use HTTPS in production
- Must be publicly accessible (or accessible from validator)
- Should respond within timeout (default 10s)

### Skill Requirements

- Each skill must have a unique `id`
- At least one skill is required
- Skill `id` should be kebab-case (`code-review`, not `CodeReview`)

---

## Best Practices

### Naming

- Use clear, descriptive names
- Avoid generic names like "Agent" or "Assistant"
- Include your organization name if appropriate

### Descriptions

- Write clear, concise descriptions
- Explain what the agent does, not how
- Include key capabilities

### Skills

- Define focused, single-purpose skills
- Use descriptive skill names
- Provide helpful examples
- Use appropriate tags for discovery

### Versioning

- Use semantic versioning (semver)
- Update version when capabilities change
- Document breaking changes

---

## JSON Schema

The full JSON Schema is available at:

```
https://registry.capisc.io/schemas/agent-card/v1.json
```

### Validating with JSON Schema

```bash
# Using ajv-cli
npx ajv validate -s https://registry.capisc.io/schemas/agent-card/v1.json -d ./agent-card.json

# Using capiscio (recommended)
capiscio validate ./agent-card.json --schema-only
```

---

## Examples

### Minimal Agent

```json
{
  "name": "Echo Agent",
  "description": "Echoes back any message",
  "url": "https://echo.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "echo",
      "name": "Echo",
      "description": "Echoes back the input message"
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"]
}
```

### Full-Featured Agent

```json
{
  "name": "CodeAssist Pro",
  "description": "AI-powered code assistant for development teams",
  "url": "https://codeassist.example.com",
  "version": "2.1.0",
  "documentationUrl": "https://docs.codeassist.example.com",
  "provider": {
    "organization": "DevTools Inc",
    "url": "https://devtools.example.com",
    "contactEmail": "support@devtools.example.com"
  },
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "code-review",
      "name": "Code Review",
      "description": "Reviews code for bugs, style issues, and security vulnerabilities",
      "tags": ["code", "review", "security"],
      "examples": [
        "Review this function for potential bugs",
        "Check for security vulnerabilities"
      ],
      "inputModes": ["text", "file"],
      "outputModes": ["text"]
    },
    {
      "id": "code-generation",
      "name": "Code Generation",
      "description": "Generates code from natural language descriptions",
      "tags": ["code", "generation", "ai"],
      "examples": [
        "Write a Python function to sort a list",
        "Create a REST API endpoint"
      ],
      "inputModes": ["text"],
      "outputModes": ["text", "file"]
    },
    {
      "id": "documentation",
      "name": "Documentation",
      "description": "Generates documentation for code",
      "tags": ["docs", "documentation"],
      "inputModes": ["text", "file"],
      "outputModes": ["text"]
    }
  ],
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "authentication": {
    "schemes": ["bearer", "oauth2"],
    "credentials": "header"
  },
  "supportsAuthenticatedExtendedCard": true
}
```

---

## See Also

- [Validate Your First Agent](../getting-started/validate/1-intro.md)
- [CLI Reference](cli/index.md)
- [A2A Specification](https://a2a-protocol.org/latest/specification/)
