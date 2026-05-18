# Architectural Decision Records

## ADR-001: Use an Explicit Runtime Bootstrap

### Decision

Create a `FrameworkRuntime` built by `build_runtime()`.

### Rationale

It centralizes wiring, makes dependencies visible, and avoids hidden construction logic spread across pytest fixtures.

### Tradeoff

Slightly more bootstrap code than ad hoc fixtures.

## ADR-002: Use a Lightweight DI Container

### Decision

Implement `ServiceContainer` with singleton and factory lifecycles only.

### Rationale

The framework needs explicit construction, not a full IoC platform.

### Tradeoff

Fewer advanced features than a dedicated DI library, but much lower complexity.

## ADR-003: Introduce a Typed Hook Bus

### Decision

Create `HookManager` with typed context objects and ordered handlers.

### Rationale

Observability and optional behavior need stable lifecycle seams.

### Tradeoff

Adds runtime concepts that must be documented well.

## ADR-004: Use Import-Discovered Plugins

### Decision

Implement decorator-based plugin registration and package discovery.

### Rationale

Optional concerns such as reporting should not require core edits.

### Tradeoff

Slightly more bootstrap complexity than direct imports.

## ADR-005: Keep API Clients and Services Separate

### Decision

HTTP concerns stay in `*_api.py`; business workflows stay in `*_service.py`.

### Rationale

This keeps tests and domain logic insulated from transport details.

### Tradeoff

More files, but clearer ownership.

## ADR-006: Use Orchestrators for Multi-Service Setup

### Decision

Scenario setup spanning multiple services belongs in orchestrators.

### Rationale

It keeps tests short without turning services into scenario-specific god classes.

### Tradeoff

Adds a middle layer that should stay focused and small.
