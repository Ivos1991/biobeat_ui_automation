# Architecture

## Design Goals

- Preserve current assignment behavior.
- Make object creation explicit.
- Move cross-cutting concerns to infrastructure seams.
- Keep tests readable and interview-friendly.

## Runtime Flow

1. `pytest_configure` builds a `FrameworkRuntime`.
2. `FrameworkRuntime` wires `Settings`, `HookManager`, `PluginManager`, and service registrations into `ServiceContainer`.
3. Enabled plugins are discovered from `core.plugins.builtin` and activated.
4. Pytest hooks emit typed lifecycle events.
5. Tests consume page objects, services, and orchestrators through fixtures backed by the container.

## Layers

- Configuration: `config/settings.py`
- Dependency Injection: `core/framework/container.py`
- Runtime Bootstrap: `core/framework/runtime.py`
- Hooks: `core/framework/hooks.py`
- Plugins: `core/framework/plugins.py`, `core/plugins/builtin`
- Orchestrators: `core/orchestrators`
- API Clients: `api/*_api.py`
- Business Services: `api/*_service.py`
- UI Actions and Pages: `ui/actions`, `ui/pages`
- Tests: `tests/api`, `tests/ui`, `tests/framework`

## Design Decisions

- The container is intentionally lightweight. It supports only singleton and factory scopes because anything more would be abstraction without current value.
- Hooks are typed with dataclasses rather than free-form dictionaries to make plugin contracts explicit.
- Plugins use import-based discovery with a registration decorator. That keeps extension costs low without requiring a package manager or entry-point plumbing.
- Existing tests remain scenario-focused. The heavy lifting moved into services, orchestrators, and fixtures instead of into inheritance hierarchies.

## Tradeoffs

- Runtime registration is explicit rather than magical. It is slightly more verbose but easier to debug in interview and production settings.
- The project uses dataclasses instead of a larger DI or plugin framework to keep operational complexity low.
