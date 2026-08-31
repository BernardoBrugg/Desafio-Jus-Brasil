---
name: framework-best-practices
description: Use when working on FastAPI projects: routers, Pydantic schemas, dependencies, async behavior, OpenAPI contracts, auth, database access, tests, and production readiness. Trigger with /framework-best-practices.
---

# FastAPI Best Practices

- Read app initialization, router structure, schemas and dependencies before editing.
- Use Pydantic models for request and response contracts.
- Keep status codes and error responses explicit.
- Use dependency injection for auth, database sessions and config.
- Avoid blocking calls inside async paths unless handled safely.
- Preserve public API compatibility unless a breaking change is requested.
