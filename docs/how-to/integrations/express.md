---
title: Express Integration
description: Add CapiscIO security to Express.js applications
---

# Express Integration

Protect your Express-based A2A agent with request signing and verification.

---

## Problem

You have an Express.js application serving as an A2A agent and need to:

- Verify incoming request signatures
- Sign outgoing responses  
- Create reusable middleware
- Handle errors appropriately

---

## Solution: Express Middleware

```javascript
const express = require('express');
const { SimpleGuard } = require('capiscio');

const app = express();
const guard = new SimpleGuard({
    privateKeyPath: 'capiscio_keys/private.pem',
    trustStorePath: 'capiscio_keys/trusted/'
});

// Middleware to verify signatures
const requireSignature = async (req, res, next) => {
    const authHeader = req.headers.authorization || '';
    
    if (!authHeader.startsWith('Bearer ')) {
        return res.status(401).json({
            error: 'Missing or invalid Authorization header'
        });
    }
    
    const jwsToken = authHeader.slice(7);
    
    try {
        const claims = await guard.verifyInbound(jwsToken, req.rawBody);
        req.verifiedClaims = claims;
        next();
    } catch (err) {
        return res.status(401).json({
            error: `Signature verification failed: ${err.message}`
        });
    }
};

// Capture raw body for signature verification
app.use(express.json({
    verify: (req, res, buf) => {
        req.rawBody = buf;
    }
}));

app.post('/a2a/tasks', requireSignature, async (req, res) => {
    const issuer = req.verifiedClaims?.iss || 'unknown';
    
    const result = {
        status: 'completed',
        taskId: req.body.id,
        verifiedFrom: issuer
    };
    
    // Sign the response
    const responseBody = JSON.stringify(result);
    const signature = await guard.signOutbound(Buffer.from(responseBody));
    
    res.setHeader('X-A2A-Signature', signature);
    res.json(result);
});

app.listen(8000, () => {
    console.log('A2A agent running on port 8000');
});
```

---

## Step-by-Step Setup

### Step 1: Install Dependencies

```bash
npm install express capiscio
```

### Step 2: Generate Keys

```bash
npx capiscio key gen --out capiscio_keys/
mkdir -p capiscio_keys/trusted/
```

### Step 3: Create the Application

Create `app.js`:

```javascript
const express = require('express');
const { SimpleGuard } = require('capiscio');
const path = require('path');

const app = express();

// Configuration
const DEV_MODE = process.env.CAPISCIO_DEV_MODE === 'true';
const PORT = process.env.PORT || 8000;

// Initialize SimpleGuard
const guard = new SimpleGuard({
    privateKeyPath: path.join(__dirname, 'capiscio_keys/private.pem'),
    trustStorePath: path.join(__dirname, 'capiscio_keys/trusted/'),
    devMode: DEV_MODE
});

// Capture raw body for signature verification
app.use(express.json({
    verify: (req, res, buf) => {
        req.rawBody = buf;
    }
}));

// Signature verification middleware
const requireSignature = async (req, res, next) => {
    const authHeader = req.headers.authorization || '';
    
    if (!authHeader.startsWith('Bearer ')) {
        return res.status(401).json({
            jsonrpc: '2.0',
            error: {
                code: -32001,
                message: 'Missing or invalid Authorization header'
            },
            id: req.body?.id || null
        });
    }
    
    const jwsToken = authHeader.slice(7);
    
    try {
        const claims = await guard.verifyInbound(jwsToken, req.rawBody);
        req.verifiedClaims = claims;
        next();
    } catch (err) {
        return res.status(401).json({
            jsonrpc: '2.0',
            error: {
                code: -32001,
                message: `Signature verification failed: ${err.message}`
            },
            id: req.body?.id || null
        });
    }
};

// Response signing middleware
const signResponse = (handler) => {
    return async (req, res) => {
        const result = await handler(req);
        const responseBody = JSON.stringify(result);
        
        const signature = await guard.signOutbound(Buffer.from(responseBody));
        
        res.setHeader('X-A2A-Signature', signature);
        res.json(result);
    };
};

// Routes
app.post('/a2a/tasks', requireSignature, signResponse(async (req) => {
    const issuer = req.verifiedClaims?.iss || 'unknown';
    const task = req.body;
    
    // Process the task
    return {
        status: 'completed',
        taskId: task.id,
        verifiedFrom: issuer
    };
}));

// Agent card (no signature required)
app.get('/.well-known/agent-card.json', async (req, res) => {
    res.json({
        name: 'My Express Agent',
        url: `http://localhost:${PORT}`,
        capabilities: { streaming: false },
        skills: [{ id: 'example', name: 'Example Skill' }],
        public_keys: [await guard.getPublicKeyJwk()]
    });
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

// Error handler
app.use((err, req, res, next) => {
    console.error('Error:', err);
    res.status(500).json({
        jsonrpc: '2.0',
        error: {
            code: -32603,
            message: 'Internal server error'
        },
        id: req.body?.id || null
    });
});

