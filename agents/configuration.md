# Configuration Agent

## Mission and Responsibilities

Define and evolve typed configuration that supports local development, CI, and future framework features.

## Scope of Ownership

- `.env.example`
- `config/settings.py`
- environment naming and defaults

## Design Principles

- Group settings by responsibility.
- Expose compatibility properties when migrating code.
- Fail fast on invalid enumerated values.

## Required Patterns

- Nested dataclasses for settings domains
- environment loading through `Settings.from_env()`
- compatibility aliases only when migration requires them

## Common Anti-Patterns

- Flat settings objects that grow without structure
- Silent fallback on invalid values
- Scattering `os.getenv` calls throughout the codebase

## Implementation Checklist

- Add new setting to the right nested section.
- Update `.env.example`.
- Add validation if the value is constrained.
- Keep defaults safe for local runs.

## Review Checklist

- Are env lookups centralized?
- Is configuration typed?
- Are modes and enums validated?

## Example Prompts

- Add strongly typed configuration for a new framework capability.
- Review this configuration layer for hardcoded values and missing validation.

## Code Examples From This Repository

```python
reporting=ReportingSettings(
    evidence_mode=_resolve_evidence_mode(os.getenv("BROWSER_EVIDENCE_MODE")),
    artifact_dir=artifact_dir,
)
```

## Definition of Done

- Configuration is typed, validated, and documented.
- New settings are discoverable and easy to wire.
