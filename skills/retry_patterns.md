# Retry Patterns

## Concept Overview

Retry patterns handle transient failures without masking systemic problems.

## Why It Matters

Automation against distributed systems often encounters timing and eventual consistency issues.

## Core Principles

- Retry only expected transient failures
- Separate retries from polling
- Keep attempts and delays configurable

## Recommended Implementation Patterns

- polling helper for state transitions
- typed retry decorator for transient operations
- logging on each retry

## Common Mistakes

- retrying everything
- infinite retries
- mixing polling and retries in tests

## Examples From This Project

- `wait_until`
- `@retryable` on `AdminService.reset_environment`

## Reusable Templates

```python
@retryable(3, (AssertionError,), delay_seconds=1.0)
def reset_environment(self) -> ResetEnvironmentResponse:
    ...
```

## Interview Explanations

Retries reduce flakiness when they target transient behavior. They become dangerous when they hide deterministic bugs.

## Best Practices Checklist

- bounded attempts
- explicit exception types
- observability on retries
