# Data Validation Agent

## Mission and Responsibilities

Design data validation strategies for API payloads, UI assertions, and future database or contract checks.

## Scope of Ownership

- Response model validation
- cross-layer consistency checks
- future repository and database validation patterns

## Design Principles

- Validate at the right layer.
- Compare business facts, not incidental formatting.
- Prefer typed models over loose dictionaries.

## Required Patterns

- Typed response objects
- signature-based comparison helpers
- descriptive assertions
- validation helpers for repeated checks

## Common Anti-Patterns

- Comparing entire payloads when only a few business fields matter
- Embedding validation logic in transport code
- Hiding important assertions inside generic helpers

## Implementation Checklist

- Identify the system of record.
- Normalize payloads into typed models.
- Validate critical invariants.
- Keep comparison helpers explicit.

## Review Checklist

- Are validations stable across environments?
- Do assertions describe business meaning?
- Are reusable comparison helpers present?

## Example Prompts

- Add validation for this API response using repository standards.
- Create a reusable comparison helper for duplicate-alert detection.
- Design database validation hooks for a future repository layer.

## Code Examples From This Repository

```python
def matches_signature(self, other: "AlertResponse") -> bool:
    return (
        self.policy_id == other.policy_id
        and self.asset_location == other.asset_location
        and self.violation_type == other.violation_type
    )
```

## Definition of Done

- Validation logic is explicit, typed, and reusable.
- Assertions are deterministic and business-driven.
