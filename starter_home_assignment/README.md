# Python Pytest Playwright Starter

Generic home-assignment starter based on the architecture used in this repository.

## Included

- environment-based settings
- shared pytest fixtures
- Playwright browser configuration
- Allure reporting helpers
- logging to console and file
- API base client
- UI base page/actions
- optional GitHub Actions workflow for artifacts and Allure HTML

## Structure

```text
starter_home_assignment
|-- api
|   `-- base_api.py
|-- config
|   `-- settings.py
|-- core
|   |-- core_utils
|   |-- testing_utils
|   |-- exceptions.py
|   `-- reporting.py
|-- tests
|   |-- api
|   `-- ui
|-- ui
|   |-- actions
|   `-- pages
|-- .github
|   `-- workflows
|-- conftest.py
|-- pyproject.toml
`-- pytest.ini
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m playwright install chromium
```

Create a `.env` from `.env.example` and fill in the target application values.

## Adaptation Checklist

1. Replace the placeholder URLs and credentials in `.env.example`.
2. Add product-specific API modules under `api/`.
3. Add page objects under `ui/pages/`.
4. Add assignment scenarios under `tests/api/` and `tests/ui/`.
5. If your target system needs Docker startup in CI, extend `.github/workflows/ci.yml`.

## Local Run

```bash
.venv\Scripts\python -m pytest -q -rs --alluredir artifacts\allure-results
```

Or use:

```bash
powershell -ExecutionPolicy Bypass -File .\run-tests.ps1
```
