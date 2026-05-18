# Reporting Patterns

## Concept Overview

Reporting patterns govern how test evidence, attachments, and logs are collected and presented.

## Why It Matters

Good reporting shortens debug loops and makes CI failures reviewable without rerunning everything locally.

## Core Principles

- Automatic evidence where possible
- Configurable noise level
- Shared attachment helpers

## Recommended Implementation Patterns

- Attach API payloads in the base client
- Attach failure evidence through plugins
- Attach UI artifacts in teardown fixtures

## Common Mistakes

- manual evidence per test
- inconsistent artifact locations
- no evidence strategy for expected failures

## Examples From This Project

- `allure_evidence` plugin
- `attach_artifacts_from_output_path`
- evidence mode parsing in settings

## Reusable Templates

```python
runtime.hooks.register("on_failure", on_failure, owner=self.name, order=50)
```

## Interview Explanations

Configurable evidence modes balance signal and cost. `failure_only` keeps runs lean, while `full_evidence` helps with debugging and demos.

## Best Practices Checklist

- Evidence is configurable
- Attachments are centralized
- Artifact paths are predictable
