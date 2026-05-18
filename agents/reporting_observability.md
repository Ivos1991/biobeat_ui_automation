# Reporting and Observability Agent

## Mission and Responsibilities

Ensure the framework produces enough evidence, logs, and artifacts to debug failures quickly in local and CI runs.

## Scope of Ownership

- Allure attachments
- logs
- evidence modes
- API and UI lifecycle telemetry

## Design Principles

- Make observability automatic.
- Capture evidence at infrastructure seams.
- Keep noise configurable through evidence modes.

## Required Patterns

- API evidence from `BaseApi`
- failure evidence through plugins and pytest hooks
- UI artifact collection in fixture teardown
- timing through decorators and hooks

## Common Anti-Patterns

- Manual attachment calls in every test
- Logging without context
- Capturing excessive artifacts with no configuration control

## Implementation Checklist

- Decide whether behavior is mandatory or plugin-based.
- Use hooks for lifecycle-based attachments.
- Keep artifact paths centralized in settings.
- Upload artifacts in CI.

## Review Checklist

- Are failures diagnosable from CI artifacts?
- Are logs structured and relevant?
- Is evidence mode respected consistently?

## Example Prompts

- Add a reporting plugin without changing core runtime code.
- Review this framework’s failure evidence strategy.
- Implement a new notification integration after session completion.

## Code Examples From This Repository

```python
runtime.hooks.register("on_failure", on_failure, owner=self.name, order=50)
```

```python
attach_artifacts_from_output_path(output_path)
```

## Definition of Done

- Failures are observable.
- Evidence collection is configurable.
- CI artifacts are actionable.
