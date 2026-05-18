# Clean Code

## Concept Overview

Clean code in a framework means the right logic lives in the right layer and names reveal intent.

## Why It Matters

Automation frameworks degrade quickly when helpers accumulate without ownership boundaries.

## Core Principles

- Intent-revealing names
- High cohesion
- Low coupling
- Short, purposeful methods

## Recommended Implementation Patterns

- Keep tests declarative
- Put setup logic in fixtures or orchestrators
- Move duplicated logic into services or actions

## Common Mistakes

- God utility modules
- vague method names
- hidden side effects

## Examples From This Project

- `create_manual_alert`
- `wait_for_status`
- `open_alert_by_policy_name`

## Reusable Templates

Use `test_action_expects_result` naming and prefer method names that describe business intent.

## Interview Explanations

Clean code is not minimal code. It is code with clear ownership, predictable behavior, and low surprise.

## Best Practices Checklist

- Names are precise
- Methods do one thing
- Layers are respected
