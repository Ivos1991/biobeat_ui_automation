# Extensibility

## Current Extension Seams

- Plugin registry for optional behavior
- Hook bus for lifecycle integrations
- DI container for new services and clients
- Orchestrators for cross-service workflows
- Page factory for runtime-aware page object creation

## How New Capabilities Fit

### Browser Extension Testing

- Add a browser-extension service and page models.
- Register extension-specific hooks or evidence plugins.

### Mobile Testing

- Add a mobile client and service module.
- Reuse the same runtime, settings, and plugin model.

### Contract Testing

- Add schema validators as plugins or dedicated services.
- Emit API hooks for request/response evidence.

### Visual Testing

- Implement a plugin that subscribes to `after_step` or `after_test`.
- Add snapshot comparison services through the container.

### Performance Checks

- Use `before_api_call` and `after_api_call` hooks for timing capture.
- Add threshold validators as plugins.

## Practical Guardrails

- Prefer composition over inheritance.
- Register new dependencies in one place.
- Keep plugin behavior optional and config-driven.
- Add hooks only when they represent stable lifecycle boundaries.
