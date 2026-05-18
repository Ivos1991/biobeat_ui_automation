# CI/CD Patterns

## Concept Overview

CI/CD patterns define how automation quality is validated and how results are preserved.

## Why It Matters

A framework that only works locally is incomplete.

## Core Principles

- static checks before environment-dependent suites
- artifact retention on failure
- workflow inputs for controlled execution modes

## Recommended Implementation Patterns

- dedicated quality job
- Python version matrix for static checks
- conditional E2E scope selection

## Common Mistakes

- no linting or type checking
- all tests coupled to one environment
- losing diagnostic artifacts

## Examples From This Project

- `quality` job in `ci.yml`
- Allure artifact upload
- optional GitHub Pages publication

## Reusable Templates

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12"]
```

## Interview Explanations

A good pipeline separates code-quality failures from environment failures so engineers can triage faster.

## Best Practices Checklist

- quality gates exist
- artifacts are uploaded
- run scope is configurable