app.listen(PORT, () => {
    console.log(`A2A agent running on port ${PORT}`);
    console.log(`Dev mode: ${DEV_MODE}`);
});
```

### Step 4: Run the Application

```bash
# Development
CAPISCIO_DEV_MODE=true node app.js

# Production
node app.js
```

---

## TypeScript Version

```typescript
// app.ts
import express, { Request, Response, NextFunction } from 'express';
import { SimpleGuard } from 'capiscio';
import path from 'path';

interface VerifiedRequest extends Request {
    rawBody?: Buffer;
    verifiedClaims?: {
        iss: string;
        iat: number;
        [key: string]: unknown;
    };
}

const app = express();
const DEV_MODE = process.env.CAPISCIO_DEV_MODE === 'true';

const guard = new SimpleGuard({
    privateKeyPath: path.join(__dirname, 'capiscio_keys/private.pem'),
    trustStorePath: path.join(__dirname, 'capiscio_keys/trusted/'),
    devMode: DEV_MODE
});

// Capture raw body
app.use(express.json({
    verify: (req: VerifiedRequest, _res, buf) => {
        req.rawBody = buf;
    }
}));

// Middleware
const requireSignature = async (
    req: VerifiedRequest,
    res: Response,
    next: NextFunction
) => {
    const authHeader = req.headers.authorization || '';
    
    if (!authHeader.startsWith('Bearer ')) {
        res.status(401).json({ error: 'Missing Authorization header' });
        return;
    }
    
    try {
        const claims = await guard.verifyInbound(
            authHeader.slice(7),
            req.rawBody!
        );
        req.verifiedClaims = claims;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Verification failed' });
    }
};

app.post('/a2a/tasks', requireSignature, async (req: VerifiedRequest, res) => {
    const result = {
        status: 'completed',
        verifiedFrom: req.verifiedClaims?.iss
    };
    
    const signature = await guard.signOutbound(
        Buffer.from(JSON.stringify(result))
    );
    
    res.setHeader('X-A2A-Signature', signature);
    res.json(result);
});

app.listen(8000);
```

---

## Router Pattern

For larger applications:

```javascript
// routes/a2a.js
const express = require('express');
const router = express.Router();

module.exports = (guard) => {
    const requireSignature = async (req, res, next) => {
        // ... middleware logic
    };
    
    router.post('/tasks', requireSignature, async (req, res) => {
        // ... handler logic
    });
    
    return router;
};
```

```javascript
// app.js
const express = require('express');
const { SimpleGuard } = require('capiscio');
const a2aRoutes = require('./routes/a2a');

const app = express();
const guard = new SimpleGuard({ /* config */ });

app.use('/a2a', a2aRoutes(guard));
```

---

## Error Handling Patterns

### JSON-RPC Style Errors

```javascript
const errorHandler = (err, req, res, next) => {
    console.error('Error:', err);
    
    const errorResponse = {
        jsonrpc: '2.0',
        error: {
            code: err.code || -32603,
            message: err.message || 'Internal server error'
        },
        id: req.body?.id || null
    };
    
    res.status(err.status || 500).json(errorResponse);
};

app.use(errorHandler);
```

### Custom Error Classes

```javascript
class SignatureError extends Error {
    constructor(message) {
        super(message);
        this.name = 'SignatureError';
        this.status = 401;
        this.code = -32001;
    }
}

class TrustError extends Error {
    constructor(message) {
        super(message);
        this.name = 'TrustError';
        this.status = 403;
        this.code = -32002;
    }
}
```

---

## Testing

```javascript
// test/app.test.js
const request = require('supertest');
const app = require('../app');

describe('A2A Endpoints', () => {
    test('rejects requests without auth header', async () => {
        const response = await request(app)
            .post('/a2a/tasks')
            .send({ id: 'test' });
        
        expect(response.status).toBe(401);
    });
    
    test('rejects invalid signatures', async () => {
        const response = await request(app)
            .post('/a2a/tasks')
            .set('Authorization', 'Bearer invalid.token.here')
            .send({ id: 'test' });
        
        expect(response.status).toBe(401);
    });
});
```

---

## Production Deployment

### PM2

```bash
npm install -g pm2
pm2 start app.js --name a2a-agent
```

### Docker

```dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Don't include keys in image - mount at runtime
EXPOSE 8000

CMD ["node", "app.js"]
```

```bash
docker run -p 8000:8000 \
  -v $(pwd)/capiscio_keys:/app/capiscio_keys \
  -e CAPISCIO_DEV_MODE=false \
  myagent:latest
```

---

## See Also

- [FastAPI Integration](fastapi.md) — Python equivalent
- [Flask Integration](flask.md) — Flask equivalent  
- [Sign Outbound Requests](../security/sign-outbound.md) — Signing details
