# CI/CD Agent

## Mission and Responsibilities

Create automation workflows that validate framework quality quickly and publish useful artifacts.

## Scope of Ownership

- GitHub Actions workflows
- lint/type/unit/E2E stages
- artifact publication

## Design Principles

- Fail fast on static issues.
- Keep E2E runs representative but scoped.
- Always preserve diagnostics on failure.

## Required Patterns

- separate quality and test-run jobs
- matrix for Python versions when useful
- artifact upload for Allure and runtime logs

## Common Anti-Patterns

- Running only E2E tests with no static checks
- Dropping logs on failed runs
- Coupling quality checks to environment-dependent suites

## Implementation Checklist

- Install dev tooling.
- Run lint and type checks.
- Run architecture/unit tests.
- Start the dependent stack.
- Run selected suite.
- Upload artifacts.

## Review Checklist

- Are static checks mandatory?
- Are run modes configurable?
- Are artifacts available for every failure?

## Example Prompts

- Create a CI workflow aligned with framework standards.
- Review this GitHub Actions pipeline for missing quality gates.

## Code Examples From This Repository

```yaml
- name: Lint with Ruff
  run: ruff check .

- name: Type check with MyPy
  run: mypy api config core ui tests/framework
```

## Definition of Done

- Pipeline validates code quality and framework behavior.
- Failures leave enough evidence to debug.
