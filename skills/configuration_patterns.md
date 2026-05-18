# Configuration Patterns

## Concept Overview

Configuration patterns define how runtime behavior is controlled across environments.

## Why It Matters

Typed configuration prevents invalid runs and reduces hidden environment dependencies.

## Core Principles

- Centralize env parsing
- Group settings by domain
- Validate constrained values

## Recommended Implementation Patterns

- nested settings dataclasses
- compatibility properties during migrations
- `.env.example` as living documentation

## Common Mistakes

- calling `os.getenv` everywhere
- stringly typed mode handling
- undocumented defaults

## Examples From This Project

- `Settings`
- `ReportingSettings`
- `_resolve_evidence_mode`

## Reusable Templates

```python
class ReportingSettings:
    evidence_mode: EvidenceMode
    artifact_dir: Path
```

## Interview Explanations

Typed configuration improves reliability by making invalid states harder to represent and easier to catch at startup.

## Best Practices Checklist

- parsing is centralized
- defaults are documented
- constrained values are validated
