# Lifecycle Hooks

## Concept Overview

Hooks define stable execution points across session, test, step, failure, and API lifecycles.

## Why It Matters

They prevent reporting, evidence, and other integrations from being hardcoded into business logic.

## Core Principles

- Stable hook names
- Typed context objects
- Ordered execution
- Fault isolation

## Recommended Implementation Patterns

- Register handlers with `owner` and `order`
- Use dataclass context objects
- Keep hook handlers small

## Common Mistakes

- Too many granular hooks
- Untyped dictionaries as context
- Critical hooks used for non-critical behavior

## Examples From This Project

- `before_session`
- `after_test`
- `after_api_call`
- `on_failure`

## Reusable Templates

```python
runtime.hooks.register("after_test", callback, owner="plugin_name", order=50)
```

## Interview Explanations

Hooks are useful because they preserve separation of concerns while still allowing broad instrumentation and extension.

## Best Practices Checklist

- Hooks map to real lifecycle boundaries
- Contexts are typed
- Failure behavior is explicit
