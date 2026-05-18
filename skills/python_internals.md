# Python Internals

## Concept Overview

Use Python features that improve correctness and maintainability without making the framework obscure.

## Why It Matters

Senior-level Python frameworks benefit from well-chosen typing, dataclasses, protocols, and decorators, but they should stay readable under code review pressure.

## Core Principles

- Use dataclasses for stable data carriers
- Use protocols for contracts where inheritance is unnecessary
- Use decorators for cross-cutting concerns
- Keep metaprogramming minimal and purposeful

## Recommended Implementation Patterns

- `@dataclass(slots=True)` for contexts and settings groups
- `Protocol` for plugin contracts and hook handlers
- `ParamSpec` and `TypeVar` for decorator typing

## Common Mistakes

- Using metaclasses where a function or protocol would do
- Overusing `Any`
- Hiding control flow in decorators

## Examples From This Project

- Hook and plugin contracts in `core/framework/hooks.py` and `core/framework/plugins.py`
- Typed decorators in `core/framework/decorators.py`

## Reusable Templates

```python
class FrameworkPlugin(Protocol):
    name: str
    def register(self, runtime: Any) -> None: ...
```

## Interview Explanations

Describe the difference between “using advanced Python” and “showing off advanced Python.” The framework should do the former.

## Best Practices Checklist

- Types improve decisions
- Protocols replace unnecessary inheritance
- Decorators stay explicit and typed
