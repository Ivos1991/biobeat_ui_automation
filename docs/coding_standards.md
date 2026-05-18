# Coding Standards

## Naming Conventions

- Test names follow `test_<action>_expects_<result>`.
- Services use domain nouns: `AlertsService`, `ScansService`.
- Clients use transport nouns: `AlertsApi`, `ScansApi`.
- Orchestrators use workflow nouns: `AlertWorkflowOrchestrator`.

## Typing Standards

- Add full type hints to public functions and methods.
- Prefer typed models over raw dictionaries in services and tests.
- Use `Protocol`, `Literal`, `NewType`, and `TypedDict` where they sharpen intent.
- Use `Any` only at integration boundaries or plugin contracts where generic behavior is required.

## Dataclass Standards

- Use `@dataclass(slots=True)` for settings groups, hook contexts, and stable response carriers.
- Avoid `frozen=True` unless immutability provides real value.

## Assertion Standards

- Assertions must explain business meaning.
- Prefer descriptive messages with `assertpy` or explicit `assert` values.
- Keep repeated assertions in services or helpers when they express domain invariants.

## Testing Standards

- Shared fixtures belong in root `conftest.py`.
- Folder-local concerns belong in folder `conftest.py`.
- Keep setup and teardown out of test bodies when reusable.
- Keep tests deterministic and isolated.

## Hardcoded Values

- Configuration belongs in `Settings`.
- Known business constants may remain in code when they are true domain invariants.
- Selector strings stay in page objects, not tests.

## Extensibility Standards

- Optional behavior belongs in plugins.
- Cross-cutting lifecycle logic belongs in hooks.
- Multi-service setup belongs in orchestrators.
- Object construction belongs in runtime bootstrap.

## Documentation Standards

- Public architectural modules should have docstrings.
- Every major design decision should have rationale in docs.
- Examples in docs should match real repository patterns.
