# Architecture Principles

## Concept Overview

This framework favors explicit, layered architecture with clear seams for change. Core infrastructure lives under `core/framework`, domain behavior lives in services and orchestrators, and tests remain scenario-focused.

## Why It Matters

- Easier maintenance
- Faster onboarding
- Better interview explainability
- Lower regression risk when adding features

## Core Principles

- Explicit runtime wiring
- Open/Closed principle through hooks and plugins
- Composition over inheritance
- Thin tests, rich framework
- Infrastructure separated from domain flows

## Recommended Implementation Patterns

- Central bootstrap function
- Typed settings grouped by domain
- Shared base clients for cross-cutting behavior
- Orchestrators for multi-service workflows

## Common Mistakes

- Mixing setup code into tests
- Creating too many abstraction layers too early
- Treating helpers as architecture

## Examples From This Project

- `build_runtime()` wires the entire object graph.
- `AlertWorkflowOrchestrator` removes repeated scan-and-find setup from tests.

## Reusable Templates

```python
def build_runtime(settings: Settings | None = None) -> FrameworkRuntime:
    ...
```

## Interview Explanations

Explain that explicit architecture trades a bit of verbosity for debuggability and lower cognitive load. That is valuable in both production systems and take-home assignments.

## Best Practices Checklist

- Single bootstrap entry point
- Layer ownership is clear
- Extension points are deliberate
- Docs explain tradeoffs
