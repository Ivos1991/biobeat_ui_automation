# Dependency Injection

## Concept Overview

Dependency injection centralizes object construction and keeps business logic free from wiring concerns.

## Why It Matters

It improves testability, makes dependencies visible, and prevents hidden coupling through ad hoc instantiation.

## Core Principles

- Explicit registrations
- Minimal lifecycle model
- One bootstrap location

## Recommended Implementation Patterns

- Use singleton scope for shared services and clients
- Use factory scope for per-use objects when needed
- Resolve through fixtures rather than constructing objects in tests

## Common Mistakes

- Building a full IoC framework for a small project
- Hiding registration across multiple modules
- Injecting everything everywhere

## Examples From This Project

- `ServiceContainer`
- `build_runtime()`
- pytest fixtures backed by the container

## Reusable Templates

```python
container.register_singleton(MyService, lambda c: MyService(c.typed_resolve(MyClient, MyClient)))
```

## Interview Explanations

Dependency injection improves testability by making construction explicit and substitutable. The key tradeoff is some bootstrap verbosity, which is usually worth it.

## Best Practices Checklist

- Construction is centralized
- Dependencies are visible
- Tests consume already-wired services
