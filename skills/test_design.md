# Test Design

## Concept Overview

Good tests express business behavior, not framework plumbing.

## Why It Matters

Interview-quality test suites are easy to read, deterministic, and cheap to maintain.

## Core Principles

- Tests describe actions and expected outcomes
- Fixtures manage setup and teardown
- Assertions are descriptive

## Recommended Implementation Patterns

- Use global `conftest.py` for shared fixtures
- Use folder-specific fixtures for local concerns
- Keep tests thin and scenario-driven

## Common Mistakes

- setup logic inline in every test
- brittle assertion strings
- hardcoded waits

## Examples From This Project

- `test_open_alert_status_transition_expects_rejected_direct_resolve`
- `test_manual_remediation_alert_lifecycle_expects_resolved_status_and_persisted_comment`

## Reusable Templates

```python
def test_<action>_expects_<result>(...):
    ...
```

## Interview Explanations

The best tests read like executable behavior specifications and push mechanical details into the framework.

## Best Practices Checklist

- Deterministic setup
- Descriptive naming
- Thin tests
