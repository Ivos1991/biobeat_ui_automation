# DSMP Full-Stack Automation Framework

Production-grade Python automation framework for UI and API validation. The project keeps the original Cyera assignment scenarios intact while refactoring the internals around dependency injection, hooks, plugins, and typed configuration.

## What Changed

- Added a lightweight DI container with singleton and factory lifecycles.
- Added a typed lifecycle hook bus for session, test, step, failure, and API events.
- Added import-discovered plugins with config-based enable/disable.
- Reworked settings into nested typed dataclasses loaded from `.env` and environment variables.
- Introduced workflow orchestrators and page factories to reduce duplication across tests.
- Added framework-level unit tests plus CI steps for linting, type checking, and architecture validation.

## Repository Layout

```text
.
|-- api
|-- config
|-- core
|   |-- framework
|   |-- orchestrators
|   |-- plugins
|   |-- core_utils
|   `-- testing_utils
|-- docs
|-- tests
|   |-- api
|   |-- framework
|   `-- ui
|-- ui
|   |-- actions
|   |-- pages
|   `-- page_factory.py
`-- .github/workflows
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
python -m playwright install chromium
```

Copy `.env.example` to `.env` when running locally.

## Configuration

Core settings are loaded by `Settings.from_env()` and grouped by responsibility:

- `urls`
- `credentials`
- `browser`
- `timeouts`
- `retries`
- `reporting`
- `plugins`
- `runtime`

Evidence modes:

- `off`
- `failure_only`
- `full_evidence`

Compatibility aliases `on_failure` and `always` are still accepted.

## Running Tests

Framework unit tests:

```bash
.venv\Scripts\python -m pytest tests\framework -q
```

API tests:

```bash
.venv\Scripts\python -m pytest tests\api -m api -q -rs --alluredir artifacts\allure-results
```

UI tests:

```bash
.venv\Scripts\python -m pytest tests\ui -m ui -q -rs --alluredir artifacts\allure-results
```

Full suite:

```bash
.venv\Scripts\python -m pytest -q -rs --alluredir artifacts\allure-results
```

## CI/CD

`ci.yml` now runs:

- Ruff linting
- MyPy type checking
- framework unit tests
- selected E2E/API/UI suite
- Allure artifact generation and upload
- optional GitHub Pages publication for the latest report

## Extension Points

- Plugins: `core/plugins/builtin`
- Hook contracts: `core/framework/hooks.py`
- DI registrations: `core/framework/runtime.py`
- Orchestrators: `core/orchestrators`
- Page factories: `ui/page_factory.py`

## Documentation

- [Architecture](docs/architecture.md)
- [Plugin System](docs/plugin-system.md)
- [Hooks](docs/hooks.md)
- [Dependency Injection](docs/dependency-injection.md)
- [Extensibility](docs/extensibility.md)
