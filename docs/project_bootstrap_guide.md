# Project Bootstrap Guide

## Goal

Start a new automation framework from scratch using the patterns proven in this repository.

## Step 1: Create the Repository Skeleton

```text
api/
config/
core/framework/
core/orchestrators/
core/plugins/builtin/
tests/api/
tests/ui/
ui/actions/
ui/pages/
```

## Step 2: Add Typed Settings

- create `config/settings.py`
- group env values by domain
- add `.env.example`

## Step 3: Build the Runtime

- create `ServiceContainer`
- create `HookManager`
- create `PluginManager`
- create `FrameworkRuntime`
- wire everything in `build_runtime()`

## Step 4: Add the API Layer

- implement `BaseApi`
- add first domain client
- add request and response models
- add a service layer

## Step 5: Add the UI Layer

- implement `PlaywrightActions`
- implement `BasePage`
- add a page factory
- add one real page object flow

## Step 6: Add Cross-Cutting Features

- retries
- polling
- logging
- evidence plugins
- failure hooks

## Step 7: Add Tests

- framework unit tests for runtime seams
- API tests for service/client flows
- UI tests for one critical scenario

## Step 8: Add CI/CD

- lint
- type check
- framework unit tests
- target E2E runs
- artifact upload

## Step 9: Add Docs

- README
- architecture guide
- plugin and hook docs
- ADRs

## Final Bootstrap Checklist

- Runtime builds cleanly
- Configuration is typed
- At least one plugin works
- At least one hook emits
- Tests stay thin
- CI publishes artifacts
