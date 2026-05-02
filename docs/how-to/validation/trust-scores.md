# Monitor and Improve Trust Scores

Check your agent's validation score and fix common issues.

---

## Check Your Score

```bash
capiscio validate ./agent-card.json --json | jq '.scores'
```

Output:

```json
{
  "compliance": 95,
  "trust": 80,
  "availability": 100
}
```

---

## Score Categories

| Category | What It Measures |
|----------|------------------|
| **Compliance** | Schema correctness, required fields |
| **Trust** | Signature validity, identity verification |
| **Availability** | Endpoint reachability, response times |

---

## Improve Your Score

- **Compliance**: Fix all schema warnings (`capiscio validate --strict`)
- **Trust**: Use CA-signed badges (trust level 2+)
- **Availability**: Ensure `/.well-known/agent.json` is publicly accessible
