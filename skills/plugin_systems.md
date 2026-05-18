# Plugin Systems

## Concept Overview

Plugins add optional behavior without forcing core framework changes.

## Why It Matters

They keep reporting, notifications, and future integrations decoupled from the runtime core.

## Core Principles

- Discovery is automatic
- Activation is configuration-driven
- Core runtime remains stable

## Recommended Implementation Patterns

- Decorator-based registration
- Import discovery inside a known package
- Runtime registration through hooks

## Common Mistakes

- Hardcoding plugin lists in tests
- Requiring core edits for every new plugin
- Letting plugin failures crash the whole run without intention

## Examples From This Project

- `session_logger`
- `allure_evidence`

## Reusable Templates

```python
@plugin("notifications")
class NotificationPlugin:
    ...
```

## Interview Explanations

Plugins improve extensibility by letting optional behavior evolve independently from the core. The tradeoff is added bootstrap complexity, which this project contains through explicit discovery and config.

## Best Practices Checklist

- Plugin contracts are small
- Discovery path is predictable
- Enable/disable is config-based
