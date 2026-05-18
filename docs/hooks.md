# Hooks

## Purpose

Hooks provide stable framework lifecycle points for plugins and future integrations.

## Supported Hooks

- `before_session`
- `after_session`
- `before_test`
- `after_test`
- `before_step`
- `after_step`
- `on_failure`
- `before_api_call`
- `after_api_call`

## Context Types

Defined in `core/framework/hooks.py`:

- `SessionContext`
- `TestContext`
- `StepContext`
- `ApiCallContext`
- `FailureContext`

## Execution Model

- Multiple handlers per hook are supported.
- Hooks execute in ascending `order`.
- Non-critical hook failures are isolated and logged.
- Critical handlers can stop execution when required.

## Example

```python
def register(self, runtime) -> None:
    runtime.hooks.register(
        "after_test",
        self.publish_results,
        owner=self.name,
        order=100,
    )
```

## Why This Matters

The hook bus lets reporting, evidence, environment initialization, and future integrations evolve independently from API clients and tests.
