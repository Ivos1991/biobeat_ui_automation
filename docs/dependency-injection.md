# Dependency Injection

## Container Design

The framework uses `ServiceContainer` as a small explicit service registry.

Supported lifecycles:

- Singleton
- Factory

## Registration

Registrations are centralized in `core/framework/runtime.py`.

Examples:

- `Settings`
- `HookManager`
- `PluginManager`
- API clients
- business services
- orchestrators

## Why Explicit Registration

- Easier debugging
- Predictable ownership boundaries
- Simple interview discussion
- No hidden import side effects outside plugin discovery

## Pytest Integration

Pytest fixtures resolve container entries and expose them to tests:

- `framework`
- `service_container`
- `settings`
- `auth_service`
- `alerts_service`
- `scans_service`
- `alert_workflows`
- `page_factory`

## Extension Example

To add a new mobile service:

1. Create `mobile_api.py` and `mobile_service.py`.
2. Register both in `build_runtime`.
3. Expose them through fixtures if tests need direct access.

No existing service class needs to be modified.
