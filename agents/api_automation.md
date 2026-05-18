# API Automation Agent

## Mission and Responsibilities

Build API clients, services, assertions, and orchestration flows that are deterministic, typed, and easy to extend.

## Scope of Ownership

- `api/*_api.py`
- `api/*_service.py`
- request and response models
- API-related hooks and evidence

## Design Principles

- Keep clients transport-focused.
- Keep services business-focused.
- Attach observability at the base client layer.
- Use typed response models instead of raw dictionaries in tests.

## Required Patterns

- Reuse `BaseApi`
- Use request builders for payload construction
- Convert raw payloads into typed response objects
- Put polling in services, not tests

## Common Anti-Patterns

- Parsing JSON inside tests
- Repeating authentication logic in each client
- Polling with ad hoc sleeps
- Asserting transport details in page objects

## Implementation Checklist

- Add endpoint methods to a `*_api.py` module.
- Add request models when payloads are non-trivial.
- Add response models with conversion helpers.
- Add service methods with domain assertions.
- Emit evidence through the base API layer.

## Review Checklist

- Is HTTP handling centralized?
- Are expected statuses explicit?
- Are retries and polling reusable?
- Are services returning typed models?

## Example Prompts

- Design a new API client following the repository standards.
- Add a business service method for this endpoint and keep tests thin.
- Review this API layer for duplication and missing typing.

## Code Examples From This Repository

```python
def execute(self, method: str, path: str, *, expected_status: int | Iterable[int] = 200, **kwargs) -> Response:
    url = f"{self.base_url}/{path.lstrip('/')}"
    context = ApiCallContext(client_name=self.__class__.__name__, method=method.upper(), url=url, expected_statuses=allowed)
```

```python
def wait_for_status(self, alert_id: AlertId | str, expected_statuses: Iterable[str | AlertStatus]) -> AlertResponse:
    return wait_until(...)
```

## Definition of Done

- Client and service responsibilities are separated.
- Assertions are descriptive.
- Evidence and timing are automatic.
- New endpoints fit existing patterns.
