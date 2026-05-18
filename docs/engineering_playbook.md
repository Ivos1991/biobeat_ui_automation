# Engineering Playbook

## End-to-End Development Methodology

### 1. Define the Smallest Viable Architecture

- Create repository structure first.
- Add typed settings and runtime bootstrap.
- Decide which layers are required: API, UI, services, orchestrators, reporting.

### 2. Establish Core Infrastructure

- Add a central DI container.
- Add a base API client with observability.
- Add page-object and action-layer foundations.
- Add hook and plugin seams for optional behavior.

### 3. Build One Golden Flow Per Layer

- One API scenario that proves service/client patterns.
- One UI scenario that proves page-object patterns.
- One framework-unit area that proves runtime architecture.

### 4. Add Cross-Cutting Concerns

- logging
- evidence
- retries
- polling
- CI quality gates

### 5. Harden for Reuse

- move duplicated setup into fixtures or orchestrators
- add typed response models
- add docs for extension points

### 6. Final Review

- architecture review
- typing review
- test readability review
- CI review
- documentation review

## Practical Working Rules

- Start explicit, generalize only after seeing repetition.
- Keep tests declarative and business-driven.
- Use plugins for optional concerns.
- Use hooks for lifecycle integration.
- Use DI for construction, not as an ideology.

## Repository Mapping

- Runtime: `core/framework`
- Orchestration: `core/orchestrators`
- API domain: `api`
- UI domain: `ui`
- Validation and coverage: `tests`

## Release Readiness Checklist

- lint and type checks pass
- framework unit tests pass
- target scenarios pass in the intended environment
- docs reflect the current architecture
- artifacts and logs are available in CI
