# Framework Review

## Summary

This repository is a solid home-assignment framework baseline. It has the right top-level separation between configuration, API clients, service/domain helpers, UI page objects, shared test infrastructure, and CI reporting. The current implementation is good enough to demonstrate thoughtfulness and practical automation engineering, but it is still tightly coupled to the DSMP assignment and has a few design choices that should be cleaned up before reusing it as a generic base.

## What Is Strong

- Clear separation of `api`, `ui`, `core`, `config`, and `tests`.
- Reusable fixture-driven setup through root `conftest.py`.
- Good operational support: Allure, Playwright evidence, runtime logs, Docker-based CI execution.
- Sensible layering for UI actions and page objects.
- Service layer shields tests from raw request/response payloads.

## What Should Be Kept For The Next Assignment

- Root `conftest.py` structure for shared configuration and infrastructure.
- `Settings` dataclass pattern for environment-driven runtime configuration.
- `BaseApi` request wrapper and dedicated service classes.
- `PlaywrightActions` plus `BasePage` abstraction.
- Allure attachment helpers and Playwright artifact collection hooks.
- CI artifact upload and report generation flow.

## What Should Change Before Reuse

### 1. Remove product-specific assertions from shared services

The current auth and service layers contain hardcoded product assumptions such as admin role and display name checks. Those are valid for the current assignment, but they reduce portability and make the framework less reusable for a new system under test.

Recommended direction:

- Keep structural assertions in the infrastructure layer.
- Move business expectations into tests or scenario helpers.
- Treat service classes as domain operations, not as assertion-heavy test scripts.

### 2. Separate framework behavior from test assertions

Several service methods both execute business actions and assert outcomes using `assertpy`. That speeds up authoring, but it couples framework code to specific expected behaviors and makes the services harder to reuse from negative tests, exploratory flows, and alternative systems.

Recommended direction:

- Let service methods return typed results.
- Add optional assertion helpers where useful.
- Keep assertions closest to the test intent.

### 3. Make logging less invasive

The logger setup clears root handlers globally. That works locally, but it can interfere with pytest plugins, future log capture extensions, and other libraries if this base grows.

Recommended direction:

- Configure a dedicated framework logger tree.
- Avoid `root.handlers.clear()` unless the process is fully owned.
- Consider structured logging fields for request IDs, test IDs, and scenario names.

### 4. Reduce assignment-specific CI assumptions

The workflow is effective, but it is currently opinionated around one Dockerized stack, one serial environment, and GitHub Pages report publishing. That is fine for this repo, but a starter template should keep the artifact/report pattern while making application startup pluggable.

Recommended direction:

- Make system startup optional or project-specific.
- Keep the report upload path.
- Treat report publication as an opt-in extension, not a default requirement.

### 5. Add engineering guardrails

The repo is missing a few standard maintainability controls for a reusable base:

- formatting/linting
- static typing checks
- pre-commit hooks
- dependency locking strategy
- contributor bootstrap script beyond local test execution

Those are not blockers for a home assignment, but they do affect perceived production readiness.

## Suggested Reuse Strategy

For the next home assignment:

1. Keep the same layered shape.
2. Start from a generic starter rather than copying DSMP-specific modules directly.
3. Add only the domain-specific APIs, page objects, and workflows required by the assignment.
4. Keep reporting and CI generic until the target app’s deployment model is known.

## Deliverable Added In This Repo

The folder `starter_home_assignment/` is a generic Python + Pytest + Playwright starter built from this repository’s strongest reusable pieces. It is intended to be copied as the base for a new assignment project and then adapted to the target system.
