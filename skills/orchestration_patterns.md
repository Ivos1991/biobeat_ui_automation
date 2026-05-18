# Orchestration Patterns

## Concept Overview

Orchestrators coordinate multi-service workflows that would otherwise be duplicated across tests.

## Why It Matters

They keep tests short without bloating low-level services with scenario-specific flows.

## Core Principles

- orchestrate across services
- return meaningful bundles
- keep scenario setup reusable

## Recommended Implementation Patterns

- dedicated orchestrator classes
- small immutable bundle objects where helpful
- reuse service methods instead of bypassing them

## Common Mistakes

- putting orchestration in tests
- turning services into giant scenario classes
- making orchestrators too generic

## Examples From This Project

- `AlertWorkflowOrchestrator`
- `ScanAlertBundle`

## Reusable Templates

```python
def create_manual_alert(self) -> ScanAlertBundle:
    ...
```

## Interview Explanations

Orchestrators are the right middle layer when a workflow spans multiple services but should not live in tests.

## Best Practices Checklist

- orchestration is reusable
- returned objects are meaningful
- service boundaries stay intact
