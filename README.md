# BioBeat UI Automation Home Assignment

Live Playwright UI automation suite for the BioBeat Patient Admission workflow.

## Target Application

- URL: `https://bpm-demo.eu.bio-beat.cloud/login`
- Business hierarchy: `Clients -> Departments -> Patients -> Sessions`

Verified live behavior used by the suite:

- Session Management is the reliable source for admission verification.
- Patient Lookup may lag behind newly created admissions.
- Session removal requires the same Patient ID, not Device ID.
- Verified device states:
  - `676767`: working creation path
  - `126875`: in use
  - `676733`: not activated or does not exist

## Repository Layout

```text
.
|-- .github/workflows/ui-tests.yml
|-- config/
|-- core/
|-- docs/
|   `-- manual_test_cases.md
|-- flows/
|   `-- admission_flow.py
|-- skills/
|-- test_data/
|   `-- patient_admission_cases.py
|-- tests/
|   `-- ui/
|       |-- patient_admission/
|       |   |-- conftest.py
|       |   |-- support.py
|       |   |-- test_admission_cleanup.py
|       |   |-- test_admission_happy_path.py
|       |   |-- test_admission_negative_validation.py
|       |   `-- test_admission_popup_behavior.py
|       |-- conftest.py
|       |-- test_login.py
|       `-- test_navigation.py
|-- ui/
|   `-- pages/
|-- utils/
|   `-- assertions.py
|-- .env.example
|-- conftest.py
|-- pyproject.toml
|-- pytest.ini
`-- run-tests.ps1
```

## Architecture Summary

- `config/`: typed runtime settings from environment variables.
- `ui/pages/`: locator-first page objects containing locators, UI actions, and data reads only.
- `flows/`: thin orchestration across page objects.
- `tests/ui/`: scenario tests organized by login, navigation, happy path, validation, popup behavior, and cleanup.
- `utils/assertions.py`: small assertion facade used consistently across tests and fixtures.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
python -m playwright install chromium
Copy-Item .env.example .env
```

## Configuration

The suite reads the following environment variables:

- `WEB_BASE_URL`
- `BIOBEAT_USERNAME`
- `BIOBEAT_PASSWORD`
- `BROWSER`
- `HEADLESS`
- `SLOW_MO_MS`
- `DEFAULT_TIMEOUT_MS`
- `EXPECT_TIMEOUT_MS`
- `NAVIGATION_TIMEOUT_MS`
- `BROWSER_EVIDENCE_MODE`
- `IGNORE_HTTPS_ERRORS`
- `ARTIFACT_DIR`

Compatibility aliases are also supported:

- `APP_USERNAME`
- `APP_PASSWORD`

## Running Tests

Collect tests only:

```powershell
.venv\Scripts\python -m pytest tests\ui --collect-only -q
```

Run the complete UI suite:

```powershell
.venv\Scripts\python -m pytest tests\ui -m ui -q --alluredir artifacts\allure-results
```

Run smoke coverage:

```powershell
.venv\Scripts\python -m pytest tests\ui -m "ui and smoke" -q --alluredir artifacts\allure-results
```

Run through the helper script:

```powershell
.\run-tests.ps1
.\run-tests.ps1 -Headed -SlowMoMs 100
```

## Allure

Generate a local report after a run:

```powershell
allure generate artifacts\allure-results --clean -o artifacts\allure-report
allure open artifacts\allure-report
```

## CI

Workflow: [`.github/workflows/ui-tests.yml`](.github/workflows/ui-tests.yml)

Expected GitHub repository secrets:

- `BIOBEAT_USERNAME`
- `BIOBEAT_PASSWORD`

Optional repository variable:

- `WEB_BASE_URL`

The workflow:

- installs Python dependencies
- installs Playwright Chromium
- runs `python -m pytest tests/ui -m ui -q --alluredir artifacts/allure-results`
- uploads Allure results
- uploads Playwright screenshots, videos, traces, and logs

## Manual Test Cases

See [docs/manual_test_cases.md](docs/manual_test_cases.md).

## Submission Notes

- The suite was verified live against the BioBeat application.
- Cleanup is built into the creation flow and verified through a dedicated cleanup test.
- No xfail placeholders, exploratory exceptions, or generated TODO tests remain in the active UI suite.
