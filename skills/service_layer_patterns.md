# Service Layer Patterns

## Concept Overview

Services translate transport-layer clients into domain-level operations and reusable assertions.

## Why It Matters

They prevent tests from becoming tightly coupled to endpoint details.

## Core Principles

- Services orchestrate
- Clients transport
- Tests consume domain operations

## Recommended Implementation Patterns

- Convert client payloads into typed models
- Put polling and retries in services
- Keep assertions close to business operations

## Common Mistakes

- putting HTTP logic in services and tests
- returning raw payloads to tests
- duplicating domain assertions

## Examples From This Project

- `AlertsService`
- `ScansService`
- `AuthService`

## Reusable Templates

```python
def start_scan(self) -> ScanResponse:
    response = ScanResponse.from_dict(self.scans_api.start_scan())
    ...
```

## Interview Explanations

Services make tests more expressive and allow transport details to change with minimal test churn.

## Best Practices Checklist

- Client and service roles are distinct
- Domain assertions are reused
- Polling is centralized
