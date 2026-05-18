# Typing and Metaprogramming

## Concept Overview

Use typing and light metaprogramming to reduce bugs and duplication while keeping the codebase approachable.

## Why It Matters

Strong typing turns framework conventions into enforceable design decisions.

## Core Principles

- Types should communicate intent
- Decorators should stay transparent
- Metaprogramming must solve a concrete problem

## Recommended Implementation Patterns

- `Literal` for hook names and evidence modes
- `NewType` for identifiers
- `Protocol` for contracts
- `ParamSpec` for decorator signatures

## Common Mistakes

- Returning `dict[str, Any]` everywhere
- Overusing runtime introspection
- Decorators that erase function intent

## Examples From This Project

- `EvidenceMode`
- `HookName`
- `AlertId`, `ScanId`

## Reusable Templates

```python
AlertId = NewType("AlertId", str)
```

## Interview Explanations

Protocols improve design because they let you code to behavior without forcing inheritance. Decorators reduce duplication when they stay focused on cross-cutting concerns like logging and timing.

## Best Practices Checklist

- Types narrow critical domains
- `Any` is minimized
- Decorators are typed and documented
