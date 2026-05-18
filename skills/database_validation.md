# Database Validation

## Concept Overview

This repository does not yet implement a repository layer, but future automation frameworks often need direct persistence validation.

## Why It Matters

Database checks can validate side effects that are difficult to prove through UI or API alone.

## Core Principles

- Treat the database as another integration boundary
- Keep queries out of tests
- Normalize results into typed models

## Recommended Implementation Patterns

- Add repository classes under a dedicated module
- Register repositories through the service container
- Use orchestrators when validation spans API and DB

## Common Mistakes

- embedding SQL in tests
- validating too many internal details
- coupling tests to unstable schemas

## Examples From This Project

The current framework prepares for this with a DI container, orchestrators, and typed settings.

## Reusable Templates

```python
container.register_singleton(UserRepository, lambda c: UserRepository(c.typed_resolve(DbSession, DbSession)))
```

## Interview Explanations

A repository layer keeps persistence checks reusable and prevents direct database access from spreading across tests.

## Best Practices Checklist

- Queries are centralized
- Results are typed
- Tests assert business outcomes
