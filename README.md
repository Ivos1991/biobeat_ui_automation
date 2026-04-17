# DSMP Full-Stack Automation

Python automation framework for DSMP. The framework separates UI and API tests, reuses shared infrastructure across both layers, and keeps the code readable enough for interview discussion.

## Project Purpose

- Automate the required manual-remediation lifecycle as a UI test.
- Automate the required auto-remediation plus rescan verification flow as an API test.
- Provide reusable infrastructure for configuration, API access, page objects, logging, reporting, and cleanup.

## Architecture Overview

```text
.
|-- api
|   |-- base_api.py
|   |-- admin
|   |-- alerts
|   |-- auth
|   |-- scans
|   `-- system
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

## Prerequisites

- Python 3.11+
- Docker Desktop installed and running
- For local runs, either:
  - start the provided assignment app source from `C:\Users\Seguras\Downloads\platform-home-assignment`, or
  - log in to `ghcr.io` and use the published images below
- For GitHub Actions full E2E runs, the workflow pulls these published images:
  - `ghcr.io/ivos1991/platform-home-assignment-api:assignment-one`
  - `ghcr.io/ivos1991/platform-home-assignment-web:assignment-one`

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m playwright install chromium
```

For local development you can also create a `.env` file in the repo root. A starter template is available in [`.env.example`](.env.example).

Optional environment variables:

```bash
set WEB_BASE_URL=http://localhost:3000
set API_BASE_URL=http://localhost:8080/api
set APP_USERNAME=admin
set APP_PASSWORD=Aa123456
set HEADLESS=true
set SLOW_MO_MS=0
set BROWSER_EVIDENCE_MODE=on_failure
```

For GitHub Actions, the same values can be supplied as repository variables and secrets:

- Secrets: `APP_USERNAME`, `APP_PASSWORD`
- Variables: `API_IMAGE`, `WEB_IMAGE`, `WEB_BASE_URL`, `API_BASE_URL`, `BROWSER_EVIDENCE_MODE`

`BROWSER_EVIDENCE_MODE` supports:

- `off`: do not auto-enable Playwright screenshot/video/trace collection
- `on_failure`: keep and attach evidence only for failing tests
- `always`: keep and attach evidence for every UI test in the run

## How To Start The System

Option 1, from `C:\Users\Seguras\Downloads\platform-home-assignment`:

```bash
docker compose up -d
```

Option 2, from this repository using the published images:

```bash
docker compose -f .github/docker-compose.e2e.yml up -d
```

Verified readiness checks:

```bash
docker compose ps
powershell -Command "(Invoke-WebRequest -UseBasicParsing http://localhost:8080/api/health).Content"
powershell -Command "(Invoke-WebRequest -UseBasicParsing http://localhost:3000).StatusCode"
```

For image-based startup, this repo also includes [`.github/docker-compose.e2e.yml`](.github/docker-compose.e2e.yml), which runs the published GHCR images used by CI.

## How To Run UI Tests

```bash
.venv\Scripts\python -m pytest tests\ui -m ui -q -rs --alluredir artifacts\allure-results
```

Collect full Playwright evidence for every UI test:

```bash
set BROWSER_EVIDENCE_MODE=always
.venv\Scripts\python -m pytest tests\ui -m ui -q -rs --alluredir artifacts\allure-results
```

## How To Run API Tests

```bash
.venv\Scripts\python -m pytest tests\api -m api -q -rs --alluredir artifacts\allure-results
```

## How To Run All Tests

```bash
.venv\Scripts\python -m pytest -q -rs --alluredir artifacts\allure-results
```

Use the local runner to execute tests and generate a static Allure HTML report in one step:

```bash
powershell -ExecutionPolicy Bypass -File .\run-tests.ps1
```

Run with full evidence collection:

```bash
powershell -ExecutionPolicy Bypass -File .\run-tests.ps1 -EvidenceMode always
```

Run headed with slow motion and open the generated report:

```bash
powershell -ExecutionPolicy Bypass -File .\run-tests.ps1 -EvidenceMode always -Headed -SlowMoMs 1000 -PytestTarget tests\ui -PytestMarker ui -OpenReport
```

## GitHub Actions

- The `PR Checks` workflow runs on every push and pull request.
- The same workflow also supports manual runs through `workflow_dispatch`.
- Manual run inputs:
  - `run_type`: `ui`, `api`, or `e2e`
  - `evidence_mode`: `on_failure` or `always`
- When the workflow produces Allure results, it:
  - uploads the static Allure HTML report as an artifact
  - publishes the latest report to the `gh-pages` branch at the site root
  - writes the Pages URL into the run summary

## Reporting

- Runtime logs are written to `artifacts/logs/framework.log`
- Allure results are written to `artifacts/allure-results`
- Static Allure HTML output is generated into `artifacts/allure-report`
- In `on_failure` mode, Playwright screenshot, video, and trace are attached to Allure for failing UI tests
- In `always` mode, Playwright screenshot, video, and trace are attached to Allure for every UI test
- Individual tests can force full evidence attachment with the `@pytest.mark.collect_all_evidence` marker

Generate a local report:

```bash
allure generate artifacts\allure-results --clean -o artifacts\allure-report
allure open artifacts\allure-report
```

## Logging

- Shared Python logging is configured once in `conftest.py`
- API requests and major UI actions are logged with contextual details
- Polling and cleanup actions log success and timeout/error conditions

## Assumptions And Notes

- The framework resets the environment before and after each test through `POST /api/admin/reset`.
- The UI lifecycle test uses API setup to create deterministic alert preconditions, then validates the remediation flow through the web application.
- The auto-remediation rescan verification scenario is intentionally marked as `xfail(strict=True)` because the application re-detects the alert on purpose.
- The verified full-suite result is `2 passed, 1 xfailed`.
- The assignment app exposes a single shared resettable environment, so the CI suite runs serially rather than in parallel.
- The UI shows `Awaiting User Verification` for the backend status `REMEDIATED_WAITING_FOR_CUSTOMER`, so the UI test verifies the backend state and the user-facing label separately.
- `pytest.ini` disables the cache provider to avoid a Windows workspace permission warning during verified runs.
- GitHub Actions is configured to pull the published app images from GHCR, run the full suite, generate a static Allure HTML report, upload the report artifact, and publish the latest report to the `gh-pages` branch.
- If the GHCR packages remain private, the repository must have permission to read them with `GITHUB_TOKEN`, or the workflow login step must be adjusted.
- Username and password can be moved to GitHub Secrets; image names and URLs are better kept as GitHub Variables rather than hardcoded workflow values.
