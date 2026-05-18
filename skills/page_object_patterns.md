# Page Object Patterns

## Concept Overview

Page objects encapsulate UI behavior and selectors so tests stay focused on scenario intent.

## Why It Matters

They reduce duplication and isolate selector churn.

## Core Principles

- One page object per meaningful screen or region
- Actions express intent, not clicks
- Shared primitives belong in an actions layer

## Recommended Implementation Patterns

- `BasePage` for navigation helpers
- region objects like `AlertDetailsDrawer`
- action helpers for fill/click/select/expect

## Common Mistakes

- exposing raw locators to tests
- mixing business assertions with selector plumbing
- giant page objects with unrelated flows

## Examples From This Project

- `AlertsPage`
- `AlertDetailsDrawer`
- `LoginPage`

## Reusable Templates

```python
class LoginPage(BasePage):
    def login(self, username: str, password: str) -> None:
        ...
```

## Interview Explanations

The page-object pattern is valuable when it models user intent cleanly rather than becoming a wrapper around every locator.

## Best Practices Checklist

- Page methods are intent-based
- Selectors are encapsulated
- Shared actions are reused
